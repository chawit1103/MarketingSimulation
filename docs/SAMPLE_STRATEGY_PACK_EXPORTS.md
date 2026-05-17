# Sample Strategy Pack Exports

These sample export structures are for controlled paid pilot sales conversations using synthetic/demo data only. They are not production-readiness evidence, not public-pilot evidence, and not guaranteed prediction output.

Use these structures when showing what 3C Simulator can produce from the existing strategy-pack export flow. Do not add real customer data, real campaign briefs, PII, provider credentials, API keys, graph credentials, raw CRM records, internal logs, or live integration screenshots.

## Readiness Boundary

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

## Required Provenance Footer

Every sample strategy-pack slide should include a compact provenance footer:

```text
Source: <source mode> | Basis: <data basis> | Run ID: <run/demo ID if available> | Decision-support estimate, not a guaranteed prediction
```

Required footer fields:

- `source mode`: Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source.
- `data basis`: demo fixture, local estimate, backend generated, real simulation, manual input, or unknown.
- `run/demo ID`: include only safe generated IDs or demo fixture IDs.
- disclaimer: `Decision-support estimate, not a guaranteed prediction`.

Do not remove source/provenance labels from screenshots, decks, exports, or recordings.

## Brand Executive Summary Deck

Use this structure for a marketing manager, brand lead, innovation lead, or executive sponsor.

Recommended slide sequence:

1. Cover / white-label context
   - Synthetic campaign name.
   - Prepared-for context such as "Brand leadership review".
   - Demo Mode or Backend Verified source label.
   - No real customer, client, or market-confidential names.
2. Executive Decision Summary
   - Recommended decision path.
   - One-line reason.
   - Confidence level and recommended next validation step.
   - Explicit note that outputs are decision-support estimates.
3. Decision Gate & KPI Summary
   - Overall sentiment, conversion probability, brand perception shift, crisis risk, and social influence.
   - Directional interpretation only.
   - No exact ROI/ROAS prediction claims.
4. Segment Reactions
   - Synthetic segment-level reactions.
   - Segment support/resistance summary.
   - Example simulated quotes clearly framed as synthetic.
5. Risk Drivers & Crisis Watchouts
   - Main risk drivers.
   - Watchouts for legal, trust, misinformation, competitor, or cultural sensitivity.
   - Mitigation prompts for a human team.
6. Recommended Action Plan
   - Next actions by priority and timing.
   - Message revisions.
   - Validation plan before broader spend.
7. Limitations & Recommended Validation
   - Assumptions.
   - Data limitations.
   - Source/provenance summary.
   - Recommended controlled validation step.

## Agency Client Pitch Summary Deck

Use this structure for an agency strategist, account lead, or pitch team comparing multiple creative routes.

Recommended slide sequence:

1. Cover / white-label context
   - Agency/client placeholder labels only.
   - Synthetic scenario title.
   - Source/provenance footer.
2. Executive Decision Summary
   - Winning route or recommended route.
   - Why it is recommended.
   - Trade-offs and confidence.
3. Decision Gate & KPI Summary
   - A/B/C comparison table.
   - Sentiment, conversion, risk, brand lift, and segment fit.
   - "Directional estimate" wording.
4. Segment Reactions
   - Which audience each route wins or loses.
   - Synthetic persona reactions.
   - Client-safe message implications.
5. Risk Drivers & Crisis Watchouts
   - Route-specific risks.
   - Competitor or category watchouts.
   - Brand-safety constraints.
6. Recommended Action Plan
   - Route to present.
   - Creative revisions.
   - Validation sprint before media spend.
7. Limitations & Recommended Validation
   - Not market research replacement.
   - No live social listening or CRM integration in the first pilot.
   - Suggested client validation method.

## Generating Sample PPTX Exports

Use only synthetic/demo data for sample PPTX exports.

Safe options:

- Demo dashboard fixtures such as Premium Water Launch, InsurTech Trust Recovery, or Community Energy Narrative.
- Synthetic sample briefs from `docs/SAMPLE_DEMO_BRIEFS.md`.
- Strategy-pack payloads generated from local/demo workflows with visible source metadata.

Do not use:

- real customer briefs,
- customer campaign names,
- PII,
- raw CRM records,
- uploaded customer files,
- internal logs,
- provider tokens,
- API keys,
- graph credentials,
- live social listening exports.

Suggested local flow:

1. Start from a synthetic demo scenario.
2. Confirm Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source labels are visible in the UI.
3. Generate the strategy-pack payload or PPTX.
4. Open the deck and verify every slide has a provenance footer.
5. Verify the limitations slide is present.
6. Verify there are no production-readiness, public-pilot, guaranteed-prediction, or exact ROI/ROAS claims.
7. Run the artifact through `docs/DEMO_ARTIFACT_CHECKLIST.md` before sharing.

Do not commit binary PPTX files unless they are intentionally small, synthetic-only, clearly labeled, and reviewed with the demo artifact checklist.
