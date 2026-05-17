# Customer Data Handling

Updated: 2026-05-17

## Readiness Statement

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

## Pilot Data Rules

- Use synthetic, anonymized, or explicitly approved campaign briefs.
- Do not enter PII, raw CRM records, customer lists, regulated personal data, provider secrets, API keys, tokens, passwords, or graph credentials as campaign content.
- Use aggregate calibration records only. Do not upload raw customer, lead, CRM, or social-post records.
- Keep output provenance labels visible in the UI, screenshots, exports, and docs.
- Follow [DATA_RETENTION_AND_DELETION.md](DATA_RETENTION_AND_DELETION.md) for retention periods and deletion requests.

## Audit Logging

Pilot audit logs record operational metadata for login, campaign changes, simulation lifecycle, report/export generation or download, calibration import, and settings updates. Audit logs are designed to store IDs, event types, changed field names, source labels, formats, and timestamps only.

Audit logs must not contain raw briefs, PII, credentials, raw CRM data, customer records, uploaded file contents, or report body text.
