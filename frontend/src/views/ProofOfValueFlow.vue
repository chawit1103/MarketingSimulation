<template>
  <div class="pov-page">
    <nav class="navbar">
      <div class="nav-brand">3C SIMULATOR</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/comparator" class="nav-link">Comparator</router-link>
        <router-link to="/budget-planner" class="nav-link">Budget Planner</router-link>
        <router-link to="/resources" class="nav-link">Resources</router-link>
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>
    </nav>

    <main class="pov-shell">
      <header class="pov-header">
        <div>
          <span class="page-kicker">Proof of Value</span>
          <h1>Approved Brief to Strategy Pack</h1>
          <p>
            Assemble one customer-approved campaign brief into an operator checklist, structured payload,
            and customer-facing deliverable sequence without PII, raw CRM records, secrets, or live integrations.
          </p>
        </div>
        <ResultSourceBadge
          source="local_estimate"
          warning="Operator worksheet from an approved brief. Not backend-verified output."
        />
      </header>

      <section class="guardrail-strip" aria-label="Proof-of-value guardrails">
        <span v-for="guardrail in proofPackage.guardrails" :key="guardrail">{{ guardrail }}</span>
      </section>

      <section class="ai-helper-panel" aria-label="Prepare brief with AI prompt pack">
        <div>
          <span class="page-kicker">มีแค่โจทย์ดิบ?</span>
          <h2>ใช้ Prompt Pack เพื่อเตรียม Brief</h2>
          <p>
            ให้ ChatGPT/Claude/Gemini ช่วยแปลงโจทย์ภาษาไทยเป็น brief ที่พร้อมให้ operator ตรวจ ก่อนนำมากรอกแบบปลอดภัย.
            แอปนี้ไม่ส่งข้อมูลไป external AI provider และยังต้องห้าม PII, raw CRM, customer lists, secrets, และ live integrations.
          </p>
        </div>
        <div class="helper-links">
          <a v-for="link in aiHelperLinks" :key="link.href" :href="link.href" target="_blank" rel="noreferrer">
            {{ link.label }}
          </a>
          <router-link to="/resources">Resources Hub</router-link>
        </div>
      </section>

      <section class="pov-layout">
        <form class="intake-panel" @submit.prevent>
          <div class="panel-heading">
            <h2>Customer Brief Intake</h2>
            <p>Use one approved campaign brief or historical scenario. Keep personal and customer-record data out.</p>
          </div>

          <div class="field-grid">
            <label v-for="field in primaryFields" :key="field.key" class="field">
              <span>{{ field.label }}</span>
              <input
                v-if="field.rows === 1"
                v-model="intake[field.key]"
                type="text"
                :placeholder="field.placeholder"
              />
              <textarea
                v-else
                v-model="intake[field.key]"
                :rows="field.rows"
                :placeholder="field.placeholder"
              ></textarea>
            </label>
          </div>

          <fieldset class="approval-panel">
            <legend>Approval Confirmations</legend>
            <label v-for="item in confirmationItems" :key="item.key" class="check-row">
              <input v-model="intake.confirmations[item.key]" type="checkbox" />
              <span>{{ item.label }}</span>
            </label>
            <label class="check-row">
              <input v-model="intake.confirmations.aggregateActualsApproved" type="checkbox" />
              <span>Aggregate actuals are approved and aggregate-only if provided</span>
            </label>
          </fieldset>
        </form>

        <aside class="workflow-panel">
          <section :class="['status-panel', proofPackage.validation.ready ? 'ready' : 'blocked']">
            <span class="page-kicker">Operator Status</span>
            <h2>{{ proofPackage.validation.ready ? 'Ready for Operator Review' : 'Blocked Until Safe and Approved' }}</h2>
            <p>
              Decision-support estimate, not a guaranteed prediction. This workflow does not approve production SaaS,
              public pilot access, public internet exposure, exact ROI/ROAS, or live customer-data integrations.
            </p>
          </section>

          <section v-if="blockers.length" class="review-panel">
            <h3>Blockers</h3>
            <ul>
              <li v-for="blocker in blockers" :key="blocker">{{ blocker }}</li>
            </ul>
          </section>

          <section v-if="proofPackage.validation.unsafeSignals.length" class="review-panel warning">
            <h3>Unsafe Intake Signals</h3>
            <ul>
              <li v-for="signal in proofPackage.validation.unsafeSignals" :key="`${signal.field}-${signal.reason}`">
                <strong>{{ signal.field }}:</strong> {{ signal.reason }}
              </li>
            </ul>
          </section>

          <section class="review-panel">
            <h3>Deliverable Sequence</h3>
            <ol>
              <li v-for="step in proofPackage.workflow_steps" :key="step">{{ step }}</li>
            </ol>
          </section>

          <section class="review-panel">
            <h3>Customer Outputs</h3>
            <ul class="tag-list">
              <li v-for="deliverable in proofPackage.deliverables" :key="deliverable">{{ deliverable }}</li>
            </ul>
          </section>
        </aside>
      </section>

      <section class="payload-panel">
        <div class="panel-heading">
          <h2>Structured Operator Payload</h2>
          <p>Unsafe fields are blocked from this generated package until the intake is corrected.</p>
        </div>
        <pre class="payload-preview">{{ structuredPayload }}</pre>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'
import ResultSourceBadge from '@/components/ResultSourceBadge.vue'
import {
  buildProofOfValuePackage,
  defaultProofOfValueIntake,
  proofOfValueConfirmations,
} from '@/services/proofOfValue'

const intake = reactive(defaultProofOfValueIntake())

const githubBlobRoot = 'https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/'

const aiHelperLinks = [
  { label: 'AI Research Prompt Pack', href: `${githubBlobRoot}docs/AI_RESEARCH_PROMPT_PACK.md` },
  { label: 'Intake Import Template', href: `${githubBlobRoot}docs/POV_INTAKE_IMPORT_TEMPLATE.md` },
]

const primaryFields = [
  { key: 'campaignNameOrCode', label: 'Campaign name or anonymized code', rows: 1, placeholder: 'POV-WATER-001 or approved campaign name' },
  { key: 'productService', label: 'Product/service', rows: 1, placeholder: 'Product, service, or offer' },
  { key: 'objective', label: 'Objective', rows: 2, placeholder: 'What decision should this proof-of-value session support?' },
  { key: 'targetSegment', label: 'Target segment', rows: 2, placeholder: 'Audience or segment, without personal records' },
  { key: 'marketContext', label: 'Market context', rows: 3, placeholder: 'Category, demand, timing, and constraints' },
  { key: 'channelPlan', label: 'Channel plan', rows: 2, placeholder: 'Owned, paid, earned, retail, events, or partner channels' },
  { key: 'budgetBand', label: 'Budget band', rows: 1, placeholder: 'Broad band only unless exact figures are approved' },
  { key: 'competitorContext', label: 'Competitor context', rows: 2, placeholder: 'Relevant competitors or substitute choices' },
  { key: 'creativeA', label: 'Creative direction A', rows: 2, placeholder: 'First message or execution route' },
  { key: 'creativeB', label: 'Creative direction B', rows: 2, placeholder: 'Second message or execution route' },
  { key: 'creativeC', label: 'Creative direction C', rows: 2, placeholder: 'Third message or execution route' },
  { key: 'riskConcerns', label: 'Risk concerns', rows: 2, placeholder: 'Sensitivity, compliance, backlash, or trust risks' },
  { key: 'successKpis', label: 'Success KPIs', rows: 2, placeholder: 'Awareness, consideration, leads, trust, or other approved KPIs' },
  { key: 'aggregateActuals', label: 'Optional aggregate actuals', rows: 2, placeholder: 'Aggregate-only historical ranges if approved' },
]

const confirmationItems = proofOfValueConfirmations

const proofPackage = computed(() => buildProofOfValuePackage(intake))

const blockers = computed(() => [
  ...proofPackage.value.validation.missingFields.map((field) => `Missing required field: ${field}`),
  ...proofPackage.value.validation.missingConfirmations.map((item) => `Missing confirmation: ${item}`),
])

const structuredPayload = computed(() => JSON.stringify(proofPackage.value, null, 2))
</script>

<style scoped>
.pov-page {
  min-height: 100vh;
  color: var(--text-secondary);
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-8);
  background: var(--bg-glass);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(18px);
}

.nav-brand {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-weight: 900;
  letter-spacing: 0;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.nav-link {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 800;
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-muted);
}

.pov-shell {
  width: min(1480px, calc(100% - 32px));
  margin: 0 auto;
  padding: var(--space-8) 0 var(--space-16);
}

.pov-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(260px, 420px);
  gap: var(--space-8);
  align-items: end;
  margin-bottom: var(--space-6);
}

.pov-header h1 {
  margin-bottom: var(--space-4);
}

.pov-header p,
.panel-heading p,
.status-panel p {
  max-width: 860px;
  color: var(--text-secondary);
}

.page-kicker {
  display: block;
  margin-bottom: var(--space-2);
  color: var(--teal);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.guardrail-strip {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
}

.ai-helper-panel {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(240px, auto);
  gap: var(--space-5);
  align-items: center;
  margin-bottom: var(--space-6);
  padding: var(--space-5);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  box-shadow: var(--shadow-card);
}

.ai-helper-panel h2 {
  margin: 0 0 var(--space-2);
}

.ai-helper-panel p {
  margin: 0;
  max-width: 900px;
  color: var(--text-secondary);
}

.helper-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  justify-content: flex-end;
}

.helper-links a {
  display: inline-flex;
  align-items: center;
  min-height: 36px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 800;
  text-decoration: none;
}

.helper-links a:hover {
  border-color: var(--border-accent);
  background: var(--bg-muted);
}

.guardrail-strip span,
.tag-list li {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  background: var(--bg-panel);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: 800;
}

.pov-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(340px, 0.75fr);
  gap: var(--space-6);
  align-items: start;
}

.intake-panel,
.workflow-panel,
.payload-panel,
.review-panel,
.status-panel {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  box-shadow: var(--shadow-card);
}

.intake-panel,
.payload-panel {
  padding: var(--space-6);
}

.workflow-panel {
  display: grid;
  gap: var(--space-4);
  padding: var(--space-4);
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.field {
  display: grid;
  gap: var(--space-2);
}

.field span,
.approval-panel legend {
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 900;
}

.field input,
.field textarea {
  width: 100%;
  min-width: 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  color: var(--text-primary);
  padding: var(--space-3);
  resize: vertical;
}

.field input:focus,
.field textarea:focus {
  outline: 2px solid var(--teal-soft);
  border-color: var(--teal);
}

.approval-panel {
  display: grid;
  gap: var(--space-2);
  margin: var(--space-6) 0 0;
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
}

.check-row {
  display: grid;
  grid-template-columns: 18px minmax(0, 1fr);
  gap: var(--space-3);
  align-items: start;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: 700;
}

.status-panel,
.review-panel {
  padding: var(--space-5);
}

.status-panel.ready {
  border-color: var(--green);
  background: var(--green-soft);
}

.status-panel.blocked {
  border-color: var(--yellow);
  background: var(--yellow-soft);
}

.review-panel.warning {
  border-color: var(--red);
  background: var(--red-soft);
}

.review-panel ul,
.review-panel ol {
  margin: var(--space-3) 0 0;
  padding-left: var(--space-5);
}

.review-panel li {
  margin-bottom: var(--space-2);
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding: 0;
  list-style: none;
}

.payload-panel {
  margin-top: var(--space-6);
}

.payload-preview {
  overflow: auto;
  max-height: 520px;
  margin: 0;
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.5;
  white-space: pre-wrap;
}

@media (max-width: 980px) {
  .pov-header,
  .ai-helper-panel,
  .pov-layout,
  .field-grid {
    grid-template-columns: 1fr;
  }

  .helper-links {
    justify-content: flex-start;
  }

  .navbar {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
