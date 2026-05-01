# Security Review

Updated: 2026-05-01

Scope reviewed: authentication and authorization, tenant isolation, public APIs and rate limiting, error handling, demo/local/source labeling, environment variables, storage of campaign/user/API-key data, and frontend exposure of sensitive configuration.

This review did not make product-code changes. It records release blockers and focused follow-up PR recommendations.

## Executive Summary

The repository has several good security foundations: password hashing now uses Werkzeug adaptive hashes, legacy password hashes are rehashed on login, production rejects known fallback auth secrets, public/demo routes are rate-limited, client-facing traceback payloads are sanitized, and demo/local/live/backend-verified source labels exist in the UI.

However, the current repository is not production-ready for external customers. The main blockers are secret handling, tenant/object authorization gaps, settings exposure, role enforcement, and result-provenance accuracy.

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
- Status: Blocker
- Evidence: `backend/app/api/settings.py` masks `llm.api_key` and `embedding.api_key`, but does not mask `graph_db.password` before returning settings. `backend/app/models/settings.py` stores `graph_db.password` in the persisted settings model.
- Impact: Any authenticated browser session that can call `GET /api/settings` can receive the Neo4j password. Because role checks are not enforced on this route, this can expose graph credentials beyond administrators.
- Recommended fix: Mask or omit `graph_db.password` in all read responses, return only `password_present: true/false`, and require re-entry for updates/tests.

### SEC-003: Tenant isolation is incomplete for ID-addressed resources

- Severity: Critical
- Status: Blocker
- Evidence:
  - `backend/app/api/campaign.py` authenticates pipeline status, but `PipelineOrchestrator.get_pipeline_status()` calls `campaign_service.get_campaign(campaign_id)` without `org_id`, which searches all organizations.
  - `SimulationState` does not include `org_id`, and many `/api/simulation/<simulation_id>/...` routes operate by global simulation ID.
  - `ReportManager` stores reports globally under `Config.UPLOAD_FOLDER/reports` and report routes fetch by `report_id` or `simulation_id` without an org ownership check.
- Impact: An authenticated user who learns or guesses another tenant's object ID may be able to read status, report, simulation, or generated artifact data outside their organization.
- Recommended fix: Add org ownership metadata to simulation/report records, enforce `org_id` checks on every object fetch/download/delete/status route, and add cross-tenant negative tests.

### SEC-004: Role-based authorization is mostly absent

- Severity: Critical
- Status: Blocker
- Evidence: `UserRole` exists, but protected routes generally only require authentication. Sensitive routes such as settings update, campaign deletion, report deletion, API-key generation, and simulation lifecycle operations do not consistently enforce admin/analyst/viewer permissions.
- Impact: A viewer or low-privilege user may be able to mutate settings, delete data, start/stop simulations, or access privileged operational flows.
- Recommended fix: Add a centralized `role_required()` guard and enforce route-level RBAC. Start with settings, auth API key, destructive campaign/report routes, simulation start/stop/cleanup, and provider live tests.

## High Findings

### SEC-005: Backend-verified labels are applied to mock KPI output

- Severity: High
- Status: Blocker for product trust
- Evidence: `backend/app/api/dashboard.py` marks dashboard action-plan source as `backend_verified`, while `KPICalculator.calculate()` falls back to mock data when no real simulation data is provided. It does not verify campaign existence or ownership before returning generated KPI values.
- Impact: A user can request a dashboard for an arbitrary campaign ID and receive plausible-looking KPI values labeled as backend verified. This is not a direct secret leak, but it violates the repository's source-labeling safety rule and can mislead business decisions.
- Recommended fix: Require campaign ownership/existence before dashboard KPI/report/timeline/segment responses. If mock output is used, source must be `local_estimate` or `demo_mode`, never `backend_verified`.

### SEC-006: Auth routes bypass centralized tenant middleware and contain broken privileged paths

- Severity: High
- Status: Blocker for auth/API-key flows
- Evidence:
  - `TenantMiddleware.PUBLIC_PREFIXES` marks all `/api/auth/` routes as public.
  - `auth_required()` reimplements token checks, does not reject `None` payload before `.get()`, loads users globally, and allows downstream execution when user/org lookup fails.
  - `/api/auth/api-key` calls `UserService.generate_and_store_api_key()`, which is not implemented.
  - `/api/auth/switch-org` calls `AuthService.switch_org()`, which is not implemented.
- Impact: Protected auth routes are inconsistent with the main auth/tenant control. API-key and org-switch flows fail, and token/user/org state checks are weaker than the main middleware.
- Recommended fix: Make only `/api/auth/login` and `/api/auth/register` public. Protect `/me`, `/api-key`, and `/switch-org` with the same tenant middleware and explicit role checks. Fix or remove broken API-key/org-switch implementations.

### SEC-007: Runtime settings are stored plaintext on local disk

- Severity: High
- Status: Blocker before multi-user/cloud deployment
- Evidence: `SettingsManager.save()` persists LLM API keys, embedding API keys, and graph passwords into `backend/uploads/settings.json`.
- Impact: File-system compromise, backups, logs, or volume snapshots can expose provider credentials. The file is gitignored, which helps source control, but not production runtime security.
- Recommended fix: Store secrets in environment variables or a secret manager. If file storage remains for local demo, encrypt at rest and keep permissions restricted. Never persist masked placeholder secrets as real values.

### SEC-008: Request body debug logging can record secrets and campaign briefs

- Severity: High
- Status: Blocker if debug logging is enabled outside local development
- Evidence: `create_app()` logs JSON request bodies at debug level. `Config.DEBUG` defaults to true.
- Impact: Login passwords, provider API keys, settings payloads, campaign briefs, and customer data can enter logs.
- Recommended fix: Do not log request bodies by default. Add a redacting logger if request-body debugging is ever needed. Make production/default debug false.

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
- `/api/industry/templates*`
- `/api/auth/*`

Concerns:

- `/api/auth/*` is too broad. Only login/register should be public.
- `/api/decision`, `/api/brief`, and `/api/competitor` are deterministic and currently acceptable for demo mode, but need payload-size, rate-limit, and abuse monitoring before public exposure.
- `/api/industry/templates/import`, `/validate`, and DELETE routes inherit the `/api/industry/templates` public prefix because prefix matching is broad. This should be narrowed so only safe read/catalog routes are public.

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
   - Mask/omit `graph_db.password` in GET responses.
   - Return only presence flags for all secrets.
   - Add tests proving secrets are not returned.

3. Tenant isolation PR:
   - Add `org_id` metadata to simulation/report records.
   - Enforce org ownership on all ID-addressed campaign, simulation, report, graph, and pipeline routes.
   - Add cross-tenant denial tests.

4. RBAC PR:
   - Add centralized route role guards.
   - Enforce admin-only settings/API-key/org management and analyst-only simulation mutation.
   - Ensure viewers are read-only.

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
