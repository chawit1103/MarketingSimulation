# Pilot Operator Runbook

Updated: 2026-05-17

This runbook is for internal operators preparing a controlled private pilot dry run. It complements [Pilot Deployment Dry Run Checklist](PILOT_DRY_RUN_CHECKLIST.md) and does not approve public pilot, public internet exposure, or production customer deployment.

## Operating Principles

- Use synthetic/demo data for dry runs.
- Keep source/provenance labels visible.
- Keep outputs framed as decision-support estimates.
- Do not collect PII, raw CRM records, live social-listening data, provider tokens, API keys, passwords, graph credentials, or customer-owned secrets.
- Do not enter customer-owned credentials through browser fields.
- Do not share screenshots, decks, recordings, or exports until they pass [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md).

## Roles

| Role | Responsibility |
| --- | --- |
| Deployment owner | Approves environment, secrets, CORS/CSP, rate limits, logging, and rollback readiness. |
| Pilot operator | Runs the dry-run checklist, records evidence, and owns cleanup. |
| Security reviewer | Reviews secret handling, audit log safety, CORS/CSP, logs, and artifact hygiene. |
| Demo owner | Owns sales walkthrough, sample briefs, screenshots, decks, and prospect-facing talk track. |

## Pre-Dry-Run Setup

1. Confirm the current branch and commit.
2. Confirm deployment environment variables are present without printing secret values.
3. Confirm the pilot org, admin, analyst, and viewer test users are internal-only.
4. Confirm dry-run scenarios are synthetic/demo-only.
5. Confirm deletion owner and artifact owner are assigned.

## Dry-Run Sequence

1. Environment and status check.
2. CORS/CSP and rate-limit check.
3. Debug and logging check.
4. Demo dashboard smoke check.
5. Source/provenance label check.
6. Strategy Pack PPTX export smoke check.
7. Audit event smoke check.
8. Data retention/deletion dry run.
9. Screenshot/deck artifact safety review.
10. Rollback drill if any gate fails.

## Evidence To Record

Record evidence in an internal tracker or dry-run note, not in public docs:

- date and operator,
- environment URL,
- backend URL,
- git branch,
- git commit,
- source labels observed,
- artifact names reviewed,
- deletion categories tested,
- audit log safety result,
- blockers and owner.

Do not paste secrets, tokens, raw request bodies, raw briefs, customer data, screenshots with credentials, or audit log lines containing sensitive data into the evidence record.

## Customer Invite Decision

Customers or prospects may be invited only after:

- [ ] [Pilot Deployment Checklist](PILOT_DEPLOYMENT_CHECKLIST.md) is reviewed.
- [ ] [Pilot Deployment Dry Run Checklist](PILOT_DRY_RUN_CHECKLIST.md) passes.
- [ ] [Customer Data Handling](CUSTOMER_DATA_HANDLING.md) rules are accepted.
- [ ] [Data Retention and Deletion](DATA_RETENTION_AND_DELETION.md) ownership is assigned.
- [ ] [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md) passes for any shared artifact.

If any item is incomplete, keep the pilot internal-only.

## Incident Or Failed Gate Response

1. Stop external sharing.
2. Revoke temporary test users if access scope is uncertain.
3. Delete unsafe generated reports, decks, screenshots, uploads, and exports.
4. Confirm audit logs contain metadata only and no raw secrets or customer data.
5. Disable the pilot URL or restrict access if exposure is uncertain.
6. Record the issue owner and remediation.
7. Repeat the dry run after remediation.

## Rollback Checklist

- [ ] Revoke test admin, analyst, and viewer users.
- [ ] Delete generated reports/exports.
- [ ] Delete uploaded pilot files and parsed temporary files.
- [ ] Delete local downloaded decks from operator machines.
- [ ] Remove shared-folder copies of demo artifacts unless approved as synthetic-only.
- [ ] Confirm logs and audit events do not contain raw secrets or customer data.
- [ ] Confirm environment access is restricted or disabled.
- [ ] Record rollback completion date and owner.
