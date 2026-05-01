# 3C Simulator Roadmap

Updated: 2026-05-01

This roadmap reflects the current implementation after the production-hardening, security, brief-quality, War Room, Action Plan, Settings Wizard, and release-readiness passes.

## Now: Release Candidate Hardening

- Keep demo/local/live/backend-verified result source labels visible across dashboards, comparator, and War Room.
- Keep route-contract tests current whenever frontend API helpers change.
- Expand backend smoke tests around auth, campaign CRUD, template validation, KPI calculation, export, and report generation status.
- Validate frontend demo flows manually before each release candidate:
  - `/dashboard/demo-premium-water`
  - `/campaigns`
  - `/comparator`
  - `/war-room`
  - `/impact`
  - `/settings`
- Remove remaining misleading fallback behavior where a local estimate could be mistaken for a measured backend run.

## Next: Product Trust

- Calibrate deterministic KPI, Decision Engine, Action Plan, and War Room rules against real campaign outcomes.
- Store simulation run metadata and provenance so every dashboard can show run ID, source, persona count, provider/model, and limitations consistently.
- Replace browser-side comparator fallback with backend-provided demo comparator fixtures.
- Add demo dashboards for more sample campaigns beyond premium water.
- Add a brief-quality gate before expensive simulation runs in production flows.

## Next: Enterprise Readiness

- Replace in-memory rate limiting with edge/API-gateway or shared-store rate limiting for multi-worker deployments.
- Complete environment-specific secret rotation and production secret management.
- Add deployment health checks for backend, frontend, Neo4j, model provider readiness, storage, and export generation.
- Add CI gates for backend tests, frontend build, locale JSON validation, route-contract checks, and security smoke tests.
- Add audit logs for authentication, settings changes, simulation launches, exports, and admin actions.

## Later: Product Expansion

- Expand Thai industry templates for healthcare, restaurants/franchise, EV/automotive, FMCG, cosmetics, public policy, agriculture, insurance, and real estate.
- Improve PPTX templates into agency/client-ready executive packs with stronger narrative structure.
- Add collaboration workflows such as shared campaign review, comments, version compare, and approval.
- Add a calibration loop that compares simulation guidance with real campaign performance.
- Evaluate billing, usage metering, and team administration only after pilot validation.

## Out Of Scope For The Current Release

- Database migration.
- Billing or paid-plan enforcement.
- New LLM or embedding providers.
- Full OASIS calibration against live social data.
- Enterprise SSO.
