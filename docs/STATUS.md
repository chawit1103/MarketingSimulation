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
- Deterministic Brief Quality Score is available at `POST /api/brief/quality` and does not require an LLM.
- War Room now defaults to the backend deterministic competitor simulation API at `POST /api/competitor/simulate`.
- Structured Action Plan output is available for dashboards and demo dashboards, with source mode, sectioned recommendations, reasons, expected impact, and risks.
- Settings Wizard supports Demo only, Local model, and Cloud API setup readiness checks without exposing secrets.
- Frontend source badges identify result provenance: Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source.

## Demo / Prototype

- Demo campaign dashboards use deterministic sample data and are labeled as Demo Mode.
- War Room backend output is deterministic scenario planning, not a calibrated live OASIS or social-listening run.
- War Room browser-side output remains available only as an explicit Local Estimate fallback after backend failure.
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
- Brief Quality Score checks objective, target audience, market/region, duration, budget, KPI, channel mix, competitor context, brand constraints, and risk/legal notes before simulation.
- Dashboard now includes a Confidence & Evidence panel with source mode, run ID when available, persona count, brief completeness, safe provider/model display, limitations, and next validation step.
- War Room calls the backend competitor API by default, exposes Local Estimate only as an explicit fallback, and labels fallback/backend source state visibly.
- War Room scenario templates now include price war, influencer backlash, product recall, regulatory issue, ESG controversy, fake news/rumor amplification, and competitor launch.
- War Room backend responses include expected sentiment movement, affected segments, amplification channels, key drivers, recommended response, and first 2h/24h/72h playbooks.
- Dashboard Action Plans now include creative adjustment, channel allocation, crisis prevention, and validation plan sections.
- Dashboard export payloads, CSV export, quick download, and PPTX action-plan slides can include structured action plan rows.
- Settings Wizard adds mode selection, deterministic readiness checks for LLM/embedding/Neo4j config, safe provider catalog access, sanitized provider errors, sample simulation guidance, and clearly labeled cost estimates.

## Remaining Gaps

- Rate limiting is in-memory and per-process; production should still use an edge/API-gateway limiter for multi-worker deployments.
- Legacy SHA256 password support should be removed after a migration window.
- Brief Quality Score is deterministic completeness scoring only; it does not validate factual accuracy or calibrate confidence against real-world outcomes.
- War Room should still be connected to full OASIS simulation records and real campaign calibration before being treated as measured market prediction.
- Action Plan recommendations remain deterministic planning guidance and still need calibration against real campaign outcomes.
- Settings Wizard readiness checks validate configuration completeness; LLM live tests still depend on authenticated runtime access and real provider availability.
- Comparator fallback should eventually be replaced by backend-provided demo comparator fixtures.
- Demo dashboards should be expanded for every demo campaign instead of relying on one premium-water sample shape.
- Production deployment still needs environment-specific secret rotation, TLS, backup, observability, and CI gates.
- KPI and Decision Engine scoring should be calibrated against real campaign outcomes.
