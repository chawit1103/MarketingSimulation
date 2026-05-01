# 3C Simulator Status

Updated: 2026-05-01

## Production-Ready

- Flask blueprints are consistently mounted under `/api/*`.
- Public no-key demo entrypoints are available for onboarding:
  - `GET /api/demo/campaigns`
  - `GET /api/demo/campaigns/<demo_id>/dashboard`
- Public quick impact estimate is available at `GET /api/impact/scenarios/<sentiment_value>`.
- Client-facing API responses are sanitized so raw tracebacks are not exposed.
- Production startup refuses known fallback auth/session secrets.
- New user passwords are stored with Werkzeug adaptive password hashing instead of custom salted SHA256.
- Legacy salted SHA256 password hashes are temporarily accepted and rehashed on successful login.
- In-memory rate limiting protects auth login/register, demo, status, decision, and simulation endpoint groups.
- Frontend source badges identify result provenance: Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source.

## Demo / Prototype

- Demo campaign dashboards use deterministic sample data and are labeled as Demo Mode.
- War Room output is currently a browser-side deterministic strategy estimate, not a live OASIS run.
- Comparator can fall back to browser-side sample output for demo continuity; fallback output is visibly labeled as Local Estimate.
- Quick impact scenarios are deterministic business estimates based on sentiment and supplied business inputs.

## Fixed In This PR

- `/api/impact/scenarios/<sentiment_value>` is now reachable without auth for the frontend quick scenario flow.
- `/api/demo/campaigns/<demo_id>/dashboard` has smoke coverage and returns result-source metadata.
- Public route contract tests cover demo dashboard and impact scenario endpoints.
- Raw `traceback` fields are stripped from JSON API responses before reaching clients.
- Production secret handling rejects default fallback secrets.
- Comparator and War Room now display visible result-source warnings when using demo or client-side fallback data.
- Password hashing moved from custom salted SHA256 to Werkzeug password hashes.
- Legacy password hashes are migrated lazily on successful login.
- Rate limits are configurable with `RATE_LIMIT_*` environment variables, including per-window limits for auth, demo, status, decision, and simulation groups.

## Remaining Gaps

- Rate limiting is in-memory and per-process; production should still use an edge/API-gateway limiter for multi-worker deployments.
- Legacy SHA256 password support should be removed after a migration window.
- War Room should be connected to backend campaign, competitor, and OASIS simulation records before being treated as a live simulation.
- Comparator fallback should eventually be replaced by backend-provided demo comparator fixtures.
- Demo dashboards should be expanded for every demo campaign instead of relying on one premium-water sample shape.
- Production deployment still needs environment-specific secret rotation, TLS, backup, observability, and CI gates.
- KPI and Decision Engine scoring should be calibrated against real campaign outcomes.
