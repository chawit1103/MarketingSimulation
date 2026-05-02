# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR AB: Manual Data Import + Calibration v1**

## Why PR AB Was Selected

PR AA was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR AB: Manual Data Import + Calibration v1.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-ab-manual-calibration-v1`.
- Release-candidate, strategy-pack, comparator, revised-brief, and deep-preset roadmap work is present.
- Budget Scenario Planner is present.
- There was no manual aggregate actual-results workflow or estimate-vs-actual calibration comparison.

## Completed In PR AB

- Added deterministic backend Calibration Service for manual aggregate actual-results import.
- Added `POST /api/calibration/actual-results` for analyst/admin import.
- Added `GET /api/calibration/status/<campaign_id>` for authenticated calibration status reads.
- Supported manual JSON payloads and single-row aggregate CSV/JSON uploads.
- Supported actual result fields include:
  - campaign ID and date range.
  - impressions, clicks, CTR, conversion count/rate, sales lift, sentiment score, and crisis incident flag.
  - optional anonymized qualitative notes.
  - optional prior estimates for estimate-vs-actual deltas.
- Added calibration output for:
  - estimate vs actual comparison.
  - metric delta and absolute error percentage.
  - matched/missed risk classification.
  - segment assumption gaps when supplied.
  - calibration status: `not_calibrated`, `partially_calibrated`, or `calibrated_with_n_campaigns`.
  - privacy review, limitations, and recommended next validation step.
- Added privacy safeguards that reject PII-like fields, raw CRM/contact data, raw social posts/comments, and PII-like notes.
- Added `/calibration` frontend view for manual import and upload workflow.
- Added Campaigns navigation entry for Calibration.
- Added e2e smoke coverage for calibration status, manual evidence labeling, and privacy wording.
- Updated status, limitations, pilot plan, checklist, release notes, and roadmap progress.

## Not Completed In PR AB

- No live CRM, ad-platform, or social-listening integrations were added.
- No raw customer lists, CRM contact data, raw social posts, or PII ingestion was added.
- Calibration does not retrain, self-improve, overwrite, or automatically adjust existing simulation output.
- Calibration records are local JSON aggregate records scoped by organization in the current storage architecture.
- Calibration status is directional and depends on user-supplied aggregate actuals and prior estimates.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests/test_calibration_service.py backend/tests/test_api_contract.py -q`: passed, 9 passed.
- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 79 passed and 49 warnings.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 13 passed.
- CI-equivalent secret hygiene scan: passed.
- `git diff --check`: passed.

## Remaining Blockers / Accepted Risks

- Manual credential rotation evidence is still required for any historical provider/API/graph credentials that may have been committed before secret hygiene remediation.
- Public deployments still need edge/API-gateway or shared-store rate limiting.
- Browser auth storage is mitigated but still needs HttpOnly cookie, refresh-token, or equivalent production hardening before public/customer deployment.
- External pilot data-retention and deletion procedures still need approval.
- Legacy local JSON records without `org_id` need review, backfill, or re-creation before production use.
- Deep industry presets, budget plans, and calibration comparisons must be treated as directional evidence until enough approved real campaign outcomes are imported and reviewed.

## Next Recommended Roadmap Item

After PR AB is reviewed and merged, proceed to the next incomplete item in `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
