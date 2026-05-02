# 5-Minute Demo Script

Updated: 2026-05-02

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

## 1:30-2:10 — Deep Industry Preset And Brief Quality Score

Open Campaigns, create a new campaign, and choose a deep industry preset such as FMCG / CPG, Insurance / InsurTech, Retail / Ecommerce, Real Estate, EV / Automotive, or Healthcare / Wellness.

Key message:

> The template gets a planner from blank page to a realistic campaign shape in minutes, but its assumptions and limitations are visible and must be reviewed.

Show:

- Preset assumptions and limitations.
- Common objections and proof requirements.
- Prefilled duration, budget, KPI, competitor context, brand constraints, risk/legal notes, and channel mix.
- Score percentage.
- Confidence impact.
- Missing fields or strong-brief signal.
- Deterministic, non-LLM scoring.

For Healthcare / Wellness, say explicitly that the preset is conservative communication planning and not medical advice.

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

Click **Create Revised Brief**.

Show:

- Original brief vs Revised Brief v2.
- Key message, proof points, channel recommendations, risk guardrails, and validation plan.
- Provenance label and next validation step.

Screenshots:

- `docs/screenshots/simulation-dashboard-kpis.png`
- `docs/screenshots/action-plan.png`

## 3:00-3:30 — Budget Scenario Planner

Open `/budget-planner`.

Key message:

> Budget Planner is a channel mix what-if tool. It gives directional allocation ranges and trade-offs, not exact ROI or ROAS prediction.

Show:

- Demo Mode or Live Backend source label.
- Total budget, duration, target segments, channel mix, risk tolerance, and objective.
- Suggested allocation ranges by channel and segment.
- Confidence level.
- Assumptions, limitations, and recommended validation step.

Say clearly that no live ad-platform cost data is used unless the user provides approved planning inputs.

## 3:30-4:00 — A/B/C Comparator

Open `/comparator`.

Key message:

> Agencies and brand teams can compare multiple campaign directions before pitching or launching. Demo comparison uses backend fixtures and is labeled Demo Mode; browser fallback must be explicitly run as Local Estimate.

Show:

- Emotional/storytelling, proof-led/trust, and price/promotion variants.
- Ranked recommendation.
- Segment strengths and weaknesses.
- Trade-offs and recommended use case.
- Source label on the comparison result.

## 4:00-4:40 — War Room

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

## 4:40-5:00 — Settings Wizard And Close

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
