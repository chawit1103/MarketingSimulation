# PM2.5 Canva Design Guide

Purpose: Design guide for creating a Thai-first Canva presentation from the Strategic Command PM2.5 demo package.

## Recommended Format

- Format: 16:9 presentation
- Suggested length: 7 slides
- Use as a meeting deck, follow-up deck, or exported image sequence
- Do not create binary PPTX/PDF/video files in this repo

## Visual Style

- Executive policy briefing
- Navy / blue / white base
- Clean dashboard-like panels
- Evidence-led, restrained, and readable
- Not playful, not agency/consumer marketing style
- Avoid dramatic disaster imagery or partisan campaign visuals

## Canva Thai Fonts

Recommended Canva fonts:

- Anuphan
- Sarabun
- IBM Plex Sans Thai
- Noto Sans Thai

Suggested usage:

- Headline: Anuphan SemiBold or IBM Plex Sans Thai Bold
- Body: Sarabun or Noto Sans Thai
- Footer/provenance: IBM Plex Sans Thai or Noto Sans Thai, small but visible

## Suggested Colors

| Role | Color Direction | Usage |
| --- | --- | --- |
| Navy background | Deep navy / blue-black | Cover, CTA, executive framing |
| White text | White / near-white | Main title and high-contrast copy |
| Cyan/blue accents | Cyan or medium blue | Workflow arrows, section labels, proof highlights |
| Amber risk | Amber / gold | Risk cards, caution notes, open questions |
| Red crisis | Muted red only | Crisis warning or high-severity watchout |

Avoid a one-color blue page. Use white space, amber risk tags, and small cyan accents to keep the deck scannable.

## Screenshot Source

Use screenshots from:

`docs/screenshots/strategic-command/`

Available screenshots:

- `strategic-command-desktop.png`
- `strategic-command-mobile.png`
- `strategic-command-output-package.png`
- `strategic-command-safety-boundaries.png`
- `resources-strategic-command-section.png`

## Suggested Screenshot Layouts

### Desktop Screenshot

Use on Slide 1 or Slide 3.

- Crop to show Strategic Command title, Thai headline, and dashboard preview
- Keep `Local Estimate` visible if possible
- Place title text on the left or use screenshot as right-side visual

### Mobile Screenshot

Use as a small device mockup on Slide 3 or appendix.

- Show Thai headline and CTA buttons
- Do not stretch; use phone-frame crop

### Output Package Screenshot

Use on Slide 4 or Slide 6.

- Show Output Package cards
- Show Executive Strategy Pack preview
- Keep `Demo Mode`, `Synthetic Scenario`, and decision-support wording visible

### Safety Boundaries Screenshot

Use on Slide 7 or appendix.

- Show the safety boundary cards
- Ensure no PII, no voter list, no raw CRM, election/vote-impact exclusions, and human review are visible

### Resource Hub Screenshot

Use in follow-up or appendix.

- Show Public Policy / Strategic Command section
- Show PM2.5 demo package links

## Footer / Provenance Rule

Every slide with simulated output, scenario data, synthetic persona analysis, risk brief, message revision, response playbook, recommendation, or next-step CTA must include a visible provenance footer.

Required footer:

`Demo Mode | Synthetic Scenario | Decision-Support Estimate`

For CTA or safety-heavy slides, add:

`Not election prediction | Not vote impact | Not public sentiment guarantee`

For recommendation-heavy slides, use:

`Not election prediction | Not vote impact | Human review required`

Do not crop, cover, recolor into low contrast, or hide the provenance footer in slide exports, social crops, thumbnails, video exports, or follow-up images.

## Content Rules

- Use only user-provided PM2.5 scenario details
- Mark any inference as assumption, operator note, or decision-support estimate
- Do not use real political party data
- Do not use confidential government data
- Do not use PII, voter lists, raw CRM, party membership data, secrets, or private screenshots
- Do not claim production readiness
- Do not claim exact public reaction, election outcome, or vote impact
- Do not remove provenance footers when adapting the deck for social/video formats

## Export Guidance

If exporting from Canva:

- Use PNG for individual slide previews
- Use PDF only outside the repo if needed for a meeting
- Check each exported slide/video crop to confirm provenance footer remains visible
- Do not commit Canva exports, PPTX, PDF, or video files unless explicitly approved in a future task
