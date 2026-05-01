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
