# Contributing

Updated: 2026-05-01

MarketingSimulation is a product-trust-sensitive decision simulator. Keep changes focused, testable, and explicit about result provenance.

## Pull Request Expectations

- Keep PRs small enough to review in one pass.
- Do not commit secrets, API keys, provider tokens, passwords, auth headers, customer data, or real campaign data.
- Do not expose raw tracebacks or internal file paths to clients.
- Clearly label simulation and recommendation output as `Demo Mode`, `Local Estimate`, `Live Backend`, `Backend Verified`, or `Unknown Source`.
- Do not fabricate live simulation results. Demo fixtures and local estimates must stay visibly labeled.
- Add or update tests for changed backend routes and critical frontend journeys.

## Secret Hygiene

Real secrets must never be committed. Keep local provider keys, graph
passwords, auth secrets, customer data, runtime settings, uploads, and generated
reports out of Git.

For local development:

```bash
cp .env.dev.example .env.dev
```

Then edit `.env.dev` locally. Do not commit it. If any real provider/API/graph
credential was previously committed, rotate it manually in the provider console
or Neo4j environment. Removing it from Git does not revoke the credential.

CI blocks tracked local `.env*` files except `.env.example` and
`.env.dev.example`, and scans for common provider-key patterns.

Runtime Settings API responses must never return raw or masked secrets. Use
presence flags such as `api_key_present` and `password_present` so the browser
can display whether a credential exists without receiving it. Blank fields or
masked placeholders from the browser should preserve existing stored secrets;
explicit clear behavior must be opt-in and tested.

Local/demo runtime settings may still be stored in `backend/uploads/settings.json`
for developer convenience. Production deployments should provide provider keys,
graph credentials, and auth secrets through environment variables or a managed
secret store rather than relying on plaintext runtime files.

## Local Validation

Run the checks that match your change:

```bash
backend/.venv/bin/python -m pytest backend/tests
```

```bash
cd frontend
npm run build
npm run test:e2e
```

The e2e tests use mocked API responses. They should not require live LLM providers, Neo4j cloud credentials, paid APIs, or real API keys.

## CI

GitHub Actions runs:

- secret hygiene scan,
- backend contract/smoke tests,
- frontend build,
- mocked Playwright e2e smoke tests.

CI sets safe dummy values for provider and graph settings. If a test requires a real API key or live external service, it should be redesigned as a mocked contract/smoke test or documented as a manual check outside the default PR gate.

## Security And Privacy Review

Treat these as high-priority regressions:

- auth or tenant isolation bypass,
- client-facing secrets or raw tracebacks,
- unlabeled fallback/demo/local results,
- tests or CI that call live LLM/network providers,
- screenshots or docs that include private customer data.

When in doubt, prefer a visible `Unknown Source` or `Local Estimate` label over implying backend verification.
