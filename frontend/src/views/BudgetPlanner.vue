<template>
  <div class="budget-page">
    <nav class="navbar">
      <div class="nav-brand">3C SIMULATOR</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/budget-planner" class="nav-link active">Budget Planner</router-link>
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>
    </nav>

    <main class="planner-shell">
      <header class="planner-header">
        <div>
          <span class="page-kicker">Scenario Estimate</span>
          <h1>Budget Scenario Planner</h1>
          <p>
            Explore directional channel and segment allocation ranges before committing spend.
            This is assumption-based planning, not exact ROI or ROAS prediction.
          </p>
        </div>
        <router-link to="/campaigns" class="back-link">Back to Campaigns</router-link>
      </header>

      <section class="planner-layout">
        <form class="input-panel" @submit.prevent="runScenario">
          <div class="panel-heading">
            <h2>Inputs</h2>
            <p>Use approved planning numbers or demo-safe assumptions only.</p>
          </div>

          <label class="field">
            <span>Total budget</span>
            <input v-model.number="form.total_budget" type="number" min="0" step="50000" />
          </label>

          <label class="field">
            <span>Campaign duration (weeks)</span>
            <input v-model.number="form.duration_weeks" type="number" min="1" max="52" />
          </label>

          <div class="field-grid">
            <label class="field">
              <span>Objective</span>
              <select v-model="form.objective">
                <option value="awareness">Awareness</option>
                <option value="conversion">Conversion</option>
                <option value="retention">Retention</option>
                <option value="crisis_recovery">Crisis recovery</option>
              </select>
            </label>

            <label class="field">
              <span>Risk tolerance</span>
              <select v-model="form.risk_tolerance">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>
          </div>

          <label class="field">
            <span>Target segments</span>
            <textarea v-model="segmentsText" rows="3" placeholder="Urban families, Creator-led discovery, Price-sensitive shoppers"></textarea>
          </label>

          <div class="channel-mix">
            <div class="mix-heading">
              <span>Channel mix what-if</span>
              <strong>{{ mixTotal }}%</strong>
            </div>
            <label v-for="channel in channels" :key="channel.key" class="channel-row">
              <span>{{ channel.label }}</span>
              <input v-model.number="form.channel_mix[channel.key]" type="range" min="0" max="60" step="5" />
              <strong>{{ form.channel_mix[channel.key] }}%</strong>
            </label>
          </div>

          <label class="demo-toggle">
            <input v-model="form.demo" type="checkbox" />
            <span>Run as Demo Mode fixture</span>
          </label>

          <button class="btn-primary" type="submit" :disabled="loading">
            {{ loading ? 'Planning...' : 'Run Budget Scenario' }}
          </button>

          <p v-if="error" class="error-box">{{ error }}</p>
        </form>

        <section class="results-panel">
          <div v-if="!result && !loading" class="empty-state">
            <h2>Ready for a budget what-if</h2>
            <p>Run a scenario to see allocation ranges, trade-offs, confidence, assumptions, and validation steps.</p>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Creating scenario estimate...</p>
          </div>

          <div v-if="result" class="result-stack">
            <div class="result-head">
              <div>
                <span class="page-kicker">{{ result.objective.replace('_', ' ') }}</span>
                <h2>{{ formatCurrency(result.total_budget) }} over {{ result.duration_weeks }} weeks</h2>
                <p>{{ result.disclaimer }}</p>
              </div>
              <ResultSourceBadge
                :source="result.source?.type"
                :warning="result.source?.warning"
              />
            </div>

            <div class="confidence-band">
              <div>
                <span>Confidence</span>
                <strong>{{ confidenceLabel(result.confidence_level) }}</strong>
              </div>
              <div>
                <span>Score</span>
                <strong>{{ result.confidence_score }}/100</strong>
              </div>
              <div>
                <span>Validation</span>
                <strong>{{ result.recommended_validation_step }}</strong>
              </div>
            </div>

            <div class="result-section">
              <h3>Suggested Allocation Range by Channel</h3>
              <div class="allocation-list">
                <article v-for="item in result.allocation_ranges" :key="item.channel" class="allocation-item">
                  <div class="allocation-top">
                    <strong>{{ formatChannel(item.channel) }}</strong>
                    <span>{{ item.recommended_pct_midpoint }}%</span>
                  </div>
                  <div class="range-bar">
                    <span :style="{ width: `${Math.max(item.recommended_pct_midpoint, 5)}%` }"></span>
                  </div>
                  <div class="money-row">
                    <span>{{ formatCurrency(item.budget_range.low) }}</span>
                    <strong>{{ formatCurrency(item.budget_range.midpoint) }}</strong>
                    <span>{{ formatCurrency(item.budget_range.high) }}</span>
                  </div>
                  <p>{{ item.role }}</p>
                  <small>{{ item.risk_note }}</small>
                </article>
              </div>
            </div>

            <div class="result-section two-col">
              <div>
                <h3>Segment Ranges</h3>
                <ul class="plain-list">
                  <li v-for="segment in result.segment_allocation_ranges" :key="segment.segment">
                    <strong>{{ segment.segment }}</strong>
                    <span>{{ formatCurrency(segment.budget_range.low) }} - {{ formatCurrency(segment.budget_range.high) }}</span>
                  </li>
                </ul>
              </div>
              <div>
                <h3>Trade-offs</h3>
                <ul class="plain-list">
                  <li v-for="tradeoff in result.trade_offs" :key="tradeoff.choice">
                    <strong>{{ tradeoff.choice }}</strong>
                    <span>{{ tradeoff.upside }} Risk: {{ tradeoff.risk }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <div class="result-section two-col">
              <div>
                <h3>Assumptions</h3>
                <ul class="compact-list">
                  <li v-for="item in result.assumptions" :key="item">{{ item }}</li>
                </ul>
              </div>
              <div>
                <h3>Limitations</h3>
                <ul class="compact-list">
                  <li v-for="item in result.limitations" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, reactive, ref, onMounted } from 'vue'
import ResultSourceBadge from '@/components/ResultSourceBadge.vue'
import { runBudgetScenario } from '@/api/budget'
import { sourceModeFromValue, trackEvent } from '@/services/analytics'

const channels = [
  { key: 'facebook', label: 'Facebook' },
  { key: 'instagram', label: 'Instagram' },
  { key: 'tiktok', label: 'TikTok' },
  { key: 'youtube', label: 'YouTube' },
  { key: 'line', label: 'LINE' },
  { key: 'twitter_x', label: 'Twitter/X' },
]

const form = reactive({
  total_budget: 2500000,
  duration_weeks: 8,
  objective: 'conversion',
  risk_tolerance: 'medium',
  demo: true,
  channel_mix: {
    facebook: 30,
    instagram: 20,
    tiktok: 25,
    youtube: 10,
    line: 15,
    twitter_x: 0,
  },
})

const segmentsText = ref('Urban families, Creator-led discovery, Price-sensitive shoppers')
const result = ref(null)
const loading = ref(false)
const error = ref('')

const mixTotal = computed(() => Object.values(form.channel_mix).reduce((sum, value) => sum + Number(value || 0), 0))

function targetSegments() {
  return segmentsText.value
    .split(',')
    .map((segment) => segment.trim())
    .filter(Boolean)
}

async function runScenario() {
  loading.value = true
  error.value = ''
  try {
    const response = await runBudgetScenario({
      ...form,
      target_segments: targetSegments(),
      currency: 'THB',
    })
    result.value = response.data || response
    trackEvent('budget_scenario_run', {
      source_mode: sourceModeFromValue(result.value?.source?.type || result.value?.source?.source_mode),
      objective: result.value?.objective || form.objective,
      risk_tolerance: result.value?.risk_tolerance || form.risk_tolerance,
      channel_count: Object.values(form.channel_mix).filter(value => Number(value || 0) > 0).length,
      segment_count: targetSegments().length,
      duration_weeks: Number(form.duration_weeks || 0),
      demo: Boolean(form.demo),
    })
  } catch (err) {
    error.value = 'Budget scenario planner is unavailable. No local estimate was generated automatically.'
  } finally {
    loading.value = false
  }
}

function formatCurrency(value) {
  const n = Number(value || 0)
  if (n >= 1000000) return `THB ${(n / 1000000).toFixed(1)}M`
  if (n >= 1000) return `THB ${(n / 1000).toFixed(0)}K`
  return `THB ${Math.round(n)}`
}

function formatChannel(channel) {
  return String(channel || '').replace('_', '/').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function confidenceLabel(level) {
  return String(level || 'unknown').replaceAll('_', ' ')
}

onMounted(runScenario)
</script>

<style scoped>
.budget-page {
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

.planner-shell {
  max-width: 1320px;
  margin: 0 auto;
  padding: var(--space-10) var(--space-8) var(--space-16);
}

.planner-header {
  display: flex;
  justify-content: space-between;
  gap: var(--space-6);
  align-items: flex-start;
  margin-bottom: var(--space-8);
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

.planner-header h1 {
  margin: 0 0 var(--space-3);
  font-family: var(--font-display);
  font-size: clamp(2.1rem, 4vw, 3.4rem);
  line-height: 1.04;
}

.planner-header p,
.panel-heading p,
.result-head p,
.empty-state p {
  max-width: 720px;
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

.planner-layout {
  display: grid;
  grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
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

.field {
  display: grid;
  gap: var(--space-2);
}

.field span,
.mix-heading span,
.channel-row span {
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
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.channel-mix {
  display: grid;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.mix-heading,
.channel-row,
.money-row,
.allocation-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.channel-row input {
  flex: 1;
}

.demo-toggle {
  display: flex;
  gap: var(--space-2);
  align-items: center;
  color: var(--text-secondary);
  font-weight: 800;
}

.btn-primary {
  border: none;
  border-radius: var(--radius-md);
  background: var(--accent);
  color: var(--text-inverse);
  padding: 14px 18px;
  font-weight: 900;
  cursor: pointer;
}

.btn-primary:disabled {
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

.result-stack {
  display: grid;
  gap: var(--space-6);
}

.result-head {
  display: flex;
  justify-content: space-between;
  gap: var(--space-5);
  align-items: flex-start;
}

.confidence-band {
  display: grid;
  grid-template-columns: 150px 110px minmax(0, 1fr);
  gap: var(--space-3);
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.confidence-band span {
  display: block;
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  margin-bottom: 4px;
}

.confidence-band strong {
  color: var(--text-primary);
  text-transform: capitalize;
}

.result-section {
  display: grid;
  gap: var(--space-3);
}

.allocation-list {
  display: grid;
  gap: var(--space-3);
}

.allocation-item {
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.range-bar {
  height: 8px;
  margin: var(--space-3) 0;
  border-radius: var(--radius-pill);
  background: var(--bg-elevated);
  overflow: hidden;
}

.range-bar span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--accent);
}

.money-row {
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.allocation-item p,
.allocation-item small {
  display: block;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: var(--space-2) 0 0;
}

.allocation-item small {
  color: var(--text-tertiary);
}

.two-col {
  grid-template-columns: 1fr 1fr;
}

.plain-list,
.compact-list {
  display: grid;
  gap: var(--space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.plain-list li,
.compact-list li {
  padding: var(--space-3);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.plain-list strong {
  display: block;
  margin-bottom: 4px;
}

.plain-list span,
.compact-list li {
  color: var(--text-secondary);
  line-height: 1.55;
}

@media (max-width: 900px) {
  .navbar,
  .planner-header,
  .result-head {
    flex-direction: column;
    align-items: stretch;
  }

  .planner-layout,
  .two-col,
  .confidence-band,
  .field-grid {
    grid-template-columns: 1fr;
  }

  .nav-links {
    flex-wrap: wrap;
  }
}
</style>
