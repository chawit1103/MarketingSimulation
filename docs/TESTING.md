# Testing

Updated: 2026-05-01

This repo has backend contract/smoke tests, a frontend production build check, and Playwright smoke tests for the main user journeys.

## Backend Tests

Run from the repo root:

```bash
backend/.venv/bin/python -m pytest backend/tests
```

These tests avoid live LLM/provider calls and cover public route contracts, security controls, brief quality scoring, settings readiness, competitor scenarios, and action plan generation.

## Frontend Build

Run from the repo root:

```bash
cd frontend
npm run build
```

## E2E Smoke Tests

The Playwright smoke tests live in `frontend/e2e/smoke.spec.js`.

Install dependencies:

```bash
cd frontend
npm install
npx playwright install chromium
```

Run:

```bash
cd frontend
npm run test:e2e
```

The e2e tests start the Vite dev server automatically and mock `/api/*` responses in-browser. They do not require:

- a running Flask backend,
- paid API keys,
- live LLM providers,
- Neo4j,
- external network calls from the app.

## Smoke Coverage

Current e2e coverage verifies visible UI states for:

- Home page entry points.
- Demo dashboard with `Demo Mode`.
- Dashboard route with `Backend Verified`.
- Action Plan source inheritance.
- Brief Quality Score.
- War Room with `Live Backend`.
- War Room explicit `Local Estimate` fallback.
- Settings Wizard demo readiness.

These tests intentionally avoid pixel-perfect assertions. They check user-visible labels and high-value decision surfaces instead.

## Current Gaps

- No frontend unit/component test runner is configured yet.
- No lint/typecheck script is configured yet.
- E2E tests use mocked API fixtures, so they complement but do not replace backend contract tests.
- Manual screenshot review remains useful before public demos.
