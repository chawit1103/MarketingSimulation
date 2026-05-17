# Customer Data Handling

Updated: 2026-05-17

This policy applies to controlled paid pilots. It is intentionally conservative because the product is not yet cleared for public internet exposure or production customer deployment.

## Data Rules For The First Pilot

- No PII.
- No raw CRM records.
- No customer lists, phone numbers, email addresses, or account IDs.
- No live social-listening integration.
- No live CRM, ad-platform, or marketing automation integration.
- Use anonymized or explicitly approved campaign briefs only.
- Keep source/provenance labels visible in the UI, screenshots, exports, and decks.

## Allowed Inputs

Use these input types only after customer approval:

- Campaign name or anonymized campaign code.
- Product category and market context.
- Target audience descriptions at segment level.
- Channel mix at planning level.
- Non-sensitive competitor context.
- Budget range or relative spend band.
- Risk/legal notes that do not include personal data.
- Publicly known industry context.

## Disallowed Inputs

Do not collect:

- Names, phone numbers, emails, addresses, device IDs, or account IDs.
- Customer support transcripts tied to identifiable people.
- Raw CRM exports, transaction logs, or lead lists.
- API keys, provider tokens, OAuth credentials, or passwords.
- Confidential board materials unless explicitly approved and sanitized.
- Regulated personal data, health data, financial account data, or children's data.

## Recommended Anonymization

Before intake:

1. Replace real campaign names with neutral labels when possible.
2. Convert individual customer records into aggregate segment descriptions.
3. Replace exact budget with a range.
4. Remove names of employees, customers, influencers, and private accounts unless they are public and approved.
5. Summarize legal constraints without including privileged legal advice.

## Storage Expectations

For the first paid pilot:

- Prefer local or private controlled environment.
- Keep secrets in environment variables or approved secret storage.
- Do not store provider API keys in browser local storage.
- Do not commit `.env`, `.env.*`, generated reports with customer data, or uploads.
- Delete pilot artifacts at exit unless the customer approves retention.

## Customer-Facing Disclosure

Use this plain-language disclosure in onboarding:

> 3C Simulator uses approved campaign context to generate decision-support estimates. The pilot does not require PII, raw CRM data, or live integrations. Outputs should guide discussion and validation planning; they are not guaranteed predictions.

