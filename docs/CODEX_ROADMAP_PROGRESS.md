# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR V: Release Candidate Integration**

## Why PR V Was Selected

PR V is the first roadmap item and is required when the latest security, demo, screenshot, public pilot, and product-trust work is still spread across open stacked PRs instead of being cleanly integrated into the target/default branch.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Latest local branch includes the full stacked work through PR U plus the synthetic influence-node labeling fix.
- The GitHub PR stack remains open and stacked rather than merged into `multilang-v0.3`.
- `.env.dev` is not tracked in the current branch.
- `.env.dev.example` is present.

Therefore PR V is needed before starting PR W.

## Completed In PR V

- Created a release-candidate integration branch from the latest completed stack.
- Re-read repository source-of-truth docs: `README.md`, `AGENTS.md`, `docs/SECURITY_REVIEW.md`, `docs/RELEASE_READINESS_CHECKLIST.md`, `docs/KNOWN_LIMITATIONS.md`, `docs/STATUS.md`, `docs/PILOT_PLAN.md`, and `docs/RELEASE_NOTES.md`.
- Confirmed release readiness wording remains:
  - Local demo: allowed with synthetic data and no real secrets.
  - Controlled private pilot: conditional.
  - Public internet exposure: blocked.
  - Production customer deployment: blocked.
- Confirmed source/provenance language remains explicit for demo, local estimate, live backend, backend verified, and unknown source modes.
- Confirmed simulated influence-node wording avoids implying real scraped social profiles.
- Updated the Playwright authenticated dashboard smoke fixture to use `sessionStorage`, matching the PR S browser token behavior.

## Not Completed In PR V

- PR W Client-Ready Strategy Pack was not started.
- No product features were added.
- No database migration, billing, production auth rewrite, live social listening, CRM integration, calibration loop, or social account discovery was added.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 56 passed and 39 warnings.
- `backend/.venv/bin/python -m pytest backend/tests/test_rbac.py backend/tests/test_tenant_isolation.py backend/tests/test_settings_readiness.py backend/tests/test_dashboard_provenance.py backend/tests/test_production_hardening.py backend/tests/test_security_controls.py -q`: passed, 39 passed and 21 warnings.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 9 passed after updating the smoke auth fixture from localStorage to sessionStorage.
- CI-equivalent secret hygiene scan: passed.
- `git diff --check`: passed.

GitNexus note: `impact` and `context` calls for `installApiMocks` failed with a local GitNexus WAL corruption error, so final scope validation used `detect_changes` instead.

## Remaining Blockers / Accepted Risks

- Manual credential rotation evidence is still required for any historical provider/API/graph credentials that may have been committed before secret hygiene remediation.
- Public deployments still need edge/API-gateway or shared-store rate limiting.
- Browser auth storage is mitigated but still needs HttpOnly cookie, refresh-token, or equivalent production hardening before public/customer deployment.
- External pilot data-retention and deletion procedures still need approval.
- Legacy local JSON records without `org_id` need review, backfill, or re-creation before production use.

## Next Recommended Roadmap Item

After PR V is reviewed and merged, proceed to **PR W: Client-Ready Strategy Pack**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
