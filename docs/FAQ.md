# FAQ

Updated: 2026-05-01

## What is 3C Simulator?

3C Simulator is a decision-intelligence workflow for testing campaign, competitor, and crisis assumptions before spending real budget. It helps teams compare likely reactions, risk drivers, and recommended next actions using synthetic personas and deterministic decision layers.

## Does it predict real market outcomes?

No. It supports scenario planning and decision review. Outputs should be treated as directional guidance until calibrated against real campaign results, market research, or live pilot data.

## What do the source labels mean?

- **Demo Mode**: safe synthetic sample data for onboarding.
- **Local Estimate**: browser-side deterministic fallback, not a backend simulation.
- **Live Backend**: backend-generated deterministic output.
- **Backend Verified**: persisted real simulation KPI/evidence for an owned campaign/run. Backend route success alone is not enough.
- **Unknown Source**: source metadata was unavailable; treat the output cautiously.

## Can I demo it without API keys?

Yes. Use the sample campaign at `/dashboard/demo-premium-water`. Demo Mode is designed to show product value without LLM keys, Neo4j cloud credentials, or paid services.

## What data should I avoid entering during demos?

Do not enter real customer names, private customer data, regulated personal data, secrets, API keys, unreleased financials, or confidential campaign details unless your organization has explicitly approved that pilot setup.

## What makes a good campaign brief?

A useful brief includes objective, target audience, market or region, duration, budget range, primary KPI, channel mix, competitor context, brand constraints, and risk/legal notes. The Brief Quality Score checks these fields deterministically before simulation.

## Why does the dashboard show assumptions and limitations?

Business users need to know where the result came from and what could make it wrong. Confidence & Evidence is meant to make the simulation reviewable, not to imply certainty.

## What should I say if someone asks whether the KPI numbers are accurate?

Say: "These numbers are scenario-planning outputs based on synthetic inputs and deterministic rules. They are useful for comparing options and identifying risks, but they should be validated with real campaign data before major decisions."

## How should teams use the Action Plan?

Use it as a structured discussion guide. Each action item includes recommendation, reason, expected impact, and risk across creative adjustment, channel allocation, crisis prevention, and validation planning.

## What is War Room for?

War Room helps pressure-test competitor or crisis scenarios such as a price war, influencer backlash, regulatory issue, product recall, rumor amplification, ESG controversy, or competitor launch. Local fallback output must be explicitly selected and labeled Local Estimate.

## Is this ready for production?

It is ready for controlled demos and pilot discovery. Production rollout still needs deployment hardening, observability, data governance, calibration with real outcomes, and organization-specific privacy review.

## Can screenshots be shared publicly?

Only share screenshots using synthetic/demo data with visible source labels. Do not include customer data, API keys, auth tokens, internal URLs, or private business material.
