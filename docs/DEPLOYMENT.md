# Deployment Notes

Updated: 2026-05-01

This project is ready for local demo usage and conditionally ready for controlled private pilots. It is not yet ready for public internet exposure or production customer deployment without the remaining release-readiness work in `docs/RELEASE_READINESS_CHECKLIST.md`.

## Secret Handling

Real secrets must never be committed to Git or included in docs, screenshots, logs, test fixtures, or issue comments.

Production mode uses environment variables for runtime secrets. The local `settings.json` file stores non-secret runtime preferences only in production. Provider API keys, embedding API keys, and graph passwords are written as blank fields even if `SETTINGS_PERSIST_SECRETS=true` is configured by mistake.

Local/demo mode may persist provider secrets to `settings.json` only when `SETTINGS_PERSIST_SECRETS=true`. This is for single-developer/local workflows, not shared production deployments.

## Required Production Environment Variables

Set these values in the deployment environment or a managed secret store:

- `APP_ENV=production`
- `SECRET_KEY`
- `AUTH_SECRET_KEY`
- `CORS_ALLOWED_ORIGINS`
- `LLM_API_KEY`, when using a cloud LLM provider
- `EMBEDDING_API_KEY`, when using a cloud embedding provider
- `NEO4J_PASSWORD`, when using Neo4j

Optional provider/config values:

- `LLM_PROVIDER`
- `LLM_MODEL_NAME`
- `LLM_BASE_URL`
- `EMBEDDING_PROVIDER`
- `EMBEDDING_MODEL`
- `EMBEDDING_BASE_URL`
- `NEO4J_URI`
- `NEO4J_USER`
- `SETTINGS_PERSIST_SECRETS=false`
- `RATE_LIMIT_TRUSTED_PROXIES`, only if the app runs behind trusted proxies that overwrite forwarding headers

Do not use placeholder, demo, or previously committed values for production.

## CORS

Local development keeps browser testing easy. Production is stricter: startup fails unless `CORS_ALLOWED_ORIGINS` is set to explicit trusted origins.

Example:

```bash
CORS_ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com
```

Do not use `*` for production API routes.

## Rate Limiting

The bundled limiter is dependency-free and suitable for local/demo protection. It is still in-memory and per-process, so it is not enough by itself for public internet exposure or multi-worker production deployments.

Production deployments should add edge/API-gateway or shared-store rate limiting. If traffic reaches Flask through a proxy, set `RATE_LIMIT_TRUSTED_PROXIES` only to proxies that overwrite inbound forwarding headers.

Examples:

```bash
RATE_LIMIT_TRUSTED_PROXIES=127.0.0.1
RATE_LIMIT_TRUSTED_PROXIES=10.0.0.0/8,192.168.0.0/16
```

When `RATE_LIMIT_TRUSTED_PROXIES` is empty, `X-Forwarded-For` is ignored and the limiter keys by the direct remote address.

## API Key Transport

Authenticated API requests must send credentials through one of these headers:

- `Authorization: Bearer <token>`
- `X-Api-Key: <api-key>`

Query-parameter credentials such as `?api_key=...` are not accepted.

## Browser Auth Storage And Security Headers

The frontend now stores browser auth tokens in `sessionStorage`, not persistent `localStorage`. On load, legacy `3c-auth-token` values are migrated into `sessionStorage` and removed from `localStorage`; legacy `3c-api-key` values are removed from `localStorage` and are not persisted for normal UI sessions.

This reduces persistence risk, but it is not a complete production auth hardening. Session storage is still readable by JavaScript if an XSS vulnerability exists. Before customer production deployment, prefer secure HttpOnly cookies, a short-lived access-token plus refresh-token flow, or an equivalent hardened browser-auth strategy.

The Flask app emits these browser hardening headers by default:

- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `X-Frame-Options: DENY`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

Deployment operators can override the CSP with `CONTENT_SECURITY_POLICY` or disable these headers with `SECURITY_HEADERS_ENABLED=false` for troubleshooting. If the frontend is served by a CDN, reverse proxy, or static host rather than Flask, configure equivalent headers there too.

Production token lifetime defaults to 8 hours and can be changed with `AUTH_TOKEN_EXPIRY_SECONDS`. Local/demo mode keeps the historical 24-hour default unless overridden.

## Manual Credential Rotation

Repository secret hygiene has been improved, but the repository cannot prove whether historical provider/API/graph credentials were real or whether they have been rotated.

The repository owner must manually rotate any credentials that may have been committed before the secret-hygiene remediation. Do not mark SEC-001 complete until that external rotation is done and recorded outside this repository.

## Runtime Settings Behavior

In production:

- `GET /api/settings` returns only presence flags such as `api_key_present` and `password_present`.
- `PUT /api/settings` can update non-secret settings such as provider, model, base URL, language, and graph URI.
- Blank values and masked placeholders do not erase existing runtime secrets.
- New secret values sent from the browser are not persisted to `settings.json`.
- Effective provider secrets come from environment variables.

In local/demo mode:

- Demo mode works without provider API keys.
- Local model settings can be saved for convenience.
- Local file settings use restrictive permissions where supported.

## Public Exposure Gate

Before public internet exposure, complete or explicitly risk-accept:

- manual credential rotation for any historical committed secrets,
- full RBAC/org-switching policy for production users,
- edge/API-gateway or shared-store rate limiting,
- safer browser auth storage strategy,
- deployment logging, backup, retention, and deletion policies,
- review of legacy local JSON records without `org_id`.

PR T verification keeps public internet exposure as a no-go. Local demo is acceptable with synthetic data. Controlled private pilot is conditional and should not proceed until credential rotation is evidenced and the deployment owner has added the required operational controls.
