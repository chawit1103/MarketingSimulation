<div align="center">

<!<img src="./static/image/image.png" alt="MiroFish MultiLang" width="30%"/>>

# MarketingSimulation (MSaaS)

**Marketing Simulation as a Service — B2B Multi-Agent Platform**

*Simulate marketing campaigns against hundreds of AI-generated Thai consumers. Predict sentiment, conversion, and social influence before spending a single baht on real ads.*

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue?style=flat-square)](./LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Build-2496ED?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://python.org)
[![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org)

</div>

---

## What is MarketingSimulation?

MarketingSimulation is a **B2B SaaS platform** that lets brands and agencies simulate marketing campaigns against synthetic consumer personas before launching in the real world.

**Here's how it works:**

1. You upload a marketing brief, press release, or campaign plan
2. The system generates **hundreds of AI-powered Thai consumer personas** grounded in real demographic and cultural data
3. These personas debate, discuss, and react to your campaign on **simulated social media** (Twitter/X + Reddit)
4. You get an **Executive Dashboard** with quantitative KPIs — sentiment score, conversion probability, crisis risk, and an action plan

**Think of it as a "flight simulator for marketing campaigns."**

---

## Why MSaaS?

| Traditional Approach | MSaaS Approach |
|---|---|
| Launch campaign → wait weeks → analyze results | Simulate first → predict results → launch with confidence |
| Real consumers = real risk | Synthetic personas = zero risk |
| One outcome per budget | Run 10 scenarios, compare A/B |
| Gut feeling + past data | Quantitative KPIs + social dynamics modeling |
| Panic when crisis hits | Simulate crisis scenarios before they happen |

---

## Key Features

### 🏢 Multi-Tenant B2B Platform
- Organization-based workspaces with isolated data
- Role-based access (Admin, Analyst, Viewer)
- JWT authentication + API key support
- Tiered plans (Free / Pro / Enterprise)

### 🧠 17 LLM Providers
Choose any AI model to power your simulations — local or cloud:

| Provider | Type | Best For |
|----------|------|----------|
| Ollama | Local | Privacy-first, no API costs |
| OpenAI | Cloud | GPT-4o, highest quality |
| Anthropic | Cloud | Claude, nuanced analysis |
| Google | Cloud | Gemini, large context |
| DeepSeek | Cloud | Cost-effective, strong reasoning |
| Groq | Cloud | Ultra-fast inference |
| OpenRouter | Cloud | Access any model |
| xAI | Cloud | Grok, real-time aware |
| Mistral | Cloud | European, multilingual |
| Together AI | Cloud | Open-source models |
| GLM, MiniMax, Kimi, DashScope | Cloud | Chinese/Asian markets |
| HuggingFace, Bedrock, Vercel | Cloud | Custom endpoints |

### 👥 Thai Persona Factory
- **8 Consumer Archetypes**: Young Urban Professional, Family Mom, Rural Elder, Gen Z Student, SME Owner, Digital Nomad, Factory Worker
- **7 Regional Profiles**: Bangkok, Central, North, Northeast, East, South, West
- **10 Thai Value Dimensions**: เกรงใจ, รักษาหน้า, ครอบครัว, บุญคุณ, สนุกสนาน, ใจเย็น, ไม่เป็นไร, น้ำใจ, เคารพผู้อาวุโส
- **Contextual Grounding**: Income, education, occupation, media habits, brand loyalty, price sensitivity
- **LLM-Generated Backstories**: Each persona has a unique life story in Thai

### 📊 Executive Dashboard (Think to Finish)
- **7 Quantitative KPIs**: Overall Sentiment, Conversion Probability, Social Influence Index, Message Resonance, Crisis Risk, Brand Perception Shift, Opinion Polarization
- **Sentiment Timeline**: Round-by-round tracking
- **Segment Breakdown**: By region, age, income
- **Top Influencers**: Most impactful agents identified
- **Action Plan**: Winning strategy + risk areas + priority actions
- **Thai Executive Summary**: บทสรุปผู้บริหาร

### 🌐 11-Language UI
English, 简体中文, हिन्दी, Español, Français, العربية, বাংলা, Português, Русский, اردو, **ไทย**

### ⚙️ Runtime Settings
Switch providers, models, and API keys from the Settings page — no restart required. Per-task model overrides (NER, Report, Simulation, Ontology).

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- (Optional) GPU for local LLM — not required when using cloud providers

### Option A: Cloud LLM (Recommended — No GPU Needed)

```bash
git clone https://github.com/chawit1103/MarketingSimulation.git
cd MarketingSimulation
cp .env.example .env

# Edit .env with your cloud provider:
#   LLM_PROVIDER=deepseek
#   LLM_API_KEY=sk-your-key
#   LLM_MODEL_NAME=deepseek-chat
#   EMBEDDING_PROVIDER=openai
#   EMBEDDING_API_KEY=sk-your-key

docker compose -f docker-compose.dev.yml up -d --build
```

Open `http://localhost:3001` → Settings → configure your LLM → start simulating.

### Option B: Fully Local (Ollama)

```bash
git clone https://github.com/chawit1103/MarketingSimulation.git
cd MarketingSimulation
cp .env.example .env

docker compose --profile local up -d
docker exec mirofish-ollama ollama pull qwen2.5:7b
docker exec mirofish-ollama ollama pull nomic-embed-text
```

Open `http://localhost:3000`.

### Dev Stack Ports

| Service | Dev | Prod |
|---------|-----|------|
| Frontend | `:3001` | `:3000` |
| Backend | `:5002` | `:5001` |
| Neo4j Browser | `:7475` | `:7474` |
| Neo4j Bolt | `:7688` | `:7687` |

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                 Vue 3 Frontend                        │
│  Home · Campaigns · Dashboard · Settings             │
│  11 languages · i18n · Dark theme                    │
└────────────────────┬─────────────────────────────────┘
                     │ JWT / API Key
┌────────────────────▼─────────────────────────────────┐
│              Flask Backend (Python 3.11)              │
│                                                       │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐           │
│  │ Auth    │ │ Tenant   │ │ Settings     │           │
│  │ JWT+Key │ │ Middleware│ │ 17 Providers │           │
│  └─────────┘ └──────────┘ └──────────────┘           │
│                                                       │
│  ┌──────────┐ ┌────────────┐ ┌─────────────────┐     │
│  │ Persona  │ │ Dashboard  │ │ Campaign        │     │
│  │ Factory  │ │ KPI Engine │ │ Pipeline        │     │
│  └──────────┘ └────────────┘ └─────────────────┘     │
│                                                       │
│  ┌──────────────────────────────────────────────┐    │
│  │ OASIS Multi-Agent Simulation Engine           │    │
│  │ Twitter/X + Reddit · Multi-round · Emergent   │    │
│  └──────────────────────────────────────────────┘    │
│                                                       │
│  Organization · User · Campaign · Persona (JSON)      │
└────────────────────┬─────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │    Neo4j 5.18       │
          │  Knowledge Graph    │
          └─────────────────────┘
```

**Key Architecture Decisions:**
- **GraphStorage** abstract interface — swap Neo4j for any graph DB
- **LLMProviderFactory** — 17 providers, single interface, runtime switching
- **Tenant Middleware** — auto-injects org_id into every request
- **Pipeline Orchestrator** — 5-step persona→graph→sim→report flow
- **Hybrid Search**: 0.7 × vector similarity + 0.3 × BM25

---

## Workflow: Campaign Pipeline

```
1. CREATE CAMPAIGN         2. GENERATE PERSONAS
   Set objective, target       PersonaFactory creates
   audience, platform          100+ Thai consumers

3. BUILD KNOWLEDGE GRAPH   4. RUN SIMULATION
   Extract entities from      OASIS engine: agents
   document → Neo4j           post, reply, debate

5. EXECUTIVE DASHBOARD
   KPIs + Action Plan
   Sentiment · Conversion · Risk
```

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create organization + admin user |
| POST | `/api/auth/login` | Get JWT token |
| GET | `/api/auth/me` | Current user profile |

### Campaigns
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/campaign` | Create campaign |
| GET | `/api/campaign` | List organization's campaigns |
| GET | `/api/campaign/{id}` | Campaign details |
| POST | `/api/campaign/{id}/pipeline/start` | Start simulation pipeline |
| GET | `/api/campaign/{id}/pipeline/status` | Pipeline progress |

### Personas
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/persona/archetypes` | 8 Thai consumer archetypes |
| GET | `/api/persona/regions` | 7 regional profiles |
| POST | `/api/persona/generate` | Generate personas for campaign |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/campaign/{id}/kpi` | 7 quantitative KPIs |
| GET | `/api/dashboard/campaign/{id}/report` | Full executive report |
| GET | `/api/dashboard/campaign/{id}/timeline` | Sentiment timeline |
| GET | `/api/dashboard/campaign/{id}/segments` | Segment breakdown |

### Settings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/settings` | Current configuration |
| PUT | `/api/settings` | Update runtime settings |
| GET | `/api/settings/providers` | 17 LLM + 4 embedding providers |

---

## Use Cases

### For Brands
- **Message Testing**: A/B test 3 campaign angles against 500 personas, pick the winner
- **Crisis Simulation**: "What if our product recall goes viral?" — simulate 48 hours of social media reaction
- **Product Launch**: Predict sentiment for a new product in Bangkok vs. Northeast Thailand
- **Competitor Response**: "If competitor X drops prices 20%, how will our customers react?"

### For Agencies
- **Client Pitch**: Show predicted sentiment before the campaign launches
- **Multi-Scenario Planning**: Compare optimistic, neutral, and pessimistic simulation runs
- **Post-Campaign Analysis**: Compare simulated vs. real outcomes to calibrate the model

### For Enterprises
- **Brand Health Tracking**: Run monthly simulations to detect perception shifts
- **Policy Testing**: Simulate employee reaction to new policies
- **Market Entry**: Test brand perception in a new region before entering

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, Vite, vue-i18n, Vue Router |
| Backend | Python 3.11, Flask, Pydantic |
| Simulation | OASIS (CAMEL-AI), camel-oasis 0.2.5 |
| Graph DB | Neo4j Community 5.18 |
| LLM | 17 providers via OpenAI-compatible API |
| Embeddings | 4 providers (Ollama, OpenAI, Google, Cohere) |
| Auth | JWT (HMAC-SHA256), API Keys |
| Storage | JSON file-based per tenant |
| DevOps | Docker Compose, dev/prod profiles |

---

## Credits

This project is built on:
- [MiroFish](https://github.com/666ghj/MiroFish) by 666ghj (Shanda Group) — original multi-agent simulation engine
- [OASIS](https://github.com/camel-ai/oasis) from CAMEL-AI — social media simulation framework
- [MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) by nikmcfly — Neo4j + Ollama migration

**MSaaS extensions by [chawit1103](https://github.com/chawit1103):**
- Multi-tenant B2B platform (Organization, User, Campaign, JWT auth)
- Thai Persona Factory (8 archetypes, 7 regions, 10 cultural values)
- Executive Dashboard (7 KPIs, Think→Finish action plan)
- Campaign Pipeline Orchestrator (end-to-end automation)
- 17 LLM providers (from 3), 4 embedding providers
- 11-language UI (from 2)
- Runtime settings API

---

## License

AGPL-3.0 — see [LICENSE](./LICENSE)
