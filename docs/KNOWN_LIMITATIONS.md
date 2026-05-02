# Known Limitations

Updated: 2026-05-02

This document separates what the system currently does from what should not yet be claimed.

## Simulation And Calibration

- Current demo dashboards are deterministic sample outputs, not measured market results.
- War Room output is deterministic scenario planning and should not be treated as calibrated social-listening prediction.
- Decision Engine, What-if, and Action Plan recommendations are rule-based guidance. They are not guaranteed campaign outcomes.
- Confidence values describe data completeness and provenance signals where available; they are not statistical confidence intervals.
- Manual Calibration v1 can compare aggregate actual campaign results against prior estimates, but it does not retrain models, self-improve future simulations, or overwrite original simulation outputs.
- Calibration status depends on approved user-supplied aggregate actuals and prior estimate fields. Missing or inconsistent actuals should be treated as incomplete evidence.

## Fallback Behavior

- Browser-side fallback output exists to preserve local demo continuity.
- Local fallback output must be treated as Local Estimate and should not be used as evidence of backend simulation success.
- Comparator still has browser-side demo fallback. A backend demo comparator fixture should replace it later.
- Demo dashboards are strongest for `demo-premium-water`; broader demo campaign coverage remains pending.
- Any new dashboard, export, or recommendation surface must inherit and show source-mode metadata before being considered release-ready.
- Calibration import accepts manual JSON and one-row aggregate CSV/JSON uploads only. It does not connect to live CRM, ad-platform, or social-listening systems.

## Infrastructure

- Rate limiting is in-memory and per-process. It trusts `X-Forwarded-For` only from configured `RATE_LIMIT_TRUSTED_PROXIES`, but production deployments with multiple workers still need edge/API-gateway or shared-store rate limiting.
- Tenant data still relies on JSON storage paths plus Neo4j, not a production relational database migration.
- Production deployment still needs TLS, backups, observability, environment-specific credential rotation, and deployment-owned shared/edge rate limiting.
- Neo4j availability warnings can appear during local tests when no local graph database is running.
- Audit logging and data-retention policies are not complete enough for broad enterprise rollout.
- Legacy local JSON simulation/report/project/task records created before `org_id` metadata was added may need to be re-created or backfilled before production use.

## Provider And Settings Readiness

- Settings readiness is deterministic configuration validation; it does not prove a cloud provider will accept a live request.
- The optional live LLM test requires authenticated runtime settings and real provider availability.
- Readiness and provider APIs intentionally do not return API keys or graph passwords.
- Cost estimate values are directional placeholders only and are not billing-grade.
- Local JSON settings secret storage is for demo/local use only. Production ignores provider/graph secret values in `settings.json`, resolves them from environment variables, and writes blank secret fields to the runtime settings file. A managed secret store is still recommended for mature deployments.

## Security Readiness

- Historical secret-like values may have been committed before repository secret hygiene was added. The repository cannot prove external credential rotation; owners must rotate any affected provider/API/graph credentials manually outside Codex.
- RBAC is enforced for the current route set, but newly added routes still need explicit role and tenant review before release.
- Organization switching is safely disabled and cannot issue cross-org tokens until a real multi-organization membership model exists.
- Browser auth tokens now use `sessionStorage` and legacy `localStorage` auth/API-key entries are removed, but the token is still readable by JavaScript if an XSS bug exists. Public or customer production deployments should use HttpOnly cookies, short-lived access tokens with refresh flow, or an equivalent hardened auth design.
- Browser API keys are treated as ephemeral session-only credentials for explicit admin/API workflows. Normal users should not store provider keys or API keys in the browser.
- 5xx API responses are sanitized globally, but long-tail route-specific validation/error messages should continue to be reviewed for internal-detail leakage.
- PR T verification keeps public pilot and public internet exposure blocked until manual credential rotation is evidenced, edge/shared rate limiting is deployed, browser auth storage is production-hardened or explicitly risk-accepted, and external data-retention/deletion expectations are approved.

## Testing

- Backend smoke and contract tests exist for critical public/product routes.
- Frontend production build is validated.
- Frontend unit tests, lint, and typecheck scripts are not configured yet.
- More backend coverage is needed for campaign CRUD, export edge cases, report generation flows, and full OASIS runner lifecycle.
- Manual pilot scripts and screenshot checks are documented, but not yet automated.
- Manual Calibration v1 records are local JSON aggregate records scoped by organization. Production deployments still need retention/deletion policy approval and a more durable governed storage model before broad external use.

## Privacy And Governance

- External pilot users should use non-confidential or approved campaign briefs until data-retention and deletion policies are formalized.
- Screenshots and docs should use demo or synthetic data only.
- Future Codex agents should follow repository-specific guidance in `AGENTS.md` before making implementation or review changes.

## Product Claims To Avoid

Do not claim:

- real-world outcome prediction accuracy,
- calibrated market-share forecasting,
- automatic model self-improvement from imported actual results,
- guaranteed crisis prevention,
- live social-listening integration,
- enterprise compliance certification,
- billing-ready usage metering,
- production SSO or audit-log completeness.

Safe positioning:

> 3C Simulator is a decision-intelligence and scenario-planning system for testing campaign, competitor, and crisis assumptions before real spend.
