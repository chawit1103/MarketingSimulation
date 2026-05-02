# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR W: Client-Ready Strategy Pack**

## Why PR W Was Selected

PR V was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR W: Client-Ready Strategy Pack.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-w-client-ready-strategy-pack`.
- Release-candidate integration docs from PR V are present.
- Export architecture already supports authenticated PPTX/CSV routes under `/api/export`.
- No client-ready Brand/Agency strategy pack route existed before this PR.

Therefore PR W is the next correct focused PR.

## Completed In PR W

- Added a deterministic backend strategy-pack builder.
- Added `POST /api/export/strategy-pack` protected by analyst/admin export authorization.
- Added two pack modes:
  - Brand Executive Summary.
  - Agency Client Pitch Summary.
- Added white-label/report metadata placeholders for agency name, client name, prepared by, report date, campaign name, scenario name, and logo presence without echoing logo URLs.
- Added meeting-ready sections:
  - Executive decision summary.
  - Launch / revise / do-not-launch recommendation.
  - KPI summary.
  - Segment reactions.
  - Risk drivers.
  - Crisis watchouts.
  - Recommended action plan.
  - Next validation steps.
- Added section-level source/provenance metadata including source mode, data basis, run/campaign/simulation IDs when available, confidence level, assumptions, limitations, and next validation step.
- Added tests for strategy pack payload shape, mode behavior, logo URL safety, source labels, route contract, and viewer denial.
- Updated README and demo/user journey docs.

## Not Completed In PR W

- No frontend export UI was added; this PR adds the backend JSON strategy-pack contract only.
- No PPTX white-label template rendering was added.
- No exact ROI, sales forecast, or guaranteed prediction language was added.
- No database migration, billing, production auth rewrite, live social listening, CRM integration, calibration loop, or social account discovery was added.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests/test_strategy_pack.py backend/tests/test_api_contract.py backend/tests/test_rbac.py -q`: passed, 13 passed and 4 warnings.
- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 59 passed and 38 warnings.
- `cd frontend && npm run build`: passed.
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

After PR W is reviewed and merged, proceed to **PR X: Comparator Backend-First**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
