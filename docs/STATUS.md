# 3C Simulator Status

Updated: 2026-05-02

## Current Release Readiness

- Local demo: ready with synthetic data and no real secrets.
- Controlled private pilot: conditional candidate with trusted users, credential rotation evidence, environment-provided secrets, visible source labels, and deployment controls.
- Public pilot: blocked.
- Public internet exposure: blocked.
- Production customer deployment: blocked.

This document lists implemented controls and remaining gaps. It does not claim the full product is production-ready.

## Implemented / Hardened Controls

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
- Frontend source badges identify result provenance: Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source. Backend Verified is reserved for persisted real simulation KPI/evidence for an owned campaign/run; backend route success alone is not enough.
- Dashboard influence surfaces now describe demo/local accounts as simulated influence nodes, not real scraped or verified social profiles.
- Comparator now uses backend demo fixtures for emotional/storytelling, proof-led/trust, and price/promotion directions and keeps browser-side output as explicit Local Estimate fallback only.
- Revised Brief v2 is available from dashboard Action Plans through `POST /api/brief/revise`; it preserves action-plan provenance and can be reviewed against the original brief.
- Deep industry presets are available for FMCG/CPG, Insurance/InsurTech, Retail/Ecommerce, Real Estate, EV/Automotive, and Healthcare/Wellness. Each preset includes assumptions, limitations, common objections, crisis triggers, proof requirements, risk checklist, and action-plan hints.
- Budget Scenario Planner is available at `POST /api/decision/budget-scenario` and `/budget-planner`; it provides assumption-based channel/segment allocation ranges, trade-offs, confidence, assumptions, limitations, and validation steps without claiming exact ROI or ROAS prediction.
- Manual Calibration v1 is available at `POST /api/calibration/actual-results`, `GET /api/calibration/status/<campaign_id>`, and `/calibration`; it compares aggregate actual campaign results against prior estimates without live CRM/social ingestion or model self-learning claims.
- Provider-neutral pilot analytics emits sanitized browser `3c:analytics` events for key journeys and feedback without installing a third-party SDK or sending network requests by default.
- Brand/Agency roadmap documentation now provides separate Brand Safety / C-Level and Agency Pitch / A/B/C demo tracks, with screenshot inventory and readiness language kept aligned to this checklist.
- Critical frontend route contracts are covered by backend smoke tests for demo, impact, decision, comparator, competitor, export, settings readiness, and report status endpoints.
- API response safety removes raw traceback keys and redacts common secret-like strings before JSON responses reach clients.

## Demo / Prototype

- Demo campaign dashboards use deterministic sample data and are labeled as Demo Mode. Public demo dashboards are available for premium water, InsurTech trust recovery, and community energy scenarios.
- War Room backend output is deterministic scenario planning, not a calibrated live OASIS or social-listening run.
- War Room browser-side output remains available only as an explicit Local Estimate fallback after backend failure.
- Comparator can use browser-side output only after the user explicitly runs Local Estimate; backend demo fixtures are preferred for no-key demo comparison.
- Quick impact scenarios are deterministic business estimates based on sentiment and supplied business inputs.
- Budget Scenario Planner outputs are deterministic scenario estimates. Demo mode uses synthetic fixtures, and backend planner output is directional guidance rather than calibrated media performance evidence.
- Manual Calibration v1 stores user-supplied aggregate actuals as local organization-scoped JSON records. It is calibration evidence capture, not live market sensing or automatic model improvement.
- Pilot analytics is local/browser-event based by default. A real analytics destination, retention policy, opt-out behavior, and privacy review are still required before external customer analytics collection.

## Recently Fixed / Hardened

- `/api/impact/scenarios/<sentiment_value>` is now reachable without auth for the frontend quick scenario flow.
- `/api/demo/campaigns/<demo_id>/dashboard` has smoke coverage and returns result-source metadata.
- Public demo list now includes only demo campaigns with matching industry-specific dashboard fixtures; unknown demo IDs return safe 404 instead of falling back to another demo.
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
- Client-ready strategy pack export is available at `POST /api/export/strategy-pack` with Brand Executive Summary and Agency Client Pitch Summary modes; every section includes source/provenance metadata. `POST /api/export/strategy-pack/pptx` renders the same payload as a PPTX deck with provenance metadata on every slide and a limitations / recommended validation slide.
- Settings Wizard adds mode selection, deterministic readiness checks for LLM/embedding/Neo4j config, safe provider catalog access, sanitized provider errors, sample simulation guidance, and clearly labeled cost estimates.
- Frontend report status helper now uses the backend `POST /api/report/generate/status` contract.
- Response sanitization now redacts API-key, token, password, bearer-token, and `sk-*` style values from client-facing JSON.
- Release-readiness documentation was added for checklist, known limitations, roadmap, and post-implementation action planning.

## Remaining Gaps

- Rate limiting is in-memory and per-process; public internet exposure requires edge/API-gateway or shared-store rate limiting before deployment.
- Legacy SHA256 password support should be removed after a migration window.
- Brief Quality Score is deterministic completeness scoring only; it does not validate factual accuracy or calibrate confidence against real-world outcomes.
- War Room should still be connected to full OASIS simulation records and real campaign calibration before being treated as measured market prediction.
- Action Plan recommendations remain deterministic planning guidance and still need calibration against real campaign outcomes.
- Revised Brief v2 is a deterministic draft-generation workflow from the Action Plan; it does not guarantee improved campaign performance and should be reviewed before saving or re-simulation.
- Strategy packs are structured JSON payloads for meeting preparation; PPTX/template rendering for white-label agency decks still needs a dedicated design pass.
- Settings Wizard readiness checks validate configuration completeness; LLM live tests still depend on authenticated runtime access and real provider availability.
- Comparator backend demo fixtures are deterministic planning examples; they are not real-world A/B test evidence or calibrated campaign lift.
- Deep industry presets are deterministic starter assumptions. They must be reviewed, localized, and adjusted with real brand, legal, compliance, and market context before pilot or client use.
- Budget Scenario Planner does not use live ad-platform costs, exact ROI/ROAS modeling, CAC prediction, or sales forecasting. It needs calibration with real media benchmarks and pilot outcomes.
- Additional demo dashboards beyond the current premium water, InsurTech trust recovery, and community energy fixtures can be added when they have industry-specific evidence and source labels.
- Production deployment still needs environment-specific secret rotation, TLS, backup, observability, and CI gates.
- KPI and Decision Engine scoring should be calibrated against real campaign outcomes.
- Manual Calibration v1 needs real approved aggregate campaign outcomes from multiple comparable campaigns before any calibration status should influence high-stakes spend decisions.
