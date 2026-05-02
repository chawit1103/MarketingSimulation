# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR X: Campaign A/B/C Comparator Backend-First**

## Why PR X Was Selected

PR W was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR X: Campaign A/B/C Comparator Backend-First.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-x-comparator-backend-first`.
- Release-candidate integration docs from PR V are present.
- PR W strategy-pack export exists.
- Comparator frontend previously called backend first but silently generated browser-side fallback results after failure.
- Comparator demo options were browser-local rather than backend fixtures.
- Frontend comparison results hardcoded `backend_verified` after any successful comparator API response instead of inheriting backend provenance.

Therefore PR X is the next correct focused PR.

## Completed In PR X

- Added backend comparator demo fixtures for three variants:
  - Emotional / storytelling direction.
  - Proof-led / trust direction.
  - Price / promotion direction.
- Added public no-key demo comparator routes:
  - `GET /api/comparator/demo/campaigns`.
  - `POST /api/comparator/demo/compare`.
- Expanded comparator output with:
  - overall winner and ranked recommendation.
  - segment-level strengths and weaknesses.
  - conversion and engagement estimates.
  - crisis/risk comparison.
  - trade-offs.
  - recommended use case per variant.
  - source/provenance metadata per variant and for the comparison result.
- Updated authenticated comparator results so `backend_verified` is used only when all compared variants are persisted real simulation KPI records.
- Labeled deterministic fallback KPI comparisons as `local_estimate`.
- Updated Comparator UI to use backend demo fixtures first and to require an explicit Local Estimate action after backend failure.
- Added backend comparator tests, route contract coverage, and e2e smoke coverage for backend demo comparator labels.
- Updated README, demo script, user journey, status, checklist, and release notes.

## Not Completed In PR X

- No live simulation calibration was added.
- No real-world A/B accuracy, sales lift, ROAS, or ROI guarantee was claimed.
- No social listening, CRM integration, or paid provider integration was added.
- No database migration was added.
- No exact ROI, sales forecast, or guaranteed prediction language was added.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests/test_comparator_api.py backend/tests/test_api_contract.py -q`: passed, 7 passed and 4 warnings.
- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 63 passed and 38 warnings.
- `python3 -m json.tool src/locales/en.json` and `src/locales/th.json`: passed.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 10 passed.
- CI-equivalent secret hygiene scan: passed.
- `git diff --check`: passed.

GitNexus note: `impact` and `context` calls failed with a local GitNexus WAL corruption error during this work, so final scope validation will use `detect_changes` instead.

## Remaining Blockers / Accepted Risks

- Manual credential rotation evidence is still required for any historical provider/API/graph credentials that may have been committed before secret hygiene remediation.
- Public deployments still need edge/API-gateway or shared-store rate limiting.
- Browser auth storage is mitigated but still needs HttpOnly cookie, refresh-token, or equivalent production hardening before public/customer deployment.
- External pilot data-retention and deletion procedures still need approval.
- Legacy local JSON records without `org_id` need review, backfill, or re-creation before production use.

## Next Recommended Roadmap Item

After PR X is reviewed and merged, proceed to **PR Y: Revised Brief v2 From Action Plan**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
