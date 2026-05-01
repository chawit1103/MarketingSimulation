# Post-Implementation Action Plan

Updated: 2026-05-01

This plan focuses on turning the current release candidate into a reliable pilot and then an enterprise-ready product.

## Product

1. Run five guided pilot scenarios with target users:
   - FMCG launch
   - crisis response
   - competitor launch
   - premium pricing test
   - regulated/finance campaign
2. Capture where users hesitate: brief entry, source labels, confidence/evidence, War Room, export, and Settings Wizard.
3. Turn the best demo paths into first-run templates with sample campaigns and expected outputs.
4. Replace browser-side comparator fallback with backend demo fixtures.
5. Expand demo dashboards beyond `demo-premium-water`.
6. Calibrate KPI, Decision Engine, War Room, and Action Plan rules against real or historical campaign outcomes.
7. Maintain product claims discipline: describe outputs as scenario planning until calibration evidence exists.

## QA

1. Add CI for backend tests, frontend build, and locale validation.
2. Add frontend unit/component tests for:
   - ResultSourceBadge
   - Settings Wizard readiness display
   - Comparator fallback warnings
   - War Room backend failure and explicit Local Estimate flow
   - Dashboard Confidence & Evidence panel
3. Add backend tests for:
   - campaign CRUD
   - export PPTX/CSV error handling
   - report status route
   - settings update safety
   - public route rate limits
4. Add manual release screenshots for dashboard, comparator, War Room, impact, and settings.
5. Track test warnings separately from failures so Neo4j local warnings do not hide real regressions.
6. Add regression checks for source labels, fallback warnings, and sanitized client-facing errors before every demo release.

## Deployment

1. Define production `.env` requirements and block deployment when required secrets are missing.
2. Add a deployment health page or release runbook that checks:
   - backend liveness
   - `/api/status`
   - Neo4j connectivity
   - configured LLM provider
   - configured embedding provider
   - export generation
   - disk/storage availability
3. Put rate limiting at the edge or API gateway for production.
4. Add structured logs for auth events, settings changes, simulation runs, export attempts, and backend fallback/errors.
5. Add backups for tenant JSON storage and Neo4j data.
6. Add TLS, secret rotation, observability, and rollback steps before public launch.
7. Document data retention and deletion expectations before inviting external pilot users.

## Pilot Users

1. Start with controlled internal or partner pilots; avoid broad public claims about prediction accuracy.
2. Ask each pilot user to bring one real campaign brief and one risky competitor/crisis scenario.
3. Require users to record:
   - campaign objective
   - audience assumptions
   - source mode shown in the UI
   - confidence/evidence notes
   - action plan accepted/rejected
   - eventual real-world outcome if available
4. Use pilot feedback to tune brief-quality scoring and deterministic recommendation rules.
5. Convert successful pilot outputs into anonymized case studies only after validating the underlying assumptions.

See [PILOT_PLAN.md](PILOT_PLAN.md) for the recommended pilot structure, participant profile, session script, and success criteria.

## Governance

1. Use [../AGENTS.md](../AGENTS.md) as the standing instruction set for future Codex implementation and review tasks.
2. Keep PRs focused by theme: security, product trust, demo/docs, QA, deployment, or UX.
3. Require explicit source-mode labeling for every new result surface.
4. Treat privacy, tenant isolation, auth, and fallback transparency regressions as release blockers.
5. Keep docs synchronized with implementation whenever API routes, result-source modes, provider readiness, or demo paths change.

## Recommended Next PRs

1. Add CI workflow for backend tests, frontend build, and locale validation.
2. Add frontend component tests for source labels and explicit fallback warnings.
3. Add backend demo comparator fixture route to remove browser-side comparator fallback.
4. Add broader demo dashboards and industry sample briefs.
5. Add production deployment runbook with environment validation and rollback steps.
