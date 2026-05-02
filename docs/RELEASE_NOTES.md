# Release Notes

Updated: 2026-05-01

## PR T: Public Pilot Go/No-Go Verification

This verification pass adds no product features. It records the current release posture after PR P, PR Q, PR R, and PR S.

### Verification Summary

- Backend tests passed.
- Focused security tests passed.
- Frontend production build passed.
- Mocked Playwright e2e smoke tests passed.
- CI-equivalent secret hygiene scan passed.
- `git diff --check` passed.

### Go/No-Go Decision

| Release path | Current decision | Reason |
| --- | --- | --- |
| Local demo | Go | Demo mode works without real provider keys when synthetic data is used. |
| Controlled private pilot | Conditional go | Acceptable only for trusted users after manual credential rotation is confirmed, deployment secrets come from environment variables, and pilot data is non-confidential or explicitly approved. |
| Public pilot / public internet exposure | No-go | Manual credential rotation is not evidenced, production rate limiting still requires edge/shared enforcement, and browser auth storage is mitigated but not fully hardened. |
| Production customer deployment | No-go | Requires manual credential rotation, shared/edge rate limiting, hardened browser auth, formal data-retention/deletion policy, production storage decisions, and deployment operations controls. |

### Remaining Blockers

- Repository owners must rotate any provider/API/graph credentials that may have been committed before SEC-001 remediation.
- Public deployments need edge/API-gateway or shared-store rate limiting.
- Public/customer deployments need HttpOnly cookie auth, refresh-token auth, or an equivalent hardened browser-auth strategy.
- Pilot data-retention and deletion procedures must be approved before external users enter real scenarios.
- Legacy local JSON records without `org_id` must be reviewed, backfilled, or re-created before production use.

### Screenshot Note

No UI/security label text changed in PR T itself. Existing screenshots should still be re-reviewed before any public demo to confirm visible Demo Mode, Local Estimate, Live Backend, or Backend Verified labels and to ensure no secrets, tokens, private URLs, or customer data are visible.

## PR U: Screenshot And Demo Package Review

This pass reviewed the existing curated screenshots and demo package after PR S/PR T security hardening. It adds no product code and does not fabricate or recapture screenshots.

### Screenshot Decision

- Kept: `home-landing.png`, `demo-dashboard-overview.png`, `brief-quality-score.png`, `simulation-dashboard-kpis.png`, `war-room.png`, `action-plan.png`, and `settings-wizard.png`.
- Replaced: none.
- Reason: no visible UI/security wording changed after PR T, result screenshots already show source labels, and the Settings Wizard screenshot does not expose secrets.

### Demo Readiness Wording

- Local demo: go with synthetic data and no real secrets.
- Controlled private pilot: conditional go only after credential rotation evidence, environment-provided secrets, trusted users, and deployment controls.
- Public pilot / public internet exposure: no-go.
- Production customer deployment: no-go.

## Post-PR U Product-Trust Fix: Synthetic Influence Nodes

The dashboard influence section now uses simulated influence-node wording and explicitly states that demo/local estimate modes use synthetic nodes, not scraped or verified real social profiles.

This improves product trust without adding live social listening, real account discovery, or production-readiness claims.

## PR V: Release Candidate Integration

This integration pass selects PR V as the next roadmap item because the latest work remains open as a stacked PR chain rather than being merged into the default branch.

### Integration Decisions

- Use the latest completed branch stack as the release-candidate source of truth.
- Keep public pilot and production customer deployment as no-go.
- Keep controlled private pilot as conditional.
- Do not start PR W in this PR.

### Validation

Validation results are recorded in `docs/RELEASE_READINESS_CHECKLIST.md` and `docs/CODEX_ROADMAP_PROGRESS.md`.

## PR W: Client-Ready Strategy Pack

This pass adds a backend strategy-pack export payload for meeting preparation. It does not add new prediction claims, ROI guarantees, social integrations, or production-readiness claims.

### What Changed

- Added Brand Executive Summary and Agency Client Pitch Summary pack modes.
- Added sectioned outputs for executive decision summary, launch/revise/do-not-launch recommendation, KPI summary, segment reactions, risk drivers, crisis watchouts, recommended action plan, and next validation steps.
- Added section-level provenance so Demo Mode, Local Estimate, Live Backend, Backend Verified, and Unknown Source-style outputs remain traceable in exports.
- Added white-label metadata placeholders for agency/client/prepared-by/report-date/campaign/scenario fields without echoing logo URLs.

### Validation

- Focused backend tests passed: `backend/.venv/bin/python -m pytest backend/tests/test_strategy_pack.py backend/tests/test_api_contract.py backend/tests/test_rbac.py -q`.
- Full backend tests passed: `backend/.venv/bin/python -m pytest backend/tests -q`.
- Frontend build passed: `cd frontend && npm run build`.
- Secret hygiene scan and `git diff --check` passed.
