# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR Y: Revised Brief v2 From Action Plan**

## Why PR Y Was Selected

PR X was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR Y: Revised Brief v2 From Action Plan.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-y-revised-brief-v2`.
- Release-candidate integration docs from PR V are present.
- PR W strategy-pack export exists.
- PR X comparator backend-first work exists.
- Dashboard already had structured Action Plans, but no workflow to turn an Action Plan into a revised campaign brief.

Therefore PR Y is the next correct focused PR.

## Completed In PR Y

- Added deterministic backend Revised Brief v2 generation.
- Added `POST /api/brief/revise`.
- Revised Brief v2 output includes:
  - objective.
  - target segments.
  - key message.
  - tone and voice.
  - proof points.
  - channel recommendations.
  - risk guardrails.
  - validation plan.
  - creative team notes.
- Added provenance metadata:
  - source action plan ID.
  - campaign ID.
  - source mode.
  - data basis.
  - assumptions.
  - limitations.
  - recommended validation step.
- Added Dashboard UI entry point: Create Revised Brief.
- Added original brief vs revised brief review panel.
- Added backend tests, route contract coverage, and e2e smoke coverage.
- Updated README, demo script, user journey, status, checklist, and release notes.

## Not Completed In PR Y

- No live simulation calibration was added.
- No image prompt or Midjourney prompt generation was added.
- No LLM calls are required for revised brief tests.
- No guarantee of improved real-world outcomes was claimed.
- No save-as-new-campaign persistence was added; this PR provides reviewable v1 vs v2 output first.
- No social listening, CRM integration, or paid provider integration was added.
- No database migration was added.
- No exact ROI, sales forecast, or guaranteed prediction language was added.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests/test_revised_brief.py backend/tests/test_api_contract.py -q`: passed, 5 passed.
- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 65 passed and 40 warnings.
- `python3 -m json.tool src/locales/en.json` and `src/locales/th.json`: passed.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 11 passed.
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

After PR Y is reviewed and merged, proceed to **PR Z: Deep Industry Presets**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
