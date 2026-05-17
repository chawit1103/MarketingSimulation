# Pilot Deployment Dry Run Checklist

Updated: 2026-05-17

Use this checklist before inviting any customer, prospect, agency user, or external observer into a controlled private pilot environment. This dry run validates the environment, demo flows, artifacts, audit behavior, and rollback process using internal operators and synthetic/demo data only.

This checklist does not approve a public pilot, public internet exposure, or production customer deployment.

## Related Documents

- [Pilot Deployment Checklist](PILOT_DEPLOYMENT_CHECKLIST.md)
- [Data Retention and Deletion](DATA_RETENTION_AND_DELETION.md)
- [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md)
- [Customer Data Handling](CUSTOMER_DATA_HANDLING.md)
- [Pilot Operator Runbook](PILOT_OPERATOR_RUNBOOK.md)

## Readiness Boundary

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

Outputs remain decision-support estimates, not guaranteed predictions.

## Dry Run Record

| Field | Value |
| --- | --- |
| Dry run date |  |
| Operator |  |
| Environment URL |  |
| Backend URL |  |
| Git branch |  |
| Git commit |  |
| Pilot org ID |  |
| Test users created |  |
| Synthetic scenario used |  |
| Result | Not started / Pass / Blocked |

## 1. Environment Verification

- [ ] Environment is internal-only or access-restricted for the dry run.
- [ ] HTTPS is enabled for the pilot frontend and backend if hosted.
- [ ] Health/status endpoint responds without returning secrets, stack traces, or local paths.
- [ ] Frontend loads without a framework error overlay.
- [ ] Backend starts with `APP_ENV=production` or the approved pilot-equivalent environment mode.
- [ ] Deployment owner has documented where frontend, backend, uploads, reports, exports, and audit logs are stored.
- [ ] No real customer data, PII, raw CRM data, customer lists, provider tokens, API keys, passwords, graph credentials, or live integration credentials are present in the dry-run inputs.

## 2. Git Branch And Commit Verification

- [ ] Confirm the deployed branch matches the intended release branch.
- [ ] Confirm the deployed commit SHA matches the approved dry-run commit.
- [ ] Confirm the deployed commit includes the latest merged pilot docs and audit hardening changes.
- [ ] Confirm the deployed worktree has no uncommitted local changes.
- [ ] Record the branch and commit in the dry run record above.

Suggested commands for the operator machine:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log --oneline -5
```

## 3. Secret And Environment Variable Verification

- [ ] All secrets come from environment variables or approved secret storage.
- [ ] No `.env`, `.env.*`, local settings JSON, generated reports, uploaded files, or runtime data are committed to Git.
- [ ] `SECRET_KEY` and `AUTH_SECRET_KEY` are non-default values.
- [ ] Provider API keys, embedding API keys, OAuth credentials, graph passwords, and auth tokens are not visible in browser responses.
- [ ] `GET /api/settings` returns only presence flags for secrets.
- [ ] Settings UI shows secret presence text without revealing secret values.
- [ ] No operator copies secrets into screenshots, recordings, docs, chat, issue comments, or deck notes.

## 4. CORS And CSP Verification

- [ ] `CORS_ALLOWED_ORIGINS` is set to the exact approved frontend origin.
- [ ] No wildcard CORS origin is used for a hosted pilot.
- [ ] Preflight requests from the approved frontend origin pass.
- [ ] Preflight requests from an unapproved origin fail or do not receive access.
- [ ] `CONTENT_SECURITY_POLICY` is configured for the pilot environment.
- [ ] CSP `connect-src` allows only the approved API origin and required same-origin resources.
- [ ] Browser console does not show CSP errors for expected app resources.

## 5. Rate-Limit Verification

- [ ] Deployment-level rate limiting exists at edge, gateway, WAF, reverse proxy, or shared-store layer.
- [ ] App-level rate limiting remains enabled as a secondary safeguard.
- [ ] Auth, demo, status, decision, simulation, and settings-like endpoints have appropriate limits.
- [ ] Repeated requests trigger a safe rate-limit response without raw tracebacks.
- [ ] Rate-limit logs do not include request bodies, secrets, raw briefs, or customer data.

## 6. Debug And Request-Body Logging Verification

- [ ] `FLASK_DEBUG=false`.
- [ ] `REQUEST_BODY_LOGGING_ENABLED=false`.
- [ ] Client-facing API errors do not include tracebacks, local file paths, provider dumps, or raw exception strings.
- [ ] Backend logs do not include raw campaign briefs, uploaded file contents, generated report body text, API keys, provider tokens, passwords, graph credentials, or PII.
- [ ] Browser developer tools and network responses do not show secrets or raw customer data.

## 7. Demo Dashboard Smoke Check

- [ ] Open the local/demo dashboard route, such as `/dashboard/demo-premium-water`.
- [ ] Confirm the page loads without requiring live LLM, CRM, social-listening, ad-platform, or Neo4j credentials from the customer.
- [ ] Confirm synthetic campaign context is visible.
- [ ] Confirm source/provenance label is visible.
- [ ] Confirm limitations and recommended validation steps are visible.
- [ ] Confirm no exact ROI/ROAS or guaranteed prediction wording appears.

## 8. Source And Provenance Label Visibility

- [ ] Demo Mode label is visible on demo fixtures.
- [ ] Local Estimate label is visible on browser/local fallback output.
- [ ] Live Backend label is visible only for backend-generated output.
- [ ] Backend Verified label is visible only when backed by persisted owned simulation evidence.
- [ ] Unknown Source is displayed when source metadata is missing.
- [ ] Screenshots, decks, exports, and recordings retain these labels.

## 9. Strategy Pack PPTX Export Smoke Check

- [ ] Use synthetic/demo data only.
- [ ] Generate a sample Brand Executive Summary or Agency Client Pitch Summary PPTX.
- [ ] Confirm the deck opens locally.
- [ ] Confirm every slide includes a provenance footer with source mode, data basis, safe run/demo ID if available, and "Decision-support estimate, not a guaranteed prediction".
- [ ] Confirm the Limitations & Recommended Validation slide is present.
- [ ] Confirm no real customer name, client name, campaign name, PII, secret, raw CRM record, uploaded file content, internal log, or provider response appears.
- [ ] Delete the generated deck after the dry run unless it is intentionally retained as a synthetic-only artifact.

## 10. Audit Log Event Smoke Check

- [ ] Log in as a test admin or analyst.
- [ ] Create or update a synthetic campaign.
- [ ] Start a synthetic/demo report or export flow.
- [ ] Generate a settings update event without storing raw secrets.
- [ ] Confirm `audit_events.jsonl` is created under the expected org-scoped audit directory.
- [ ] Confirm audit events include metadata such as event type, route path, IDs, format, source labels, and timestamps only.
- [ ] Confirm audit events do not contain raw campaign briefs, PII, API keys, tokens, passwords, provider secrets, graph credentials, raw CRM records, uploaded file contents, generated report text, customer names, free-text campaign names, or arbitrary user-supplied labels.
- [ ] Confirm invalid org IDs cannot write outside the audit folder if this check is run locally.

## 11. Data Retention And Deletion Dry Run

- [ ] Create one synthetic campaign or demo run.
- [ ] Generate one report/export artifact.
- [ ] Locate generated campaign, report, export, upload, calibration, and audit directories.
- [ ] Delete generated reports/exports according to [Data Retention and Deletion](DATA_RETENTION_AND_DELETION.md).
- [ ] Delete uploaded pilot files and temporary parsed copies.
- [ ] Delete synthetic campaign data only if the dry run is not retaining it for further internal testing.
- [ ] Confirm deleted files no longer exist in primary storage.
- [ ] Confirm backup/manual share locations do not retain deleted artifacts.
- [ ] Record what was deleted, what was retained, and why.

## 12. Screenshot And Deck Artifact Safety Review

- [ ] Run every screenshot, deck, recording, and export through [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md).
- [ ] Confirm source/provenance labels are visible.
- [ ] Confirm limitations are visible.
- [ ] Confirm no real customer data, PII, secrets, provider tokens, graph credentials, raw CRM records, internal logs, raw briefs, or generated real-customer report text are visible.
- [ ] Confirm no production-readiness, public-pilot readiness, exact ROI/ROAS, or guaranteed prediction claims appear.
- [ ] Record reviewer and review date before sharing any artifact externally.

## Rollback Steps

If any gate fails, stop the dry run and complete rollback before inviting external users.

- [ ] Revoke test users and remove temporary admin, analyst, and viewer accounts.
- [ ] Rotate any test credential that may have been exposed during the dry run.
- [ ] Delete generated reports and exports.
- [ ] Delete downloaded PPTX/CSV/PDF/Markdown files from operator machines and shared folders.
- [ ] Delete uploaded pilot files and temporary parsed copies.
- [ ] Delete synthetic campaign data if it is no longer needed.
- [ ] Disable or restrict the pilot environment URL.
- [ ] Confirm audit logs contain no raw secrets, customer data, PII, raw briefs, uploaded file contents, generated report body text, free-text campaign names, or internal logs.
- [ ] Retain only safe audit metadata if needed for accountability.
- [ ] Document failure reason, owner, remediation, and date of next attempted dry run.

## Go / No-Go

Invite customers or prospects only if every required dry-run gate passes and the deployment owner accepts the remaining controlled-private-pilot risks.

If any item is blocked, keep the environment internal-only.
