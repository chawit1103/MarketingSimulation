# MarketingSimulation Agent Guide

This repository is a marketing decision-intelligence product with public demo flows, tenant-aware backend APIs, synthetic simulation outputs, and source-labeled fallback modes. Future Codex work should optimize for release safety, reviewability, and user trust.

## Non-Negotiable Product Safety Rules

- Do not expose secrets, API keys, provider tokens, passwords, auth headers, or graph credentials in logs, browser responses, screenshots, docs, or test fixtures.
- Do not return raw tracebacks, stack traces, internal file paths, or provider exception dumps to clients. Keep detailed errors in server logs and sanitize API responses.
- Clearly label result provenance everywhere users see simulation or recommendation output:
  - Demo Mode
  - Local Estimate
  - Live Backend
  - Backend Verified
  - Unknown Source
- Do not fabricate live simulation results. Demo fixtures and local estimates are allowed only when visibly labeled and documented as deterministic/synthetic.
- Treat auth, tenant isolation, fallback transparency, and data privacy regressions as high-priority issues in code review.
- Keep PRs focused and reviewable. Avoid bundling unrelated product features, refactors, migrations, providers, or design rewrites into release-readiness/security/docs PRs.

## Engineering Expectations

- Add or update tests for changed backend routes and critical frontend flows.
- Route changes must keep frontend API helpers and Flask blueprint routes aligned.
- Public/demo endpoints must remain rate-limited and must not require live LLM or network calls in automated tests.
- Preserve local/demo development behavior unless the task explicitly asks to remove it.
- Preserve i18n behavior where practical when changing user-facing UI text.
- If adding screenshots or demo docs, use synthetic/demo data only and confirm source labels are visible where relevant.
- If changing export, dashboard, comparator, War Room, decision, or settings flows, verify that result-source metadata is preserved.

## Code Review Priorities

Flag these as high severity:

- Any client-facing raw traceback or secret leak.
- Any fallback output that appears to be live/backend-verified when it is actually demo or local estimate data.
- Any auth bypass or tenant data isolation issue.
- Any route mismatch between frontend API calls and backend routes.
- Any test that makes live LLM/provider/network calls.
- Any docs or UI copy that claims guaranteed prediction accuracy, calibrated market-share forecasting, or real-world outcome certainty.

## Recommended Validation

- Backend: `backend/.venv/bin/python -m pytest backend/tests`
- Frontend build: `cd frontend && npm run build`
- Locale JSON: `python3 -m json.tool frontend/src/locales/en.json` and `frontend/src/locales/th.json`
- Diff hygiene: `git diff --check`
- If frontend source changes, manually inspect the affected flow or capture an updated screenshot when practical.

## Current Product Boundaries

- This is ready for controlled demos and pilot discovery, not guaranteed market prediction.
- Decision Engine, War Room, Action Plan, and KPI outputs remain deterministic guidance until calibrated with real campaign outcomes.
- Browser-side local fallback exists for demo continuity only and must remain explicit.
- Production still needs edge/shared rate limiting, observability, backup, CI gates, deployment runbooks, and calibration.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **MiroFish-Offline** (6353 symbols, 10065 relationships, 192 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/MiroFish-Offline/context` | Codebase overview, check index freshness |
| `gitnexus://repo/MiroFish-Offline/clusters` | All functional areas |
| `gitnexus://repo/MiroFish-Offline/processes` | All execution flows |
| `gitnexus://repo/MiroFish-Offline/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
