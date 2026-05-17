# Pilot Release Candidate Validation

Updated: 2026-05-17

This report summarizes the current `multilang-v0.3` release-candidate boundary after PR #42 through PR #51. It is a documentation validation record only. It does not add product features, customer data, secrets, screenshots, decks, or binary artifacts.

## Readiness Summary

| Path | Result | Notes |
| --- | --- | --- |
| Local demo | Ready | Appropriate for internal/local walkthroughs with demo fixtures, visible source labels, and no customer data. |
| Sales demo | Ready with synthetic/demo data only | Appropriate for prospect conversations when artifacts pass the demo safety checklist and outputs are framed as decision-support estimates. |
| Controlled paid pilot | Conditional candidate | Requires a signed/approved pilot scope, trusted operators, hosted deployment controls, credential evidence, dry-run execution, audit review, and retention/deletion ownership. |
| Public pilot | Blocked | Public pilot access remains outside the current release boundary. |
| Public internet exposure | Blocked | Public internet exposure remains blocked until deployment-level controls and operational evidence are complete. |
| Production customer deployment | Blocked | The current package is not a production SaaS or production customer deployment. |

Canonical readiness wording remains:

- Local demo: ready.
- Sales demo: ready with synthetic/demo data only.
- Controlled private pilot: conditional candidate.
- Public pilot: blocked.
- Public internet exposure: blocked.
- Production customer deployment: blocked.

## Validation Checklist

| Area | Status | Validation note |
| --- | --- | --- |
| CI status | Required before release candidate approval | GitHub Actions must be green on the final release-candidate commit before inviting any customer or prospect. |
| Secret hygiene | Locally checked for this docs PR; CI gate remains required | CI Secret Hygiene allows only `.env.example`, `.env.dev.example`, and `.env.production.example` as tracked env examples, and continues scanning for secret-like tokens outside allowed examples. |
| Backend tests | Required before release candidate approval | Run `backend/.venv/bin/python -m pytest backend/tests -q` on the final release-candidate commit. |
| Frontend quality | Required before release candidate approval | Run the frontend lint/typecheck/test gates available in `frontend/package.json` on the final release-candidate commit. |
| Frontend build | Required before release candidate approval | Run `cd frontend && npm run build` on the final release-candidate commit. |
| E2E smoke | Required before customer invite | Run a local or hosted smoke check for demo dashboard, source labels, Strategy Pack export, audit event creation, and deletion/rollback paths using synthetic/demo data only. |
| Documentation links | Locally checked for reviewed docs | Local Markdown links in the pilot/demo/sales/readiness docs should resolve before sharing the package. |
| Customer data handling | Documented; operational approval required | Follow [Customer Data Handling](CUSTOMER_DATA_HANDLING.md). No PII, raw CRM records, customer lists, or customer-owned secrets should be used in the first pilot. |
| Audit logging | Documented and test-covered; dry-run evidence required | Audit events should contain operational metadata only, not raw briefs, customer names, generated report text, PII, secrets, or arbitrary user-supplied labels. |
| Retention/deletion | Documented; dry-run evidence required | Follow [Data Retention and Deletion](DATA_RETENTION_AND_DELETION.md) and record deletion owner, retention period, and dry-run result before customer data is accepted. |
| Demo artifacts | Documented; manual review required | Every screenshot, deck, export, or recording must pass [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md) before external sharing. |

## Remaining Blockers

These items block moving beyond internal demos and synthetic-data sales demos:

- Credential rotation evidence for any previously exposed or reused provider/API/graph credentials.
- Hosted pilot deployment controls, including HTTPS, restricted CORS/CSP, non-debug environment settings, and request-body logging disabled.
- Deployment-level rate limiting at edge, gateway, WAF, reverse proxy, or shared-store layer.
- Audit and retention/deletion dry-run execution with recorded operator, environment, synthetic scenario, and result.
- Manual screenshot, deck, export, and demo-recording review before sharing externally.
- No real customer data until a pilot agreement, data-handling rules, and retention/deletion owner are approved.

## Go / No-Go

| Use case | Decision | Conditions |
| --- | --- | --- |
| Internal local demo | Go | Use local/demo fixtures only, keep source labels visible, and avoid real customer data. |
| Customer sales demo | Go with synthetic/demo data only | Use approved synthetic briefs and artifacts, keep limitations visible, and avoid production-readiness or guaranteed-outcome claims. |
| Controlled paid pilot | Conditional go after blockers are cleared | Proceed only after CI, backend/frontend checks, hosted controls, credential evidence, dry run, audit review, retention/deletion ownership, and artifact review are complete. |
| Public SaaS | No-go | Public pilot, public internet exposure, and production customer deployment remain blocked. |

## Reviewed Documents

- [Customer Pilot Playbook](CUSTOMER_PILOT_PLAYBOOK.md)
- [Customer Data Handling](CUSTOMER_DATA_HANDLING.md)
- [Pilot Deployment Checklist](PILOT_DEPLOYMENT_CHECKLIST.md)
- [Pilot Deployment Dry Run Checklist](PILOT_DRY_RUN_CHECKLIST.md)
- [Pilot Operator Runbook](PILOT_OPERATOR_RUNBOOK.md)
- [Demo Artifact Checklist](DEMO_ARTIFACT_CHECKLIST.md)
- [Sample Strategy Pack Exports](SAMPLE_STRATEGY_PACK_EXPORTS.md)
- [Sales Demo Walkthrough](SALES_DEMO_WALKTHROUGH.md)
- [Sample Demo Briefs](SAMPLE_DEMO_BRIEFS.md)
- [Data Retention and Deletion](DATA_RETENTION_AND_DELETION.md)
- [Customer Demo Readiness Review](CUSTOMER_DEMO_READINESS_REVIEW.md)

## Claim-Safety Notes

The release-candidate package should continue to avoid claims of:

- production readiness,
- public pilot readiness,
- public internet readiness,
- guaranteed prediction,
- exact ROI or ROAS prediction,
- replacement for market research.

Outputs should remain framed as decision-support estimates, scenario-planning estimates, or directional planning inputs that require validation.
