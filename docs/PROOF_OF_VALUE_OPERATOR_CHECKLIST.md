# Proof-of-Value Operator Checklist

Updated: 2026-05-17

Use this checklist after `/proof-of-value` intake validation passes and before sharing proof-of-value outputs with a customer or prospect.

## Intake Gate

- [ ] `/proof-of-value` status is ready for operator review.
- [ ] Structured payload values are visible only after required safety confirmations pass.
- [ ] No intake field is blocked by `[blocked: safety confirmations required]`.
- [ ] No intake field is blocked by `[blocked: unsafe intake signal]`.
- [ ] The brief or historical scenario is approved for pilot use.
- [ ] Optional aggregate actuals are aggregate-only and approved if used.

## Data Boundary

- [ ] No PII.
- [ ] No raw CRM records.
- [ ] No customer lists.
- [ ] No account-level, household-level, or individual-level customer records.
- [ ] No API keys, provider tokens, OAuth credentials, passwords, graph credentials, private keys, or secrets.
- [ ] No live CRM, social-listening, ad-platform, analytics, or marketing automation integrations.

## Output Assembly

- [ ] Copy the structured payload from `/proof-of-value`.
- [ ] Run Brief Quality Score.
- [ ] Run Campaign Simulation Summary.
- [ ] Run A/B/C Creative Comparator if creative directions A, B, and C are present.
- [ ] Review Risk and Crisis Watchouts.
- [ ] Create Revised Brief v2.
- [ ] Generate Strategy Pack PPTX.
- [ ] If approved aggregate actuals are provided, run or prepare the Optional Actual vs Estimate comparison using aggregate-only values.
- [ ] Add or preserve recommended validation step.

## Customer Package Review

- [ ] One-page executive summary is included.
- [ ] Brief quality finding is included.
- [ ] Simulation summary is included.
- [ ] Creative comparison result is included when applicable.
- [ ] Risk watchouts are included.
- [ ] Revised Brief v2 is included.
- [ ] Strategy Pack PPTX is included when requested.
- [ ] Optional Actual vs Estimate comparison is included when approved aggregate actuals were provided.
- [ ] Limitations and assumptions are visible.
- [ ] Source/provenance labels are visible.

## Claim Safety

- [ ] Outputs are described as decision-support estimates.
- [ ] No guaranteed prediction claims.
- [ ] No exact ROI/ROAS claims.
- [ ] No production SaaS claims.
- [ ] No public pilot readiness claims.
- [ ] No public internet readiness claims.
- [ ] No claims that the output replaces market research.

## Final Step

- [ ] Run [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md) before sharing any screenshot, deck, export, recording, or written summary externally.
- [ ] Record who reviewed the package and when.
- [ ] Confirm retention/deletion owner if the output package will be retained after the session.
