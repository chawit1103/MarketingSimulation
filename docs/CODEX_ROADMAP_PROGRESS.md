# Codex Roadmap Progress

Updated: 2026-05-02

Roadmap source: `CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md`  
Controller source: `CODEX_SEQUENTIAL_ORCHESTRATOR_PROMPT.md`

## Current Stage

Selected roadmap item: **PR AC: Pilot Feedback Analytics**

## Why PR AC Was Selected

PR AB was completed on the current stacked roadmap branch. The next incomplete roadmap item in order is PR AC: Pilot Feedback Analytics.

Current repository inspection found:

- GitHub default branch: `multilang-v0.3`.
- Current branch: `codex/pr-ac-pilot-feedback-analytics`.
- Release-candidate, strategy-pack, comparator, revised-brief, and deep-preset roadmap work is present.
- Budget Scenario Planner and Manual Calibration v1 are present.
- A lightweight analytics/feedback foundation existed, but the allowlist and feedback payload did not yet cover the full PR AC pilot-learning scope.

## Completed In PR AC

- Expanded the provider-neutral frontend analytics allowlist to include PR AC pilot journey events:
  - `demo_dashboard_opened`
  - `brief_quality_scored`
  - `simulation_started`
  - `simulation_completed`
  - `dashboard_viewed`
  - `action_plan_viewed`
  - `revised_brief_created`
  - `comparator_used`
  - `budget_scenario_run`
  - `export_clicked`
  - `war_room_scenario_run`
  - `settings_provider_test_failed`
  - `feedback_submitted`
- Connected missing event instrumentation for Comparator and Budget Scenario Planner.
- Renamed settings provider failure tracking to the explicit `settings_provider_test_failed` event.
- Improved the global feedback widget with fixed-choice pilot questions:
  - usefulness rating.
  - confusion area.
  - missing need.
  - source/confidence clarity.
- Preserved the no-free-text feedback approach to avoid collecting raw briefs, PII, secrets, tokens, or customer data.
- Added dependency-free Node analytics sanitization tests.
- Updated e2e smoke feedback assertions and analytics docs.

## Not Completed In PR AC

- No third-party analytics SDK or network destination was added.
- Analytics remains browser-local `CustomEvent` emission unless a future provider integration is explicitly reviewed and documented.
- No free-form feedback text, raw campaign brief, PII, tokens, API keys, secrets, or customer records are collected.
- No backend event ingestion, dashboard, or product analytics database was added.
- Manual credential rotation was not marked complete because it requires repository-owner action outside Codex.

## Tests And Checks

- `cd frontend && npm run test:analytics`: passed, 2 passed.
- `python3 -m json.tool frontend/src/locales/en.json` and `frontend/src/locales/th.json`: passed.
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
- Pilot analytics are local/provider-neutral by default. Any third-party analytics destination still needs privacy, retention, opt-out, and data-owner review.
- Deep industry presets, budget plans, and calibration comparisons must be treated as directional evidence until enough approved real campaign outcomes are imported and reviewed.

## Next Recommended Roadmap Item

After PR AC is reviewed and merged, proceed to **PR AD: Final Brand/Agency Go-No-Go + screenshots/docs refresh**.

Short prompt for the next run:

```text
Continue the 3C Simulator Brand & Agency Value Roadmap.

Use CODEX_BRAND_AGENCY_VALUE_ROADMAP_PROMPTS.md and docs/CODEX_ROADMAP_PROGRESS.md as context.

Select the next incomplete roadmap item in order and implement only that one focused PR.

Do not implement later roadmap items.
Follow all security, provenance, readiness, and testing constraints from the roadmap and repo docs.
```
