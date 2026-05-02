# 5-Minute Demo Script

Updated: 2026-05-01

Use this script for a concise product walkthrough. Keep the message grounded: the demo is deterministic scenario planning, not guaranteed prediction. Say the source mode out loud whenever a result appears: Demo Mode, Local Estimate, Live Backend, or Backend Verified.

## 0:00-0:30 — Position The Product

Open the landing page.

Key message:

> 3C Simulator helps marketing, PR, and strategy teams test campaign, competitor, and crisis assumptions before spending real budget.

Show:

- Product category: decision intelligence.
- Primary promise: simulate public opinion, de-risk decisions, win markets.
- First action: Try Sample Campaign.

Screenshot: `docs/screenshots/home-landing.png`

## 0:30-1:30 — Demo Dashboard

Open `/dashboard/demo-premium-water`.

Key message:

> The first value moment is no-key demo mode. Users can see KPI, evidence, confidence, and action guidance without configuring an LLM.

Show:

- Demo Mode label.
- Campaign brief and persona count.
- Confidence & Evidence panel.
- KPI cards and next validation step.

Do not say the numbers are real market predictions. Say they are safe synthetic demo outputs used to show the workflow.

Screenshot: `docs/screenshots/demo-dashboard-overview.png`

## 1:30-2:10 — Brief Quality Score

Open Campaigns, create a new campaign, skip template if needed, and scroll to Brief Quality Score.

Key message:

> The system checks whether the brief is complete enough before simulation time or model spend is used.

Show:

- Score percentage.
- Confidence impact.
- Missing fields or strong-brief signal.
- Deterministic, non-LLM scoring.

Screenshot: `docs/screenshots/brief-quality-score.png`

## 2:10-3:00 — Simulation Evidence And Action Plan

Return to the demo dashboard and scroll through evidence and Action Plan.

Key message:

> The dashboard is designed to answer “what should we do next?” rather than only showing charts.

Show:

- Source label.
- Assumptions and limitations.
- Decision evidence.
- Structured Action Plan sections:
  - Creative Adjustment
  - Channel Allocation
  - Crisis Prevention
  - Validation Plan

Point out that the Action Plan inherits the same source label as the dashboard result.

Mention that the same evidence can be packaged as either a Brand Executive Summary or Agency Client Pitch Summary strategy pack, and that every exported section keeps the same source/provenance label.

Screenshots:

- `docs/screenshots/simulation-dashboard-kpis.png`
- `docs/screenshots/action-plan.png`

## 3:00-4:10 — War Room

Open `/war-room`.

Key message:

> War Room lets the team pressure-test competitor and crisis scenarios. Backend output is labeled Live Backend; local fallback must be explicitly chosen and labeled Local Estimate.

Show:

- Scenario templates.
- Response strategy.
- Live Backend badge.
- Expected sentiment movement.
- Affected segments and amplification channels.
- First response playbook.

Screenshot: `docs/screenshots/war-room.png`

## 4:10-5:00 — Settings Wizard And Close

Open `/settings`.

Key message:

> Teams can start in Demo only mode, move to local models for private development, then configure cloud APIs when ready. Readiness checks do not expose secrets.

Show:

- Demo only / Local model / Cloud API modes.
- LLM, embedding, Neo4j, and sample run steps.
- Directional cost estimate disclaimer.
- System Health below the wizard.

Screenshot: `docs/screenshots/settings-wizard.png`

Close with:

> The current release is ready for local demos with synthetic data. Controlled private pilots are conditional on credential rotation evidence and deployment controls. Public pilot and production customer deployment remain blocked until the release checklist is green.

Optional handoff:

- Share [DEMO_DATA.md](DEMO_DATA.md) if the audience wants safe briefs to try.
- Share [FAQ.md](FAQ.md) for trust, privacy, and accuracy questions.
- Share [PILOT_PLAN.md](PILOT_PLAN.md) when a team wants to test with real internal stakeholders.
