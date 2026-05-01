# Security Review

Updated: 2026-05-01

Scope reviewed: authentication and authorization, tenant isolation, public APIs and rate limiting, error handling, demo/local/source labeling, environment variables, storage of campaign/user/API-key data, and frontend exposure of sensitive configuration.

This review did not make product-code changes. It records release blockers and focused follow-up PR recommendations.

## Executive Summary

The repository has several good security foundations: password hashing now uses Werkzeug adaptive hashes, legacy password hashes are rehashed on login, production rejects known fallback auth secrets, public/demo routes are rate-limited, client-facing traceback payloads are sanitized, and demo/local/live/backend-verified source labels exist in the UI.

However, the current repository is not production-ready for external customers. The main blockers are tenant/object authorization gaps, role enforcement, plaintext runtime secret storage, debug logging defaults, and result-provenance accuracy.

## Critical Findings

### SEC-001: Tracked environment file contains secret-like values

- Severity: Critical
- Status: Partially remediated in PR I; manual credential rotation remains required
- Evidence: `.env.dev` is tracked by Git and contains provider-key pattern matches plus password-style assignments. Values were not printed in this review.
- Impact: Any real key committed to Git must be treated as exposed. A leaked provider key can create cost, data, and account compromise risk.
- Remediation: `.env.dev` has been removed from Git tracking, `.env.dev.example` now contains safe placeholders only, `.gitignore` ignores local env/runtime/credential files, and CI blocks tracked local env/runtime files plus common provider-key patterns.
- Remaining manual action: Repository owners must rotate any provider/API/graph credentials that may have been committed before this PR. This cannot be completed from the repository.

### SEC-002: Settings API can expose graph credentials to the browser

- Severity: Critical
- Status: Remediated in PR J for browser/API read exposure; RBAC remains covered by SEC-004
- Evidence: `backend/app/api/settings.py` masks `llm.api_key` and `embedding.api_key`, but does not mask `graph_db.password` before returning settings. `backend/app/models/settings.py` stores `graph_db.password` in the persisted settings model.
- Impact: Any authenticated browser session that can call `GET /api/settings` can receive the Neo4j password. Because role checks are not enforced on this route, this can expose graph credentials beyond administrators.
- Remediation: `GET /api/settings` now omits raw and masked credential fields and returns only `api_key_present` / `password_present` flags. Settings updates preserve existing saved secrets when the browser sends blank values, masked placeholders, or presence flags. New secrets can be accepted but are not echoed in API responses.
- Remaining action: Add admin-only RBAC to settings read/update/test routes under SEC-004.

### SEC-003: Tenant isolation is incomplete for ID-addressed resources

- Severity: Critical
- Status: Remediated in PR L for ID-addressed campaign, pipeline, dashboard, simulation, report, project, graph, and graph-task routes in the current local JSON architecture
- Evidence:
  - `backend/app/api/campaign.py` authenticates pipeline status, but `PipelineOrchestrator.get_pipeline_status()` calls `campaign_service.get_campaign(campaign_id)` without `org_id`, which searches all organizations.
  - `SimulationState` does not include `org_id`, and many `/api/simulation/<simulation_id>/...` routes operate by global simulation ID.
  - `ReportManager` stores reports globally under `Config.UPLOAD_FOLDER/reports` and report routes fetch by `report_id` or `simulation_id` without an org ownership check.
- Impact: An authenticated user who learns or guesses another tenant's object ID may be able to read status, report, simulation, or generated artifact data outside their organization.
- Remediation: Simulation, report, project, graph-build task, and pipeline status records now carry `org_id` ownership metadata where applicable. Routes that fetch, download, delete, or poll by `campaign_id`, `simulation_id`, `report_id`, `project_id`, `graph_id`, or graph `task_id` now verify the current organization before returning data. Cross-tenant negative tests cover campaign pipeline status, simulation reads, dashboard KPI reads, report download, report delete, safe unknown IDs, and owner-positive reads.
- Remaining action: Legacy simulation/report/project/task records created before ownership metadata was introduced may need a one-time backfill or should remain inaccessible in production until re-created. This PR does not replace local JSON storage with a database-level tenant constraint.

### SEC-004: Role-based authorization is mostly absent

- Severity: Critical
- Status: Partially remediated in PR K; route ownership isolation completed in PR L for ID-addressed resources
- Evidence: `UserRole` exists, but protected routes generally only require authentication. Sensitive routes such as settings update, campaign deletion, report deletion, API-key generation, and simulation lifecycle operations do not consistently enforce admin/analyst/viewer permissions.
- Impact: A viewer or low-privilege user may be able to mutate settings, delete data, start/stop simulations, or access privileged operational flows.
- Remediation: A centralized `role_required()` guard now enforces admin-only settings/API-key/destructive operations, analyst-or-admin campaign/report/simulation generation flows, and viewer read-only behavior on the covered routes.
- Remaining action: Continue auditing newly added routes for explicit role checks and ownership checks as part of normal PR review.

## High Findings

### SEC-005: Backend-verified labels are applied to mock KPI output

- Severity: High
- Status: Blocker for product trust
- Evidence: `backend/app/api/dashboard.py` marks dashboard action-plan source as `backend_verified`, while `KPICalculator.calculate()` falls back to mock data when no real simulation data is provided. It does not verify campaign existence or ownership before returning generated KPI values.
- Impact: A user can request a dashboard for an arbitrary campaign ID and receive plausible-looking KPI values labeled as backend verified. This is not a direct secret leak, but it violates the repository's source-labeling safety rule and can mislead business decisions.
- Recommended fix: Require campaign ownership/existence before dashboard KPI/report/timeline/segment responses. If mock output is used, source must be `local_estimate` or `demo_mode`, never `backend_verified`.

### SEC-006: Auth routes bypass centralized tenant middleware and contain broken privileged paths

- Severity: High
- Status: Partially remediated in PR K
- Evidence:
  - `TenantMiddleware.PUBLIC_PREFIXES` marks all `/api/auth/` routes as public.
  - `auth_required()` reimplements token checks, does not reject `None` payload before `.get()`, loads users globally, and allows downstream execution when user/org lookup fails.
  - `/api/auth/api-key` calls `UserService.generate_and_store_api_key()`, which is not implemented.
  - `/api/auth/switch-org` calls `AuthService.switch_org()`, which is not implemented.
- Impact: Protected auth routes are inconsistent with the main auth/tenant control. API-key and org-switch flows fail, and token/user/org state checks are weaker than the main middleware.
- Remediation: Only `/api/auth/login` and `/api/auth/register` remain public. `/me`, `/api-key`, and `/switch-org` now use tenant middleware plus explicit role guards. API-key generation uses the existing `UserService.generate_api_key()` path. Organization switching is disabled with a client-safe `501` until a tenant-membership model is implemented.
- Remaining action: Implement real multi-organization membership and safe org switching, or remove the route entirely before production.

### SEC-007: Runtime settings are stored plaintext on local disk

- Severity: High
- Status: Partially mitigated in PR J; blocker before multi-user/cloud deployment
- Evidence: `SettingsManager.save()` persists LLM API keys, embedding API keys, and graph passwords into `backend/uploads/settings.json`.
- Impact: File-system compromise, backups, logs, or volume snapshots can expose provider credentials. The file is gitignored, which helps source control, but not production runtime security.
- Mitigation: Browser reads no longer receive stored secret values, settings updates no longer persist masked placeholders as real values, and the Settings UI stores only presence metadata in local browser settings.
- Recommended fix: Store production secrets in environment variables or a secret manager. If file storage remains for local demo, encrypt at rest and keep permissions restricted.

### SEC-008: Request body debug logging can record secrets and campaign briefs

- Severity: High
- Status: Partially mitigated in PR J; blocker if debug logging is enabled outside local development
- Evidence: `create_app()` logs JSON request bodies at debug level. `Config.DEBUG` defaults to true.
- Impact: Login passwords, provider API keys, settings payloads, campaign briefs, and customer data can enter logs.
- Mitigation: Request JSON debug logs now redact credential-like fields before writing to logs.
- Recommended fix: Do not log request bodies by default. Make production/default debug false and consider disabling body logging entirely outside local development.

## Medium Findings

### SEC-009: In-memory rate limiting is not sufficient for production

- Severity: Medium
- Status: Non-blocking for local demos; blocker for public internet exposure without edge controls
- Evidence: `RateLimitMiddleware` is per-process, memory-backed, and keys on `X-Forwarded-For` when present.
- Impact: Multi-worker deployments do not share counters, restarts reset limits, and spoofed forwarding headers can bypass limits unless a trusted proxy overwrites them.
- Recommended fix: Keep the current limiter for local/demo mode, but add edge/API-gateway or Redis-backed rate limiting for production. Only trust `X-Forwarded-For` from configured proxies.

### SEC-010: API keys are accepted in query parameters

- Severity: Medium
- Status: Non-blocking improvement
- Evidence: `TenantMiddleware._extract_token()` accepts `?api_key=...`.
- Impact: Query tokens are commonly captured in access logs, browser history, analytics, referrers, and screenshots.
- Recommended fix: Remove query-parameter API-key auth. Require `Authorization: Bearer` or `X-Api-Key` headers only.

### SEC-011: CORS is wide open for all API routes

- Severity: Medium
- Status: Non-blocking for local demos; production hardening required
- Evidence: `CORS(app, resources={r"/api/*": {"origins": "*"}})`.
- Impact: The app uses Authorization headers rather than cookies, so this is not a classic cookie CSRF issue. Still, broad CORS weakens browser-origin boundaries and should not be the production default.
- Recommended fix: Make allowed origins configurable and restrict production to trusted frontend origins.

### SEC-012: Frontend stores auth tokens/API keys in localStorage

- Severity: Medium
- Status: Non-blocking improvement
- Evidence: `frontend/src/api/index.js` reads `3c-auth-token` and `3c-api-key` from `localStorage`.
- Impact: Any XSS in the frontend can exfiltrate tokens/API keys. No CSP was observed in this review.
- Recommended fix: Prefer short-lived access tokens with refresh flow or secure HttpOnly cookies if feasible. Add CSP and avoid storing API keys in the browser for normal users.

### SEC-013: Error handling strips tracebacks but still returns raw exception strings in many handlers

- Severity: Medium
- Status: Non-blocking improvement
- Evidence: Many API handlers return `error: str(e)`; the global sanitizer removes traceback keys and redacts some common secret patterns.
- Impact: Non-traceback exception strings can still reveal internal paths, provider details, object IDs, or unrecognized secret formats.
- Recommended fix: Return stable client-safe error codes/messages from handlers and keep detailed exceptions only in server logs.

## Positive Controls Observed

- Passwords use Werkzeug adaptive hashing, and legacy SHA256 hashes are rehashed on login.
- Production rejects known fallback Flask/auth secrets when `APP_ENV`/`FLASK_ENV`/`ENV` is production.
- Public demo, decision, brief, competitor, settings-readiness, status, and simulation routes have a lightweight rate limiter.
- Client-facing traceback fields are stripped by response-safety middleware.
- Source labels exist for Demo Mode, Local Estimate, Live Backend, Backend Verified, and Unknown Source.
- Analytics/feedback events are provider-neutral and sanitize payload fields.
- Runtime upload/settings directories are gitignored.

## Public Endpoint Review

Public by design:

- `/health`
- `/api/status`
- `/api/demo/*`
- `/api/decision/*`
- `/api/brief/*`
- `/api/competitor/*`
- `/api/settings/providers`
- `/api/settings/readiness`
- `/api/impact/scenarios/*`
- `/api/persona/archetypes`
- `/api/persona/regions`
- `/api/persona/countries`
- `GET /api/industry/templates*`
- `/api/auth/login`
- `/api/auth/register`

Concerns:

- `/api/auth/*` broad public access was narrowed in PR K. Only login/register should remain public.
- `/api/decision`, `/api/brief`, and `/api/competitor` are deterministic and currently acceptable for demo mode, but need payload-size, rate-limit, and abuse monitoring before public exposure.
- `/api/industry/templates/import`, `/validate`, and DELETE are no longer covered by a broad public prefix; only GET template catalog reads are public.

## Storage Review

- Campaigns and users are stored as JSON files under per-org folders.
- User JSON files include email/name plus `password_hash`, `api_key_hash`, and `api_key_prefix`; `to_dict(safe=True)` removes sensitive hashes from normal responses.
- API keys are stored as SHA256 hashes. Because generated keys are high entropy, this is acceptable for local/demo use, but a keyed HMAC/pepper would reduce risk if storage is stolen.
- Settings currently persist provider and graph secrets in plaintext local JSON.
- Simulation and report storage are global rather than clearly tenant-scoped.

## Frontend Exposure Review

- Frontend environment exposure is limited to Vite-prefixed variables such as `VITE_API_BASE_URL` and analytics flags.
- No backend secret environment variables are intentionally exposed through Vite config.
- The main browser-side risk is token/API-key storage in `localStorage`.
- Feedback and analytics intentionally avoid raw brief content and PII.

## Recommended Focused Follow-Up PRs

1. Secret hygiene PR:
   - Remove tracked `.env.dev`. Completed in PR I.
   - Add `.env.dev.example`. Completed in PR I.
   - Add CI secret scanning. Completed in PR I with a lightweight tracked-file and provider-key-pattern scan.
   - Rotate any exposed provider/graph credentials. Still required outside the repo by the owner.

2. Settings secrets PR:
   - Mask/omit `graph_db.password` in GET responses. Completed in PR J.
   - Return only presence flags for all secrets. Completed in PR J.
   - Preserve existing secrets when blank/masked browser values are submitted. Completed in PR J.
   - Add tests proving secrets are not returned. Completed in PR J.

3. Tenant isolation PR:
   - Add `org_id` metadata to simulation/report records. Completed in PR L.
   - Enforce org ownership on all ID-addressed campaign, simulation, report, graph, and pipeline routes. Completed in PR L for the current local JSON storage architecture.
   - Add cross-tenant denial tests. Completed in PR L.

4. RBAC PR:
   - Add centralized route role guards. Completed in PR K.
   - Enforce admin-only settings/API-key/org management and analyst-only simulation mutation. Partially completed in PR K for critical routes.
   - Ensure viewers are read-only. Covered by PR K tests for campaign/settings/API-key/destructive operations.

5. Provenance labeling PR:
   - Stop returning mock KPI data as `backend_verified`.
   - Require campaign existence/ownership before dashboard APIs.
   - Label any deterministic fallback as `local_estimate` or `demo_mode`.

6. Production hardening PR:
   - Set debug false by default.
   - Disable request body logging or redact it.
   - Restrict CORS by environment.
   - Remove query-parameter API-key auth.
   - Document required edge/shared rate limiting.

## Release Decision

For controlled local demos, the current repository is acceptable if no real secrets are used and demo/local labels remain visible.

For a public pilot or customer deployment, SEC-001 through SEC-008 should be treated as blockers. SEC-009 through SEC-013 are important hardening items that can follow once the blockers are closed, unless the deployment is internet-facing, in which case rate limiting, CORS, debug logging, and token storage should be addressed before launch.
