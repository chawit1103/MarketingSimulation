# 3C Simulator Roadmap

Updated: 2026-05-02

This roadmap reflects the current implementation after the production-hardening, security, brief-quality, War Room, Action Plan, Settings Wizard, and release-readiness passes.

## Current Readiness

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

## Completed Brand & Agency Value Roadmap

- Client-ready strategy pack payloads for Brand Executive Summary and Agency Client Pitch Summary.
- Backend-first A/B/C Comparator demo fixtures with explicit Local Estimate fallback.
- Revised Brief v2 from Action Plan.
- Deep industry presets for high-value pilot categories.
- Budget Scenario Planner with assumption-based channel/segment allocation ranges.
- Manual Calibration v1 for aggregate actual-results comparison.
- Privacy-conscious pilot feedback analytics.
- Final Brand/Agency demo tracks and screenshot inventory review.

## Short-Term Priorities: Release Candidate And Pilot Readiness

- Keep demo/local/live/backend-verified result source labels visible across dashboards, comparator, and War Room.
- Keep route-contract tests current whenever frontend API helpers change.
- Expand backend smoke tests around auth, campaign CRUD, template validation, KPI calculation, export, and report generation status.
- Add CI for backend tests, frontend build, locale validation, diff hygiene, and route-contract tests.
- Validate frontend demo flows manually before each release candidate:
  - `/dashboard/demo-premium-water`
  - `/campaigns`
  - `/comparator`
  - `/war-room`
  - `/impact`
  - `/budget-planner`
  - `/calibration`
  - `/settings`
- Remove remaining misleading fallback behavior where a local estimate could be mistaken for a measured backend run.
- Run a controlled pilot with real marketing, PR, or strategy users and capture qualitative feedback.

## Mid-Term Priorities: Product Trust And Calibration

- Calibrate deterministic KPI, Decision Engine, Action Plan, and War Room rules against real campaign outcomes.
- Store simulation run metadata and provenance so every dashboard can show run ID, source, persona count, provider/model, and limitations consistently.
- Replace browser-side comparator fallback with backend-provided demo comparator fixtures.
- Add future public demo campaigns only when a matching industry-specific dashboard fixture and contract test are ready.
- Add a brief-quality gate before expensive simulation runs in production flows.
- Add pilot feedback review loops for brief quality, confidence/evidence, and action-plan usefulness.
- Improve PPTX templates into agency/client-ready executive packs with stronger narrative structure.

## Mid-Term Priorities: Enterprise Readiness

- Add edge/API-gateway or shared-store rate limiting before public internet exposure or multi-worker deployments.
- Complete environment-specific secret rotation and production secret management.
- Add deployment health checks for backend, frontend, Neo4j, model provider readiness, storage, and export generation.
- Add CI gates for backend tests, frontend build, locale JSON validation, route-contract checks, and security smoke tests.
- Add audit logs for authentication, settings changes, simulation launches, exports, and admin actions.
- Add production runbook coverage for backups, rollback, TLS, storage, and provider outage handling.

## Long-Term Priorities: Product Expansion

- Expand Thai industry templates for healthcare, restaurants/franchise, EV/automotive, FMCG, cosmetics, public policy, agriculture, insurance, and real estate.
- Add collaboration workflows such as shared campaign review, comments, version compare, and approval.
- Add a calibration loop that compares simulation guidance with real campaign performance.
- Evaluate billing, usage metering, and team administration only after pilot validation.
- Explore enterprise integrations only after auth, tenant isolation, data retention, and audit requirements are documented.

## Out Of Scope For The Current Release

- Database migration.
- Billing or paid-plan enforcement.
- New LLM or embedding providers.
- Full OASIS calibration against live social data.
- Enterprise SSO.
