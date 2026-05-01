# Release Readiness Checklist

Updated: 2026-05-01

Use this checklist before tagging or deploying a release candidate.

## Scope Control

- [x] No database migration added in the release-readiness pass.
- [x] No billing, metering, or paid-plan enforcement added.
- [x] No unsupported LLM, embedding, or graph providers added.
- [x] Demo mode remains available without API keys.
- [x] Local estimate fallbacks remain explicit and labeled.
- [x] Repository governance is documented in top-level `AGENTS.md`.

## Critical Route Contracts

- [x] `/api/demo/campaigns`
- [x] `/api/demo/campaigns/<demo_id>/dashboard`
- [x] `/api/brief/quality`
- [x] `/api/decision/analyze`
- [x] `/api/decision/what-if`
- [x] `/api/comparator/compare`
- [x] `/api/comparator/metrics`
- [x] `/api/impact/scenarios/<sentiment_value>`
- [x] `/api/competitor/scenarios`
- [x] `/api/competitor/simulate`
- [x] `/api/export/pptx`
- [x] `/api/export/csv`
- [x] `/api/settings/providers`
- [x] `/api/settings/readiness`
- [x] `/api/report/generate/status`
- [x] campaign CRUD and pipeline routes used by the Campaigns view
- [x] dashboard KPI/report/timeline/segments routes
- [x] simulation create/prepare/start/stop/status routes

Backend smoke tests cover these contracts through `backend/tests/test_api_contract.py`.

## Result Source And Fallback Safety

- [x] Demo dashboards are labeled Demo Mode.
- [x] Dashboard local fallbacks are labeled Local Estimate.
- [x] Comparator demo/local fallback output is visibly labeled.
- [x] War Room calls the backend by default and exposes Local Estimate only after an explicit fallback action.
- [x] Action plans inherit source metadata.
- [x] Unknown source is displayed conservatively when source metadata is missing.

## Security And Abuse Protection

- [x] SEC-001 repository secret hygiene is partially remediated: `.env.dev` is removed from Git tracking, safe `.env.dev.example` placeholders are provided, and CI blocks tracked local env/runtime files plus common secret-like token patterns.
- [ ] SEC-001 manual credential rotation is complete and evidenced outside the repository. Remaining manual action: rotate any provider/API/graph credentials that may have been committed before remediation.
- [x] Production refuses known fallback auth/session secrets.
- [x] New passwords use Werkzeug adaptive hashes.
- [x] Legacy salted SHA256 hashes are rehashed on successful login.
- [x] Public/high-risk endpoints are rate-limited in-process for local/demo use.
- [x] Raw traceback and stack fields are stripped from client-facing API JSON.
- [x] Common secret-like strings are redacted from client-facing API JSON.
- [x] Settings readiness checks do not echo API keys or graph passwords.
- [x] SEC-002 settings read exposure is remediated: `GET /api/settings` returns only secret presence flags and never raw or masked API keys/passwords.
- [x] Settings updates preserve existing secrets when blank fields, masked placeholders, or presence flags are submitted.
- [x] SEC-004 RBAC baseline is remediated for the current route set: centralized role guards protect settings/API-key/destructive/admin operations, analyst/admin mutation flows, persona generation, report/export/simulation actions, and viewer read-only behavior.
- [x] SEC-006 auth route exposure is remediated by safe disablement: only auth login/register remain public, `/me` is authenticated, API-key generation is admin-only, cross-org switching is denied without existence leakage, and current-org switching returns a safe disabled response without a token.
- [x] SEC-003 tenant isolation for ID-addressed resources is remediated for the current local JSON architecture: campaign pipeline status, dashboard KPI/report/timeline/segment routes, simulation reads/status/actions, reports, projects, graphs, and graph tasks are scoped to the authenticated organization.
- [x] SEC-005 dashboard provenance is remediated: fallback/mock KPI output is labeled `local_estimate`, demo fixtures are labeled `demo_mode`, and `backend_verified` is reserved for explicit persisted real simulation KPI metrics.
- [x] SEC-008/010/011/013 production hardening baseline is remediated: debug/body logging are opt-in, query-parameter API keys are rejected, production CORS fails startup without explicit trusted origins, and 5xx API errors return stable client-safe messages.
- [x] SEC-007 production settings secret persistence is remediated for local files: production resolves LLM/embedding/graph secrets from environment variables, ignores local JSON secret fields, writes blank secret fields to `settings.json`, and keeps restrictive settings-file permissions where supported.
- [x] Local demo settings can still persist secrets only when explicitly allowed outside production.
- [x] SEC-009 limiter spoofing hardening is in place: `X-Forwarded-For` is trusted only from configured `RATE_LIMIT_TRUSTED_PROXIES`.
- [ ] SEC-009 production rate limiting uses an edge/API-gateway or shared Redis-backed limiter; the built-in limiter remains in-memory and local/demo oriented.
- [x] SEC-012 browser token persistence is reduced: auth tokens use `sessionStorage`, legacy `localStorage` auth tokens are migrated then removed, and browser API keys are not kept in persistent storage for normal UI sessions.
- [x] SEC-012 CSP/security headers are emitted by the Flask app for API responses.
- [ ] SEC-012 production auth uses secure HttpOnly cookies, a refresh-token flow, or an equivalent hardened browser-auth strategy.
- [ ] SEC-013 long-tail route handlers have been reviewed so route-level validation/errors do not reveal internal paths, object IDs, provider details, or unrecognized secrets.
- [x] Code supports production secrets through environment variables rather than local JSON settings.
- [ ] Deployment environment provides real production secrets through environment variables or an external secret manager.
- [ ] Legacy local JSON simulation/report/project/task records without `org_id` are reviewed, backfilled, or re-created before production use.
- [ ] External pilot data-retention and deletion procedure is documented and approved.

## Security Remediation Gate

- [x] SEC-002, SEC-003, SEC-005, SEC-008, SEC-010, and SEC-011 are fixed for the current architecture.
- [x] SEC-001 and SEC-013 are tracked as partially fixed with remaining actions.
- [x] SEC-004 and SEC-006 are fixed for the current local single-org architecture.
- [x] SEC-007 is fixed for production local-file secret persistence; managed secret-store adoption remains recommended.
- [x] SEC-009 and SEC-012 are documented accepted risks for local/demo and controlled private pilot contexts only.
- [x] Local demo readiness: acceptable when demo data is used, no real secrets are entered, and source-mode labels remain visible.
- [x] Controlled private pilot readiness: conditionally acceptable with trusted users, rotated credentials, environment-provided secrets, no confidential briefs, explicit source labels, and deployment-level rate limiting/CORS/log controls.
- [ ] Public pilot readiness: blocked until manual credential rotation is evidenced and deployment owners close SEC-009/SEC-012 public-exposure risks.
- [ ] Public internet exposure readiness: blocked until production rate limiting, auth storage, and deployment controls are complete.
- [ ] Production customer deployment readiness: blocked until manual credential rotation, shared rate limiting, safer auth storage, data-retention policy, storage architecture decisions, and any required multi-org membership feature are complete.

## Automated Validation

- [x] Backend tests: `backend/.venv/bin/python -m pytest backend/tests`
- [x] Frontend production build: `cd frontend && npm run build`
- [x] Locale JSON validation: `python3 -m json.tool frontend/src/locales/en.json` and `th.json`
- [ ] Frontend unit tests: not configured.
- [ ] Frontend lint/typecheck: not configured.

### PR O Verification Run

- [x] `backend/.venv/bin/python -m pytest backend/tests -q` passed on 2026-05-01: 47 passed, 26 warnings.
- [x] `backend/.venv/bin/python -m pytest backend/tests/test_rbac.py backend/tests/test_tenant_isolation.py backend/tests/test_settings_readiness.py backend/tests/test_dashboard_provenance.py backend/tests/test_production_hardening.py backend/tests/test_security_controls.py -q` passed on 2026-05-01: 30 passed, 20 warnings.
- [x] CI-equivalent secret hygiene scan passed on 2026-05-01.
- [x] `git diff --check` passed on 2026-05-01.
- [ ] Frontend build was not rerun for PR O because this PR changes documentation only.

### PR P Verification Run

- [x] `backend/.venv/bin/python -m pytest backend/tests/test_production_hardening.py backend/tests/test_settings_readiness.py -q` passed on 2026-05-01: 14 passed, 5 warnings.
- [x] `backend/.venv/bin/python -m pytest backend/tests -q` passed on 2026-05-01: 49 passed, 27 warnings.
- [x] CI-equivalent secret hygiene scan passed on 2026-05-01.
- [x] `git diff --check` passed on 2026-05-01.
- [ ] Frontend build was not rerun for PR P because no frontend files were changed.

### PR Q Verification Run

- [x] `backend/.venv/bin/python -m pytest backend/tests/test_rbac.py -q` passed on 2026-05-01: 7 passed, 5 warnings.
- [x] `backend/.venv/bin/python -m pytest backend/tests -q` passed on 2026-05-01: 51 passed, 38 warnings.
- [x] CI-equivalent secret hygiene scan passed on 2026-05-01.
- [x] `git diff --check` passed on 2026-05-01.
- [ ] Frontend build was not rerun for PR Q because no frontend files were changed.

### PR R Verification Run

- [x] `backend/.venv/bin/python -m pytest backend/tests/test_security_controls.py backend/tests/test_production_hardening.py -q` passed on 2026-05-01: 15 passed, 4 warnings.
- [x] `backend/.venv/bin/python -m pytest backend/tests -q` passed on 2026-05-01: 54 passed, 38 warnings.
- [x] CI-equivalent secret hygiene scan passed on 2026-05-01.
- [x] `git diff --check` passed on 2026-05-01.
- [ ] Frontend build was not rerun for PR R because no frontend files were changed.

### PR S Verification Run

- [x] `backend/.venv/bin/python -m pytest backend/tests/test_production_hardening.py -q` passed on 2026-05-01: 10 passed, warnings only.
- [x] `backend/.venv/bin/python -m pytest backend/tests -q` passed on 2026-05-01: 56 passed, 39 warnings.
- [x] `cd frontend && npm run build` passed on 2026-05-01.
- [x] CI-equivalent secret hygiene scan passed on 2026-05-01.
- [x] `git diff --check` passed on 2026-05-01.

### PR T Go/No-Go Verification Run

- [x] Source-of-truth docs re-read: `SECURITY_REVIEW.md`, `RELEASE_READINESS_CHECKLIST.md`, `KNOWN_LIMITATIONS.md`, `PILOT_PLAN.md`, and `DEPLOYMENT.md`.
- [x] `backend/.venv/bin/python -m pytest backend/tests -q` passed on 2026-05-01: 56 passed, 39 warnings.
- [x] `backend/.venv/bin/python -m pytest backend/tests/test_rbac.py backend/tests/test_tenant_isolation.py backend/tests/test_settings_readiness.py backend/tests/test_dashboard_provenance.py backend/tests/test_production_hardening.py backend/tests/test_security_controls.py -q` passed on 2026-05-01: 39 passed, 21 warnings.
- [x] `cd frontend && npm run build` passed on 2026-05-01.
- [x] `cd frontend && npm run test:e2e -- --project=chromium --workers=1` passed on 2026-05-01: 9 passed.
- [x] CI-equivalent secret hygiene scan passed on 2026-05-01.
- [x] `git diff --check` passed on 2026-05-01.

## Manual Demo Flow Checks

- [ ] Open `/dashboard/demo-premium-water` and confirm KPIs, confidence/evidence, source badge, and action plan render.
- [ ] Open `/comparator` without auth and confirm demo/local labels are visible.
- [ ] Open `/war-room`, run backend simulation, then verify explicit Local Estimate behavior if backend is unavailable.
- [ ] Open `/impact` and verify quick scenarios use `/api/impact/scenarios/<sentiment_value>`.
- [ ] Open `/settings` and verify Demo only, Local model, and Cloud API wizard paths do not expose secrets.

## Pre-Merge Governance Checks

- [ ] PR is focused and does not mix unrelated features, security work, docs, migrations, and refactors.
- [ ] Any changed backend route has a test or an explicit reason why it cannot be tested.
- [ ] Any changed critical frontend flow has a build check and either a manual check note or automated coverage.
- [ ] Any new result surface labels Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source.
- [ ] Docs are updated if API routes, demo paths, source labels, provider readiness, or release claims changed.

## Release Decision

This repository is suitable for local demo use with synthetic data and no real secrets.

Controlled private pilot remains conditional: it is acceptable only for trusted participants after manual credential rotation is evidenced, deployment secrets come from environment variables or a secret manager, demo/source labels remain visible, and pilot data-retention expectations are approved.

Public pilot, public internet exposure, and production customer deployment are blocked. The current blockers are missing manual credential-rotation evidence, lack of shared/edge production rate limiting, mitigated-but-not-fully-hardened browser auth storage, incomplete external pilot data-retention/deletion approval, and unresolved production storage/legacy-record review work.
