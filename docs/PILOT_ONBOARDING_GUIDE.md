# Pilot Onboarding Guide

Updated: 2026-05-17

Use this guide for the first customer session after a paid pilot is approved.

## Before The Session

Confirm:

- Pilot sponsor and pilot lead.
- Approved scenario list.
- Data approver.
- No PII, raw CRM records, or live integrations.
- Source/provenance labels must remain visible.
- Outputs are decision-support estimates, not guaranteed predictions.

## Onboarding Agenda

### 1. Set Expectations

Explain:

- Local demo is ready.
- Controlled private pilot is a conditional candidate.
- Public pilot, public internet exposure, and production customer deployment are blocked.
- The pilot is a guided controlled engagement, not self-serve production SaaS.

### 2. Show Source Labels

Walk through:

- Demo Mode: synthetic demo fixture.
- Local Estimate: deterministic fallback or local-only estimate.
- Live Backend: backend-generated output that is not yet persisted evidence.
- Backend Verified: persisted real simulation KPI/evidence for an owned campaign/run.
- Unknown Source: insufficient provenance.

### 3. Review Data Rules

State clearly:

- No PII.
- No raw CRM records.
- No API keys, provider tokens, OAuth credentials, passwords, graph credentials, or customer-owned provider secrets may be entered into browser fields.
- If customer-owned credentials are ever needed in a later approved phase, configure them only through an approved deployment secret path, environment variable, or secret manager. Never capture them in browser forms, screenshots, docs, exports, recordings, chat logs, or pilot artifacts.
- Use anonymized or approved campaign briefs.
- No live social-listening or CRM integration.

### 4. Run The First Scenario

Recommended path:

1. Open demo dashboard.
2. Review Brief Quality Score criteria.
3. Enter approved scenario summary.
4. Review dashboard evidence and limitations.
5. Review Action Plan.
6. Export Strategy Pack if useful.

### 5. Capture Feedback

Ask:

- What decision does this help you make?
- What would you trust?
- What would you challenge?
- What validation step is required before launch?
- Would you pay to run another scenario?

## After The Session

Send:

- Scenario summary.
- Source-labeled output summary.
- Action Plan.
- Open questions.
- Data deletion or retention decision.
- Next meeting agenda.
