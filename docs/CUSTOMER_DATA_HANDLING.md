# Customer Data Handling

Updated: 2026-05-17

This policy applies to controlled paid pilots. It is intentionally conservative because the product is not yet cleared for public internet exposure or production customer deployment.

## Readiness Statement

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

Outputs remain decision-support estimates, not guaranteed predictions.

## Data Rules For The First Pilot

- No PII.
- No raw CRM records.
- No customer lists, phone numbers, email addresses, or account IDs.
- No live social-listening integration.
- No live CRM, ad-platform, or marketing automation integration.
- Use synthetic, anonymized, or explicitly approved campaign briefs only.
- Use aggregate calibration records only. Do not upload raw customer, lead, CRM, or social-post records.
- Keep source/provenance labels visible in the UI, screenshots, exports, docs, and decks.
- Follow [DATA_RETENTION_AND_DELETION.md](DATA_RETENTION_AND_DELETION.md) for retention periods and deletion requests.

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
- Aggregate calibration metrics only, such as impressions, CTR, conversion count/rate, sales lift, sentiment summary, or crisis incident flag.

## Disallowed Inputs

Do not collect:

- Names, phone numbers, emails, addresses, device IDs, or account IDs.
- Customer support transcripts tied to identifiable people.
- Raw CRM exports, transaction logs, lead lists, or customer records.
- API keys, provider tokens, OAuth credentials, passwords, tokens, or secrets.
- Graph credentials or customer-owned provider secrets.
- Any credentials entered through browser forms, screenshots, docs, exports, recordings, chat logs, or pilot artifacts.
- Uploaded file contents containing PII, raw CRM data, customer records, or regulated personal data.
- Confidential board materials unless explicitly approved and sanitized.
- Regulated personal data, health data, financial account data, or children's data.

## Recommended Anonymization

Before intake:

1. Replace real campaign names with neutral labels when possible.
2. Convert individual customer records into aggregate segment descriptions.
3. Replace exact budget with a range.
4. Remove names of employees, customers, influencers, and private accounts unless they are public and approved.
5. Summarize legal constraints without including privileged legal advice.
6. Replace unsafe campaign IDs or labels with internal generated IDs where possible.

## Storage Expectations

For the first paid pilot:

- Prefer local or private controlled environment.
- Keep secrets in environment variables or approved secret storage.
- Do not store provider API keys in browser local storage.
- If customer-owned credentials are ever needed in a later approved phase, configure them only through an approved deployment secret path, environment variable, or secret manager.
- Do not commit `.env`, `.env.*`, runtime settings files, uploads, generated reports with customer data, or provider credentials.
- Delete pilot artifacts at exit unless the customer approves retention.

## Audit Logging

Pilot audit logs record operational metadata for login, campaign changes, simulation lifecycle, report/export generation or download, calibration import, and settings updates.

Audit logs are designed to store IDs, event types, changed field names, source labels, formats, route paths, and timestamps only.

Audit logs must not contain raw briefs, PII, API keys, tokens, passwords, provider secrets, graph credentials, raw CRM data, customer records, uploaded file contents, generated report body text, customer names, or free-text campaign names.

If a campaign identifier is not a safe generated internal ID, audit metadata should record `unknown` or omit the value rather than storing the raw user-supplied label.

## Customer-Facing Disclosure

Use this plain-language disclosure in onboarding:

> 3C Simulator uses approved campaign context to generate decision-support estimates. The pilot does not require PII, raw CRM data, or live integrations. Outputs should guide discussion and validation planning; they are not guaranteed predictions.
