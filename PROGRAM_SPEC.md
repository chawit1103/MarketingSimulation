# 3C Simulator — Program Specification v0.4

> **Handoff Document** — ให้ AI Codex / Claude Code / Cursor รับงานต่อได้ทันที
>
> จัดทำ: 1 พฤษภาคม 2026 | Branch: `multilang-v0.3`

---

## 1. Executive Summary

> **3C = Campaign · Competitor · Crisis** — the three pillars of marketing simulation this platform was built for.


**3C Simulator** คือ B2B SaaS แพลตฟอร์มจำลองความคิดเห็นสาธารณะ (Social Simulation) สำหรับ Marketing Manager, PR Agency, และ Crisis Response Team  

ใช้ **Multi-Agent AI** สร้างโลกคู่ขนานของ persona เสมือนนับร้อย พร้อมจำลองการโต้ตอบบนโซเชียลมีเดีย วิเคราะห์ sentiment, conversion, และ brand perception — ทั้งหมดใน 11 ภาษา ผ่าน 7 LLM provider implementations

### Key Selling Points (สำหรับ Sales Deck)
- 🏭 **Industry Templates** — เลือกอุตสาหกรรม (Energy, Finance, Real Estate, FMCG) แล้วระบบ pre-fill Persona + Crisis + Document Seeds ให้อัตโนมัติ
- ⚖️ **A/B Comparator** — เทียบ 2-5 campaigns side-by-side, 7 metrics (sentiment, conversion, influence, resonance, crisis risk, brand shift, polarization)
- 📊 **Business Impact Simulator** — ปรับ sliders (sentiment, conversion, crisis) → คำนวณ revenue projection, ROI, crisis loss ทันที
- ⚔️ **Competitor War Room** — จำลอง 4 แบรนด์แข่งกัน 12 rounds, 3 scenarios (Price War, First Mover, Scandal) — market share เปลี่ยน real-time
- 📥 **Export-to-Slide** — ดาวน์โหลดผลลัพธ์เป็น PPTX (native PowerPoint) หรือ CSV ได้ทันที

---

## 2. Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Vue 3 (Composition API) | 3.5.24 |
| Router | Vue Router | 4.6.3 |
| i18n | Vue I18n | 10.0.8 |
| Charts | D3.js | 7.9.0 |
| HTTP | Axios | 1.13.2 |
| Build | Vite | 7.2.4 |
| Backend | Flask (Python) | 3.0+ |
| Database | Neo4j (Graph) | 5.18 Community |
| LLM SDKs | OpenAI, Anthropic, Google GenAI, Groq | latest |
| Persona Simulation | CAMEL-AI OASIS | 0.2.5 |
| Export | python-pptx | 0.6.21+ |
| Container | Docker + Docker Compose | latest |
| Package | uv (Python), npm (Node) | latest |

---

## 3. Project Structure

```
3c-simulator/
├── Dockerfile                         # Single container: frontend + backend
├── docker-compose.dev.yml             # Dev stack: 3c-simulator-dev + neo4j-dev
├── docker-compose.yml                 # Production stack (with Ollama profile)
├── package.json                       # Root: concurrently runs both
│
├── backend/
│   ├── run.py                         # Entry point: python run.py → port 5001
│   ├── pyproject.toml                 # Python deps (uv)
│   └── app/
│       ├── __init__.py                # Flask factory, blueprint registration
│       ├── config.py                  # Config from .env
│       │
│       ├── api/                       # 12 API blueprints
│       │   ├── auth.py                # POST /register, /login, /me, /api-key, /switch-org
│       │   ├── campaign.py            # CRUD + pipeline start/status
│       │   ├── comparator.py          # POST /compare, GET /metrics
│       │   ├── competitor.py          # GET /scenarios, POST /simulate
│       │   ├── dashboard.py           # GET /campaign/:id/kpi, /report, /timeline, /segments
│       │   ├── export.py              # POST /pptx, /csv
│       │   ├── graph.py               # Graph build + NER pipeline
│       │   ├── impact.py              # POST /calculate, GET /scenarios/:value
│       │   ├── industry.py            # Template CRUD: /templates, /import, /validate
│       │   ├── persona.py             # POST /generate, GET /archetypes, /regions, /countries
│       │   ├── report.py              # POST /generate, GET /:id, /chat, /download
│       │   ├── settings.py            # GET/PUT settings, GET /providers, POST /test-llm
│       │   └── simulation.py          # Full simulation lifecycle + interview APIs
│       │
│       ├── services/                  # Business logic layer (25 modules)
│       │   ├── industry_templates/    # Built-in JSON templates (energy, finance) + uploads/
│       │   ├── competitor_engine.py   # Multi-brand simulation engine
│       │   ├── export_engine.py       # PPTXGenerator with 5-slide templates
│       │   ├── impact_calculator.py   # Revenue/ROI projection formulas
│       │   ├── kpi_calculator.py      # KPI computation engine
│       │   ├── persona_factory.py     # 11-country Persona generation
│       │   ├── persona_context/       # 11 locale-specific context modules
│       │   ├── simulation_runner.py   # OASIS simulation orchestration
│       │   └── pipeline_orchestrator.py
│       │
│       ├── storage/                   # Neo4j + Embedding + Search
│       ├── llm/                       # Multi-provider LLM factory (7 providers)
│       ├── models/                    # Pydantic data models
│       ├── middleware/                # JWT + API Key tenant auth
│       └── utils/                     # Logger, file parser, LLM client
│
├── frontend/
│   ├── vite.config.js                 # Dev proxy: /api → localhost:5001, server port 3000
│   ├── index.html                     # Entry HTML (fonts: Inter + JetBrains Mono + Space Grotesk + Noto Sans SC)
│   └── src/
│       ├── main.js                    # Vue app bootstrap + i18n
│       ├── App.vue                    # Root layout + lang switcher + design-system.css import
│       ├── i18n.js                    # Vue I18n setup (11 locales)
│       ├── router/index.js            # 12 routes (see §5)
│       ├── assets/
│       │   └── design-system.css      # Linear-inspired premium dark theme
│       ├── api/                       # Axios API clients (8 files)
│       ├── components/                # 10 shared components
│       ├── views/                     # 12 page views
│       └── locales/                   # 11 locale JSON files (en, th, zh-CN, ar, bn, es, fr, hi, pt, ru, ur)
│
├── docs/
│   ├── AI_TEMPLATE_GUIDE.md           # How AI should generate industry templates
│   ├── TEMPLATE_CREATOR_PROMPT.md     # Prompt template for AI template creation
│   └── progress.md                    # Development log
│
└── .env / .env.dev                    # Environment config (see §6)
```

---

## 4. API Reference

### 4.1 Blueprint URL Prefixes

| Blueprint | Registered Prefix | Full URL Examples | Auth Required |
|-----------|------------------|-------------------|--------------|
| `auth_bp` | `/api/auth` | `/api/auth/login`, `/api/auth/register` | Mixed |
| `graph_bp` | `/api/graph` | `/api/graph/build`, `/api/graph/project/...` | Yes |
| `simulation_bp` | `/api/simulation` | `/api/simulation/start`, `/api/simulation/...` | Yes |
| `report_bp` | `/api/report` | `/api/report/generate`, `/api/report/:id` | Yes |
| `dashboard_bp` | `/api/dashboard` | `/api/dashboard/campaign/:id/kpi` | Yes |
| `settings_bp` | `/api/settings` | `/api/settings`, `/api/settings/providers` | No (public) |
| `persona_bp` | `/api/persona` | `/api/persona/generate` | Yes |
| `campaign_bp` | `/api/campaign` | `/api/campaign`, `/api/campaign/:id` | Yes |
| `industry_bp` | `/industry` (no /api) | `/industry/templates`, `/industry/templates/import` | Mixed |
| `comparator_bp` | `/comparator` (no /api) | `/comparator/compare`, `/comparator/metrics` | Yes |
| `impact_bp` | `/impact` (no /api) | `/impact/calculate` | Yes |
| `competitor_bp` | `/competitor` (no /api) | `/competitor/scenarios`, `/competitor/simulate` | Yes |
| `export_bp` | `/export` (no /api) | `/export/pptx`, `/export/csv` | Yes |
| `health` | `/health` | `/health` | No |

> **⚠️ KNOWN ISSUE — Blueprint Prefix Mismatch:** Blueprints `industry`, `comparator`, `impact`, `competitor`, `export` are registered WITHOUT the `/api/` prefix (e.g., `/industry/templates` instead of `/api/industry/templates`). The Vite dev proxy only routes `/api/*` → backend. This means these endpoints are **NOT reachable through the proxy**. Currently the frontend works around this by using **client-side computation with demo data** for Comparator, Impact, and War Room. To fix: either (a) register these blueprints with `url_prefix='/api/industry'` etc. in `__init__.py`, or (b) add explicit proxy rules for `/industry`, `/comparator`, `/impact`, `/competitor`, `/export` in `vite.config.js`.
>
> **For Docker:** In production or when using `docker-compose.dev.yml`, the same issue applies — the Vite proxy inside the container only handles `/api` paths. Direct calls to `http://localhost:5002/industry/templates` bypass the frontend proxy.

### LLM Provider Implementations (7)

| Provider File | Backend |
|---------------|---------|
| `openai_provider.py` | OpenAI (GPT-4o, etc.) |
| `anthropic_provider.py` | Anthropic (Claude) |
| `google_provider.py` | Google (Gemini) |
| `deepseek_provider.py` | DeepSeek |
| `groq_provider.py` | Groq |
| `ollama_provider.py` | Ollama (local) |
| `openrouter_provider.py` | OpenRouter (multi-model gateway) |

> Note: Original MiroFish docs mention "17 providers" — this counts individual models accessible via OpenRouter (which aggregates many providers). The codebase has 7 provider *implementations*. The current deployment uses `deepseek-chat` as default.

### 4.2 Key Endpoints by Feature

**Auth:**
```
POST /api/auth/register        → Register org + admin user
POST /api/auth/login           → Login, returns JWT + API key
GET  /api/auth/me              → Current user/org info
POST /api/auth/api-key         → Generate new API key
POST /api/auth/switch-org      → Switch tenant context
```

**Campaigns (Phase 1):**
```
POST   /api/campaign           → Create campaign
GET    /api/campaign           → List campaigns (by org)
GET    /api/campaign/:id       → Get campaign detail
PUT    /api/campaign/:id       → Update campaign
DELETE /api/campaign/:id       → Delete campaign
POST   /api/campaign/:id/pipeline/start   → Start pipeline
GET    /api/campaign/:id/pipeline/status  → Get pipeline status
```

**Industry Templates (Phase 1):**
```
GET    /industry/templates                    → List all templates
POST   /industry/templates/import             → Import JSON template
POST   /industry/templates/validate           → Validate template schema
DELETE /industry/templates/:id                → Delete template
GET    /industry/templates/:id/preset         → Get campaign preset
GET    /industry/templates/:id/personas       → Get persona segments
GET    /industry/templates/:id/crises         → Get crisis scenarios
GET    /industry/templates/:id/seeds          → Get document seeds
GET    /industry/templates/:id/seeds/:sid/content → Get seed content
```

**A/B Comparator (Phase 2):**
```
POST /comparator/compare        → Compare 2-5 campaigns (body: {campaign_ids: [...]})
GET  /comparator/metrics        → Get available comparison metrics
```

**Business Impact Simulator (Phase 3):**
```
POST /impact/calculate          → Calculate impact (body: {campaign_id, sentiment, conversion, crisis_probability})
GET  /impact/scenarios/:value   → Quick scenario lookup
```

**Competitor War Room (Phase 4):**
```
GET  /competitor/scenarios      → List available scenarios
POST /competitor/simulate       → Run simulation (body: {scenario, brands: [...], rounds})
```

**Export (Phase 5):**
```
POST /export/pptx               → Generate PPTX file (binary download)
POST /export/csv                → Generate CSV file (binary download)
```

**Dashboard:**
```
GET /api/dashboard/campaign/:id/kpi        → KPI metrics
GET /api/dashboard/campaign/:id/report     → Full report
GET /api/dashboard/campaign/:id/timeline   → Timeline data
GET /api/dashboard/campaign/:id/segments   → Segment analysis
```

---

## 5. Frontend Routes

| Path | Component | Description | Phase |
|------|-----------|-------------|-------|
| `/` | `Home.vue` | Landing page (needs redesign — see §8) | — |
| `/campaigns` | `Campaigns.vue` | Campaign list + create modal | 1 |
| `/settings` | `Settings.vue` | LLM config + template import | 1 |
| `/dashboard/:campaignId` | `Dashboard.vue` | KPI dashboard for campaign | core |
| `/comparator` | `ComparatorView.vue` | A/B side-by-side comparison | 2 |
| `/impact` | `ImpactSimulator.vue` | Revenue/ROI impact sliders | 3 |
| `/war-room` | `WarRoom.vue` | Competitor simulation | 4 |
| `/process/:projectId` | `MainView.vue` | Graph build workflow (legacy) | core |
| `/simulation/:simulationId` | `SimulationView.vue` | Simulation detail (legacy) | core |
| `/simulation/:simulationId/start` | `SimulationRunView.vue` | Simulation runner (legacy) | core |
| `/report/:reportId` | `ReportView.vue` | Report view (legacy) | core |
| `/interaction/:reportId` | `InteractionView.vue` | Agent chat interface (legacy) | core |

---

## 6. Environment Configuration

### 6.1 Required Environment Variables

```bash
# .env (for bare metal) or .env.dev (for Docker)
LLM_API_KEY=***                # DeepSeek / OpenAI API key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL_NAME=deepseek-chat

NEO4J_URI=bolt://localhost:7688   # Bare metal → Docker dev port
# NEO4J_URI=bolt://neo4j-dev:7687 # Docker → service name
NEO4J_USER=neo4j
NEO4J_PASSWORD=***

EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_BASE_URL=http://localhost:11434

OPENAI_API_KEY=(same as LLM_API_KEY)
OPENAI_API_BASE_URL=(same as LLM_BASE_URL)

FLASK_DEBUG=True
LLM_TIMEOUT=600
```

### 6.2 Docker Port Mapping (Dev)

| Service | Host Port | Container Port |
|---------|-----------|---------------|
| Frontend (Vite) | 3001 | 3000 |
| Backend (Flask) | 5002 | 5001 |
| Neo4j Browser | 7475 | 7474 |
| Neo4j Bolt | 7688 | 7687 |

---

## 7. Core Architecture Decisions

1. **Client-side fallback for demo** — Comparator, Impact Simulator, War Room ใช้ client-side calculation เพื่อ bypass Docker networking issues (auth, timeout). API endpoints มีอยู่จริงใน backend แต่ frontend อาจไม่เรียกใช้

2. **Industry Templates** — JSON-based, importable. มี built-in 2 templates (`energy.json`, `finance.json`) และ uploadable via API (มี `realestate.json`, `fmcg.json`, `insurance_insurtech_th.json`, `retail_ecommerce_th.json` ใน uploads/)

3. **Design System** — `frontend/src/assets/design-system.css` (Linear-inspired premium dark theme) ใช้ CSS custom properties ทุกสี/font/spacing/shadow/border

4. **Multi-tenant** — JWT + API Key auth ผ่าน `tenant_middleware.py`. ทุก endpoint scoped ตาม org_id ใน token

5. **Simulation Engine** — CAMEL-AI OASIS (0.2.5) สำหรับ social media simulation, รองรับ Twitter + Reddit platform actions

6. **LLM Providers** — 7 provider implementations: OpenAI, Anthropic, Google (Gemini), DeepSeek, Groq, Ollama (local), OpenRouter (multi-model gateway). Default deployment uses `deepseek-chat`.

7. **11-Country Persona Factory** — แต่ละประเทศมี context module แยก (`persona_context/`) — ภาษา, วัฒนธรรม, พฤติกรรมผู้บริโภค, แพลตฟอร์มที่นิยม

---

## 8. Remaining Work (Prioritized)

### 🔴 High Priority

1. **Home Page Redesign** — `Home.vue` ยังเป็น legacy (ขาว-ดำ, content เก่า, inline styles แทน design-system.css)
   - Rewrite ทั้ง template + script ให้ใช้ design tokens
   - Content ใหม่ที่สะท้อน 5 ฟีเจอร์ + 4 Industry Templates + B2B value prop
   - Hero: "Simulate Public Opinion. De-risk Decisions. Win Markets."
   - Feature cards: Industry Templates → A/B Compare → Impact Sim → War Room → Export

2. **i18n Completion** — Step Components (Step1-5) + GraphPanel ยังใช้ hardcoded EN/CN, ต้อง refactor ให้ใช้ `$t()`
   - เพิ่ม keys ใน `en.json` และ `th.json`

3. **Export Functionality Testing** — ทดสอบ POST `/api/export/pptx` และ `/api/export/csv` ด้วย campaign ที่มีผลลัพธ์จริง

4. **🔴 Fix Blueprint Prefix Mismatch** — `industry`, `comparator`, `impact`, `competitor`, `export` blueprints ต้องมี `/api/` prefix (หรือเพิ่ม Vite proxy rules) เพื่อให้ frontend เรียก API ได้ผ่าน proxy
   - Fix: `app.register_blueprint(industry_bp, url_prefix='/api/industry')` ใน `__init__.py` (×5 blueprints)
   - หรือ: เพิ่ม proxy rules ใน `vite.config.js` สำหรับ `/industry`, `/comparator`, `/impact`, `/competitor`, `/export`

### 🟡 Medium Priority

5. **More Industry Templates** — ประกันภัย (`insurance_insurtech_th.json`) และ ค้าปลีก (`retail_ecommerce_th.json`) มีไฟล์ใน uploads แล้ว แต่ยังไม่ได้ validate schema
   - สร้าง Healthcare, Education, Travel templates เพิ่ม

6. **Sales Deck / One-Pager** — สำหรับ pitch agency / potential customer
   - PPTX หรือ PDF ที่โชว์ 5 ฟีเจอร์ + mockup screenshots

7. **VPS Deployment** — localhost.run tunnel ไม่เสถียร ควร migrate ไป VPS (DigitalOcean / Hetzner)

### 🟢 Low Priority

8. **Unit Tests** — ปัจจุบันไม่มี test suite. Backend มี `pytest` ใน deps แล้ว แต่ยังไม่มี test files

9. **Error State UI** — หลายหน้าไม่มี empty state / loading state / error state ที่สวย (มีแต่ fallback ธรรมดา)

---

## 9. Database Schema (Neo4j)

Key node labels and relationships:

```
(:Organization) -[:OWNS]-> (:Campaign)
(:Campaign) -[:HAS_PIPELINE]-> (:Pipeline)
(:Campaign) -[:USES_TEMPLATE]-> (:IndustryTemplate)
(:Persona) -[:BELONGS_TO]-> (:Campaign)
(:Report) -[:GENERATED_FOR]-> (:Simulation)
(:Simulation) -[:BASED_ON]-> (:GraphData)
(:GraphData) -[:EXTRACTED_FROM]-> (:Document)

Platform-specific:
(:Agent) -[:ACTS_ON]-> (:Platform)   # Twitter, Reddit
(:Agent) -[:POSTS]-> (:Post)
(:Post) -[:HAS_COMMENT]-> (:Comment)
```

Neo4j constraints use `org_id` property on Campaign, Persona, Report nodes for multi-tenant isolation.

---

## 10. How to Run

### Docker (Recommended)
```bash
cd /Users/chawit/3c-simulator
docker compose -f docker-compose.dev.yml up -d --build
# Frontend: http://localhost:3001
# Backend:  http://localhost:5002
# Neo4j:    http://localhost:7475
```

### Bare Metal Backend
```bash
cd /Users/chawit/3c-simulator/backend
uv sync
uv run python run.py
# Backend: http://localhost:5001
# Requires Neo4j running: docker compose -f docker-compose.dev.yml up -d neo4j-dev
```

### Frontend Only (dev with HMR)
```bash
cd /Users/chawit/3c-simulator/frontend
npm install
npm run dev
# Frontend: http://localhost:3001 (proxies /api/* to backend)
```

---

## 11. Key Files for Quick Navigation

| File | Purpose |
|------|---------|
| `backend/app/__init__.py:84-107` | All blueprint registrations |
| `backend/app/config.py` | All config + validation |
| `frontend/src/router/index.js` | All frontend routes |
| `frontend/src/assets/design-system.css` | CSS custom properties (all colors, fonts, spacing) |
| `frontend/src/locales/en.json` | Primary i18n file (371 lines) |
| `frontend/src/locales/th.json` | Thai translations (339 lines) |
| `backend/app/services/industry_templates/energy.json` | Built-in template (example for new templates) |
| `docs/TEMPLATE_CREATOR_PROMPT.md` | AI prompt for generating new templates |
| `docs/AI_TEMPLATE_GUIDE.md` | Enum constraints + key constraints for template schema |

---

## 12. Known Issues & Gotchas

1. **Docker networking** — Frontend dev server proxy `/api/*` → backend (internal port 5001) แต่ browser เรียกผ่าน localhost:3001. API ที่ต้องการ auth อาจล้มเหลว → หลายฟีเจอร์ใช้ client-side fallback

2. **Industry Template Import Auth** — Import endpoint ต้องการ auth token → ใช้ internal HTTP หรือ import ผ่าน frontend UI เท่านั้น

3. **Template Schema Constraints** — Persona มี ENUM constraints: purchase_style (7), income (4), channels (9), regions (8), objectives (5), impact (3). AI-generated templates ต้อง validate ก่อน import

4. **CSS Conflict** — `Home.vue` ใช้ inline styles (`:style="s.xxx"`) แทนที่ `design-system.css` → ต้อง rewrite

5. **ExportButton** ใน ImpactSimulator อาจไม่ปรากฏทันทีจาก HMR → rebuild Docker

6. **`.env` vs `.env.dev`** — `.env` ใช้สำหรับ bare metal (Neo4j `localhost:7688`), `.env.dev` ใช้สำหรับ Docker (Neo4j `neo4j-dev:7687`)

7. **Windows Compatibility** — `run.py` มี UTF-8 encoding workaround สำหรับ Windows console. ยังไม่เคยทดสอบบน Windows จริง

8. **Duplicate Google Fonts Import** — `index.html` โหลด Inter + JetBrains Mono ผ่าน `<link>` tag โดยตรง, ส่วน `design-system.css` ก็ import Inter + JetBrains Mono ผ่าน `@import` อีกครั้ง → double download. ควรย้ายมาที่เดียว (แนะนำ: เก็บไว้ใน `design-system.css` แล้วเอา `<link>` ออกจาก `index.html`)

9. **Blueprint Prefix Mismatch** (CRITICAL — see §4.1) — `industry`, `comparator`, `impact`, `competitor`, `export` blueprints ลงทะเบียนโดยไม่มี `/api/` prefix ทำให้ Vite proxy ส่ง request ผิด path

---

## 13. Git History (Last 15 Commits)

```
d13ad85 feat: 11-country Persona Factory
97c10b6 docs: comprehensive README for MSaaS platform
17f2007 feat: Phase 6+7 — Thai Persona Factory + Executive Dashboard
d712402 feat: Phase 1 — Multi-Tenant Foundation (MSaaS)
a2167e8 feat: 3C Simulator v0.4 (renamed from 3C Simulator v0.4) — multi-provider, multi-language overhaul
313fe64 fix: force English-only output in report agent
f47fa5c Merge PR #10: fix Neo4j version to 5.18
b372c40 Fix Neo4j version to support relationship vector search
60a574f Merge PR #5: fix GraphToolsService injection
65d0ea2 Merge branch 'main' into fix/report-agent-graph-tools-injection
f2e8e20 fix: inject GraphToolsService into ReportAgent
0eb8083 i18n: fix garbled word-soup docstrings
40b68d3 i18n: translate all remaining comments
58e51c9 i18n: translate LLM prompts
8b08aae i18n: translate report_agent.py
```

Branch: `multilang-v0.3` | Remote: `github.com/chawit1103/MarketingSimulation`

---

## 14. Handoff Checklist

ก่อนส่งมอบให้ AI Codex ทำงานต่อ:

- [ ] อ่านทั้ง `PROGRAM_SPEC.md` นี้ให้จบ
- [ ] รัน `docker compose -f docker-compose.dev.yml ps` เพื่อดูสถานะปัจจุบัน
- [ ] เปิด `http://localhost:3001/campaigns` เพื่อเห็น UI จริง
- [ ] เปิด `http://localhost:3001/comparator` และ `/impact` และ `/war-room` เพื่อเข้าใจฟีเจอร์
- [ ] อ่าน `frontend/src/assets/design-system.css` เพื่อเข้าใจ CSS tokens
- [ ] อ่าน `docs/TEMPLATE_CREATOR_PROMPT.md` ก่อนสร้าง template ใหม่
- [ ] เช็ค `frontend/src/locales/en.json` ก่อนเพิ่ม i18n keys
- [ ] ใช้ `docker compose -f docker-compose.dev.yml up -d --build` เมื่อแก้ backend code
- [ ] Frontend HMR ทำงานอัตโนมัติ — ไม่ต้อง rebuild สำหรับ `.vue` / `.css` / `.js` changes
- [ ] **⚠️ FIX FIRST**: Blueprint prefix mismatch (§4.1) — add `/api/` prefix to 5 blueprints before making API calls
