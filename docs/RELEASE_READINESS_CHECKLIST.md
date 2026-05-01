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

- [x] SEC-001 repository secret hygiene is partially remediated: `.env.dev` is removed from Git tracking, safe `.env.dev.example` placeholders are provided, and CI blocks tracked local env/runtime files plus common secret-like token patterns. Remaining manual action: rotate any provider/API/graph credentials that may have been committed before this PR.
- [x] Production refuses known fallback auth/session secrets.
- [x] New passwords use Werkzeug adaptive hashes.
- [x] Legacy salted SHA256 hashes are rehashed on successful login.
- [x] Public/high-risk endpoints are rate-limited in-process for local/demo use.
- [x] Raw traceback and stack fields are stripped from client-facing API JSON.
- [x] Common secret-like strings are redacted from client-facing API JSON.
- [x] Settings readiness checks do not echo API keys or graph passwords.
- [x] SEC-002 settings read exposure is remediated: `GET /api/settings` returns only secret presence flags and never raw or masked API keys/passwords.
- [x] Settings updates preserve existing secrets when blank fields, masked placeholders, or presence flags are submitted.
- [x] SEC-004 RBAC baseline is partially remediated: centralized role guards protect settings/API-key/destructive/admin operations and analyst/admin mutation flows.
- [x] SEC-006 auth route exposure is partially remediated: only auth login/register remain public, `/me` is authenticated, API-key generation is admin-only, and broken org switching returns a safe disabled response.
- [x] SEC-003 tenant isolation for ID-addressed resources is remediated for the current local JSON architecture: campaign pipeline status, dashboard KPI/report/timeline/segment routes, simulation reads/status/actions, reports, projects, graphs, and graph tasks are scoped to the authenticated organization.
- [x] SEC-005 dashboard provenance is remediated: fallback/mock KPI output is labeled `local_estimate`, demo fixtures are labeled `demo_mode`, and `backend_verified` is reserved for explicit persisted real simulation KPI metrics.
- [ ] Legacy local JSON simulation/report/project/task records without `org_id` are reviewed, backfilled, or re-created before production use.
- [ ] External pilot data-retention and deletion procedure is documented and approved.

## Automated Validation

- [x] Backend tests: `backend/.venv/bin/python -m pytest backend/tests`
- [x] Frontend production build: `cd frontend && npm run build`
- [x] Locale JSON validation: `python3 -m json.tool frontend/src/locales/en.json` and `th.json`
- [ ] Frontend unit tests: not configured.
- [ ] Frontend lint/typecheck: not configured.

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

This repository is suitable for a controlled demo, internal pilot, or product-discovery release candidate after manual demo-flow verification. It is not yet a fully calibrated enterprise prediction system.
