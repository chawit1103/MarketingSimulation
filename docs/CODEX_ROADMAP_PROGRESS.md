# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR Z: Deep Industry Presets**

## Why PR Z Was Selected

PR Y was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR Z: Deep Industry Presets.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-z-deep-industry-presets`.
- Release-candidate, strategy-pack, comparator, and revised-brief roadmap work is present.
- Industry templates existed for energy and finance, but priority brand/agency presets were still shallow or missing.
- The Campaigns template selector and campaign creation flow already supported applying template presets, so this PR could focus on richer backend templates plus a small detail-panel improvement.

## Completed In PR Z

- Added deep built-in industry presets for:
  - FMCG / CPG.
  - Insurance / InsurTech.
  - Retail / Ecommerce.
  - Real Estate.
  - EV / Automotive.
  - Healthcare / Wellness.
- Each deep preset includes:
  - target segment archetypes.
  - common objections.
  - crisis triggers.
  - typical KPIs.
  - channel behavior.
  - competitor archetypes.
  - legal/regulatory sensitivities.
  - proof-point requirements.
  - sample brief.
  - sample risk checklist.
  - sample action-plan hints.
  - assumptions.
  - limitations.
- Extended the industry preset API response so campaign setup can receive:
  - campaign duration.
  - budget range.
  - primary KPI.
  - competitor context.
  - brand constraints.
  - risk/legal notes.
  - deep preset metadata.
- Added optional validation for `deep_preset` schema when a template includes it.
- Updated the template detail UI to show common objections, proof requirements, assumptions, and limitations before applying a preset.
- Added backend tests for deep preset listing, validation, API prefill shape, incomplete deep schema rejection, and conservative healthcare/wellness language.
- Updated README, demo data, demo script, status, and release notes.

## Not Completed In PR Z

- No calibration loop was added.
- No live social listening, CRM import, marketplace import, or paid provider integration was added.
- No exact ROI, sales forecast, or guaranteed prediction language was added.
- Healthcare / Wellness remains conservative communication planning only and is not medical advice.
- Deep presets remain assumption-based starter scaffolds and must be reviewed with real brand, legal, compliance, and market context before pilot or client use.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests/test_industry_deep_presets.py -q`: passed, 5 passed.
- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 70 passed and 38 warnings.
- JSON validation for six new built-in template files: passed.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 11 passed.
- CI-equivalent secret hygiene scan: passed.
- `git diff --check`: passed.

## Remaining Blockers / Accepted Risks

- Manual credential rotation evidence is still required for any historical provider/API/graph credentials that may have been committed before secret hygiene remediation.
- Public deployments still need edge/API-gateway or shared-store rate limiting.
- Browser auth storage is mitigated but still needs HttpOnly cookie, refresh-token, or equivalent production hardening before public/customer deployment.
- External pilot data-retention and deletion procedures still need approval.
- Legacy local JSON records without `org_id` need review, backfill, or re-creation before production use.
- Deep industry presets must be treated as assumptions until calibrated with real campaign data and client-approved market inputs.

## Next Recommended Roadmap Item

After PR Z is reviewed and merged, proceed to **PR AA: Budget Scenario Planner, not ROI Predictor**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
