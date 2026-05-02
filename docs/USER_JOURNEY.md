# First-Time User Journey

Updated: 2026-05-01

This journey describes the recommended path for a new user evaluating 3C Simulator.

## 1. Understand The Product

Start at the landing page.

Goal:

- Understand that 3C Simulator is a campaign, competitor, and crisis decision-support product.
- Avoid framing it as a general AI playground.

Recommended action:

- Click **Try Sample Campaign**.

Screenshot:

- `docs/screenshots/home-landing.png`

## 2. Explore A No-Key Demo

Open the Premium Water demo dashboard.

Goal:

- See immediate value without API keys.
- Learn that demo output is clearly labeled Demo Mode.
- Review the campaign brief, persona count, confidence/evidence, KPIs, and validation guidance.

Recommended action:

- Read the Confidence & Evidence panel before interpreting KPI cards.
- Treat the result as synthetic demo data, not a live market result.

Screenshot:

- `docs/screenshots/demo-dashboard-overview.png`

## 3. Prepare A Real Brief

Go to Campaigns and create a new campaign.

Goal:

- Provide enough context before running a simulation.
- Make the campaign brief useful for business decision-making.

Recommended brief inputs:

- Objective
- Target audience
- Market/region
- Campaign duration
- Budget range
- Primary KPI
- Channel mix
- Competitor context
- Brand constraints
- Risk/legal notes

Use the Brief Quality Score before launching a simulation.

Screenshot:

- `docs/screenshots/brief-quality-score.png`

## 4. Review Simulation Evidence

Open the dashboard for a demo or completed campaign.

Goal:

- Read source mode and confidence context first.
- Understand assumptions and limitations.
- Review KPIs, segment reactions, and decision evidence.

Recommended action:

- Confirm whether the source is Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source.
- Do not treat Local Estimate as measured backend output.

Screenshot:

- `docs/screenshots/simulation-dashboard-kpis.png`

## 5. Decide What To Do Next

Scroll to the Action Plan.

Goal:

- Convert results into concrete next steps.
- Separate creative changes, channel allocation, crisis prevention, and validation.

Recommended action:

- Copy/export the Action Plan for team review.
- Use the strategy pack export when the next meeting needs a Brand Executive Summary or Agency Client Pitch Summary with source/provenance labels attached to every section.
- Validate high-risk recommendations with a small live-market or audience test before full spend.

Screenshot:

- `docs/screenshots/action-plan.png`

## 6. Stress-Test Competitors And Crisis Moves

Open War Room.

Goal:

- Test competitor moves and crisis scenarios.
- Understand which segments and channels amplify the issue.
- Review backend-labeled response recommendations.

Recommended action:

- Start with Price War, Influencer Backlash, Product Recall, Regulatory Issue, ESG Controversy, Fake News/Rumor, or Competitor Launch.
- If backend simulation fails, use Local Estimate only as an explicit fallback.

Screenshot:

- `docs/screenshots/war-room.png`

## 7. Configure The Runtime

Open Settings.

Goal:

- Choose the right setup mode.
- Check readiness without exposing secrets.

Recommended path:

- Use **Demo only** for onboarding.
- Use **Local model** for private development with local providers.
- Use **Cloud API** when provider keys and graph storage are ready.

Screenshot:

- `docs/screenshots/settings-wizard.png`

## Recommended First Pilot

For a first real pilot, choose one campaign with:

- a clear business objective,
- a known audience,
- one primary KPI,
- known competitor pressure,
- a specific launch window,
- a realistic budget range,
- one risk or legal concern,
- and a planned validation step after simulation.

Success criteria:

- The team can explain why the dashboard recommends a specific action.
- The team can identify the highest-risk segment.
- The team can name what evidence is missing before full launch.
- The team can export or copy an Action Plan for decision review.
