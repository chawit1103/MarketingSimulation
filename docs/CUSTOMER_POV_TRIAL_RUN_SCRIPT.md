# Customer Proof-of-Value Trial Run Script

Updated: 2026-05-17

Use this script for the first real customer proof-of-value session using one customer-approved campaign brief or one approved historical campaign scenario. The session is designed to show practical value from approved business context while keeping personal data, raw customer records, credentials, screenshots, binary decks, and unapproved material out of scope.

This is a customer proof-of-value trial, not a production SaaS deployment or public pilot.

## Related Resources

- App route: [`/proof-of-value`](/proof-of-value)
- App route: [`/resources`](/resources)
- [Proof-of-Value One-Page Copy](PROOF_OF_VALUE_ONE_PAGE_COPY.md)
- [Customer Brief Intake Template](CUSTOMER_BRIEF_INTAKE_TEMPLATE.md)
- [Proof-of-Value Output Package](PROOF_OF_VALUE_OUTPUT_PACKAGE.md)
- [Sample Proof-of-Value Package](SAMPLE_PROOF_OF_VALUE_PACKAGE.md)

## First Customer Trial Flow

1. Ask for one approved campaign brief or approved historical campaign scenario.
2. Confirm the brief includes no PII, raw CRM records, customer lists, credentials, or secrets.
3. Enter the approved fields in `/proof-of-value`.
4. Resolve every missing approval and unsafe intake signal before copying the structured payload.
5. Assemble the output package using [Proof-of-Value Output Package](PROOF_OF_VALUE_OUTPUT_PACKAGE.md).
6. Review the result with the customer as a decision-support estimate.
7. Ask whether the result is useful enough to scope a controlled paid pilot.

## Pre-Session Checklist

- [ ] Customer has one campaign brief or historical scenario approved for proof-of-value use.
- [ ] Customer has completed or reviewed [Customer Brief Intake Template](CUSTOMER_BRIEF_INTAKE_TEMPLATE.md).
- [ ] Customer has confirmed the intake contains no PII.
- [ ] Customer has confirmed the intake contains no raw CRM records.
- [ ] Customer has confirmed the intake contains no customer lists.
- [ ] Customer has confirmed the intake contains no API keys, provider tokens, OAuth credentials, passwords, graph credentials, private keys, or other secrets.
- [ ] Customer has confirmed no live CRM, social-listening, ad-platform, analytics, or marketing automation integration is required.
- [ ] Optional historical actuals, if used, are approved and aggregate-only.
- [ ] Operator can access `/proof-of-value` and `/resources`.
- [ ] Operator has reviewed [Proof-of-Value Output Package](PROOF_OF_VALUE_OUTPUT_PACKAGE.md) and [Sample Proof-of-Value Package](SAMPLE_PROOF_OF_VALUE_PACKAGE.md).
- [ ] Operator has confirmed source/provenance labels remain visible in any customer-facing output.
- [ ] Operator has prepared a short explanation that outputs are decision-support estimates and should be validated through the customer's normal review process.

## Customer Brief Request Message

Subject: Brief needed for 3C Simulator proof-of-value session

Hi {{customer_name}},

For the proof-of-value session, please send one campaign brief or historical campaign scenario that your team has approved for pilot use. The brief can use real business context if approved, or an anonymized campaign code if that is safer.

Please include only the information needed to evaluate the campaign decision:

- objective,
- product or service,
- target segment,
- market context,
- channel plan,
- budget band,
- competitor context,
- creative directions if available,
- risk concerns,
- success KPIs,
- aggregate historical actuals if approved.

Please do not include PII, raw CRM records, customer lists, account-level records, contact details, API keys, provider tokens, passwords, graph credentials, or live integration credentials.

Before the session, we will confirm the data boundary together. The output will be used as a decision-support estimate for pilot evaluation, and should be validated through your normal research, analytics, or post-campaign measurement process.

Thanks,
{{operator_name}}

## Data Boundary Confirmation

Use this at the start of the live session before entering or reviewing any brief content:

> Today we are using one customer-approved campaign brief or approved historical scenario. We are not using PII, raw CRM records, customer lists, account-level records, live integrations, credentials, API keys, provider tokens, passwords, graph credentials, or other secrets. Any optional actuals must be aggregate-only and approved for this session. Outputs are decision-support estimates for pilot evaluation and should be validated through your normal decision process.

If the customer cannot confirm the boundary, pause the session and ask for an anonymized or approved replacement brief.

## Operator Steps Using `/proof-of-value`

1. Open `/proof-of-value`.
2. Enter only approved intake fields from the customer brief.
3. Use an anonymized campaign code if the real campaign name is not approved for pilot use.
4. Enter aggregate actuals only if they are approved and aggregate-only.
5. Complete the approval confirmations with the customer.
6. Check the status panel.
7. If status is blocked, resolve missing fields, missing confirmations, or unsafe intake signals before continuing.
8. Confirm the structured payload no longer contains blocked placeholders.
9. Copy the structured payload for operator use.
10. Keep any copied payload inside the agreed pilot storage boundary.

Do not paste disallowed data into screenshots, issue comments, public docs, chat tools, or customer-facing decks.

## 30-Minute Live Session Script

| Time | Step | Operator talk track |
| --- | --- | --- |
| 0-3 min | Welcome and purpose | "We will use one approved brief to see whether 3C Simulator can produce useful campaign decision support." |
| 3-6 min | Confirm data boundary | Use the data boundary confirmation above. Pause if any disallowed data is present. |
| 6-10 min | Review intake readiness | Open `/proof-of-value`, confirm approvals, and show whether the structured payload is ready. |
| 10-15 min | Brief quality finding | Review the strongest brief inputs, missing assumptions, and recommended cleanup. |
| 15-20 min | Simulation and creative readout | Review directional segment reactions and A/B/C creative comparison if creative directions are present. |
| 20-24 min | Risks and revised brief | Review risk watchouts and the Revised Brief v2 direction. |
| 24-27 min | Output package preview | Show the expected proof-of-value package structure and visible provenance labels. |
| 27-30 min | Decision close | Ask whether the result is useful enough to scope a controlled paid pilot with agreed data handling, success criteria, and retention/deletion ownership. |

## 60-Minute Workshop Script

| Time | Step | Operator talk track |
| --- | --- | --- |
| 0-5 min | Welcome, roles, and consent | Confirm the approved brief, customer owner, and proof-of-value purpose. |
| 5-10 min | Data boundary | Confirm no PII, raw CRM records, customer lists, credentials, secrets, or live integrations are included. |
| 10-18 min | Intake walkthrough | Enter or review the brief in `/proof-of-value`; resolve any blocked status before continuing. |
| 18-26 min | Brief Quality Score | Discuss whether the objective, segment, channel plan, competitor context, risks, and KPIs are clear enough for decision support. |
| 26-36 min | Campaign Simulation Summary | Review directional reactions, key assumptions, and the highest-value decision implication. |
| 36-44 min | A/B/C Creative Comparator | Compare creative routes if available and agree on the next validation question. |
| 44-50 min | Risk and Crisis Watchouts | Review sensitive claims, competitor risks, trust issues, and mitigation options. |
| 50-55 min | Revised Brief v2 and Strategy Pack | Review how the brief and Strategy Pack would be packaged for stakeholders. |
| 55-58 min | Optional aggregate actuals | If approved aggregate actuals were provided, review the comparison as directional and diagnostic only. |
| 58-60 min | Paid pilot decision | Decide whether to scope a controlled paid pilot, what data remains out of scope, and who owns next steps. |

## Output Package Preparation

Prepare the customer-facing package only after `/proof-of-value` is ready and no unsafe intake signals remain.

Minimum package:

- one-page executive summary,
- brief quality finding,
- campaign simulation summary,
- A/B/C creative comparison if creative directions are present,
- risk and crisis watchouts,
- Revised Brief v2,
- Strategy Pack PPTX outline or export,
- recommended validation step,
- limitations and assumptions.

Conditional package item:

- Optional Actual vs Estimate comparison only when approved aggregate actuals were provided. Use aggregate-only values and frame the comparison as directional and diagnostic.

Before sharing anything externally:

- [ ] Source/provenance labels are visible.
- [ ] Limitations and recommended validation step are visible.
- [ ] No PII, raw CRM records, customer lists, credentials, or secrets appear.
- [ ] No internal logs, stack traces, local file paths, request IDs, or provider error details appear.
- [ ] The package stays inside the agreed sharing and retention boundary.

## Post-Session Follow-Up Message

Subject: Proof-of-value session recap and next step

Hi {{customer_name}},

Thank you for reviewing the proof-of-value package with us. We used the approved campaign brief/scenario you provided and kept the agreed data boundary: no PII, raw CRM records, customer lists, credentials, secrets, or live integrations.

Attached or linked are the agreed proof-of-value materials:

- executive summary,
- brief quality finding,
- campaign simulation summary,
- creative comparison if applicable,
- risk watchouts,
- Revised Brief v2,
- Strategy Pack outline or export,
- recommended validation step,
- optional aggregate Actual vs Estimate comparison if approved aggregate actuals were provided.

The outputs are decision-support estimates for pilot evaluation and should be validated through your normal research, analytics, or post-campaign measurement process.

If the package helped clarify a campaign decision, the next step is a controlled paid pilot scoping call. In that call we would agree on the pilot question, approved data inputs, access controls, artifact sharing rules, retention/deletion owner, success criteria, and review timeline.

Thanks,
{{operator_name}}

## Paid Pilot Decision Criteria

Recommend scoping a controlled paid pilot only if the customer confirms:

- The proof-of-value output helped clarify a real campaign decision.
- The customer can name one or two validation questions for a pilot.
- The customer agrees the first pilot can proceed without PII, raw CRM records, customer lists, secrets, or live integrations.
- The customer can approve one campaign brief or historical scenario for pilot use.
- The customer accepts visible source/provenance labels and limitations in shared outputs.
- The customer has an owner for pilot scope, artifact sharing, retention/deletion, and final review.
- The customer understands the outputs support decision-making and do not replace their validation, analytics, or research process.

Do not proceed to a paid pilot if:

- The customer requires disallowed data for the first session.
- The customer wants public access, public internet exposure, or a production customer deployment.
- The customer expects outcome certainty or financial forecasting from the proof-of-value package.
- Retention/deletion ownership and artifact sharing boundaries are not agreed.
