# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR AD: Final Brand/Agency Go-No-Go + screenshots/docs refresh**

## Why PR AD Was Selected

PR AC was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR AD: Final Brand/Agency Go-No-Go + screenshots/docs refresh.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-ad-brand-agency-go-no-go`.
- Release-candidate, strategy-pack, comparator, revised-brief, and deep-preset roadmap work is present.
- Budget Scenario Planner and Manual Calibration v1 are present.
- Roadmap work PR W through PR AC is present.
- Product docs needed a final Brand vs Agency demo framing pass, screenshot inventory review, and go/no-go readiness consistency check.

## Completed In PR AD

- Reviewed roadmap features added from PR W through PR AC:
  - client-ready strategy packs.
  - backend-first comparator.
  - Revised Brief v2.
  - deep industry presets.
  - Budget Scenario Planner.
  - Manual Calibration v1.
  - Pilot Feedback Analytics.
- Updated README positioning for two user groups:
  - Marketing Manager / Brand Team.
  - Marketing Agency / Strategy Team.
- Updated README walkthrough to reference the two demo tracks and PR AD screenshot review.
- Updated `docs/DEMO_SCRIPT.md` with two 5-minute tracks:
  - Brand Safety / C-Level Decision Demo.
  - Agency Pitch / A/B/C Campaign Comparison Demo.
- Updated `docs/PILOT_PLAN.md` for Brand vs Agency pilot questions, success criteria, feedback analytics, and current PR AD go/no-go wording.
- Updated `docs/SCREENSHOT_GUIDE.md` with PR AD screenshot inventory.
- Kept all existing curated screenshots and replaced none because PR AD changed docs/demo framing only, not product UI.
- Updated checklist, release notes, and roadmap progress.

## Not Completed In PR AD

- No product features, code behavior changes, database migration, billing, providers, or screenshots were added.
- No screenshots were fabricated or recaptured.
- Public pilot, public internet exposure, and production customer deployment were not marked ready.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.
- Remaining production blockers were kept visible.

## Tests And Checks

- `backend/.venv/bin/python -m pytest backend/tests -q`: passed, 79 passed and 49 warnings.
- `cd frontend && npm run build`: passed.
- `cd frontend && npm run test:e2e -- --project=chromium --workers=1`: passed, 13 passed.
- `cd frontend && npm run test:analytics`: passed, 2 passed.
- CI-equivalent secret hygiene scan: passed.
- `git diff --check`: passed.

## Remaining Blockers / Accepted Risks

- Manual credential rotation evidence is still required for any historical provider/API/graph credentials that may have been committed before secret hygiene remediation.
- Public deployments still need edge/API-gateway or shared-store rate limiting.
- Browser auth storage is mitigated but still needs HttpOnly cookie, refresh-token, or equivalent production hardening before public/customer deployment.
- External pilot data-retention and deletion procedures still need approval.
- Legacy local JSON records without `org_id` need review, backfill, or re-creation before production use.
- Pilot analytics are local/provider-neutral by default. Any third-party analytics destination still needs privacy, retention, opt-out, and data-owner review.
- Deep industry presets, budget plans, and calibration comparisons must be treated as directional evidence until enough approved real campaign outcomes are imported and reviewed.

## Next Recommended Roadmap Item

PR AD completes the current Brand & Agency Value Roadmap sequence. Next work should be selected from product/security follow-up docs, not from this roadmap, unless a new roadmap is provided.

Suggested prompt for the next run:

```text
Select the next focused follow-up from docs/POST_IMPLEMENTATION_ACTION_PLAN.md, docs/SECURITY_REVIEW.md, or docs/KNOWN_LIMITATIONS.md.

Implement only one focused PR.
Do not claim public/production readiness unless the release checklist supports it.
```
