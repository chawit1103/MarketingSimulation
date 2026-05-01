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
5. Export the evidence into a boardroom-ready slide deck.

This is not positioned as an AI playground. It is a decision-support system for answering:

- Which message should we launch?
- Which segment will resist?
- What risk could become a crisis?
- How should we revise the campaign before spending real media budget?
- What should we show leadership or a client?

---

## Try The Demo First

New users should be able to see value before configuring an LLM provider.

The product includes a public no-key demo flow:

- Demo campaign list: `GET /api/demo/campaigns`
- Demo dashboard: `GET /api/demo/campaigns/demo-premium-water/dashboard`
- Frontend sample route: `/dashboard/demo-premium-water`

The sample dashboard includes:

- campaign brief
- 7 executive KPIs
- confidence score
- assumptions
- why-this-score explanations
- risk drivers
- simulated persona quotes
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

Model competitive dynamics across multiple brands. Simulate events such as price wars, first-mover launches, copycat moves, and scandals.

### 3. Crisis Intelligence

Stress-test sensitive narratives before they become real issues. Identify risk segments, likely objections, and message frames that reduce escalation.

---

## Key Features

### No-Key Demo Mode

Users can open a sample campaign and see a full executive dashboard without registering, creating an org, or entering an API key.

### Industry Templates

Start from industry-specific persona segments, crisis seeds, document seeds, and campaign defaults.

Current and importable template areas include:

- energy
- finance
- insurance / InsurTech
- retail / ecommerce
- real estate
- healthcare
- FMCG

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
- top influencers
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

### System Health

Settings includes a system health view backed by `GET /api/status`.

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
LLM_API_KEY=sk-your-key
LLM_MODEL_NAME=deepseek-chat

EMBEDDING_PROVIDER=openai
EMBEDDING_API_KEY=sk-your-key

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

The Settings page can manage runtime provider values, task-specific model overrides, language, and system health.

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

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create organization and admin user |
| POST | `/api/auth/login` | Login and receive JWT |
| GET | `/api/auth/me` | Current user profile |
| POST | `/api/auth/api-key` | Generate API key |

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
| POST | `/api/comparator/compare` | Compare 2-5 campaigns |
| GET | `/api/comparator/metrics` | Comparator metric definitions |
| POST | `/api/impact/calculate` | Business impact calculation |
| GET | `/api/impact/scenarios/{sentiment}` | Quick impact scenario |
| GET | `/api/competitor/scenarios` | War room scenario list |
| POST | `/api/competitor/simulate` | Run competitor simulation |
| POST | `/api/export/pptx` | Export PowerPoint deck |
| POST | `/api/export/csv` | Export CSV data |

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
  Demo API
  Status API
  Export Engine
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
./backend/.venv/bin/python -m pytest backend/tests/test_api_contract.py
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

---

## Product Roadmap

Highest priority:

- expand Thai industry templates for healthcare, restaurants, EV, FMCG, cosmetics, public policy, and agriculture
- strengthen KPI calculation with real simulation traces rather than mock fallback where possible
- improve PPTX export templates for agency/client deliverables
- add broader backend tests for auth, campaign CRUD, template validation, KPI calculation, and export
- deploy a public hosted demo

Nice-to-have:

- scenario comparison history
- calibration from real post-campaign data
- cost estimator by LLM provider and persona count
- team collaboration and comments on reports
- template marketplace / library

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
