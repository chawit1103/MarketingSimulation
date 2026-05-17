# Proof-of-Value Output Package

Updated: 2026-05-17

This guide explains how an operator turns a safe, approved `/proof-of-value` intake into customer-facing proof-of-value outputs. It applies after the structured payload is marked ready for operator review.

The output package is for decision support. It is not a guaranteed prediction, not exact ROI or ROAS forecasting, not production SaaS, and not public pilot readiness.

## Prerequisites

Before assembling outputs, confirm:

- `/proof-of-value` shows the intake as ready for operator review.
- The structured payload no longer contains safety placeholders.
- The intake uses one approved campaign brief or approved historical scenario.
- Required confirmations are complete for no PII, no raw CRM records, no customer lists, no secrets, and no live integrations.
- Optional aggregate actuals are approved and aggregate-only if provided.
- Source/provenance labels remain visible in every output.

If any prerequisite fails, stop and return to intake cleanup.

## Operator Sequence

1. Copy the structured payload from `/proof-of-value`.
2. Run Brief Quality Score using the approved brief context.
3. Run Campaign Simulation Summary using the same approved context.
4. Run A/B/C Creative Comparator if creative directions A, B, and C are present.
5. Review Risk and Crisis Watchouts.
6. Create Revised Brief v2 from the safe action-plan or decision-support output.
7. Generate Strategy Pack PPTX.
8. If approved aggregate actuals are provided, run or prepare the Optional Actual vs Estimate comparison using aggregate-only values.
9. Run [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md) before sharing any screenshot, deck, export, recording, or written summary.

Keep the payload and outputs within the agreed pilot storage and retention boundary.

## Customer-Facing Output Package

| Output | Include | Format |
| --- | --- | --- |
| One-page executive summary | Business question, directional recommendation, source/provenance label, limitations, recommended validation step | Short Markdown/PDF section or first slide |
| Brief quality finding | Brief Quality Score, missing assumptions, recommended brief cleanup | In-app summary or excerpt |
| Simulation summary | Segment reactions, likely friction, directional opportunity, assumptions | In-app summary or report excerpt |
| Creative comparison result | A/B/C comparison, preferred direction, tradeoffs, validation question | Comparator screenshot or summary table |
| Risk watchouts | Risk drivers, crisis watchouts, mitigation notes | In-app summary or Strategy Pack slide |
| Revised Brief v2 | Revised objective, target segment, message, proof points, risk guardrails, validation plan | Markdown section or report excerpt |
| Strategy Pack PPTX | Executive summary, decision gate, segment reactions, risks, action plan, limitations | PPTX export |
| Recommended validation step | What the customer should validate next through research, media, analytics, or post-campaign measurement | Final section or closing slide |

## Include In Customer Delivery

- Approved campaign name or anonymized campaign code only.
- Decision-support estimate language.
- Source/provenance labels such as Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source.
- Data basis when available.
- Safe run/demo ID only if it does not expose customer data.
- Limitations and assumptions.
- Recommended validation step.
- Retention/deletion reminder if outputs will be retained after the session.

## Exclude From Customer Delivery

- PII.
- Raw CRM records.
- Customer lists.
- Account-level, household-level, or individual-level records.
- API keys, provider tokens, OAuth credentials, passwords, graph credentials, private keys, or customer-owned secrets.
- Live CRM, social-listening, ad-platform, analytics, or marketing automation integrations.
- Internal logs, stack traces, local file paths, request IDs, or provider error dumps.
- Raw intake fields while safety confirmations are incomplete.
- Production-readiness, public-pilot readiness, public-internet readiness, guaranteed-prediction, exact ROI/ROAS, or market-research replacement claims.

## Source And Provenance Requirements

Every shared output should preserve visible source/provenance labels. Strategy Pack PPTX exports should include a footer with:

- source mode,
- data basis,
- safe run/demo ID if available,
- `Decision-support estimate, not a guaranteed prediction`.

If source metadata is missing, use Unknown Source and treat the output as requiring additional validation before use.

## Final Share Gate

Before external sharing, the operator should confirm:

- [ ] [Proof-of-Value Operator Checklist](PROOF_OF_VALUE_OPERATOR_CHECKLIST.md) is complete.
- [ ] [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md) is complete.
- [ ] No disallowed data or secrets appear in the output package.
- [ ] Limitations and recommended validation are visible.
- [ ] The output is framed as decision support, not a guaranteed forecast.
