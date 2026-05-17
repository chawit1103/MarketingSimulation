# Testing

Updated: 2026-05-17

This repo has backend contract/smoke tests, a frontend production build check, and Playwright smoke tests for the main user journeys.

## Backend Tests

Run from the repo root:

```bash
backend/.venv/bin/python -m pytest backend/tests
```

These tests avoid live LLM/provider calls and cover public route contracts, security controls, brief quality scoring, settings readiness, competitor scenarios, and action plan generation.

Focused RBAC/security checks:

```bash
backend/.venv/bin/python -m pytest backend/tests/test_rbac.py
```

This covers unauthenticated auth-route denial, viewer read-only behavior, analyst restrictions for settings/API-key/provider live-test flows, admin-positive privileged flows, and safe org-switch disablement without cross-org token issuance.

## Frontend Build

Run from the repo root:

```bash
cd frontend
npm run build
```

## Frontend Quality Gate

Run from the repo root:

```bash
cd frontend
npm run lint
npm run typecheck
npm run test:unit
npm run test:analytics
```

Or run the combined quality gate:

```bash
cd frontend
npm run test:frontend
```

The unit tests use Vitest, Vue Test Utils, and mocked API modules. They do not require:

- a running Flask backend,
- paid API keys,
- live LLM providers,
- Neo4j,
- real customer data.

Current unit coverage verifies:

- `ResultSourceBadge` labels for Demo Mode, Local Estimate, Live Backend, Backend Verified, and Unknown Source.
- Settings secret presence display using `api_key_present` / `password_present` flags without rendering raw secrets.
- Comparator demo/backend result labels and explicit Local Estimate fallback.
- Budget Planner disclaimer wording for assumption-based planning, not exact ROI/ROAS prediction.
- Calibration privacy warnings for aggregate-only actuals.
- Strategy Pack source/provenance formatting for slide footer and validation-summary rendering.
- Customer pilot readiness copy for controlled-pilot language without production-readiness claims.

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

## CI

GitHub Actions runs the same release-safe checks on pull requests and pushes to main release branches plus `codex/**` branches:

- `Secret Hygiene`: scans committed files for common API-key/private-key patterns.
- `Backend Tests`: installs `backend` with dev dependencies and runs `python -m pytest tests`.
- `Frontend Build`: runs `npm ci` and `npm run build`.
- `Frontend Quality`: runs `npm run test:frontend`, which includes lint, typecheck, Vitest unit tests, and analytics tests.
- `E2E Smoke`: installs Chromium and runs the mocked Playwright smoke suite.

CI uses dummy test-mode environment values for LLM, embedding, and Neo4j settings. It must not require real provider keys, Neo4j cloud credentials, paid services, or live model calls.

## Current Gaps

- Frontend lint is intentionally lightweight and currently functions as a parse/configuration gate rather than a style-enforcement pass.
- E2E tests use mocked API fixtures, so they complement but do not replace backend contract tests.
- Manual screenshot review remains useful before public demos.
