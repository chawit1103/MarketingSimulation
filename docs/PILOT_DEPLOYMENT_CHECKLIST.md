# Pilot Deployment Checklist

Updated: 2026-05-17

This checklist is for a controlled private pilot deployment only. It does not make 3C Simulator production-ready, publicly safe, or suitable for production customer deployment.

## Readiness Statement

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

Outputs remain decision-support estimates, not guaranteed predictions.

## Pre-Deployment Gate

- [ ] Customer has approved a controlled private pilot scope.
- [ ] Pilot will use anonymized or approved campaign briefs only.
- [ ] No PII, raw CRM records, customer lists, provider secrets, or live social-listening/CRM integrations will be used.
- [ ] Source/provenance labels will remain visible in the UI, screenshots, exports, and decks.
- [ ] Manual rotation of any previously exposed provider/API/graph credentials is evidenced by the repo owner or deployment owner.

## TLS

- [ ] Serve the pilot over HTTPS only.
- [ ] Redirect HTTP to HTTPS at the proxy or hosting layer.
- [ ] Use a valid certificate for the pilot domain.
- [ ] Disable insecure legacy TLS versions where the hosting platform allows it.

## Secrets From Environment Variables

- [ ] Use environment variables or an approved secret manager for all secrets.
- [ ] Do not persist provider API keys, embedding API keys, graph passwords, auth secrets, or API credentials in local JSON settings files for a pilot deployment.
- [ ] Use `.env.production.example` only as a placeholder reference.
- [ ] Do not commit `.env`, `.env.*`, runtime settings files, uploads, generated reports, or provider credentials.
- [ ] Confirm `GET /api/settings` returns presence flags only and never raw secrets.

## Debug False

- [ ] Set `APP_ENV=production`.
- [ ] Set `FLASK_ENV=production`.
- [ ] Set `FLASK_DEBUG=false`.
- [ ] Set `REQUEST_BODY_LOGGING_ENABLED=false`.
- [ ] Disable browser/debug analytics unless explicitly approved.
- [ ] Confirm raw exception strings and tracebacks are not returned to users.

## CORS Restricted Origins

- [ ] Configure exact allowed HTTPS origins through environment variables.
- [ ] Set `CORS_ALLOWED_ORIGINS` to the approved frontend origin.
- [ ] Set `CONTENT_SECURITY_POLICY` and restrict `connect-src` to `'self'` plus the approved pilot API origin.
- [ ] Do not use wildcard CORS origins for any hosted pilot.
- [ ] Confirm preflight responses only allow the pilot frontend origin.
- [ ] Confirm cookies/tokens are not accepted from unapproved origins.

## Deployment-Level Rate Limiting

- [ ] Add edge, API gateway, WAF, reverse proxy, or shared-store rate limiting before exposing the pilot to users.
- [ ] Keep app-level in-memory rate limiting enabled as a secondary local safeguard.
- [ ] Set `RATE_LIMIT_ENABLED=true` and configure `RATE_LIMIT_WINDOW_SECONDS`.
- [ ] Configure supported app-level limits: `RATE_LIMIT_AUTH_PER_WINDOW`, `RATE_LIMIT_DEMO_PER_WINDOW`, `RATE_LIMIT_STATUS_PER_WINDOW`, `RATE_LIMIT_DECISION_PER_WINDOW`, and `RATE_LIMIT_SIMULATION_PER_WINDOW`.
- [ ] Apply stricter limits to auth, settings, status, simulation, decision, and demo-heavy endpoints.
- [ ] Trust `X-Forwarded-For` only from configured trusted proxies.
- [ ] Document the rate-limit owner and where limits are configured.

## Backup

- [ ] Define whether pilot data will be retained or deleted at exit.
- [ ] Back up only approved pilot artifacts.
- [ ] Do not back up secrets, raw `.env` files, private keys, raw PII, or disallowed customer data.
- [ ] Test restore for any retained non-sensitive pilot artifacts.
- [ ] Record backup location, retention period, and deletion owner.

## Monitoring

- [ ] Monitor backend availability.
- [ ] Monitor frontend availability.
- [ ] Monitor error rate without logging secrets or raw briefs.
- [ ] Monitor disk usage for uploads, reports, and logs.
- [ ] Monitor rate-limit events and suspicious auth attempts.
- [ ] Define an escalation contact for pilot incidents.

## Log Redaction

- [ ] Disable request-body logging by default.
- [ ] Redact passwords, API keys, tokens, secrets, graph passwords, and campaign brief text where logging exists.
- [ ] Do not log raw customer briefs, API keys, provider responses containing secrets, or auth tokens.
- [ ] Confirm logs do not include screenshots, generated decks, or uploaded customer files unless explicitly approved.
- [ ] Define log retention and deletion policy.

## Data Deletion Process

- [ ] Agree on pilot data retention before kickoff.
- [ ] Provide a deletion process for campaign briefs, simulation outputs, exports, uploads, logs, screenshots, and generated reports.
- [ ] Confirm deletion owner and timeline.
- [ ] Verify deletion after the pilot exit checklist is completed.
- [ ] Do not retain customer data by default.

## Admin/User Access Setup

- [ ] Create named admin accounts only for deployment operators.
- [ ] Create analyst accounts only for users who need to create/update campaigns, run simulations, or generate reports.
- [ ] Create viewer accounts for read-only participants.
- [ ] Do not share admin credentials.
- [ ] Confirm viewers cannot mutate campaigns, start simulations, update settings, generate API keys, or delete resources.
- [ ] Confirm analysts cannot update settings, generate API keys, or manage organizations.
- [ ] Disable or restrict org switching unless membership is explicitly verified.
- [ ] Remove pilot access at exit.

## Go/No-Go Before Invite

Invite pilot users only when all items below are true:

- [ ] HTTPS is working.
- [ ] Secrets come from environment variables or approved secret storage.
- [ ] Debug is disabled.
- [ ] CORS is restricted.
- [ ] Deployment-level rate limiting is configured.
- [ ] Logs are redacted.
- [ ] Backup and deletion processes are documented.
- [ ] Admin/user roles are configured.
- [ ] Customer data rules are accepted.

If any item is incomplete, keep the pilot local or internal-only.
