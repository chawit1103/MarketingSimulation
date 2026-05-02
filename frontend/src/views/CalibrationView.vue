<template>
  <div class="calibration-page">
    <nav class="navbar">
      <div class="nav-brand">3C SIMULATOR</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/calibration" class="nav-link active">Calibration</router-link>
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>
    </nav>

    <main class="calibration-shell">
      <header class="calibration-header">
        <div>
          <span class="page-kicker">Manual Actuals</span>
          <h1>Calibration v1</h1>
          <p>
            Import aggregate post-campaign results, compare them against prior estimates,
            and keep calibration status visible without ingesting raw CRM, customer, or social post data.
          </p>
        </div>
        <router-link to="/campaigns" class="back-link">Back to Campaigns</router-link>
      </header>

      <section class="privacy-banner">
        <strong>No PII or raw posts</strong>
        <span>Use only campaign-level summaries. CSV/JSON uploads are accepted for one aggregate campaign row.</span>
      </section>

      <section class="calibration-layout">
        <form class="input-panel" @submit.prevent="submitManual">
          <div class="panel-heading">
            <h2>Actual Results</h2>
            <p>Analyst/admin access is required because actual campaign data may be sensitive.</p>
          </div>

          <label class="field">
            <span>Campaign ID</span>
            <input v-model.trim="form.campaign_id" required placeholder="cmp_..." />
          </label>

          <div class="field-grid">
            <label class="field">
              <span>Start date</span>
              <input v-model="form.start_date" type="date" />
            </label>
            <label class="field">
              <span>End date</span>
              <input v-model="form.end_date" type="date" />
            </label>
          </div>

          <div class="field-grid">
            <label class="field">
              <span>Impressions</span>
              <input v-model.number="form.impressions" type="number" min="0" />
            </label>
            <label class="field">
              <span>Clicks</span>
              <input v-model.number="form.clicks" type="number" min="0" />
            </label>
            <label class="field">
              <span>CTR %</span>
              <input v-model.number="form.ctr" type="number" step="0.01" />
            </label>
            <label class="field">
              <span>Conversion rate %</span>
              <input v-model.number="form.conversion_rate" type="number" step="0.01" />
            </label>
            <label class="field">
              <span>Conversion count</span>
              <input v-model.number="form.conversion_count" type="number" min="0" />
            </label>
            <label class="field">
              <span>Sentiment score</span>
              <input v-model.number="form.sentiment_score" type="number" min="-100" max="100" />
            </label>
          </div>

          <label class="field">
            <span>Crisis incident</span>
            <select v-model="form.crisis_incident_flag">
              <option value="">Unknown</option>
              <option value="false">No incident</option>
              <option value="true">Incident occurred</option>
            </select>
          </label>

          <div class="panel-heading compact">
            <h2>Prior Estimate</h2>
            <p>Optional. Add estimate fields to calculate delta/error. Leave blank if not available.</p>
          </div>

          <div class="field-grid">
            <label class="field">
              <span>Estimated impressions</span>
              <input v-model.number="form.estimated_impressions" type="number" min="0" />
            </label>
            <label class="field">
              <span>Estimated CTR %</span>
              <input v-model.number="form.estimated_ctr" type="number" step="0.01" />
            </label>
            <label class="field">
              <span>Estimated conversion %</span>
              <input v-model.number="form.estimated_conversion_rate" type="number" step="0.01" />
            </label>
            <label class="field">
              <span>Estimated sentiment</span>
              <input v-model.number="form.estimated_sentiment_score" type="number" min="-100" max="100" />
            </label>
            <label class="field">
              <span>Estimated crisis risk %</span>
              <input v-model.number="form.estimated_crisis_risk" type="number" min="0" max="100" />
            </label>
          </div>

          <label class="field">
            <span>Qualitative notes</span>
            <textarea v-model="form.qualitative_notes" rows="3" placeholder="Anonymized aggregate summary only"></textarea>
          </label>

          <div class="upload-row">
            <label class="file-picker">
              <span>CSV/JSON upload</span>
              <input type="file" accept=".csv,.json,text/csv,application/json" @change="handleFile" />
            </label>
            <button class="btn-secondary" type="button" :disabled="!selectedFile || loading" @click="submitFile">
              Upload file
            </button>
          </div>

          <button class="btn-primary" type="submit" :disabled="loading">
            {{ loading ? 'Importing...' : 'Import Actual Results' }}
          </button>

          <p v-if="error" class="error-box">{{ error }}</p>
        </form>

        <section class="results-panel">
          <div v-if="!result && !loading" class="empty-state">
            <h2>Ready to calibrate</h2>
            <p>Import aggregate actuals to see estimate-vs-actual deltas, risk matching, privacy review, and calibration status.</p>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Checking actual results...</p>
          </div>

          <div v-if="result" class="result-stack">
            <div class="result-head">
              <div>
                <span class="page-kicker">{{ result.calibration_status }}</span>
                <h2>{{ result.campaign_id }}</h2>
                <p>{{ result.source?.warning }}</p>
              </div>
              <ResultSourceBadge :source="result.source?.source_mode" :warning="result.source?.warning" />
            </div>

            <div class="status-grid">
              <div>
                <span>Status</span>
                <strong>{{ statusLabel(result.calibration_status) }}</strong>
              </div>
              <div>
                <span>Risk classification</span>
                <strong>{{ statusLabel(result.risk_classification) }}</strong>
              </div>
              <div>
                <span>Privacy review</span>
                <strong>{{ result.privacy_review?.pii_detected ? 'Needs review' : 'Aggregate only' }}</strong>
              </div>
            </div>

            <div class="result-section">
              <h3>Estimate vs Actual</h3>
              <div v-if="result.comparison?.length" class="comparison-table">
                <div class="table-row table-head">
                  <span>Metric</span>
                  <span>Estimate</span>
                  <span>Actual</span>
                  <span>Delta</span>
                  <span>Error</span>
                </div>
                <div v-for="row in result.comparison" :key="row.metric" class="table-row">
                  <span>{{ statusLabel(row.metric) }}</span>
                  <span>{{ formatMetric(row.estimate) }}</span>
                  <span>{{ formatMetric(row.actual) }}</span>
                  <strong>{{ signed(row.delta) }}</strong>
                  <span>{{ row.absolute_error_pct === null ? 'n/a' : `${row.absolute_error_pct}%` }}</span>
                </div>
              </div>
              <p v-else class="muted">No comparable estimate fields were supplied. Status remains not calibrated until estimates and actuals can be compared.</p>
            </div>

            <div class="result-section two-col">
              <div>
                <h3>Limitations</h3>
                <ul class="compact-list">
                  <li v-for="item in result.limitations" :key="item">{{ item }}</li>
                </ul>
              </div>
              <div>
                <h3>Next validation step</h3>
                <p class="muted">{{ result.recommended_validation_step }}</p>
              </div>
            </div>
          </div>
        </section>
      </section>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import ResultSourceBadge from '@/components/ResultSourceBadge.vue'
import { importActualResults } from '@/api/calibration'

const form = reactive({
  campaign_id: 'demo-premium-water',
  start_date: '',
  end_date: '',
  impressions: 120000,
  clicks: 3600,
  ctr: 3.0,
  conversion_count: 1680,
  conversion_rate: 1.4,
  sentiment_score: 62,
  crisis_incident_flag: 'false',
  estimated_impressions: 100000,
  estimated_ctr: 2.5,
  estimated_conversion_rate: 1.2,
  estimated_sentiment_score: 58,
  estimated_crisis_risk: 25,
  qualitative_notes: 'Aggregate launch readout: proof-led creative performed better than price-led copy.',
})

const result = ref(null)
const loading = ref(false)
const error = ref('')
const selectedFile = ref(null)

function cleanPayload() {
  return Object.fromEntries(
    Object.entries(form).filter(([, value]) => value !== '' && value !== null && value !== undefined)
  )
}

async function submitManual() {
  await submitPayload(cleanPayload())
}

function handleFile(event) {
  selectedFile.value = event.target.files?.[0] || null
}

async function submitFile() {
  if (!selectedFile.value) return
  const data = new FormData()
  data.append('file', selectedFile.value)
  await submitPayload(data)
}

async function submitPayload(payload) {
  loading.value = true
  error.value = ''
  try {
    const response = await importActualResults(payload)
    result.value = response.data || response
  } catch (err) {
    const status = err?.response?.status
    if (status === 401 || status === 403) {
      error.value = 'Calibration import requires analyst/admin access. No local calibration was generated automatically.'
    } else {
      error.value = err?.response?.data?.error || err?.message || 'Calibration import failed.'
    }
  } finally {
    loading.value = false
  }
}

function statusLabel(value) {
  return String(value || 'unknown').replaceAll('_', ' ')
}

function formatMetric(value) {
  if (value === null || value === undefined) return 'n/a'
  return Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 })
}

function signed(value) {
  const n = Number(value || 0)
  return `${n >= 0 ? '+' : ''}${formatMetric(n)}`
}
</script>

<style scoped>
.calibration-page {
  min-height: 100vh;
  background: var(--bg-canvas);
  color: var(--text-primary);
}

.navbar {
  height: 72px;
  padding: 0 var(--space-8);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-glass);
  backdrop-filter: blur(18px);
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 900;
  color: var(--accent);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 800;
}

.nav-link:hover,
.nav-link.active {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.calibration-shell {
  max-width: 1320px;
  margin: 0 auto;
  padding: var(--space-10) var(--space-8) var(--space-16);
}

.calibration-header {
  display: flex;
  justify-content: space-between;
  gap: var(--space-6);
  align-items: flex-start;
  margin-bottom: var(--space-5);
}

.page-kicker {
  display: inline-block;
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
  margin-bottom: var(--space-2);
}

.calibration-header h1 {
  margin: 0 0 var(--space-3);
  font-family: var(--font-display);
  font-size: clamp(2.1rem, 4vw, 3.4rem);
  line-height: 1.04;
}

.calibration-header p,
.panel-heading p,
.result-head p,
.empty-state p,
.muted {
  max-width: 760px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0;
}

.back-link {
  color: var(--accent);
  font-weight: 900;
  text-decoration: none;
  white-space: nowrap;
}

.privacy-banner {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  padding: var(--space-4);
  margin-bottom: var(--space-6);
  border: 1px solid var(--yellow);
  border-radius: var(--radius-md);
  background: var(--yellow-soft);
  color: var(--text-primary);
}

.calibration-layout {
  display: grid;
  grid-template-columns: minmax(320px, 460px) minmax(0, 1fr);
  gap: var(--space-6);
  align-items: start;
}

.input-panel,
.results-panel {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  box-shadow: var(--shadow-card);
}

.input-panel {
  padding: var(--space-6);
  display: grid;
  gap: var(--space-4);
}

.panel-heading h2,
.result-head h2,
.result-section h3,
.empty-state h2 {
  margin: 0 0 var(--space-2);
  color: var(--text-primary);
}

.panel-heading.compact {
  padding-top: var(--space-2);
  border-top: 1px solid var(--border-subtle);
}

.field {
  display: grid;
  gap: var(--space-2);
}

.field span,
.file-picker span,
.status-grid span {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: 800;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-primary);
  padding: 12px;
  font: inherit;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-3);
}

.upload-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: var(--space-3);
  align-items: end;
}

.file-picker {
  display: grid;
  gap: var(--space-2);
}

.btn-primary,
.btn-secondary {
  border: none;
  border-radius: var(--radius-md);
  padding: 14px 18px;
  font-weight: 900;
  cursor: pointer;
}

.btn-primary {
  background: var(--accent);
  color: var(--text-inverse);
}

.btn-secondary {
  background: var(--bg-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.62;
  cursor: wait;
}

.error-box {
  margin: 0;
  padding: var(--space-3);
  border: 1px solid var(--red);
  border-radius: var(--radius-md);
  color: var(--red);
  background: var(--red-soft);
}

.results-panel {
  min-height: 620px;
  padding: var(--space-6);
}

.empty-state,
.loading-state {
  min-height: 520px;
  display: grid;
  place-content: center;
  text-align: center;
  gap: var(--space-3);
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border-default);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-stack,
.result-section {
  display: grid;
  gap: var(--space-5);
}

.result-head {
  display: flex;
  justify-content: space-between;
  gap: var(--space-5);
  align-items: flex-start;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-3);
}

.status-grid div {
  display: grid;
  gap: var(--space-1);
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.comparison-table {
  display: grid;
  overflow-x: auto;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.table-row {
  display: grid;
  grid-template-columns: 1.35fr repeat(4, minmax(88px, 1fr));
  gap: var(--space-3);
  padding: var(--space-3);
  border-top: 1px solid var(--border-subtle);
  min-width: 620px;
}

.table-row:first-child {
  border-top: none;
}

.table-head {
  color: var(--text-secondary);
  background: var(--bg-surface);
  font-weight: 900;
}

.two-col {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.compact-list {
  margin: 0;
  padding-left: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 980px) {
  .calibration-layout,
  .two-col,
  .status-grid {
    grid-template-columns: 1fr;
  }

  .calibration-header,
  .result-head,
  .privacy-banner {
    flex-direction: column;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: flex-end;
  }
}

@media (max-width: 640px) {
  .navbar {
    height: auto;
    padding: var(--space-4);
    gap: var(--space-3);
    align-items: flex-start;
  }

  .field-grid,
  .upload-row {
    grid-template-columns: 1fr;
  }

  .calibration-shell {
    padding: var(--space-6) var(--space-4) var(--space-10);
  }
}
</style>
