# Customer Proof-of-Value Flow

Updated: 2026-05-17

This flow is for a customer-facing proof-of-value session using one customer-approved campaign brief or one approved historical campaign scenario. It is not a dry demo, not a public pilot, and not a production SaaS deployment.

The purpose is to help a prospect evaluate whether 3C Simulator can provide useful campaign decision support from their approved business context without requiring personal data, raw customer records, or live integrations.

## Data Boundary

Allowed input:

- one customer-approved campaign brief,
- one anonymized campaign code or approved campaign name,
- one historical campaign scenario if the customer confirms it is allowed for pilot use,
- aggregate actuals for optional comparison, such as total spend band, aggregate reach, aggregate conversions, or aggregate outcome ranges.

Not allowed:

- PII,
- raw CRM records,
- customer lists,
- account-level or household-level records,
- live CRM, social-listening, ad-platform, analytics, or marketing automation integrations,
- API keys, provider tokens, OAuth credentials, passwords, graph credentials, or customer-owned secrets,
- unapproved confidential campaign material.

If any input includes disallowed data, stop intake and ask the customer to provide an anonymized or approved replacement.

## Session Flow

1. Confirm the campaign brief is approved for pilot use.
2. Confirm no PII, raw CRM records, customer lists, live integration credentials, or secrets are included.
3. Open `/proof-of-value` and enter the approved intake fields.
4. Resolve any missing approvals or unsafe intake signals before assembling customer-facing outputs.
5. Run the brief through the local/demo or controlled pilot workflow with visible source/provenance labels.
6. Review decision-support outputs with the customer.
7. Discuss what the customer would validate next through their normal research, media, analytics, or post-campaign measurement process.
8. Agree whether the next step is a controlled paid pilot with documented scope, data handling, deployment controls, and retention/deletion ownership.

Use [Proof-of-Value Output Package](PROOF_OF_VALUE_OUTPUT_PACKAGE.md) and [Proof-of-Value Operator Checklist](PROOF_OF_VALUE_OPERATOR_CHECKLIST.md) after intake validation passes and before any customer-facing package is shared.

## Decision-Support Outputs

The proof-of-value flow can produce:

- Brief Quality Score,
- Campaign Simulation Summary,
- A/B/C Creative Comparator result,
- Risk and Crisis Watchouts,
- Revised Brief v2,
- Strategy Pack PPTX,
- optional Actual vs Estimate comparison if aggregate actuals are provided.

These outputs are decision-support estimates. They do not guarantee sentiment, conversion, revenue, ROI, ROAS, crisis probability, market share, or real-world campaign outcomes.

## Required Provenance

All customer-facing outputs should show source/provenance labels where applicable:

- Demo Mode,
- Local Estimate,
- Live Backend,
- Backend Verified,
- Unknown Source.

Strategy Pack exports should include a provenance footer with source mode, data basis, safe run/demo ID if available, and `Decision-support estimate, not a guaranteed prediction`.

## Operator Checklist

- [ ] `/proof-of-value` is used to assemble the operator checklist and structured proof-of-value payload.
- [ ] Intake uses [Customer Brief Intake Template](CUSTOMER_BRIEF_INTAKE_TEMPLATE.md).
- [ ] Customer approval checkbox is complete.
- [ ] No PII/raw CRM/customer records checkbox is complete.
- [ ] Unsafe intake signals are resolved before any generated payload, screenshot, export, or deck is shared.
- [ ] Source/provenance labels are visible before sharing outputs.
- [ ] [Proof-of-Value Deliverables](PROOF_OF_VALUE_DELIVERABLES.md) are reviewed before the session.
- [ ] [Proof-of-Value Output Package](PROOF_OF_VALUE_OUTPUT_PACKAGE.md) is used to assemble customer-facing outputs.
- [ ] [Proof-of-Value Operator Checklist](PROOF_OF_VALUE_OPERATOR_CHECKLIST.md) is complete.
- [ ] [Proof-of-Value Session Script](PROOF_OF_VALUE_SESSION_SCRIPT.md) is used for the live walkthrough.
- [ ] [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md) is completed before sending screenshots, decks, exports, or recordings externally.
- [ ] Retention/deletion ownership is agreed before retaining any customer-approved brief or generated artifact.

## Next-Step Decision

A successful proof-of-value session may support a controlled paid pilot proposal. It does not approve public pilot access, public internet exposure, production customer deployment, or live customer-data integrations.
