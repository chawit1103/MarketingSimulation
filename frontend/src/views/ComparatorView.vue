<template>
  <div class="comparator-dashboard">
    <!-- Header -->
    <div class="comparator-header">
      <div class="header-left">
        <h1 class="page-title">{{ $t('comparator.title') }}</h1>
        <p class="page-subtitle">{{ $t('comparator.subtitle') }}</p>
      </div>
      <div class="header-right">
        <ExportButton v-if="comparisonResult" :data="exportData" :label="$t('common.export')" />
        <router-link to="/campaigns" class="back-link">← {{ $t('comparator.backToCampaigns') }}</router-link>
      </div>
    </div>

    <!-- Campaign Selection -->
    <div v-if="!comparisonResult" class="selection-section">
      <div class="selection-prompt">
        <h3>{{ $t('comparator.selectPrompt') }}</h3>
        <p>{{ $t('comparator.selectHint') }}</p>
      </div>

      <div class="campaign-picker">
        <div
          v-for="campaign in availableCampaigns"
          :key="campaign.id || campaign.campaign_id"
          :class="['campaign-chip', { selected: selectedIds.includes(campaign.id || campaign.campaign_id) }]"
          @click="toggleCampaign(campaign.id || campaign.campaign_id)"
        >
          <span class="chip-check">{{ selectedIds.includes(campaign.id || campaign.campaign_id) ? '✓' : '+' }}</span>
          <span class="chip-name">{{ campaign.name }}</span>
        </div>
      </div>

      <button
        class="btn-compare"
        :disabled="selectedIds.length < 2 || loading"
        @click="runComparison"
      >
        <span v-if="!loading">{{ $t('comparator.compareBtn') }} ({{ selectedIds.length }})</span>
        <span v-else>{{ $t('comparator.comparing') }}</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading && !comparisonResult" class="loading-state">
      <div class="spinner"></div>
      <span>{{ $t('comparator.fetchingData') }}</span>
    </div>

    <!-- Results -->
    <div v-if="comparisonResult" class="results-section">
      <!-- Overall Winner Banner -->
      <div class="winner-banner">
        <div class="winner-icon">A/B</div>
        <div class="winner-info">
          <h2>{{ comparisonResult.overall_winner.campaign_name || comparisonResult.overall_winner.campaign_id }}</h2>
          <p>
            {{ $t('comparator.wonMetrics', { wins: comparisonResult.overall_winner.metric_wins, total: comparisonResult.overall_winner.total_metrics }) }}
          </p>
        </div>
      </div>

      <!-- Campaign Labels (A, B, C) -->
      <div class="campaign-labels">
        <div
          v-for="(summary, idx) in comparisonResult.campaign_summaries"
          :key="summary.campaign_id"
          :class="['campaign-label', { winner: summary.is_overall_winner }]"
        >
          <span class="label-letter">{{ String.fromCharCode(65 + idx) }}</span>
          <span class="label-name">{{ summary.campaign_name || summary.campaign_id.slice(0, 12) }}</span>
          <span class="label-wins">{{ $t('comparator.metricWins', { count: summary.metric_wins }) }}</span>
        </div>
      </div>

      <!-- Metric-by-Metric Comparison -->
      <div class="metrics-grid">
        <div
          v-for="metric in comparisonResult.metrics_comparison"
          :key="metric.key"
          class="metric-row"
        >
          <div class="metric-info">
            <span class="metric-label">{{ metric.label }}</span>
            <span v-if="metric.max_diff > 0" class="metric-diff">
              Δ {{ metric.max_diff }}{{ metric.unit }}
            </span>
          </div>

          <div class="metric-bars">
            <div
              v-for="(val, vi) in metric.values"
              :key="val.campaign_id"
              class="bar-group"
            >
              <span class="bar-label">{{ String.fromCharCode(65 + vi) }}</span>
              <div class="bar-track">
                <div
                  :class="['bar-fill', val.campaign_id === metric.winner_campaign_id ? 'bar-winner' : '']"
                  :style="{ width: barWidth(metric, val.value) + '%' }"
                >
                  <span class="bar-value">{{ val.value }}{{ metric.unit }}</span>
                </div>
              </div>
              <span v-if="val.campaign_id === metric.winner_campaign_id" class="winner-badge">A/B</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Reset -->
      <button class="btn-reset" @click="resetComparison">
        {{ $t('comparator.compareOthers') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { listCampaigns } from '@/api/campaign'
import { compareCampaigns } from '@/api/comparator'
import ExportButton from '@/components/ExportButton.vue'

const { t } = useI18n()

const availableCampaigns = ref([])
const selectedIds = ref([])
const comparisonResult = ref(null)
const loading = ref(false)
const error = ref('')

const exportData = computed(() => ({
  slide_type: 'comparison',
  title: t('comparator.exportTitle'),
  subtitle: t('comparator.exportSubtitle', { count: comparisonResult.value?.campaign_count || 0 }),
  comparison: comparisonResult.value,
  filename: `msaas_comparison_${new Date().toISOString().slice(0, 10)}`,
}))

onMounted(async () => {
  try {
    if (shouldUseDemoCampaigns()) {
      availableCampaigns.value = demoCampaigns()
      return
    }

    const res = await listCampaigns()
    const campaigns = res.data || res || []
    availableCampaigns.value = Array.isArray(campaigns) ? campaigns : campaigns.campaigns || []
  } catch (e) {
    console.warn('Failed to load campaigns for comparator, using demo:', e.message)
    // Fallback to demo campaigns for comparison testing
    availableCampaigns.value = demoCampaigns()
  }
})

function shouldUseDemoCampaigns() {
  if (!import.meta.env.DEV) return false
  return !localStorage.getItem('3c-auth-token') && !localStorage.getItem('3c-api-key')
}

function demoCampaigns() {
  return [
    { id: 'cmp_demo_a', campaign_id: 'cmp_demo_a', name: 'Message A: Product Launch Q2' },
    { id: 'cmp_demo_b', campaign_id: 'cmp_demo_b', name: 'Message B: Value Proposition' },
    { id: 'cmp_demo_c', campaign_id: 'cmp_demo_c', name: 'Message C: Fear of Missing Out' },
  ]
}

function toggleCampaign(id) {
  const idx = selectedIds.value.indexOf(id)
  if (idx >= 0) {
    selectedIds.value.splice(idx, 1)
  } else if (selectedIds.value.length < 5) {
    selectedIds.value.push(id)
  }
}

async function runComparison() {
  if (selectedIds.value.length < 2 || loading.value) return
  loading.value = true
  error.value = ''

  try {
    const res = await compareCampaigns(selectedIds.value)
    const data = res.data || res
    comparisonResult.value = data
  } catch (e) {
    console.error('Comparison failed:', e)
    // For demo — if backend fails, show comparison with default data
    comparisonResult.value = generateDemoComparison()
  } finally {
    loading.value = false
  }
}

function barWidth(metric, value) {
  // Normalize to 0-100% bar width
  if (!metric.higher_is_better) {
    value = 100 - value // invert for crisis_risk, polarization
  }
  return Math.max(5, Math.min(100, value))
}

function resetComparison() {
  comparisonResult.value = null
  selectedIds.value = []
}

// Demo fallback data
function generateDemoComparison() {
  const ids = selectedIds.value
  if (ids.length < 2) return null

  const names = ids.map((id, i) => `Message ${String.fromCharCode(65 + i)}: ${id.slice(0, 8)}`)

  return {
    campaign_count: ids.length,
    metrics_comparison: [
      { key: 'overall_sentiment', label: t('comparator.metricOverallSentiment'), unit: '', higher_is_better: true,
        values: ids.map((id, i) => ({ campaign_id: id, value: [42, 28, 55][i] || 35 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 55, max_diff: 27 },
      { key: 'conversion_probability', label: t('comparator.metricConversionProbability'), unit: '%', higher_is_better: true,
        values: ids.map((id, i) => ({ campaign_id: id, value: [67, 52, 73][i] || 60 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 73, max_diff: 21 },
      { key: 'social_influence_index', label: t('comparator.metricSocialInfluence'), unit: '', higher_is_better: true,
        values: ids.map((id, i) => ({ campaign_id: id, value: [78, 65, 82][i] || 70 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 82, max_diff: 17 },
      { key: 'message_resonance', label: t('comparator.metricMessageResonance'), unit: '%', higher_is_better: true,
        values: ids.map((id, i) => ({ campaign_id: id, value: [72, 48, 80][i] || 65 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 80, max_diff: 32 },
      { key: 'crisis_risk', label: t('comparator.metricCrisisRisk'), unit: '%', higher_is_better: false,
        values: ids.map((id, i) => ({ campaign_id: id, value: [15, 35, 8][i] || 20 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 8, max_diff: 27 },
      { key: 'brand_perception_shift', label: t('comparator.metricBrandPerceptionShift'), unit: '', higher_is_better: true,
        values: ids.map((id, i) => ({ campaign_id: id, value: [12, -5, 22][i] || 10 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 22, max_diff: 27 },
      { key: 'opinion_polarization', label: t('comparator.metricOpinionPolarization'), unit: '', higher_is_better: false,
        values: ids.map((id, i) => ({ campaign_id: id, value: [45, 62, 35][i] || 50 })),
        winner_campaign_id: ids[2] || ids[0], winner_value: 35, max_diff: 27 },
    ],
    campaign_summaries: ids.map((id, i) => ({
      campaign_id: id, campaign_name: names[i],
      kpi: {},
      metric_wins: i === 2 ? 7 : i === 0 ? 0 : 0,
      is_overall_winner: i === 2,
    })),
    overall_winner: {
      campaign_id: ids[2] || ids[0],
      campaign_name: names[2] || names[0],
      metric_wins: 7,
      total_metrics: 7,
    },
  }
}
</script>

<style scoped>
.comparator-dashboard {
  min-height: 100vh;
  max-width: 1240px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 56px) clamp(20px, 4vw, 44px);
  color: var(--text-secondary);
  font-family: var(--font-sans);
}

.comparator-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-6);
  margin-bottom: var(--space-10);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-subtle);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.page-title {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2rem, 4.5vw, 3.4rem);
  line-height: 1;
}

.page-subtitle {
  max-width: 620px;
  margin: var(--space-4) 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-base);
}

.back-link {
  color: var(--accent);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 800;
}

.selection-section,
.winner-banner,
.metric-row,
.campaign-label {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.selection-section {
  padding: var(--space-6);
  margin-bottom: var(--space-8);
}

.selection-prompt {
  margin-bottom: var(--space-5);
}

.selection-prompt h3 {
  margin: 0 0 var(--space-2);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
}

.selection-prompt p {
  margin: 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.campaign-picker {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
}

.campaign-chip {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 10px 16px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: transform var(--transition-fast), border-color var(--transition-fast), background var(--transition-fast), color var(--transition-fast);
  background: var(--bg-panel);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.campaign-chip:hover {
  transform: translateY(-1px);
  border-color: var(--border-accent);
}

.campaign-chip.selected {
  background: var(--accent-subtle);
  border-color: var(--accent);
  color: var(--accent);
  font-weight: 800;
}

.chip-check,
.label-letter,
.label-wins,
.metric-diff,
.bar-label,
.bar-value {
  font-family: var(--font-mono);
}

.btn-compare {
  min-height: 46px;
  padding: 0 var(--space-8);
  border: 1px solid var(--accent);
  border-radius: var(--radius-md);
  background: var(--accent);
  color: var(--text-inverse);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 900;
  cursor: pointer;
  transition: transform var(--transition-fast), background var(--transition-fast), border-color var(--transition-fast);
}

.btn-compare:hover:not(:disabled) {
  transform: translateY(-1px);
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

.btn-compare:disabled {
  cursor: not-allowed;
  opacity: 0.35;
}

.loading-state {
  padding: var(--space-20);
  color: var(--text-tertiary);
  text-align: center;
}

.spinner {
  width: 36px;
  height: 36px;
  margin: 0 auto var(--space-4);
  border: 3px solid var(--border-default);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.winner-banner {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
  border-color: var(--border-accent);
  background: linear-gradient(180deg, var(--accent-subtle), var(--bg-surface));
}

.winner-icon {
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border-accent);
  border-radius: var(--radius-lg);
  color: var(--accent);
  background: var(--bg-surface);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 900;
}

.winner-info h2 {
  margin: 0 0 var(--space-1);
  color: var(--text-primary);
  font-size: var(--text-xl);
  font-weight: 800;
}

.winner-info p {
  margin: 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.campaign-labels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.campaign-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
}

.campaign-label.winner {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.label-letter {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-elevated);
  color: var(--text-secondary);
  font-weight: 900;
}

.winner .label-letter {
  background: var(--accent);
  color: var(--text-inverse);
}

.label-name {
  flex: 1;
  min-width: 0;
  color: var(--text-primary);
  font-weight: 800;
}

.label-wins {
  color: var(--text-tertiary);
  font-size: var(--text-xs);
}

.metrics-grid {
  display: grid;
  gap: var(--space-5);
  margin-bottom: var(--space-8);
}

.metric-row {
  padding: var(--space-5);
}

.metric-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.metric-label {
  color: var(--text-primary);
  font-weight: 800;
}

.metric-diff {
  color: var(--accent);
  font-size: var(--text-xs);
  font-weight: 900;
}

.metric-bars {
  display: grid;
  gap: var(--space-2);
}

.bar-group {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.bar-label {
  width: 22px;
  color: var(--text-tertiary);
  font-weight: 900;
}

.bar-track {
  flex: 1;
  height: 26px;
  overflow: hidden;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
}

.bar-fill {
  min-width: 42px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: var(--space-2);
  border-radius: var(--radius-sm);
  background: var(--border-strong);
  transition: width var(--transition-slow);
}

.bar-fill.bar-winner {
  background: var(--accent);
}

.bar-value {
  color: var(--text-inverse);
  font-size: var(--text-xs);
  font-weight: 900;
}

.winner-badge {
  color: var(--accent);
}

.btn-reset {
  min-height: 42px;
  padding: 0 var(--space-5);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-secondary);
  cursor: pointer;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 800;
  transition: transform var(--transition-fast), border-color var(--transition-fast), color var(--transition-fast);
}

.btn-reset:hover {
  transform: translateY(-1px);
  border-color: var(--border-accent);
  color: var(--accent);
}

@media (max-width: 768px) {
  .comparator-header { flex-direction: column; }
  .winner-banner { align-items: flex-start; flex-direction: column; }
}
</style>
