# Screenshot Guide

Updated: 2026-05-01

Curated screenshots already live in `docs/screenshots/`, but capture is not fully automated. Use this guide when refreshing README/demo images.

## Safety Rules

- Use only synthetic demo data or approved non-confidential briefs.
- Keep Demo Mode, Local Estimate, Live Backend, or Backend Verified labels visible when a result is shown.
- Do not show API keys, passwords, auth tokens, customer names, private campaign data, browser password managers, or private tabs.
- Do not crop away warnings or limitations that explain source mode.
- Prefer stable 1440px desktop screenshots unless a mobile issue is being documented.

## Recommended Local Setup

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

Open:

```text
http://127.0.0.1:5174
```

Set language to English and theme to Dark unless the screenshot is specifically showing light/system theme behavior.

## Screenshot Checklist

Capture or refresh these files:

| Flow | Route | File |
|---|---|---|
| Home / landing page | `/` | `docs/screenshots/home-landing.png` |
| Demo dashboard | `/dashboard/demo-premium-water` | `docs/screenshots/demo-dashboard-overview.png` |
| Brief Quality Score | `/campaigns` then New Campaign | `docs/screenshots/brief-quality-score.png` |
| Simulation dashboard KPIs | `/dashboard/demo-premium-water` | `docs/screenshots/simulation-dashboard-kpis.png` |
| War Room | `/war-room` | `docs/screenshots/war-room.png` |
| Action Plan | `/dashboard/demo-premium-water` | `docs/screenshots/action-plan.png` |
| Settings Wizard | `/settings` | `docs/screenshots/settings-wizard.png` |

## Capture Notes

- For Brief Quality Score, use a sample brief from [DEMO_DATA.md](DEMO_DATA.md).
- For War Room, confirm the source badge is visible. If backend simulation is unavailable and you choose fallback, the screenshot must show `Local Estimate`.
- For Action Plan, include the source badge and at least one recommendation card.
- For Settings Wizard, use Demo only mode or safe dummy provider fields. Do not show real keys.

## Review Before Commit

Before committing screenshots:

1. Open each image and confirm no private data or secrets are visible.
2. Confirm the image is useful for docs, not a transient test artifact.
3. Keep file sizes reasonable.
4. Update README image links only if filenames changed.
