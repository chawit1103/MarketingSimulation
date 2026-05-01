# Security Review

Updated: 2026-05-01

Scope reviewed: authentication and authorization, tenant isolation, public APIs and rate limiting, error handling, demo/local/source labeling, environment variables, storage of campaign/user/API-key data, and frontend exposure of sensitive configuration.

This review did not make product-code changes. It records release blockers, remediation evidence, and focused follow-up recommendations.

## Executive Summary

The repository has several good security foundations: password hashing now uses Werkzeug adaptive hashes, legacy password hashes are rehashed on login, production rejects known fallback auth secrets, public/demo routes are rate-limited, client-facing traceback payloads are sanitized, settings secrets are masked from browser reads, ID-addressed resources are scoped to the authenticated organization in the current local JSON architecture, and demo/local/live/backend-verified source labels exist in the UI.

However, the current repository is not production-ready for external customers. The remaining blockers are manual rotation of previously committed secret-like values, shared production rate limiting, remaining browser token exposure risk, and local/demo storage architecture limitations.

## Remediation Status Table

| Finding ID | Original severity | Current status | PR or file evidence | Remaining action |
| --- | --- | --- | --- | --- |
| SEC-001 | Critical | partially fixed | `.gitignore`, `.env.dev.example`, `.github/workflows/ci.yml`, `docs/CONTRIBUTING.md` | Repository hygiene is fixed, but owners must manually rotate any provider/API/graph credentials that may have been committed before remediation. Do not mark this complete without external rotation evidence. |
| SEC-002 | Critical | fixed | `backend/app/api/settings.py`, `backend/app/models/settings.py`, `frontend/src/views/Settings.vue`, `backend/tests/test_settings_readiness.py` | Continue ensuring future settings fields use presence flags and admin-only access. |
| SEC-003 | Critical | fixed | `backend/app/api/dashboard.py`, `backend/app/api/simulation.py`, `backend/app/api/report.py`, `backend/app/services/pipeline_orchestrator.py`, `backend/tests/test_tenant_isolation.py` | Backfill or re-create legacy local JSON records without `org_id` before any production use. Database-level tenant constraints remain future work. |
| SEC-004 | Critical | fixed for current route set | `backend/app/authz.py`, `backend/app/api/auth.py`, `backend/app/api/settings.py`, `backend/app/api/campaign.py`, `backend/app/api/simulation.py`, `backend/app/api/report.py`, `backend/app/api/export.py`, `backend/app/api/persona.py`, `backend/tests/test_rbac.py` | Admin, analyst, and viewer route behavior is covered for critical routes. Every newly added route still requires explicit RBAC review. |
| SEC-005 | High | fixed | `backend/app/services/kpi_calculator.py`, `backend/app/api/dashboard.py`, `frontend/src/components/ResultSourceBadge.vue`, `backend/tests/test_dashboard_provenance.py` | Expand real KPI extraction when the simulation runner emits a stable KPI schema; do not mark raw runner output as backend verified. |
| SEC-006 | High | fixed by safe disablement | `backend/app/api/auth.py`, `backend/app/middleware/tenant.py`, `backend/tests/test_rbac.py` | Login/register are the only public auth routes. API-key generation is admin-only. Org switching cannot issue cross-org tokens and remains disabled until a real membership model exists. |
| SEC-007 | High | fixed for production file persistence | `backend/app/models/settings.py`, `backend/app/config.py`, `backend/tests/test_production_hardening.py`, `docs/DEPLOYMENT.md` | Production resolves provider/graph secrets from environment variables and writes blank secret fields to local JSON. A managed secret store is still recommended for mature deployments. |
| SEC-008 | High | fixed | `backend/app/__init__.py`, `backend/app/utils/response_safety.py`, `backend/app/config.py`, `backend/tests/test_production_hardening.py` | Keep request body logging opt-in and redacted; review new logs for campaign brief or secret leakage. |
| SEC-009 | Medium | partially fixed | `backend/app/middleware/rate_limit_middleware.py`, `backend/app/config.py`, `backend/tests/test_security_controls.py` | Built-in limiter remains local/demo oriented, but it no longer trusts `X-Forwarded-For` unless the request comes from a configured trusted proxy. Public internet deployments still need edge/API-gateway or shared Redis-backed rate limiting. |
| SEC-010 | Medium | fixed | `backend/app/middleware/tenant.py`, `backend/tests/test_production_hardening.py` | Tokens/API keys must stay in `Authorization: Bearer` or `X-Api-Key`; do not reintroduce query-token auth. |
| SEC-011 | Medium | fixed | `backend/app/config.py`, `backend/app/__init__.py`, `backend/tests/test_production_hardening.py` | Production startup fails unless explicit trusted `CORS_ALLOWED_ORIGINS` are configured. |
| SEC-012 | Medium | partially fixed | `frontend/src/api/authStorage.js`, `frontend/src/api/index.js`, `backend/app/__init__.py`, `backend/app/config.py`, `backend/app/services/auth_service.py`, `backend/tests/test_production_hardening.py` | Auth tokens now use session storage with localStorage migration/removal, persistent browser API-key storage is avoided for normal UI sessions, security headers/CSP are added, and production token lifetime defaults shorter. HttpOnly cookie or refresh-token auth remains future work. |
| SEC-013 | Medium | partially fixed | `backend/app/utils/response_safety.py`, `backend/app/__init__.py`, `backend/tests/test_public_routes.py`, `backend/tests/test_security_controls.py`, `backend/tests/test_production_hardening.py` | 5xx API errors are sanitized globally, but long-tail route-level 4xx/error messages should continue to be normalized. |

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
- Status: Fixed for the current route set in PR Q; route ownership isolation completed in PR L for ID-addressed resources
- Evidence: `UserRole` exists, but protected routes generally only require authentication. Sensitive routes such as settings update, campaign deletion, report deletion, API-key generation, and simulation lifecycle operations do not consistently enforce admin/analyst/viewer permissions.
- Impact: A viewer or low-privilege user may be able to mutate settings, delete data, start/stop simulations, or access privileged operational flows.
- Remediation: A centralized `role_required()` guard now enforces admin-only settings/API-key/destructive operations, analyst-or-admin campaign/persona/report/simulation/export generation flows, and viewer read-only behavior on the covered routes. Regression tests cover viewer mutation denial, analyst denial for settings/API-key/provider live test, and admin-positive privileged flows.
- Remaining action: Continue auditing newly added routes for explicit role checks and ownership checks as part of normal PR review.

## High Findings

### SEC-005: Backend-verified labels are applied to mock KPI output

- Severity: High
- Status: Remediated in PR M for dashboard KPI/report/timeline/segment APIs and KPI calculation provenance
- Evidence: `backend/app/api/dashboard.py` marks dashboard action-plan source as `backend_verified`, while `KPICalculator.calculate()` falls back to mock data when no real simulation data is provided. It does not verify campaign existence or ownership before returning generated KPI values.
- Impact: A user can request a dashboard for an arbitrary campaign ID and receive plausible-looking KPI values labeled as backend verified. This is not a direct secret leak, but it violates the repository's source-labeling safety rule and can mislead business decisions.
- Remediation: Dashboard APIs require campaign existence and organization ownership before returning data. `KPICalculator.calculate()` now emits explicit provenance: local deterministic fallback is labeled `local_estimate` with `data_basis=local_estimate`, demo fixtures remain `demo_mode`, and `backend_verified` is used only when explicit persisted simulation KPI metrics are provided with `data_basis=real_simulation`. Dashboard action plans inherit the same source metadata.
- Remaining action: Expand real simulation KPI extraction once the OASIS runner emits a stable sentiment/conversion KPI schema. Raw runner rounds/actions alone are intentionally not treated as backend-verified KPI evidence.

### SEC-006: Auth routes bypass centralized tenant middleware and contain broken privileged paths

- Severity: High
- Status: Fixed by safe disablement in PR Q
- Evidence:
  - `TenantMiddleware.PUBLIC_PREFIXES` marks all `/api/auth/` routes as public.
  - `auth_required()` reimplements token checks, does not reject `None` payload before `.get()`, loads users globally, and allows downstream execution when user/org lookup fails.
  - `/api/auth/api-key` calls `UserService.generate_and_store_api_key()`, which is not implemented.
  - `/api/auth/switch-org` calls `AuthService.switch_org()`, which is not implemented.
- Impact: Protected auth routes are inconsistent with the main auth/tenant control. API-key and org-switch flows fail, and token/user/org state checks are weaker than the main middleware.
- Remediation: Only `/api/auth/login` and `/api/auth/register` remain public. `/me`, `/api-key`, and `/switch-org` now use tenant middleware plus explicit role guards. API-key generation uses the existing `UserService.generate_api_key()` path and is admin-only. Organization switching denies all target organizations outside the current user's organization with the same safe `403`, never returns a token, and returns client-safe `501` for the current org until a tenant-membership model is implemented.
- Remaining action: Implement real multi-organization membership and safe org switching if the product needs it, or remove the route entirely before production.

### SEC-007: Runtime settings are stored plaintext on local disk

- Severity: High
- Status: Fixed for production file persistence in PR P; local JSON secret persistence remains allowed only for local/demo mode
- Evidence: `SettingsManager.save()` persists LLM API keys, embedding API keys, and graph passwords into `backend/uploads/settings.json`.
- Impact: File-system compromise, backups, logs, or volume snapshots can expose provider credentials. The file is gitignored, which helps source control, but not production runtime security.
- Remediation: Browser reads no longer receive stored secret values, settings updates no longer persist masked placeholders as real values, and the Settings UI stores only presence metadata in local browser settings. In production, `SettingsManager` ignores secret values from `settings.json`, resolves LLM/embedding/graph secrets from environment variables, writes blank secret fields to the runtime settings file even if `SETTINGS_PERSIST_SECRETS=true`, and applies restrictive permissions to the local settings file where supported.
- Remaining action: A managed secret store is still recommended for mature multi-user production deployments, but plaintext local JSON is no longer the production source of provider or graph secrets.

### SEC-008: Request body debug logging can record secrets and campaign briefs

- Severity: High
- Status: Remediated in PR N for default behavior; development logging remains opt-in and redacted
- Evidence: Prior to PR N, `create_app()` logged JSON request bodies at debug level and `Config.DEBUG` defaulted to true.
- Impact: Login passwords, provider API keys, settings payloads, campaign briefs, and customer data can enter logs.
- Remediation: `FLASK_DEBUG` defaults to false, request body logging is disabled unless `REQUEST_BODY_LOGGING_ENABLED=true`, and redaction covers passwords, API keys, tokens, secrets, graph passwords, and campaign brief/simulation requirement text.

## Medium Findings

### SEC-009: In-memory rate limiting is not sufficient for production

- Severity: Medium
- Status: Partially fixed in PR R; blocker for public internet exposure without edge/shared controls
- Evidence: `RateLimitMiddleware` is per-process, memory-backed, and keys on `X-Forwarded-For` when present.
- Impact: Multi-worker deployments do not share counters, restarts reset limits, and spoofed forwarding headers can bypass limits unless a trusted proxy overwrites them.
- Remediation: The built-in limiter remains dependency-free for local/demo mode and now only trusts `X-Forwarded-For` when the request remote address matches `RATE_LIMIT_TRUSTED_PROXIES`. Production startup warns when the limiter backend remains `memory`.
- Remaining action: Add edge/API-gateway or Redis-backed shared rate limiting before public internet exposure. Only configure `RATE_LIMIT_TRUSTED_PROXIES` to proxies that overwrite inbound forwarding headers.

### SEC-010: API keys are accepted in query parameters

- Severity: Medium
- Status: Remediated in PR N
- Evidence: Prior to PR N, `TenantMiddleware._extract_token()` accepted `?api_key=...`.
- Impact: Query tokens are commonly captured in access logs, browser history, analytics, referrers, and screenshots.
- Remediation: Query-parameter API keys are no longer accepted. Auth credentials must be sent through `Authorization: Bearer` or `X-Api-Key`.

### SEC-011: CORS is wide open for all API routes

- Severity: Medium
- Status: Remediated in PR N for production defaults
- Evidence: Prior to PR N, `create_app()` configured `CORS(app, resources={r"/api/*": {"origins": "*"}})`.
- Impact: The app uses Authorization headers rather than cookies, so this is not a classic cookie CSRF issue. Still, broad CORS weakens browser-origin boundaries and should not be the production default.
- Remediation: CORS origins are configurable via `CORS_ALLOWED_ORIGINS`. Local development defaults to `*`; production startup fails unless explicit trusted origins are configured.

### SEC-012: Frontend stores auth tokens/API keys in localStorage

- Severity: Medium
- Status: Partially fixed in PR S
- Original evidence: `frontend/src/api/index.js` read `3c-auth-token` and `3c-api-key` from `localStorage`.
- Impact: Any XSS in the frontend can exfiltrate tokens/API keys. No CSP was observed in this review.
- Remediation: Browser auth token access now goes through `frontend/src/api/authStorage.js`, which migrates legacy localStorage tokens into `sessionStorage` and removes persistent localStorage copies. Browser API keys are treated as ephemeral session-only credentials and persistent localStorage API keys are removed. Backend responses include `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, and `Permissions-Policy` headers by default. Production auth token lifetime now defaults to 8 hours and can be configured with `AUTH_TOKEN_EXPIRY_SECONDS`.
- Remaining action: Prefer short-lived access tokens with refresh flow or secure HttpOnly cookies before public/customer production. Session storage still remains script-readable if XSS occurs, so CSP reduces but does not eliminate the risk.

### SEC-013: Error handling strips tracebacks but still returns raw exception strings in many handlers

- Severity: Medium
- Status: Partially remediated in PR N
- Evidence: Many API handlers return `error: str(e)`; the global sanitizer removes traceback keys and redacts some common secret patterns.
- Impact: Non-traceback exception strings can still reveal internal paths, provider details, object IDs, or unrecognized secret formats.
- Remediation: The global API response sanitizer now replaces 5xx client-facing `error` strings with `Internal server error` plus `code=internal_error`, while logging details server-side. Route-level cleanup should continue for 4xx validation messages and long-tail handlers.

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
- Settings can still persist provider and graph secrets in plaintext local JSON for demo/local workflows only. Production ignores local JSON secret fields, uses environment variables for runtime secrets, and writes blank secret fields to `settings.json`.
- Simulation, report, project, pipeline, graph, and graph-task routes now carry or enforce organization ownership in the current local JSON architecture. Legacy records without ownership metadata need backfill or re-creation before production use.

## Frontend Exposure Review

- Frontend environment exposure is limited to Vite-prefixed variables such as `VITE_API_BASE_URL` and analytics flags.
- No backend secret environment variables are intentionally exposed through Vite config.
- The main browser-side risk is remaining script-readable session token storage. Persistent localStorage auth token/API-key storage has been reduced, but a full HttpOnly-cookie or refresh-token design is still pending.
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
   - Stop returning mock KPI data as `backend_verified`. Completed in PR M.
   - Require campaign existence/ownership before dashboard APIs. Completed in PR L and covered by PR M tests.
   - Label any deterministic fallback as `local_estimate` or `demo_mode`. Completed in PR M.

6. Production hardening PR:
   - Set debug false by default. Completed in PR N.
   - Disable request body logging or redact it. Completed in PR N.
   - Restrict CORS by environment. Completed in PR N.
   - Remove query-parameter API-key auth. Completed in PR N.
   - Trust `X-Forwarded-For` only from configured trusted proxies. Completed in PR R.
   - Document required edge/shared rate limiting. Updated in PR R; shared limiter implementation remains deployment responsibility.

## Release Decision

For controlled local demos, the current repository is acceptable if no real secrets are used and demo/local labels remain visible.

For a controlled private pilot, the repository is conditionally acceptable only with trusted users, rotated credentials, no confidential customer briefs, explicit source labels, environment-provided secrets, and deployment controls around rate limiting/CORS/logging. This is not a production-readiness claim.

For a public pilot, public internet exposure, or customer production deployment, the release is not ready while manual SEC-001 credential rotation lacks evidence, SEC-009 still lacks shared/edge enforcement, and SEC-012 remains only partially fixed.
