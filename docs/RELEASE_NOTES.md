# Release Notes

Updated: 2026-05-02

## PR AH: Final Branch Consolidation And Readiness Wording Fix

This pass consolidates the latest completed branch stack into a new release-candidate branch intended to become the default source of truth. It adds no product features and does not claim production readiness.

### Readiness Decision

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

### Wording Fixes

- Manual credential rotation remains a required owner action and is not marked complete.
- SEC-009 now says public internet exposure requires edge/API-gateway or shared-store rate limiting before deployment.
- SEC-012 now says production customer deployment requires HttpOnly cookies, refresh-token auth, or an equivalent hardened browser-auth strategy before release.

### Validation

- Backend tests passed.
- Focused security tests passed.
- Frontend production build passed.
- Mocked Playwright e2e smoke tests passed.
- Analytics tests passed.
- Secret hygiene scan and `git diff --check` passed.

## PR AF: Complete Demo Dashboard Fixtures

This pass completes the currently visible no-key demo dashboard set and removes the misleading fallback that could show the premium-water dashboard for unrelated demo IDs.

### What Changed

- Added industry-specific dashboard fixtures for InsurTech trust recovery and community energy.
- Kept the premium-water dashboard as the FMCG demo fixture.
- Filtered the public demo campaign list to campaigns with matching dashboard fixtures.
- Unknown demo dashboard IDs now return a safe 404 instead of unrelated sample output.
- Demo fixtures are labeled `demo_mode` and include assumptions, limitations, segment breakdowns, risk drivers, simulated quotes, action plans, and recommended validation steps.

### Validation

- Focused demo route tests passed.
- Full backend tests passed.
- Frontend production build passed.
- Mocked Playwright e2e smoke tests passed.
- Analytics tests passed.
- Secret hygiene scan and `git diff --check` passed.

## PR AG: Strategy Pack PPTX Renderer

This pass converts the existing strategy pack payload into a native PowerPoint export path without adding new prediction, ROI, or production-readiness claims.

### What Changed

- Added `POST /api/export/strategy-pack/pptx`.
- Rendered Brand Executive Summary and Agency Client Pitch Summary decks from the existing strategy pack payload.
- Added optional white-label context for agency name, client name, prepared by, report date, campaign name, scenario name, and a safe logo placeholder.
- Added source/provenance footer metadata to every strategy pack slide.
- Added a limitations and recommended validation slide.

### Validation

- Strategy pack renderer tests cover deck structure, report modes, safe logo handling, and source metadata on every slide.

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
| Local demo | Ready | Demo mode works without real provider keys when synthetic data is used. |
| Controlled private pilot | Conditional candidate | Acceptable only for trusted users after manual credential-rotation evidence is provided, deployment secrets come from environment variables, and pilot data is non-confidential or explicitly approved. |
| Public pilot | Blocked | Manual credential rotation is not evidenced, production rate limiting still requires edge/shared enforcement, and browser auth storage is mitigated but not fully hardened. |
| Public internet exposure | Blocked | Manual credential rotation is not evidenced, production rate limiting still requires edge/shared enforcement, and browser auth storage is mitigated but not fully hardened. |
| Production customer deployment | Blocked | Requires manual credential rotation, shared/edge rate limiting, hardened browser auth, formal data-retention/deletion policy, production storage decisions, and deployment operations controls. |

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

- Local demo: ready with synthetic data and no real secrets.
- Controlled private pilot: conditional candidate only after credential rotation evidence, environment-provided secrets, trusted users, and deployment controls.
- Public pilot: blocked.
- Public internet exposure: blocked.
- Production customer deployment: blocked.

## Post-PR U Product-Trust Fix: Synthetic Influence Nodes

The dashboard influence section now uses simulated influence-node wording and explicitly states that demo/local estimate modes use synthetic nodes, not scraped or verified real social profiles.

This improves product trust without adding live social listening, real account discovery, or production-readiness claims.

## PR V: Release Candidate Integration

This integration pass selects PR V as the next roadmap item because the latest work remains open as a stacked PR chain rather than being merged into the default branch.

### Integration Decisions

- Use the latest completed branch stack as the release-candidate source of truth.
- Keep public pilot, public internet exposure, and production customer deployment as blocked.
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

## PR X: Campaign A/B/C Comparator Backend-First

This pass makes the Comparator backend-first for demo and authenticated campaign comparisons. It does not claim real-world A/B test accuracy or calibrated campaign lift.

### What Changed

- Added backend demo comparator variants for emotional/storytelling, proof-led/trust, and price/promotion campaign directions.
- Added public demo comparator routes for no-key onboarding.
- Comparator results now include ranked recommendation, segment strengths/weaknesses, conversion and engagement estimates, risk comparison, trade-offs, recommended use cases, and source/provenance metadata.
- Frontend Comparator uses backend demo fixtures first and no longer silently falls back to browser-generated results.
- Browser-side comparator output is available only through an explicit Local Estimate action after backend comparison fails.

### Validation

- Focused backend comparator/API contract tests passed: `backend/.venv/bin/python -m pytest backend/tests/test_comparator_api.py backend/tests/test_api_contract.py -q`.
- Full backend tests passed: `backend/.venv/bin/python -m pytest backend/tests -q`.
- Frontend build passed: `cd frontend && npm run build`.
- E2E smoke tests passed: `cd frontend && npm run test:e2e -- --project=chromium --workers=1`.
- Secret hygiene scan and `git diff --check` passed.

## PR Y: Revised Brief v2 From Action Plan

This pass turns structured Action Plans into a reviewable revised campaign brief. It does not generate image prompts, require live LLM calls, or claim the revised brief will guarantee better market outcomes.

### What Changed

- Added deterministic Revised Brief v2 generation at `POST /api/brief/revise`.
- Revised brief output includes objective, target segments, key message, tone and voice, proof points, channel recommendations, risk guardrails, validation plan, and creative team notes.
- Added provenance fields for source action plan ID, campaign ID, source mode, data basis, assumptions, limitations, and recommended validation step.
- Added Dashboard UI to create a Revised Brief from the Action Plan and review original brief vs revised brief.
- Added backend contract tests and e2e smoke coverage for the revised brief workflow.

### Validation

- Focused backend revised-brief/API contract tests passed: `backend/.venv/bin/python -m pytest backend/tests/test_revised_brief.py backend/tests/test_api_contract.py -q`.
- Full backend tests passed: `backend/.venv/bin/python -m pytest backend/tests -q`.
- Frontend build passed: `cd frontend && npm run build`.
- E2E smoke tests passed: `cd frontend && npm run test:e2e -- --project=chromium --workers=1`.
- Secret hygiene scan and `git diff --check` passed.

## PR Z: Deep Industry Presets

This pass adds richer planner-ready industry presets without adding live social listening, calibration, or regulated advice claims.

### What Changed

- Added deep built-in presets for FMCG/CPG, Insurance/InsurTech, Retail/Ecommerce, Real Estate, EV/Automotive, and Healthcare/Wellness.
- Each preset includes segment archetypes, objections, crisis triggers, typical KPIs, channel behavior, competitor archetypes, regulatory sensitivities, proof-point requirements, sample brief, risk checklist, action-plan hints, assumptions, and limitations.
- Campaign preset API now exposes deep preset metadata plus prefill fields for duration, budget, KPI, competitor context, brand constraints, and risk/legal notes.
- Industry template detail UI now shows assumptions, limitations, common objections, and proof requirements before applying a preset.

### Validation

- Focused backend deep-preset tests passed: `backend/.venv/bin/python -m pytest backend/tests/test_industry_deep_presets.py -q`.
- Full backend tests passed: `backend/.venv/bin/python -m pytest backend/tests -q`.
- Frontend build passed: `cd frontend && npm run build`.
- E2E smoke tests passed: `cd frontend && npm run test:e2e -- --project=chromium --workers=1`.
- CI-equivalent secret hygiene scan and `git diff --check` passed.

## PR AA: Budget Scenario Planner

This pass adds a deterministic budget/channel what-if planner for demo and controlled planning workflows. It does not add live ad-platform integrations, exact ROI/ROAS prediction, billing, or calibration.

### What Changed

- Added `POST /api/decision/budget-scenario`.
- Added a deterministic budget planner service that accepts total budget, duration, target segments, channel mix, risk tolerance, and objective.
- Planner output includes channel allocation ranges, segment ranges, trade-offs, confidence level, assumptions, limitations, recommended validation step, and source/provenance metadata.
- Added `/budget-planner` frontend view with Demo Mode/Live Backend source labels and visible no-auto-fallback error behavior.
- Added Campaigns navigation entry for Budget Planner.

### Validation

- Focused backend budget/API contract tests passed: `backend/.venv/bin/python -m pytest backend/tests/test_budget_scenario_planner.py backend/tests/test_api_contract.py -q`.
- Full backend tests passed: `backend/.venv/bin/python -m pytest backend/tests -q`.
- Frontend build passed: `cd frontend && npm run build`.
- Focused e2e smoke test passed: `cd frontend && npm run test:e2e -- --project=chromium --workers=1 --grep "budget planner"`.
- Full e2e smoke tests passed: `cd frontend && npm run test:e2e -- --project=chromium --workers=1`.
- CI-equivalent secret hygiene scan and `git diff --check` passed.

## PR AB: Manual Data Import + Calibration v1

This pass adds manual aggregate actual-results import and deterministic estimate-vs-actual calibration comparison. It does not add live CRM/social-listening integrations, raw customer data ingestion, or model self-learning.

### What Changed

- Added `POST /api/calibration/actual-results` for analyst/admin actual-results import.
- Added `GET /api/calibration/status/<campaign_id>` for authenticated calibration status reads.
- Added a backend Calibration Service that supports JSON payloads plus one-row aggregate CSV/JSON uploads.
- Calibration output includes estimate-vs-actual delta, absolute error percentage by metric, matched/missed risk classification, optional segment assumption gaps, privacy review, limitations, and next validation step.
- Added privacy safeguards that reject PII-like fields, raw CRM/contact data, raw social posts/comments, and PII-like qualitative notes.
- Added `/calibration` frontend view and Campaigns navigation entry.
- Added e2e smoke coverage for calibration manual-evidence labels and privacy wording.

### Validation

- Focused backend calibration/API contract tests passed: `backend/.venv/bin/python -m pytest backend/tests/test_calibration_service.py backend/tests/test_api_contract.py -q`.
- Full backend, frontend build, e2e, secret scan, and diff validation are recorded in `docs/RELEASE_READINESS_CHECKLIST.md`.

## PR AC: Pilot Feedback Analytics

This pass improves privacy-conscious product analytics for controlled pilots. It does not add a third-party analytics SDK, backend event ingestion, or free-form feedback collection.

### What Changed

- Expanded the analytics event allowlist for pilot journeys: demo dashboard, brief quality, simulation start/complete, dashboard view, action plan view, revised brief, comparator, budget scenario, export, War Room, settings provider failures, and feedback.
- Connected missing event instrumentation for Comparator and Budget Scenario Planner.
- Renamed settings failure tracking to `settings_provider_test_failed`.
- Improved the global feedback widget with fixed-choice usefulness, confusion, missing-need, and source/confidence clarity inputs.
- Added dependency-free analytics sanitization tests.
- Updated analytics docs and e2e feedback assertions.

### Validation

- Analytics sanitization tests passed: `cd frontend && npm run test:analytics`.
- Full frontend build/e2e, backend, secret scan, and diff validation are recorded in `docs/RELEASE_READINESS_CHECKLIST.md`.

## PR AD: Final Brand/Agency Go-No-Go + Demo Refresh

This pass closes the Brand & Agency Value Roadmap with documentation, demo framing, screenshot inventory, and readiness consistency. It does not add product features or change runtime behavior.

### What Changed

- Updated README positioning for two audiences:
  - Marketing Manager / Brand Team.
  - Marketing Agency / Strategy Team.
- Updated README product walkthrough to reference Brand and Agency demo tracks.
- Reworked `docs/DEMO_SCRIPT.md` into two 5-minute tracks:
  - Brand Safety / C-Level Decision Demo.
  - Agency Pitch / A/B/C Campaign Comparison Demo.
- Updated `docs/PILOT_PLAN.md` with Brand vs Agency participant questions, success criteria, feedback analytics usage, and PR AD go/no-go language.
- Updated `docs/SCREENSHOT_GUIDE.md` with PR AD screenshot inventory.
- Kept all curated screenshots and replaced none because PR AD changed docs/demo framing only.

### Validation

- Final validation is recorded in `docs/RELEASE_READINESS_CHECKLIST.md`.

## PR AE: Merge Stacked Roadmap Into Release Candidate

This pass creates a clean release-candidate integration branch from the latest stacked roadmap branch. It does not add product features.

### Integration Decisions

- Use `codex/pr-ad-brand-agency-go-no-go` as the source of truth for the completed PR V through PR AD stack.
- Keep `.env.dev` untracked.
- Keep `.env.dev.example` and `.env.example` as safe placeholder examples.
- Align readiness language across README, status, security, limitations, checklist, pilot plan, roadmap, and release notes.
- Keep local demo as ready with synthetic data and no real secrets.
- Keep controlled private pilot as a conditional candidate with trusted users, credential-rotation evidence, environment-provided secrets, visible source labels, and deployment controls.
- Keep public pilot, public internet exposure, and production customer deployment blocked.

### Wording Fixes

- Backend Verified means persisted real simulation KPI/evidence for an owned campaign/run; backend route success alone is not enough.
- Manual credential rotation is still a required owner action and is not marked complete.
- HttpOnly cookie / refresh-token auth remains future work and is not claimed as implemented.

### Validation

- Final validation is recorded in `docs/RELEASE_READINESS_CHECKLIST.md`.
