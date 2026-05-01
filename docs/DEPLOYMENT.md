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

Do not use placeholder, demo, or previously committed values for production.

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
