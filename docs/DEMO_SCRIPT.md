# 5-Minute Demo Script

Updated: 2026-05-02

Use one of these concise tracks depending on the audience. Keep the message grounded: the demo is deterministic scenario planning, not guaranteed prediction. Say the source mode out loud whenever a result appears: Demo Mode, Local Estimate, Live Backend, or Backend Verified.

## Track A: Brand Safety / C-Level Decision Demo

Use this track for marketing managers, brand owners, PR leaders, and executives who need to decide whether to launch, revise, or hold a campaign.

### 0:00-0:30 — Position The Product

Open the landing page.

Key message:

> 3C Simulator helps brand and leadership teams test campaign, competitor, and crisis assumptions before spending real budget.

Show:

- Product category: decision intelligence.
- Primary promise: simulate public opinion, de-risk decisions, win markets.
- First action: Try Sample Campaign.

Screenshot: `docs/screenshots/home-landing.png`

## 0:30-1:20 — Demo Dashboard

Open `/dashboard/demo-premium-water`.

Key message:

> The first value moment is no-key demo mode. Users can see KPI, evidence, confidence, and action guidance without configuring an LLM.

Show:

- Demo Mode label.
- Campaign brief and persona count.
- Confidence & Evidence panel.
- KPI cards and next validation step.

Do not say the numbers are real market predictions. Say they are safe synthetic demo outputs used to show the workflow.

Screenshot kept: `docs/screenshots/demo-dashboard-overview.png`

## 1:20-2:00 — Deep Industry Preset And Brief Quality Score

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

Screenshot kept: `docs/screenshots/brief-quality-score.png`

## 2:00-3:00 — Simulation Evidence, Action Plan, And Revised Brief

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

Screenshots kept:

- `docs/screenshots/simulation-dashboard-kpis.png`
- `docs/screenshots/action-plan.png`

## 3:00-3:35 — Budget Scenario Planner

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

## 3:35-4:10 — Calibration v1

Open `/calibration`.

Key message:

> Calibration v1 lets trusted users import approved aggregate actual results and compare them against prior estimates. It is not live CRM/social listening ingestion and does not retrain the model.

Show:

- Aggregate-only actual results fields.
- Estimate-vs-actual comparison.
- Calibration status.
- Privacy warning.
- No raw customer list, raw social post, API key, or PII input.

Use only synthetic or approved aggregate sample data.

## 4:10-4:40 — War Room

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

Screenshot kept: `docs/screenshots/war-room.png`

## 4:40-5:00 — Settings Wizard And Close

Open `/settings`.

Key message:

> Teams can start in Demo only mode, move to local models for private development, then configure cloud APIs when ready. Readiness checks do not expose secrets.

Show:

- Demo only / Local model / Cloud API modes.
- LLM, embedding, Neo4j, and sample run steps.
- Directional cost estimate disclaimer.
- System Health below the wizard.

Screenshot kept: `docs/screenshots/settings-wizard.png`

Close with:

> The current release is ready for local demos with synthetic data. Controlled private pilots are conditional on credential rotation evidence and deployment controls. Public pilot and production customer deployment remain blocked until the release checklist is green.

## Track B: Agency Pitch / A/B/C Campaign Comparison Demo

Use this track for agencies, strategists, account leads, and pitch teams who need to compare creative routes and justify a recommendation to a client.

### 0:00-0:30 — Position The Agency Value

Open the landing page.

Key message:

> 3C Simulator helps an agency compare campaign routes, identify client risk, and turn simulation evidence into a client-ready pitch pack before production or media spend.

Show:

- Product category: decision intelligence.
- First action: Try Sample Campaign.
- Source labels as part of trust discipline.

Screenshot kept: `docs/screenshots/home-landing.png`

### 0:30-1:15 — Demo Dashboard As Shared Evidence

Open `/dashboard/demo-premium-water`.

Key message:

> Start by aligning the room on evidence quality: this is Demo Mode synthetic data, useful for workflow demonstration and not a live market result.

Show:

- Demo Mode label.
- Confidence & Evidence.
- Risk drivers.
- Simulated quotes.
- Action Plan as the bridge to a recommendation.

Screenshot kept: `docs/screenshots/demo-dashboard-overview.png`

### 1:15-2:10 — A/B/C Comparator

Key message:

> Agencies and brand teams can compare multiple campaign directions before pitching or launching. Demo comparison uses backend fixtures and is labeled Demo Mode; browser fallback must be explicitly run as Local Estimate.

Show:

- Emotional/storytelling, proof-led/trust, and price/promotion variants.
- Ranked recommendation.
- Segment strengths and weaknesses.
- Trade-offs and recommended use case.
- Source label on the comparison result.

### 2:10-2:55 — War Room Competitive Pressure Test

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

Screenshot kept: `docs/screenshots/war-room.png`

### 2:55-3:35 — Strategy Pack And Action Plan

Return to the dashboard Action Plan.

Key message:

> The agency deliverable is not just a chart. It is a recommendation with creative adjustment, channel allocation, crisis prevention, and validation plan.

Show:

- Action Plan.
- Revised Brief v2.
- Strategy pack positioning: Agency Client Pitch Summary.
- Source/provenance label carried into exports.

Screenshot kept: `docs/screenshots/action-plan.png`

### 3:35-4:10 — Budget And Calibration As Client Follow-Up

Open `/budget-planner`, then mention `/calibration`.

Key message:

> Budget Planner gives directional allocation ranges for the client discussion. Calibration v1 gives a follow-up mechanism once approved aggregate actuals exist.

Say clearly:

- Budget Planner is not exact ROI/ROAS prediction.
- Calibration v1 does not ingest raw CRM or social posts.
- Calibration v1 does not automatically self-improve the model.

### 4:10-4:40 — Pilot Feedback Analytics

Open the feedback widget if appropriate.

Key message:

> During controlled pilots, the product team can learn where users find value or confusion without collecting raw briefs, PII, tokens, API keys, or customer records.

Show:

- Fixed-choice usefulness rating.
- Fixed-choice missing need.
- Source/confidence clarity question.
- No free-form feedback text.

### 4:40-5:00 — Close With Go/No-Go

Close with:

> The local demo is ready with synthetic data. Controlled private pilot is conditional for trusted teams. Public pilot and production customer deployment remain blocked until credential rotation evidence, production rate limiting, auth hardening, and data-retention approvals are complete.

Optional handoff:

- Share [DEMO_DATA.md](DEMO_DATA.md) if the audience wants safe briefs to try.
- Share [FAQ.md](FAQ.md) for trust, privacy, and accuracy questions.
- Share [PILOT_PLAN.md](PILOT_PLAN.md) when a team wants to test with real internal stakeholders.

## Screenshot Status For PR AD

PR AD changes documentation and demo framing only. No product UI was changed in this PR, so screenshots were kept rather than recaptured.

Kept:

- `docs/screenshots/home-landing.png`
- `docs/screenshots/demo-dashboard-overview.png`
- `docs/screenshots/brief-quality-score.png`
- `docs/screenshots/simulation-dashboard-kpis.png`
- `docs/screenshots/war-room.png`
- `docs/screenshots/action-plan.png`
- `docs/screenshots/settings-wizard.png`

Replaced: none.
