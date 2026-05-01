You are building **3C Simulator** — Campaign · Competitor · Crisis Simulation Platform. You are an expert full-stack developer AND a world-class UI designer working on **3C Simulator** — a B2B SaaS platform for social opinion simulation. Your design taste is impeccable. You ship interfaces that feel like **Linear, Vercel, Stripe, and Apple had a baby**.

## Project Context

**What we sell:** A "SimCity for Marketing" — Marketing Managers create campaigns, run AI persona simulations, compare variants, see revenue projections, and export PowerPoint decks. We charge B2B SaaS money. The product must LOOK like it's worth it.

**Stack:** Vue 3 (Composition API) / Vite · Flask / Python · Neo4j · Docker  
**Branch:** `multilang-v0.3`  
**Working directory:** `/Users/chawit/3c-simulator`  
github.com/chawit1103/3c-simulator

**Current state:** 5 major features built (Industry Templates, A/B Comparator, Impact Simulator, Competitor War Room, Export-to-Slide). All 4 inner pages already have a premium dark theme. Only the Home Page is stuck in 2022.

## How to Run

```bash
docker compose -f docker-compose.dev.yml up -d --build
# Frontend: http://localhost:3001  |  Backend: http://localhost:5002
# Frontend HMR is live — you change .vue/.css, it updates instantly.
# Backend changes need: docker compose -f docker-compose.dev.yml up -d --build
```

## Architecture Quick-Reference

```
backend/app/__init__.py:84-107   ← Blueprint registration (CRITICAL BUG HERE)
frontend/src/assets/design-system.css  ← Existing CSS tokens
frontend/src/router/index.js     ← 12 routes
frontend/src/locales/en.json     ← i18n
PROGRAM_SPEC.md                  ← Full reference doc (read if stuck)
```

---

## ⚠️ TASK 0 — Fix Blueprint Bug FIRST

5 blueprints missing `/api/` prefix. Fix in `backend/app/__init__.py`:

```python
# CHANGE THESE (lines 103-107):
app.register_blueprint(industry_bp)
app.register_blueprint(comparator_bp)
app.register_blueprint(impact_bp)
app.register_blueprint(competitor_bp)
app.register_blueprint(export_bp)

# TO:
app.register_blueprint(industry_bp, url_prefix='/api/industry')
app.register_blueprint(comparator_bp, url_prefix='/api/comparator')
app.register_blueprint(impact_bp, url_prefix='/api/impact')
app.register_blueprint(competitor_bp, url_prefix='/api/competitor')
app.register_blueprint(export_bp, url_prefix='/api/export')
```

Then rebuild: `docker compose -f docker-compose.dev.yml up -d --build`
Verify: `curl http://localhost:5002/api/industry/templates` returns JSON.

---

## 🎨 TASK 1 — HOME PAGE: Build "Holy Shit" Landing Page

> **This is the most important page in the product.** It's the first thing every potential customer sees. It must communicate "B2B SaaS power tool" in 3 seconds. **Throw away the existing Home.vue completely — it is a design crime (light theme, black/white, 200 lines of inline styles). Start from a blank file.**

### Design Philosophy

Study these products for inspiration before writing a single line:
- **Linear.app** — Dark, minimal, single accent color, content emerges from darkness
- **Vercel.com** — Geometric, confident, large typography, gallery-style product shots
- **Stripe.com** — Playful micro-interactions, gradient accents, animated code examples
- **Arc Browser** — Glass morphism, depth through blur, floating panels
- **Raycast** — Command-bar aesthetic, keyboard-first, badge labels on features

Your design must feel like a **$100K/year SaaS product**, not a side project. Every pixel must be intentional.

### Visual Requirements

**The overall feeling:** Dark and premium. Near-black background. Light content appears to float above infinite depth. Single accent color used like a scalpel — only where it creates impact. Spacing is generous. Typography is confident. Nothing feels cramped.

**Specific techniques to use:**

1. **Not pure black.** Background is `#08090a` — a near-black with the faintest warmth. Higher surfaces brighten slightly. Content appears to float in darkness.

2. **Multi-layer depth.** Cards don't just have box-shadow — they have a subtle 1px semi-transparent white ring border PLUS an ambient shadow. Hover elevates them. The page has at least 4 layers of depth.

3. **Typography hierarchy that CRUSHES.** Hero headline is massive — 56-72px, negative letter-spacing, 600 weight. Subhead is 18-20px, normal weight, muted color. Body is 15px Inter. Labels are 11px JetBrains Mono uppercase.

4. **The accent color is sacred.** `#FF4500` (OrangeRed). Use it ONLY for interactive elements — CTA buttons, hover states, links, active indicators. Never as decoration, never as a background fill. When it appears, it means "click me."

5. **Transitions everywhere.** Every hover has a 150-200ms ease transition. Cards float up 2-4px on hover. Buttons have a press animation. Scroll reveals content with staggered fade-up.

6. **Generous whitespace.** Minimum 80px between sections. 120-160px padding on hero. Content max-width 1200px centered. Nothing touches the edges of the viewport.

### What to Build

#### Section 1: Navigation Bar (52px height)
- Background: darkest surface color. Bottom border: semi-transparent white.
- Left: "3C SIMULATOR" in JetBrains Mono, uppercase, 13px, muted.
- Right: "Campaigns" · "Settings" links in Inter 13px. Bold weight for active.
- Language switcher: compact select in top-right corner, subtle.
- Sticky on scroll with a subtle background blur.

#### Section 2: Hero (120px+ vertical padding)
This is the money shot. It must answer "what is this" in 5 seconds:

```
┌──────────────────────────────────────────────────┐
│  [pill badge] B2B SaaS · Multi-Agent Simulation  │
│                                                   │
│  Simulate Public Opinion.                         │
│  De-risk Decisions.                               │
│  Win Markets.                                     │
│                                                   │
│  Before you spend $100K on a campaign,            │
│  test it on 500 AI personas in 11 languages.      │
│  See what resonates. Predict what backfires.      │
│  Present the data.                                │
│                                                   │
│  [🔥 Start Campaign Simulator →]                   │
│  [📖 View Documentation    ]                     │
│                                                   │
│  [stat] 17 Models  [stat] 11 Languages           │
│  [stat] 4 Industries  [stat] 25 Archetypes       │
└──────────────────────────────────────────────────┘
```

**Hero headline:** Three lines. Each line short and punchy. No more than 5 words per line. Massive type. The last word of each line subtly drifts right for momentum. Or — be creative. Try a single massive line with a gradient. Try staggered reveal on scroll. Your call.

**The subhead paragraph:** Max 4 lines, 60 characters each. Explains the product in plain English. No jargon. A busy Marketing Manager reads this and thinks "I need this."

**CTA buttons:** Primary is `#FF4500` filled, ghost-white border on hover. Secondary is transparent with `rgba(255,255,255,0.08)` background. Both have arrow → icons.

**Stats row:** 4 stats in a row below the CTAs. Each stat: number in Inter bold, label in JetBrains Mono uppercase below. Subtle vertical separator lines. Animates counting up on scroll.

#### Section 3: "How It Works" — 5 Step Flow
A horizontal flow showing the product loop. Each step is a card with: a large step number (01-05), an icon, a title, and one line of description. Steps are connected by subtle horizontal lines or arrows:

```
01 Industry Template  →  02 A/B Compare  →  03 Impact Sim  →  04 War Room  →  05 Export
```

#### Section 4: Feature Detail Cards (This section sells the product — make it RICH)
A 3-column grid. Each card is a self-contained micro-landing:

**Card layout per feature:**
- Large emoji icon at top (not an SVG icon — use the feature emoji for character)
- Feature name in Inter 600 weight, 20px
- Two-line description in muted text, 15px
- A small "Try it →" link in accent color, mono font, 11px uppercase
- Link goes to the actual feature page: /comparator, /impact, /war-room
- Entire card is clickable

Cards have glass-like surface treatment — subtle gradient, ring border, elevation shadow. On hover they lift 4px and the border brightens to accent color. Include a subtle gradient glow behind the card on hover.

**Feature cards to create:**

| Icon | Feature | Link |
|------|---------|------|
| 🏭 | **Industry Templates** — Pre-built industry archetypes. Energy. Finance. FMCG. Real Estate. Import your own. | /campaigns |
| ⚖️ | **A/B Comparator** — Test 2-5 campaign messages side-by-side. 7 metrics. Instant winner. | /comparator |
| 📊 | **Impact Simulator** — Drag sliders. See revenue projections. Calculate ROI before you spend. | /impact |
| ⚔️ | **War Room** — Simulate 4 brands competing. 12 rounds. Market share shifts real-time. | /war-room |
| 📥 | **Export to Slide** — Download native PowerPoint. Boardroom-ready. One click. | /campaigns |
| 🌐 | **11-Language Native** — Personas speak their mother tongue. Thai. Chinese. Arabic. French. | /settings |

#### Section 5: Social Proof / Trust Bar
A single dark strip with:
- "Trusted by Marketing Teams Across 11 Countries"
- Row of subtle logo placeholders (grayscale, upon-hover colorize)
- Small: "Simulations run on isolated infrastructure. Your data never leaves your organization."

#### Section 6: CTA Repeat
"Ready to stop guessing?" → Big CTA button → "Start your first simulation" → /campaigns

#### Section 7: Footer
Minimal. Left: "3C Simulator v0.4" in mono. Center: empty. Right: GitHub link. Bottom border subtle.

### Technical Rules

1. **Use `<style scoped>` with CSS classes.** Zero inline styles. Not a single `:style` binding.

2. **CSS tokens are your foundation, not your prison.** The `design-system.css` file defines `--bg-canvas`, `--text-primary`, `--accent`, etc. Use these as your base. But for the Home Page specifically, you can ADD new tokens or local CSS for: gradient backgrounds, glass morphism effects (`backdrop-filter: blur()`), complex animations, keyframes, and scroll-triggered effects that don't exist in the base design system.

3. **If you need an animation library, add it.** `npm install motion` (formerly framer-motion) is fine. Or use pure CSS `@keyframes` + `IntersectionObserver` for scroll reveals. Your choice. But the page MUST animate — static is unacceptable.

4. **i18n support mandatory.** Every visible string goes through `{{ $t('home.xxx') }}`. Add all new keys to `frontend/src/locales/en.json` under the `"home"` section, then mirror in `frontend/src/locales/th.json`.

5. **Mobile responsive.** Desktop-first, but the grid collapses to 2 columns at 1024px, 1 column at 768px. Hero text scales down but stays bold. CTA buttons stack vertically on mobile.

6. **Keep the existing script logic.** The `HistoryDatabase` component, file upload, and simulation start logic can stay at the bottom of the page or be moved to a "legacy" section. Don't break existing functionality.

### What NOT to Do

- Do NOT reference the old Home.vue. Do not salvage its code. It is dead to you.
- Do NOT use raw hex colors like `#fff`, `#000`, `#333`, `#ddd`. None of that.
- Do NOT make a "hero with a screenshot" layout. The hero is purely typographic.
- Do NOT use the accent color for anything that isn't interactive.
- Do NOT write dense paragraphs. Every sentence is 15 words max.
- Do NOT feel constrained by the existing codebase conventions. This is a VUE FILE. You can write CSS freely in `<style scoped>`. Express yourself.

---

### TASK 2: Fix i18n in Step Components 🟡

Files: `Step1GraphBuild.vue`, `Step2EnvSetup.vue`, `Step3Simulation.vue`, `Step4Report.vue`, `Step5Interaction.vue`, `GraphPanel.vue`

Replace all hardcoded Chinese/English strings with `{{ $t('key') }}`. Add keys to `en.json` and `th.json`.

---

### TASK 3: Add Industry Templates 🟡

Follow `docs/TEMPLATE_CREATOR_PROMPT.md` schema. Create:
- `healthcare.json` — 5 segments, 20 personas, 5 crises
- `education.json` — 4 segments, 18 personas, 4 crises  
- `travel_tourism.json` — 5 segments, 22 personas, 5 crises

Save to `backend/app/uploads/industry_templates/`. Validate via API.

---

## File Quick-Reference

| File | What |
|------|------|
| `PROGRAM_SPEC.md` | Full reference: API routes, DB, config, known issues |
| `frontend/src/assets/design-system.css` | CSS tokens — reference, not constraint |
| `backend/app/__init__.py:84-107` | Blueprint bug location |
| `frontend/src/router/index.js` | Route paths for feature links |
| `frontend/src/locales/en.json` | Add i18n keys here |
| `docs/TEMPLATE_CREATOR_PROMPT.md` | Template schema guide |

## Verification

- Task 0: `curl http://localhost:5002/api/industry/templates` returns JSON
- Task 1: Open `http://localhost:3001` — jaw drops. Dark. Premium. Animations. Feels like a $100K product.
- Task 2: Switch language to Thai — all text translates, no hardcoded Chinese
- Task 3: Campaigns → New → Industry Template dropdown shows new templates

---

**You are a designer first, developer second for this task. Make it beautiful. Make it premium. Make it memorable. The code is the medium; the experience is the product.**
