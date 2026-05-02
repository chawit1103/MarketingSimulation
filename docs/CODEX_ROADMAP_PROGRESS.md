# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR AA: Budget Scenario Planner, not ROI Predictor**

## Why PR AA Was Selected

PR Z was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR AA: Budget Scenario Planner, not ROI Predictor.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-aa-budget-scenario-planner`.
- Release-candidate, strategy-pack, comparator, revised-brief, and deep-preset roadmap work is present.
- Decision and impact APIs existed, but there was no dedicated budget/channel allocation what-if planner with explicit safe wording and provenance.

## Completed In PR AA

- Added deterministic backend Budget Scenario Planner service.
- Added `POST /api/decision/budget-scenario`.
- Planner inputs include:
  - total budget.
  - campaign duration.
  - target segments.
  - channel mix.
  - risk tolerance.
  - objective: awareness, conversion, retention, or crisis recovery.
- Planner outputs include:
  - suggested allocation range by channel.
  - suggested allocation range by segment.
  - trade-offs.
  - confidence level and confidence score.
  - assumptions.
  - limitations.
  - recommended validation step.
  - source/provenance metadata.
- Added `/budget-planner` frontend view.
- Added Budget Planner entry point from Campaigns.
- Added e2e smoke coverage for Budget Planner source labels and safe wording.
- Updated README, demo script, user journey, status, checklist, and release notes.

## Not Completed In PR AA

- No live ad-platform integration was added.
- No real media-cost database was added.
- No billing, CRM import, social listening, or calibration loop was added.
- No precise ROI/ROAS, CAC, sales forecast, market-share forecast, or budget-optimization certainty is claimed.
- Planner outputs remain deterministic scenario estimates and must be validated with real benchmarks or pilot results before major spend.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests/test_budget_scenario_planner.py backend/tests/test_api_contract.py -q`: passed, 6 passed.
- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 73 passed and 38 warnings.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1 --grep "budget planner"`: passed, 1 passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 12 passed.
- CI-equivalent secret hygiene scan: passed.
- `git diff --check`: passed.

## Remaining Blockers / Accepted Risks

- Manual credential rotation evidence is still required for any historical provider/API/graph credentials that may have been committed before secret hygiene remediation.
- Public deployments still need edge/API-gateway or shared-store rate limiting.
- Browser auth storage is mitigated but still needs HttpOnly cookie, refresh-token, or equivalent production hardening before public/customer deployment.
- External pilot data-retention and deletion procedures still need approval.
- Legacy local JSON records without `org_id` need review, backfill, or re-creation before production use.
- Deep industry presets and budget plans must be treated as assumptions until calibrated with real campaign data, media benchmarks, and client-approved market inputs.

## Next Recommended Roadmap Item

After PR AA is reviewed and merged, proceed to **PR AB: Manual Data Import + Calibration v1**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
