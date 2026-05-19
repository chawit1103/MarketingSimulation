# PM2.5 Strategic Command Screenshot Guide

ใช้ guide นี้สำหรับเก็บภาพประกอบ PM2.5 Strategic Command demo package เท่านั้น ทุก screenshot ต้องใช้ demo/synthetic context และต้องไม่มีข้อมูลจริงของประชาชน พรรคการเมือง หน่วยงานภายใน หรือข้อมูลลับ

## Storage Path

เก็บ screenshot ไว้ที่:

`docs/screenshots/strategic-command/`

## Required Screenshots

| Filename | Route / Section | What Must Be Visible |
| --- | --- | --- |
| `strategic-command-desktop.png` | `/strategic-command` desktop | Hero, Strategic Command title, Thai headline, dashboard preview with Local Estimate |
| `strategic-command-mobile.png` | `/strategic-command` mobile | Thai headline, CTA buttons, no overflow or overlapping text |
| `strategic-command-output-package.png` | `/strategic-command#output-package` | Output Package cards, Executive Strategy Pack preview, Demo Mode, Synthetic Scenario, Decision-support estimate wording |
| `strategic-command-safety-boundaries.png` | Safety and Boundaries section | No PII, no voter list, no raw CRM, no political individual-level segmentation, no misinformation, no election forecast, no score/vote-effect estimate, human review required |
| `resources-strategic-command-section.png` | `/resources` Strategic Command section | Public Policy / Strategic Command section and PM2.5 Demo Package links |

## Capture Checklist

- [ ] No real personal data
- [ ] No voter list
- [ ] No raw CRM
- [ ] No party membership data
- [ ] No confidential government data
- [ ] No secrets, API keys, tokens, passwords, auth headers, or private browser UI
- [ ] Source/provenance labels are visible
- [ ] Safety boundaries are visible where relevant
- [ ] Screenshot supports Demo Mode / Synthetic Scenario only

## Suggested Manual Steps

1. Start frontend:

   ```bash
   cd frontend
   npm run dev -- --host 127.0.0.1 --port 5173
   ```

2. Capture desktop:

   Open `http://127.0.0.1:5173/strategic-command` at approximately 1440 x 1100 and save:

   `docs/screenshots/strategic-command/strategic-command-desktop.png`

3. Capture mobile:

   Use a 390 x 900 viewport and save:

   `docs/screenshots/strategic-command/strategic-command-mobile.png`

4. Capture Output Package:

   Open `http://127.0.0.1:5173/strategic-command#output-package` and save:

   `docs/screenshots/strategic-command/strategic-command-output-package.png`

5. Capture Safety Boundaries:

   Open the Safety and Boundaries section and save:

   `docs/screenshots/strategic-command/strategic-command-safety-boundaries.png`

6. Capture Resource Hub:

   Open `http://127.0.0.1:5173/resources`, scroll to Public Policy / Strategic Command, and save:

   `docs/screenshots/strategic-command/resources-strategic-command-section.png`

## Automation Note

If Playwright screenshot capture is available, generate the same five files automatically. If automation fails, this guide is sufficient for manual capture and the PR should not be blocked.
