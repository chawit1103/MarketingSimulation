# Pilot Plan

Updated: 2026-05-02

This plan is for controlled testing with 3-5 real users or internal stakeholders. The goal is to validate workflow value, trust, and decision usefulness before broad release. It is not a calibration study by itself, although approved aggregate campaign actuals can now be imported separately for Calibration v1.

## Pilot Objectives

- Confirm that first-time users understand the product category and recommended flow.
- Measure whether users can create or evaluate a campaign brief without help.
- Validate that Demo Mode, Local Estimate, Live Backend, and Backend Verified labels are understood.
- Learn whether Confidence & Evidence and Action Plan sections help users make a next-step decision.
- Identify which outputs users would take to a manager, client, or leadership meeting.
- Compare value perception between Brand/C-level decision users and Agency/client-pitch users.

## Participant Profile

Recruit 3-5 participants across:

- marketing managers,
- PR/crisis communication teams,
- agency strategists,
- brand managers,
- product marketers,
- strategy or insights teams.

Prefer participants who can bring one approved or non-confidential campaign scenario. Internal stakeholders can use the sample briefs in [DEMO_DATA.md](DEMO_DATA.md). Do not ask users to enter confidential customer data, regulated personal data, API keys, or real sensitive business material during early pilots.

## Pilot Setup

Before the session:

1. Confirm the participant understands that outputs are scenario-planning guidance, not guaranteed predictions.
2. Use demo data or an approved campaign brief.
3. Verify the local or hosted demo environment is working.
4. Confirm screenshots, recordings, and notes will not expose secrets or customer data.
5. Prepare the 5-minute demo script from [DEMO_SCRIPT.md](DEMO_SCRIPT.md).
6. Prepare the FAQ from [FAQ.md](FAQ.md) for trust, privacy, and accuracy questions.

Recommended starting routes:

- `/`
- `/dashboard/demo-premium-water`
- `/campaigns`
- `/war-room`
- `/calibration`
- `/settings`

## Session Structure

### 0-5 minutes: Guided Demo

Choose one track from [DEMO_SCRIPT.md](DEMO_SCRIPT.md):

- Brand Safety / C-Level Decision Demo.
- Agency Pitch / A/B/C Campaign Comparison Demo.

For both tracks, show:

- Landing page positioning.
- Demo dashboard with Demo Mode label.
- Confidence & Evidence panel.
- Brief Quality Score.
- War Room with source label.
- Action Plan.
- Settings Wizard.
- Calibration v1 with aggregate actuals only, if using approved sample data.
- Fixed-choice feedback widget if the participant is comfortable giving pilot feedback.

### 5-20 minutes: User Task

Ask the participant to complete one scenario:

1. Choose or describe a campaign.
2. Check brief quality.
3. Review dashboard evidence.
4. Identify the top risk segment.
5. Choose one recommended action.
6. Explain what they would validate before launch.
7. Optional: enter approved aggregate actual results in Calibration v1 and compare estimate-vs-actual deltas.

### 20-30 minutes: Feedback Interview

Ask:

- What did you think the product was for?
- Which result did you trust most? Why?
- Were source labels clear?
- Did any output feel like it claimed too much certainty?
- What would you show your boss or client?
- What was missing before you would use this for a real decision?
- Which step was confusing or slow?

Brand/C-level specific questions:

- Would this help you decide launch, revise, hold, or validate further?
- Which section would you show leadership?
- What evidence is still missing before real budget approval?

Agency specific questions:

- Would this help you compare creative routes for a client?
- Which output would belong in a pitch deck?
- What would a client challenge or ask you to prove?

## Data To Capture

Use a structured notes sheet with:

- participant role,
- scenario type,
- source mode shown,
- brief quality score,
- confidence/evidence interpretation,
- action plan accepted/rejected,
- top confusion point,
- top trust point,
- requested feature,
- eventual campaign outcome if later available and approved.
- pilot analytics event counts if collected locally and sanitized.

Do not capture:

- API keys,
- passwords,
- auth tokens,
- private customer data,
- regulated personal data,
- confidential campaign budgets unless explicitly approved for research.

Calibration v1 import rules:

- Accept aggregate campaign summaries only.
- Do not import customer lists, CRM records, raw social posts, raw comments, names, phone numbers, emails, handles, tokens, or API keys.
- Use synthetic actuals or owner-approved aggregate campaign readouts for early pilots.
- Treat `partially_calibrated` as directional evidence, not proof of predictive accuracy.

## Success Criteria

Pilot is successful if:

- At least 4 of 5 participants, or 3 of 4 in a smaller pilot, can explain the product purpose after the landing page and demo dashboard.
- At least 4 of 5 participants, or 3 of 4, can distinguish Demo Mode or Local Estimate from live/backend-verified output.
- At least 3 participants can identify one recommended action and one validation step.
- At least 3 participants say the Action Plan or Confidence & Evidence panel would help in a real campaign discussion.
- No participant mistakes local fallback output for measured live simulation output.
- If Calibration v1 is tested, participants understand that imported actuals are manual aggregate evidence and do not automatically retrain the simulation engine.
- If the Agency track is tested, at least 3 participants can identify a winning route, a trade-off, and a client validation step.
- If the Brand/C-level track is tested, at least 3 participants can explain launch/revise/hold decision logic from the dashboard evidence.

## Exit Criteria Before Public Demo

Before broader release:

- Resolve any issue where source labels are missed or misunderstood.
- Remove or relabel any output that appears overconfident.
- Add missing docs or UI guidance for the top three confusion points.
- Confirm production environment has no default secrets.
- Confirm data-retention and deletion expectations are documented for external users.

## Go/No-Go Gate

Current PR AD verification decision:

| Pilot path | Status | Gate |
| --- | --- | --- |
| Local demo | Go | Use synthetic demo data and no real provider secrets. |
| Controlled private pilot | Conditional go | Limit to trusted users. Confirm credential rotation, environment-provided secrets, no confidential briefs unless explicitly approved, and deployment-owned logging/rate-limit controls. |
| Public pilot | No-go | Blocked until manual credential rotation is evidenced, edge/shared rate limiting is deployed, browser auth storage is hardened or formally risk-accepted, and external data-retention/deletion expectations are approved. |

Do not invite untrusted public users or publish a public demo URL until the public-pilot gate is green.

## Screenshot Review Before Public Use

PR T did not change visible UI/security labels, so screenshots do not need recapture solely because of this verification pass. Before any public demo, re-review or recapture:

- `docs/screenshots/demo-dashboard-overview.png`
- `docs/screenshots/simulation-dashboard-kpis.png`
- `docs/screenshots/war-room.png`
- `docs/screenshots/action-plan.png`
- `docs/screenshots/settings-wizard.png`

Confirm every result screenshot shows the correct source label and that settings screenshots do not show API keys, passwords, auth tokens, private URLs, or customer data.

PR AD review kept all current curated screenshots and replaced none because PR AD changed documentation/demo framing only, not product UI. This does not remove the public-demo requirement to re-check screenshots immediately before sharing.

## Follow-Up

After each pilot:

1. Summarize findings within 48 hours.
2. Add product issues for repeated confusion points.
3. Update docs if users misunderstood product scope or output limitations.
4. Keep calibration evidence separate from anecdotal usability feedback.
5. Store Calibration v1 evidence only when approved by the data owner and delete it on request.
6. Do not publish case studies until assumptions and data permissions are validated.
