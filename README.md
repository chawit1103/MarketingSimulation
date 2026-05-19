<div align="center">

<img src="./static/image/image.png" alt="3C Simulator" width="30%"/>

# 3C Simulator

**Decision Intelligence Platform for Campaign, Competitor, and Crisis Simulation**

Simulate public opinion before spending real budget. Test campaign messages, competitor moves, and crisis scenarios against synthetic consumer personas, then turn the result into executive-ready evidence.

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue?style=flat-square)](./LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://python.org)
[![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org)
[![OASIS](https://img.shields.io/badge/Simulation-OASIS-orange?style=flat-square)](https://github.com/camel-ai/oasis)

</div>

---

## What It Is

3C Simulator is a B2B SaaS-style platform for marketing managers, PR agencies, strategy teams, and crisis response teams.

It works like a **flight simulator for market decisions**:

1. Define a campaign, audience, channel mix, competitor move, or crisis scenario.
2. Generate culturally grounded synthetic personas.
3. Run multi-agent social simulation through OASIS-style behavior models.
4. Review KPIs, segment reactions, risk drivers, assumptions, and simulated quotes.
5. Export the evidence into a boardroom-ready slide deck or client-ready strategy pack.

This is not positioned as an AI playground. It is a decision-support system for answering:

- Which message should we launch?
- Which segment will resist?
- What risk could become a crisis?
- How should we revise the campaign before spending real media budget?
- What should we show leadership or a client?

## Who It Is For

### Marketing Manager / Brand Team

Use 3C Simulator to pressure-test a launch, campaign, competitor move, or crisis-sensitive message before real spend. The recommended brand flow is:

1. Start with a safe demo or approved brief.
2. Check Brief Quality Score before simulation.
3. Review Dashboard evidence, Confidence & Evidence, and source labels.
4. Use Action Plan and Revised Brief v2 to decide what to change.
5. Use Budget Planner and Calibration v1 as directional planning inputs, not guaranteed forecasts.
6. Export a Brand Executive Summary for leadership review.

### Marketing Agency / Strategy Team

Use 3C Simulator to compare creative directions and turn scenario evidence into a client-ready recommendation. The recommended agency flow is:

1. Open the Demo Dashboard to establish source-labeling and evidence rules.
2. Compare 2-5 campaign directions in A/B/C Comparator.
3. Stress-test competitor or crisis reactions in War Room.
4. Package the recommendation as an Agency Client Pitch Summary.
5. Use pilot feedback analytics to learn where clients trust, doubt, or need more proof.

For the current production/demo readiness matrix, see [docs/STATUS.md](docs/STATUS.md).

Current release readiness:

| Path | Status |
| --- | --- |
| Local demo | Ready |
| Controlled private pilot | Conditional candidate |
| Public pilot | Blocked |
| Public internet exposure | Blocked |
| Production customer deployment | Blocked |

For demo, release validation, known limitations, and recommended next actions, see:

- [docs/CUSTOMER_PILOT_PLAYBOOK.md](docs/CUSTOMER_PILOT_PLAYBOOK.md)
- [docs/CUSTOMER_DATA_HANDLING.md](docs/CUSTOMER_DATA_HANDLING.md)
- [docs/PILOT_DISCOVERY_QUESTIONS.md](docs/PILOT_DISCOVERY_QUESTIONS.md)
- [docs/PILOT_SUCCESS_CRITERIA.md](docs/PILOT_SUCCESS_CRITERIA.md)
- [docs/SAMPLE_PILOT_SOW.md](docs/SAMPLE_PILOT_SOW.md)
- [docs/PILOT_PRICING_PACKAGES.md](docs/PILOT_PRICING_PACKAGES.md)
- [docs/PILOT_ONBOARDING_GUIDE.md](docs/PILOT_ONBOARDING_GUIDE.md)
- [docs/PILOT_EXIT_CHECKLIST.md](docs/PILOT_EXIT_CHECKLIST.md)
- [docs/PILOT_DRY_RUN_CHECKLIST.md](docs/PILOT_DRY_RUN_CHECKLIST.md)
- [docs/PILOT_OPERATOR_RUNBOOK.md](docs/PILOT_OPERATOR_RUNBOOK.md)
- [docs/SALES_FAQ.md](docs/SALES_FAQ.md)
- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)
- [docs/DEMO_DATA.md](docs/DEMO_DATA.md)
- [docs/SALES_DEMO_WALKTHROUGH.md](docs/SALES_DEMO_WALKTHROUGH.md)
- [docs/SAMPLE_STRATEGY_PACK_EXPORTS.md](docs/SAMPLE_STRATEGY_PACK_EXPORTS.md)
- [docs/SAMPLE_DEMO_BRIEFS.md](docs/SAMPLE_DEMO_BRIEFS.md)
- [docs/DEMO_ARTIFACT_CHECKLIST.md](docs/DEMO_ARTIFACT_CHECKLIST.md)
- [docs/CUSTOMER_DEMO_READINESS_REVIEW.md](docs/CUSTOMER_DEMO_READINESS_REVIEW.md)
- [docs/FAQ.md](docs/FAQ.md)
- [docs/ANALYTICS.md](docs/ANALYTICS.md)
- [docs/SCREENSHOT_GUIDE.md](docs/SCREENSHOT_GUIDE.md)
- [docs/USER_JOURNEY.md](docs/USER_JOURNEY.md)
- [docs/RELEASE_NOTES.md](docs/RELEASE_NOTES.md)
- [docs/RELEASE_READINESS_CHECKLIST.md](docs/RELEASE_READINESS_CHECKLIST.md)
- [docs/SECURITY_REVIEW.md](docs/SECURITY_REVIEW.md)
- [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)
- [docs/POST_IMPLEMENTATION_ACTION_PLAN.md](docs/POST_IMPLEMENTATION_ACTION_PLAN.md)
- [docs/PILOT_PLAN.md](docs/PILOT_PLAN.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)

---

## Customer Pilot

3C Simulator can be packaged as a controlled paid pilot for brand teams, agencies, PR teams, and strategy teams that need decision support before campaign spend.

Pilot positioning:

- Local demo: ready.
- Controlled private pilot: conditional candidate.
- Public pilot: blocked.
- Public internet exposure: blocked.
- Production customer deployment: blocked.

The pilot should be sold as a guided engagement, not production SaaS. Outputs are decision-support estimates, not guaranteed predictions of sentiment, conversion, revenue, ROI, crisis probability, or market share.

Operator proof-of-value workflow:

- Use `/proof-of-value` to turn one customer-approved campaign brief into an operator checklist, structured proof-of-value payload, and Strategy Pack deliverable sequence.
- Use `/resources` to open the in-app Proof-of-Value Resource Hub for curated customer, sales, operator, and safety documentation links.
- Use `/strategic-command` for the separate public policy and government communication vertical. It is Thai-first and focuses on policy communication risk, crisis-information watchouts, synthetic public-sentiment simulation, and executive decision support.
- The workflow flags missing approvals and unsafe intake signals before any customer-facing output is assembled.
- It does not require live LLM/API/Neo4j credentials, live integrations, PII, raw CRM records, customer lists, or secrets.

Customer data rules for the first pilot:

- No PII.
- No raw CRM records.
- No live social-listening, CRM, ad-platform, or marketing automation integration.
- No API keys, provider tokens, OAuth credentials, passwords, graph credentials, or customer-owned provider secrets may be entered into browser fields.
- If customer-owned credentials are ever needed in a later approved phase, configure them only through an approved deployment secret path, environment variable, or secret manager.
- Use anonymized or explicitly approved campaign briefs only.
- Keep Demo Mode, Local Estimate, Live Backend, Backend Verified, and Unknown Source labels visible in the UI, screenshots, exports, and decks.

Recommended customer-pilot docs:

- [Customer Pilot Playbook](docs/CUSTOMER_PILOT_PLAYBOOK.md)
- [Customer Data Handling](docs/CUSTOMER_DATA_HANDLING.md)
- [Customer Proof-of-Value Flow](docs/CUSTOMER_PROOF_OF_VALUE_FLOW.md)
- [Customer Brief Intake Template](docs/CUSTOMER_BRIEF_INTAKE_TEMPLATE.md)
- [Strategic Command Overview TH](docs/STRATEGIC_COMMAND_TH.md)
- [Public Policy PoV Intake Template TH](docs/PUBLIC_POLICY_POV_INTAKE_TEMPLATE_TH.md)
- [Strategic Command Demo Script TH](docs/STRATEGIC_COMMAND_DEMO_SCRIPT_TH.md)
- [Strategic Command Safety Boundaries TH](docs/STRATEGIC_COMMAND_SAFETY_BOUNDARIES_TH.md)
- [AI Research Prompt Pack](docs/AI_RESEARCH_PROMPT_PACK.md)
- [PoV Intake Import Template](docs/POV_INTAKE_IMPORT_TEMPLATE.md)
- [Raw Brief to PoV Example](docs/RAW_BRIEF_TO_POV_EXAMPLE.md)
- [Proof-of-Value Outreach Message Pack](docs/PROOF_OF_VALUE_OUTREACH_PACK.md)
- [Founder First Customer Close Pack](docs/FOUNDER_FIRST_CUSTOMER_CLOSE_PACK.md)
- [Proof-of-Value Sales Offer](docs/PROOF_OF_VALUE_SALES_OFFER.md)
- [Proof-of-Value One-Page Copy](docs/PROOF_OF_VALUE_ONE_PAGE_COPY.md)
- [Proof-of-Value Customer Output Template](docs/PROOF_OF_VALUE_CUSTOMER_OUTPUT_TEMPLATE.md)
- [Proof-of-Value Pricing Options](docs/PROOF_OF_VALUE_PRICING_OPTIONS.md)
- [Proof-of-Value Deliverables](docs/PROOF_OF_VALUE_DELIVERABLES.md)
- [Proof-of-Value Output Package](docs/PROOF_OF_VALUE_OUTPUT_PACKAGE.md)
- [Proof-of-Value Operator Checklist](docs/PROOF_OF_VALUE_OPERATOR_CHECKLIST.md)
- [Sample Proof-of-Value Package](docs/SAMPLE_PROOF_OF_VALUE_PACKAGE.md)
- [Proof-of-Value Session Script](docs/PROOF_OF_VALUE_SESSION_SCRIPT.md)
- [Pilot Discovery Questions](docs/PILOT_DISCOVERY_QUESTIONS.md)
- [Pilot Success Criteria](docs/PILOT_SUCCESS_CRITERIA.md)
- [Sample Pilot SOW](docs/SAMPLE_PILOT_SOW.md)
- [Pilot Pricing Packages](docs/PILOT_PRICING_PACKAGES.md)
- [Pilot Onboarding Guide](docs/PILOT_ONBOARDING_GUIDE.md)
- [Pilot Exit Checklist](docs/PILOT_EXIT_CHECKLIST.md)
- [Pilot Deployment Dry Run Checklist](docs/PILOT_DRY_RUN_CHECKLIST.md)
- [Pilot Operator Runbook](docs/PILOT_OPERATOR_RUNBOOK.md)
- [Sales FAQ](docs/SALES_FAQ.md)
- [Sales Demo Walkthrough](docs/SALES_DEMO_WALKTHROUGH.md)
- [Sample Strategy Pack Exports](docs/SAMPLE_STRATEGY_PACK_EXPORTS.md)
- [Sample Demo Briefs](docs/SAMPLE_DEMO_BRIEFS.md)
- [Demo Artifact Checklist](docs/DEMO_ARTIFACT_CHECKLIST.md)
- [Customer Demo Readiness Review](docs/CUSTOMER_DEMO_READINESS_REVIEW.md)

---

## Try The Demo First

New users should be able to see value before configuring an LLM provider.

The product includes a public no-key demo flow:

- Demo campaign list: `GET /api/demo/campaigns`
- Demo dashboard: `GET /api/demo/campaigns/{id}/dashboard`
- Frontend sample route: `/dashboard/demo-premium-water`

Current public demo dashboards:

- `demo-premium-water`: FMCG / premium water launch.
- `demo-insurtech-trust`: InsurTech trust recovery after claim delays.
- `demo-energy-community`: community energy and clean-power narrative.

Each demo dashboard includes:

- campaign brief
- 7 executive KPIs
- confidence score
- assumptions
- limitations
- why-this-score explanations
- risk drivers
- simulated persona quotes
- segment breakdown
- structured action plan
- recommended validation step
- priority recommended actions

For local development:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

Open:

```text
http://127.0.0.1:5174/dashboard/demo-premium-water
```

---

## Product Walkthrough

Screenshots below were reviewed after the PR AD roadmap pass and use the local demo flow with no auth token, API key, or real customer data. They show product workflow only; they do not claim public-pilot or production readiness.

For a 5-minute presenter script, use one of the two tracks in [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md):

- Brand Safety / C-Level Decision Demo.
- Agency Pitch / A/B/C Campaign Comparison Demo.

### 1. Start From The Landing Page

The first screen positions 3C Simulator as a decision-intelligence product, not an AI playground.

![Home landing page](docs/screenshots/home-landing.png)

### 2. Open The Demo Dashboard

The no-key demo shows source-labeled synthetic demo data, decision context, confidence/evidence, KPI cards, and recommended validation steps.

![Demo dashboard with source label](docs/screenshots/demo-dashboard-overview.png)

### 3. Check Brief Quality Before Simulation

Before spending simulation time, the Brief Quality Score checks objective, audience, market, budget, KPI, channels, competitor context, constraints, and risk/legal notes.

![Brief Quality Score](docs/screenshots/brief-quality-score.png)

### 4. Review Simulation Evidence

The dashboard keeps result-source labeling visible and separates assumptions, confidence, KPI evidence, and next validation steps.

![Simulation dashboard evidence](docs/screenshots/simulation-dashboard-kpis.png)

### 5. Stress-Test Competitive Scenarios

War Room defaults to backend deterministic simulation and labels the output as Live Backend. Local estimates are only shown as explicit fallback.

![Competitor War Room](docs/screenshots/war-room.png)

### 6. Turn Results Into Action

The Action Plan translates results into creative adjustment, channel allocation, crisis prevention, and validation guidance while preserving the result source.

![Structured Action Plan](docs/screenshots/action-plan.png)

### 7. Configure Demo, Local, Or Cloud Mode

The Settings Wizard checks readiness for demo-only, local model, and cloud API setups without exposing API keys or graph passwords.

![Settings Wizard](docs/screenshots/settings-wizard.png)

### 8. Import Aggregate Actuals For Calibration

Calibration v1 lets analyst/admin users enter approved aggregate actual campaign results and compare them against prior estimates. It rejects raw customer data, CRM records, raw social posts, and PII-like notes.

### 9. Capture Pilot Feedback Privately

Pilot analytics emits sanitized browser `3c:analytics` events and fixed-choice feedback only. No third-party analytics SDK is installed, no network destination is configured by default, and no raw campaign brief, PII, token, API key, or customer record should be collected.

For a presenter-friendly run-through, see [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md). For safe sample briefs, see [docs/DEMO_DATA.md](docs/DEMO_DATA.md). For expected buyer and pilot-user questions, see [docs/FAQ.md](docs/FAQ.md). For a first-time user path, see [docs/USER_JOURNEY.md](docs/USER_JOURNEY.md).

---

## Core Product Pillars

### 1. Campaign Simulation

Create a campaign, define target audience, select campaign channels, and simulate likely public reaction.

Supported campaign objectives:

- message testing
- product launch
- brand perception
- competitor response
- crisis simulation

### 2. Competitor War Room

Model competitive dynamics across multiple brands. Simulate events such as price wars, first-mover launches, copycat moves, creator backlash, media blitzes, and scandals.

The War Room now works like a strategy sandbox:

- choose a live or demo campaign as the brand in play
- tune competitor budget and aggression
- select a response strategy such as proof-led defense, selective price match, creator counter-wave, or containment
- review market-share movement, risk exposure, response playbook, and immediate action recommendations

### 3. Crisis Intelligence

Stress-test sensitive narratives before they become real issues. Identify risk segments, likely objections, and message frames that reduce escalation.

---

## Key Features

### No-Key Demo Mode

Users can open a sample campaign and see a full executive dashboard without registering, creating an org, or entering an API key.

### Industry Templates

Start from industry-specific persona segments, crisis seeds, document seeds, and campaign defaults.

Deep built-in presets now include richer planner scaffolding: target segment archetypes, common objections, crisis triggers, typical KPIs, channel behavior, competitor archetypes, regulatory sensitivities, proof-point requirements, sample brief, risk checklist, action-plan hints, assumptions, and limitations.

Current built-in and importable template areas include:

- energy
- finance
- FMCG / CPG
- insurance / InsurTech
- retail / ecommerce
- real estate
- EV / automotive
- healthcare / wellness

Templates are assumptions for scenario planning, not market-truth or regulated advice. Replace sample budget, duration, KPI, competitor context, risk/legal notes, and channel mix with the user's actual campaign plan before running a simulation.

### Audience Channels

The user can describe where the audience actually lives, beyond the native simulation engine:

- Facebook
- Instagram
- TikTok
- YouTube
- LINE
- Twitter/X
- Reddit
- LinkedIn

### Budget Scenario Planner

Run assumption-based channel mix what-if planning before committing media spend. The planner accepts total budget, duration, target segments, channel mix, risk tolerance, and objective, then returns directional allocation ranges, trade-offs, confidence level, assumptions, limitations, and a recommended validation step.

This is not an exact ROI or ROAS predictor. It does not use live ad-platform cost data unless the user supplies approved planning inputs.

### Manual Calibration v1

Import approved aggregate actual campaign results through `/calibration` or `POST /api/calibration/actual-results`.

Supported fields include campaign ID, date range, impressions, clicks, CTR, conversion count/rate, sales lift, sentiment score or summary, crisis incident flag, anonymized qualitative notes, and optional prior estimate fields.

The output shows estimate-vs-actual deltas, error by metric, matched/missed risk classification, segment assumption gaps when supplied, privacy review, limitations, and calibration status:

- `not_calibrated`
- `partially_calibrated`
- `calibrated_with_n_campaigns`

This is not live CRM, ad-platform, or social-listening ingestion. It does not retrain the model or overwrite original simulation outputs.

### OASIS Platform Presets

OASIS remains the core simulation engine. Platform presets translate modern channel intent into supported behavior models:

- auto
- microblog
- community forum
- group chat
- creator feed
- commerce intent

This keeps the backend compatible with the current OASIS runner while letting the product reflect real-world channel planning.

### Executive Dashboard

The dashboard is designed for business decisions, not only charts.

It includes:

- overall sentiment
- conversion probability
- social influence index
- message resonance
- crisis risk
- brand perception shift
- opinion polarization
- sentiment timeline
- segment breakdown
- simulated influence nodes
- action plan
- Thai executive summary

### Decision Evidence

Every score should be explainable.

The dashboard includes:

- confidence score
- assumptions
- persona sample evidence
- simulated quotes
- why-this-score explanations
- risk drivers
- recommended actions with priorities

Example insight:

```text
Crisis risk is medium because price-sensitive family personas reacted negatively
to premium pricing, while health-focused urban buyers remained strongly positive.
```

### Decision Engine

The dashboard now includes a deterministic strategy layer that converts KPIs into:

- recommended strategy
- next best action
- primary risk segment
- business impact
- estimated crisis loss
- projected market share shift
- KPI-to-business mapping

This layer is intentionally rule-based first, so recommendations are consistent, auditable, and easier to calibrate with real campaign outcomes.

### Strategy Sandbox

Run lightweight what-if analysis from dashboard KPIs:

- add proof points and testimonials
- reduce price by 10%
- simulate a competitor launch

The what-if engine returns KPI deltas, adjusted business impact, and an updated decision recommendation.

### Client-Ready Strategy Packs

For decision meetings, the backend can package existing dashboard/simulation payloads into two structured report modes:

- **Brand Executive Summary** for internal launch/revise/do-not-launch review.
- **Agency Client Pitch Summary** for agency-to-client strategy discussion.

Each pack includes executive decision summary, launch recommendation, KPI summary, segment reactions, risk drivers, crisis watchouts, recommended action plan, and next validation steps. Every section inherits source/provenance metadata such as `source_mode`, `data_basis`, confidence level, assumptions, limitations, and recommended validation step.

Strategy packs can also be rendered as native PowerPoint decks through `POST /api/export/strategy-pack/pptx`. Optional white-label fields include agency name, client name, prepared by, report date, campaign name, scenario name, and a safe logo placeholder. The export does not fetch or embed remote logo URLs. Every slide includes provenance footer metadata, and the deck ends with limitations and recommended validation. It is scenario-planning material, not guaranteed ROI or production-readiness evidence.

### Revised Brief v2

Dashboard Action Plans can be turned into a reviewable revised brief before the next simulation or creative review. The revised brief includes objective, target segments, key message, tone and voice, proof points, channel recommendations, risk guardrails, validation plan, and creative team notes.

The brief keeps provenance from the source action plan and is deterministic planning guidance, not a guarantee of improved market outcomes.

### Backend-First Comparator

The A/B/C Comparator compares 2-5 campaign directions through the backend first. It includes backend demo fixtures for:

- Emotional / storytelling direction.
- Proof-led / trust direction.
- Price / promotion direction.

Comparator output includes ranked recommendation, metric wins, segment strengths and weaknesses, conversion and engagement estimates, crisis/risk comparison, trade-offs, recommended use case, and source/provenance metadata per variant and for the overall comparison. Browser-side output is available only as an explicit Local Estimate fallback.

### Export To Slide

Export simulation output into client- or leadership-ready files:

- PowerPoint `.pptx`
- CSV `.csv`
- browser-side quick download fallback

Recommended deck structure:

1. Executive Summary
2. KPI Dashboard
3. Segment Insight
4. Risk & Crisis Drivers
5. Recommended Action Plan

Strategy pack PPTX structure:

1. Cover / white-label context
2. Executive Decision Summary
3. Decision Gate & KPI Summary
4. Segment Reactions
5. Risk Drivers & Crisis Watchouts
6. Recommended Action Plan
7. Limitations & Recommended Validation

### System Health

Settings includes a system health view backed by `GET /api/status`.

### Settings Wizard

Settings includes a setup wizard for three supported modes:

- **Demo only**: no LLM, embedding provider, or Neo4j connection required.
- **Local model**: configuration readiness for local Ollama-style LLM/embedding and local Neo4j.
- **Cloud API**: configuration readiness for supported cloud LLM/embedding providers and Neo4j Aura-style graph storage.

The readiness endpoint (`POST /api/settings/readiness`) is deterministic and does not make live provider calls. It validates required fields using secret-presence flags, so API keys and passwords are not echoed back to the browser. The optional LLM live test remains an authenticated runtime check and depends on real provider availability.

### Result Source Labels

The UI labels simulation and decision outputs with one of the supported result-source modes:

- **Demo Mode**: deterministic sample data intended for onboarding and product exploration.
- **Local Estimate**: browser-side deterministic fallback, visibly warned and not presented as live backend output.
- **Live Backend**: backend-generated deterministic output.
- **Backend Verified**: persisted real simulation KPI/evidence was loaded for an owned campaign/run. Backend route success by itself is not enough for this label.
- **Unknown Source**: source metadata was unavailable and should be treated conservatively.

It checks:

- backend API readiness
- Neo4j availability
- LLM provider configuration
- embedding provider configuration
- runtime storage
- default model
- rough cost estimate per 100 personas

---

## Workflow

```text
1. Pick template or demo campaign
   Choose an industry template, import a template, or open sample data.

2. Define campaign brief
   Name, objective, target segment, regions, persona count, channels, and risk concerns.

3. Select behavior model
   Choose campaign channels and OASIS behavior preset.

4. Run simulation
   Personas react, post, debate, and shift sentiment across simulated rounds.

5. Review decision evidence
   Read KPIs, segment drivers, assumptions, persona quotes, and recommended actions.

6. Export
   Generate boardroom-ready slides or CSV evidence.
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose
- Neo4j 5.18 if running graph features locally
- Optional: Ollama for local LLM / embedding

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python run.py
```

By default the backend reads configuration from environment variables and `.env`.

### Docker Dev Stack

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml up -d --build
```

### Local Ollama Mode

```bash
docker compose --profile local up -d
docker exec 3c-ollama ollama pull qwen2.5:7b
docker exec 3c-ollama ollama pull nomic-embed-text
```

---

## Runtime Configuration

Example `.env`:

```bash
LLM_PROVIDER=deepseek
LLM_API_KEY=replace-with-provider-api-key
LLM_MODEL_NAME=deepseek-chat

EMBEDDING_PROVIDER=openai
EMBEDDING_API_KEY=replace-with-embedding-api-key

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=replace-with-neo4j-password
```

The Settings page can manage runtime provider values, per-task model overrides, language, and system health.

---

## API Reference

All product APIs are registered under `/api/*`.

### Public APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Basic backend liveness |
| GET | `/api/status` | System health and readiness |
| GET | `/api/demo/campaigns` | No-key demo campaign list |
| GET | `/api/demo/campaigns/{id}/dashboard` | No-key demo dashboard |
| GET | `/api/industry/templates` | Public industry template list |
| POST | `/api/brief/quality` | Deterministic brief completeness scoring |
| POST | `/api/brief/revise` | Deterministic Revised Brief v2 from an Action Plan |
| POST | `/api/decision/budget-scenario` | Deterministic budget/channel scenario planner |
| GET | `/api/settings/providers` | Safe provider catalog |
| POST | `/api/settings/readiness` | Secret-safe setup readiness check |

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create organization and admin user |
| POST | `/api/auth/login` | Login and receive JWT |
| GET | `/api/auth/me` | Current user profile |
| POST | `/api/auth/api-key` | Generate API key |

### Calibration

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/calibration/actual-results` | Import aggregate actual results and compare against prior estimates |
| GET | `/api/calibration/status/{campaign_id}` | Read calibration status for an organization campaign |

### Campaigns

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/campaign` | Create campaign |
| GET | `/api/campaign` | List organization campaigns |
| GET | `/api/campaign/{id}` | Campaign details |
| PUT | `/api/campaign/{id}` | Update campaign |
| DELETE | `/api/campaign/{id}` | Delete campaign |
| POST | `/api/campaign/{id}/pipeline/start` | Start campaign pipeline |
| GET | `/api/campaign/{id}/pipeline/status` | Pipeline progress |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/campaign/{id}/kpi` | Executive KPIs |
| GET | `/api/dashboard/campaign/{id}/report` | Full executive report |
| GET | `/api/dashboard/campaign/{id}/timeline` | Sentiment timeline |
| GET | `/api/dashboard/campaign/{id}/segments` | Segment breakdown |

### Industry Templates

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/industry/templates` | List templates |
| POST | `/api/industry/templates/import` | Import template JSON |
| POST | `/api/industry/templates/validate` | Validate template JSON |
| DELETE | `/api/industry/templates/{id}` | Delete uploaded template |
| GET | `/api/industry/templates/{id}/preset` | Campaign preset from template |
| GET | `/api/industry/templates/{id}/personas` | Template persona segments |
| GET | `/api/industry/templates/{id}/crises` | Template crisis scenarios |
| GET | `/api/industry/templates/{id}/seeds` | Template document seeds |

### Simulation

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/simulation/create` | Create simulation instance |
| POST | `/api/simulation/prepare` | Prepare simulation assets |
| POST | `/api/simulation/start` | Start simulation runner |
| POST | `/api/simulation/stop` | Stop simulation runner |
| GET | `/api/simulation/{id}/run-status` | Runtime status |
| GET | `/api/simulation/{id}/run-status/detail` | Detailed runtime status |

### Comparator, Impact, Competitor, Export

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/decision/analyze` | Convert KPIs into recommendation, risk, actions, and business impact |
| POST | `/api/decision/what-if` | Run deterministic what-if strategy simulation |
| POST | `/api/comparator/compare` | Compare 2-5 campaigns |
| GET | `/api/comparator/metrics` | Comparator metric definitions |
| GET | `/api/comparator/demo/campaigns` | Public backend demo comparator variants |
| POST | `/api/comparator/demo/compare` | Compare backend demo comparator variants |
| POST | `/api/impact/calculate` | Business impact calculation |
| GET | `/api/impact/scenarios/{sentiment}` | Quick impact scenario |
| GET | `/api/competitor/scenarios` | War room scenario list |
| POST | `/api/competitor/simulate` | Run competitor simulation |
| POST | `/api/export/pptx` | Export PowerPoint deck |
| POST | `/api/export/csv` | Export CSV data |
| POST | `/api/export/strategy-pack` | Build a client-ready Brand or Agency strategy pack payload |
| POST | `/api/export/strategy-pack/pptx` | Render a client-ready strategy pack PPTX |

---

## Architecture

```text
Vue 3 Frontend
  Home
  Campaigns
  Dashboard
  Comparator
  Impact Simulator
  War Room
  Settings / System Health
        |
        | JWT / API key / public demo APIs
        v
Flask Backend
  Auth + Tenant Middleware
  Campaign API
  Persona Factory
  Industry Templates
  KPI Calculator
  Decision Engine
  Demo API
  Status API
  Export Engine
  Calibration Service
  OASIS Simulation Runner
        |
        v
Neo4j + JSON tenant storage + LLM providers
```

Key decisions:

- **Tenant scoped by default**: authenticated APIs resolve `org_id` through middleware.
- **Public demo path**: `/api/demo/*` lets users see value before setup.
- **OASIS-native runner**: Twitter/X and Reddit remain the execution backend, with product-level channel presets layered on top.
- **JSON templates**: industry templates are importable and versionable.
- **Runtime provider switching**: 17 LLM providers and multiple embedding providers are available through a unified configuration layer.
- **Decision evidence over black-box scores**: dashboard output includes assumptions and explanation panels.
- **Deterministic decision layer**: strategy recommendations and what-if deltas are rule-based first, not hidden in an LLM prompt.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, Vue Router, vue-i18n |
| Backend | Flask, Pydantic, Python 3.11 |
| Simulation | OASIS / CAMEL-AI |
| Graph | Neo4j 5.18 |
| LLM | Ollama, OpenAI, Anthropic, Google, DeepSeek, Groq, OpenRouter, xAI, Mistral, Together AI, GLM, MiniMax, Kimi, DashScope, Hugging Face, Bedrock, Vercel |
| Embeddings | Ollama, OpenAI, Google, Cohere |
| Export | python-pptx, CSV |
| Auth | JWT and API keys |
| Storage | Tenant-scoped JSON files plus Neo4j graph storage |

---

## Testing

Backend contract tests:

```bash
./backend/.venv/bin/python -m pytest backend/tests
```

Frontend production build:

```bash
cd frontend
npm run build
```

Locale validation:

```bash
for f in frontend/src/locales/*.json; do python3 -m json.tool "$f" >/dev/null || exit 1; done
```

Available frontend scripts:

```bash
cd frontend
npm run build
```

There is no frontend unit-test or lint script configured in `frontend/package.json` yet.

---

## Product Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md). The highest-priority next work is calibration against real campaign outcomes, broader QA automation, deployment hardening, and pilot-user feedback loops.

---

## Credits

Built on and inspired by:

- [MiroFish](https://github.com/666ghj/MiroFish) by 666ghj / Shanda Group
- [OASIS](https://github.com/camel-ai/oasis) by CAMEL-AI
- [MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) by nikmcfly

3C Simulator / MarketingSimulation extensions by [chawit1103](https://github.com/chawit1103):

- multi-tenant SaaS foundation
- campaign pipeline orchestration
- 11-country persona factory
- industry template system
- executive KPI dashboard
- decision evidence panel
- no-key demo onboarding
- export-to-slide workflow
- 11-language UI

---

## License

AGPL-3.0. See [LICENSE](./LICENSE).
