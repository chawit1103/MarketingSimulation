# Data Retention and Deletion

Updated: 2026-05-17

This policy supports controlled private pilots only. It does not make 3C Simulator production-ready, publicly safe, or suitable for production customer deployment.

## Readiness Statement

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

Outputs remain decision-support estimates, not guaranteed predictions.

## Storage Boundary

The current backend uses lightweight local JSON/file storage under the configured upload folder. Pilot data is scoped by organization where the current architecture supports it, including:

- `organizations/<org_id>/campaigns/`
- `organizations/<org_id>/audit/audit_events.jsonl`
- report, simulation, calibration, upload, and generated artifact directories configured by the backend

This is acceptable only for controlled private pilots with trusted operators and documented deletion ownership. It is not a production storage architecture.

## Data Categories

| Category | Allowed for pilot | Default retention | Deletion target |
| --- | --- | --- | --- |
| Campaign briefs | Approved or anonymized briefs only | Delete at pilot exit, or within 30 days after exit if written retention is approved | Campaign JSON, derived project text, brief-quality/revised-brief records, screenshots containing brief text |
| Simulation outputs | Deterministic/synthetic or approved pilot outputs with visible source labels | Delete at pilot exit, or within 30 days after exit if retained for review | Simulation state, generated profiles, run logs, action JSONL, KPI/dashboard outputs |
| Generated reports/exports | Approved pilot reports and decks only | Delete at pilot exit, or within 30 days after exit | Markdown reports, PPTX/CSV exports, local download artifacts, screenshots |
| Calibration records | Aggregate actuals only; no raw CRM/customer records | Delete at pilot exit unless the data owner approves up to 180 days for calibration review | Calibration JSON records and related comparison summaries |
| Uploaded pilot files | Approved files only; no raw customer lists or regulated personal data | Delete after extraction/review when practical, no later than pilot exit | Uploaded PDFs, text files, parsed copies, temporary files |
| Audit logs | Event metadata only; no raw briefs, PII, secrets, tokens, or customer records | 365 days for controlled pilot accountability unless the pilot agreement requires shorter retention | Org audit JSONL files |

## Audit Log Rules

Audit events are org-scoped and append-only in the current lightweight storage. Events may include IDs, event type, route path, actor user ID, changed field names, export format, source mode, and record IDs.

Audit events must not include raw campaign briefs, PII, API keys, tokens, passwords, provider secrets, graph credentials, raw CRM records, customer lists, uploaded file contents, or generated report body text.

## Deletion Request Workflow

1. Confirm requester authority and affected organization.
2. Record the request date, requested scope, deletion deadline, and accountable operator.
3. Pause new pilot runs for the affected organization if deletion would conflict with active work.
4. Delete or archive-for-deletion the requested categories:
   - campaign JSON and derived brief records,
   - simulation state and run outputs,
   - generated reports and exports,
   - calibration records,
   - uploaded pilot files and temporary parsed copies,
   - screenshots or demo artifacts containing customer data,
   - audit logs only when contractually allowed or legally required.
5. Verify the files no longer exist in local storage, backup locations, and any manually shared folders.
6. Confirm deletion completion to the data owner with the deletion date, categories deleted, and any retained audit/legal records.

## Operator Notes

- Do not retain customer data by default.
- Do not add live CRM or social-listening integrations for this pilot phase.
- Do not use raw customer records as calibration input.
- Keep Demo Mode, Local Estimate, Live Backend, Backend Verified, or Unknown Source labels visible wherever outputs are shown.
- If retention expectations differ from this document, record the approved override before pilot kickoff.
