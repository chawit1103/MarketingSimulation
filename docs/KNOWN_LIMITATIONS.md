# Known Limitations

Updated: 2026-05-01

This document separates what the system currently does from what should not yet be claimed.

## Simulation And Calibration

- Current demo dashboards are deterministic sample outputs, not measured market results.
- War Room output is deterministic scenario planning and should not be treated as calibrated social-listening prediction.
- Decision Engine, What-if, and Action Plan recommendations are rule-based guidance. They are not guaranteed campaign outcomes.
- Confidence values describe data completeness and provenance signals where available; they are not statistical confidence intervals.
- KPI and business-impact estimates still need calibration against real campaign results.

## Fallback Behavior

- Browser-side fallback output exists to preserve local demo continuity.
- Local fallback output must be treated as Local Estimate and should not be used as evidence of backend simulation success.
- Comparator still has browser-side demo fallback. A backend demo comparator fixture should replace it later.
- Demo dashboards are strongest for `demo-premium-water`; broader demo campaign coverage remains pending.

## Infrastructure

- Rate limiting is in-memory and per-process. Production deployments with multiple workers need edge/API-gateway or shared-store rate limiting.
- Tenant data still relies on JSON storage paths plus Neo4j, not a production relational database migration.
- Production deployment still needs TLS, backups, observability, CI gates, and environment-specific secret rotation.
- Neo4j availability warnings can appear during local tests when no local graph database is running.

## Provider And Settings Readiness

- Settings readiness is deterministic configuration validation; it does not prove a cloud provider will accept a live request.
- The optional live LLM test requires authenticated runtime settings and real provider availability.
- Readiness and provider APIs intentionally do not return API keys or graph passwords.
- Cost estimate values are directional placeholders only and are not billing-grade.

## Testing

- Backend smoke and contract tests exist for critical public/product routes.
- Frontend production build is validated.
- Frontend unit tests, lint, and typecheck scripts are not configured yet.
- More backend coverage is needed for campaign CRUD, export edge cases, report generation flows, and full OASIS runner lifecycle.

## Product Claims To Avoid

Do not claim:

- real-world outcome prediction accuracy,
- calibrated market-share forecasting,
- guaranteed crisis prevention,
- live social-listening integration,
- enterprise compliance certification,
- billing-ready usage metering,
- production SSO or audit-log completeness.

Safe positioning:

> 3C Simulator is a decision-intelligence and scenario-planning system for testing campaign, competitor, and crisis assumptions before real spend.
