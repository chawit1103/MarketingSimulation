<template>
  <div class="impact-page">
    <!-- Header -->
    <div class="impact-header">
      <div>
        <span class="page-kicker">{{ $t('impact.kicker') }}</span>
        <h1>{{ $t('impact.title') }}</h1>
        <p>{{ $t('impact.subtitle') }}</p>
      </div>
      <div class="header-actions">
        <router-link to="/campaigns" class="back-link">← {{ $t('common.backToCampaigns') }}</router-link>
        <ExportButton v-if="result" :data="exportData" :label="$t('common.export')" />
      </div>
    </div>

    <div class="impact-layout">
      <!-- Left: Inputs -->
      <div class="input-panel">
        <h3>{{ $t('impact.businessParameters') }}</h3>

        <div class="form-group">
          <label>{{ $t('impact.productName') }}</label>
          <input v-model="params.product_name" type="text" class="form-input" />
        </div>

        <div class="form-group">
          <label>{{ $t('impact.unitPrice') }}</label>
          <input v-model.number="params.unit_price" type="number" min="1" class="form-input" />
        </div>

        <div class="form-group">
          <label>{{ $t('impact.marketSize') }} / {{ timeLabel }}</label>
          <div class="slider-group">
            <input v-model.number="params.market_size" type="range" min="1000" max="10000000" step="1000" class="slider" />
            <span class="slider-val">{{ formatNumber(params.market_size) }}</span>
          </div>
        </div>

        <div class="form-group">
          <label>{{ $t('impact.currentMarketShare') }}</label>
          <div class="slider-group">
            <input v-model.number="params.current_market_share" type="range" min="0.1" max="100" step="0.1" class="slider" />
            <span class="slider-val">{{ params.current_market_share }}%</span>
          </div>
        </div>

        <div class="form-group">
          <label>{{ $t('impact.baseConversionRate') }}</label>
          <div class="slider-group">
            <input v-model.number="params.base_conversion_rate" type="range" min="0.1" max="20" step="0.1" class="slider" />
            <span class="slider-val">{{ params.base_conversion_rate }}%</span>
          </div>
        </div>

        <div class="form-group">
          <label>{{ $t('impact.campaignCost') }}</label>
          <div class="slider-group">
            <input v-model.number="params.campaign_cost" type="range" min="10000" max="50000000" step="10000" class="slider" />
            <span class="slider-val">฿{{ formatNumber(params.campaign_cost) }}</span>
          </div>
        </div>

        <div class="form-group">
          <label>{{ $t('impact.timeHorizon') }}</label>
          <select v-model.number="params.time_horizon_months" class="form-input">
            <option :value="1">{{ $t('impact.monthOption', { count: 1 }) }}</option>
            <option :value="3">{{ $t('impact.monthOption', { count: 3 }) }}</option>
            <option :value="6">{{ $t('impact.monthOption', { count: 6 }) }}</option>
            <option :value="12">{{ $t('impact.monthOption', { count: 12 }) }}</option>
          </select>
        </div>

        <!-- Sentiment Slider (quick demo) -->
        <div class="form-group sentiment-group">
          <label>{{ $t('impact.sentimentScore') }}</label>
          <div class="sentiment-slider">
            <input v-model.number="sentimentSlider" type="range" min="-100" max="100" step="1" class="slider" />
            <span :class="['sentiment-val', sentimentClass]">{{ sentimentSlider > 0 ? '+' : '' }}{{ sentimentSlider }}</span>
          </div>
        </div>

        <button class="btn-calculate" @click="calculateNow" :disabled="loading">
          {{ loading ? $t('impact.calculating') : $t('impact.calculate') }}
        </button>
      </div>

      <!-- Right: Results -->
      <div class="results-panel">
        <div v-if="!result && !loading" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M4 19V5M4 19h16M8 15l3-4 3 2 5-7" />
            </svg>
          </div>
          <p>{{ $t('impact.emptyHint') }}</p>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>{{ $t('impact.calculating') }}</p>
        </div>

        <div v-if="result" class="results-content">
          <!-- Header KPI -->
          <div class="result-header">
            <div class="big-number">
              <span class="big-number-label">{{ $t('impact.projectedRevenue', { scenario: scenarioLabel(result.best_scenario) }) }}</span>
              <span class="big-number-value">฿{{ formatNumber(result.projected_annual_revenue) }}</span>
              <span class="big-number-sub">{{ $t('impact.perYear') }}</span>
            </div>
          </div>

          <!-- 3 Scenarios -->
          <div class="scenario-cards">
            <div
              v-for="s in result.scenarios"
              :key="s.scenario"
              :class="['scenario-card', scenarioClass(s.scenario)]"
            >
              <div class="scenario-header">
                <span class="scenario-name">{{ scenarioLabel(s.scenario) }}</span>
                <span class="scenario-sentiment">{{ s.sentiment > 0 ? '+' : '' }}{{ s.sentiment }}</span>
              </div>
              <div class="scenario-metrics">
                <div class="sm-row">
                  <span class="sm-label">{{ $t('impact.conversion') }}</span>
                  <span class="sm-value">{{ s.conversion_rate }}%</span>
                </div>
                <div class="sm-row">
                  <span class="sm-label">{{ $t('impact.units') }}</span>
                  <span class="sm-value">{{ formatNumber(s.estimated_units) }}</span>
                </div>
                <div class="sm-row highlight">
                  <span class="sm-label">{{ $t('impact.revenue') }}</span>
                  <span class="sm-value">฿{{ formatNumber(s.estimated_revenue) }}</span>
                </div>
                <div :class="['sm-row', s.roi_pct > 0 ? 'positive' : 'negative']">
                  <span class="sm-label">{{ $t('impact.roi') }}</span>
                  <span class="sm-value">{{ s.roi_pct > 0 ? '+' : '' }}{{ s.roi_pct }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recommendation -->
          <div class="recommendation-box">
            {{ result.recommendation }}
          </div>

          <!-- Monthly breakdown -->
          <div class="monthly-box">
            <div class="mb-row">
              <span>{{ $t('impact.monthlyRevenue') }}</span>
              <strong>฿{{ formatNumber(result.projected_monthly_revenue) }}</strong>
            </div>
            <div class="mb-row">
              <span>{{ $t('impact.crisisRiskLoss') }}</span>
              <strong class="text-red">฿{{ formatNumber(result.crisis_risk_potential_loss) }}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import ExportButton from '@/components/ExportButton.vue'

const { t } = useI18n()

function formatNumber(n) {
  if (n >= 1000000000) return (n / 1000000000).toFixed(1) + 'B'
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return String(Math.round(n))
}

const params = reactive({
  product_name: t('impact.defaultProductName'),
  unit_price: 500,
  market_size: 500000,
  current_market_share: 5,
  base_conversion_rate: 3,
  campaign_cost: 2000000,
  time_horizon_months: 6,
})

const sentimentSlider = ref(42)
const result = ref(null)
const loading = ref(false)

const exportData = computed(() => ({
  slide_type: 'impact',
  title: t('impact.exportTitle', { product: params.product_name }),
  subtitle: t('impact.exportSubtitle', {
    sentiment: `${sentimentSlider.value > 0 ? '+' : ''}${sentimentSlider.value}`,
    market: formatNumber(params.market_size),
    price: params.unit_price,
  }),
  ...result.value,
  filename: `msaas_impact_${params.product_name.replace(/\s+/g, '_').toLowerCase()}`,
}))

// Auto-calculate on page load
onMounted(() => calculateNow())

const timeLabel = computed(() => {
  const m = { 1: t('impact.month'), 3: t('impact.quarter'), 6: t('impact.halfYear'), 12: t('impact.year') }
  return m[params.time_horizon_months] || 'period'
})

const sentimentClass = computed(() => {
  if (sentimentSlider.value > 20) return 'positive'
  if (sentimentSlider.value < -20) return 'negative'
  return 'neutral'
})

async function calculateNow() {
  loading.value = true
  result.value = null

  // Calculate immediately (synchronous, no API dependency)
  result.value = calculateClientSide()
  loading.value = false
}

function calculateClientSide() {
  const s = sentimentSlider.value
  const p = params
  
  const calcScenario = (adj, mr) => {
    const effSentiment = s + adj
    const conv = Math.max(0.1, Math.min(50, p.base_conversion_rate * (1 + effSentiment / 200) * mr))
    const share = p.current_market_share * (1 + 12 / 200) // brand shift
    const units = Math.round(p.market_size * (share / 100) * (conv / 100))
    const revenue = units * p.unit_price
    const baselineUnits = Math.round(p.market_size * (p.current_market_share / 100) * (p.base_conversion_rate / 100))
    const baselineRevenue = baselineUnits * p.unit_price
    const uplift = revenue - baselineRevenue
    const roi = ((uplift - p.campaign_cost) / p.campaign_cost) * 100
    return { sentiment: Math.round(effSentiment), conversion_rate: Math.round(conv * 10) / 10, estimated_units: units, estimated_revenue: revenue, revenue_uplift: Math.round(uplift), roi_pct: Math.round(roi * 10) / 10 }
  }

  const base = calcScenario(0, 1.0)
  const opt = calcScenario(30, 1.15)
  const pess = calcScenario(-30, 0.85)

  const best = opt.roi_pct > base.roi_pct ? 'Optimistic' : 'Base Case'
  const bestRevenue = opt.roi_pct > base.roi_pct ? opt.estimated_revenue : base.estimated_revenue
  const monthly = bestRevenue / p.time_horizon_months

  let rec
  if (opt.roi_pct > 50) {
    rec = t('impact.recommendInvest', { roi: opt.roi_pct, revenue: formatNumber(opt.estimated_revenue), months: p.time_horizon_months })
  } else if (opt.roi_pct > 0) {
    rec = t('impact.recommendOptimize', { roi: opt.roi_pct, revenue: formatNumber(opt.estimated_revenue) })
  } else {
    rec = t('impact.recommendPause', { roi: opt.roi_pct })
  }

  return {
    campaign_id: 'local', campaign_name: t('impact.localCalculation'), product_name: p.product_name,
    unit_price: p.unit_price, market_size: p.market_size,
    scenarios: [
      { scenario: 'Base Case', ...base },
      { scenario: 'Optimistic', ...opt },
      { scenario: 'Pessimistic', ...pess },
    ],
    best_scenario: best,
    projected_monthly_revenue: Math.round(monthly),
    projected_annual_revenue: Math.round(monthly * 12),
    crisis_risk_potential_loss: Math.round(base.estimated_revenue * 0.15 * 0.5),
    recommendation: rec,
  }
}

function scenarioClass(name) {
  if (name === 'Optimistic') return 'card-optimistic'
  if (name === 'Pessimistic') return 'card-pessimistic'
  return 'card-base'
}

function scenarioLabel(name) {
  return {
    'Base Case': t('impact.baseScenario'),
    'Optimistic': t('impact.optimisticScenario'),
    'Pessimistic': t('impact.pessimisticScenario'),
  }[name] || name
}
</script>

<style scoped>
.impact-page {
  min-height: 100vh;
  max-width: 1320px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 56px) clamp(20px, 4vw, 44px);
  color: var(--text-secondary);
  font-family: var(--font-sans);
}

.impact-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-6);
  margin-bottom: var(--space-10);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-subtle);
}

.page-kicker {
  display: block;
  margin-bottom: var(--space-3);
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  text-transform: uppercase;
}

.impact-header h1 {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2.1rem, 5vw, 3.8rem);
  line-height: 1;
  letter-spacing: 0;
}

.impact-header p {
  max-width: 560px;
  margin: var(--space-4) 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-base);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.back-link {
  color: var(--accent);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 800;
}

.impact-layout {
  display: grid;
  grid-template-columns: minmax(320px, 390px) minmax(0, 1fr);
  gap: var(--space-8);
  align-items: start;
}

.input-panel,
.results-panel,
.scenario-card,
.recommendation-box,
.monthly-box {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.input-panel {
  position: sticky;
  top: var(--space-6);
  max-height: calc(100vh - 48px);
  overflow-y: auto;
  padding: var(--space-6);
}

.input-panel h3 {
  margin: 0 0 var(--space-6);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
}

.form-group {
  margin-bottom: var(--space-5);
}

.form-group label {
  display: block;
  margin-bottom: var(--space-2);
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  text-transform: uppercase;
}

.form-input {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 12px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  outline: none;
  color: var(--text-primary);
  background: var(--bg-panel);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}

.slider-group,
.sentiment-slider {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.slider {
  flex: 1;
  accent-color: var(--accent);
}

.slider-val,
.sentiment-val {
  min-width: 92px;
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 800;
  text-align: right;
}

.sentiment-group {
  margin-top: var(--space-6);
  padding-top: var(--space-5);
  border-top: 1px solid var(--border-subtle);
}

.sentiment-val {
  min-width: 62px;
  font-size: var(--text-xl);
}

.sentiment-val.positive { color: var(--green); }
.sentiment-val.negative { color: var(--red); }
.sentiment-val.neutral { color: var(--yellow); }

.btn-calculate {
  width: 100%;
  min-height: 52px;
  margin-top: var(--space-2);
  border: 1px solid var(--accent);
  border-radius: var(--radius-md);
  color: var(--text-inverse);
  background: var(--accent);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 900;
  cursor: pointer;
  transition: transform var(--transition-fast), background var(--transition-fast), border-color var(--transition-fast);
}

.btn-calculate:hover:not(:disabled) {
  transform: translateY(-1px);
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

.btn-calculate:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.results-panel {
  min-height: 520px;
  padding: var(--space-6);
}

.empty-state,
.loading-state {
  min-height: 430px;
  display: grid;
  place-items: center;
  align-content: center;
  gap: var(--space-4);
  padding: var(--space-10);
  color: var(--text-tertiary);
  text-align: center;
}

.empty-icon {
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  color: var(--accent);
  background: var(--accent-subtle);
}

.empty-icon svg { width: 28px; height: 28px; }
.empty-icon path { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border-default);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.result-header {
  margin-bottom: var(--space-8);
}

.big-number {
  padding: var(--space-8);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: linear-gradient(180deg, var(--bg-panel), var(--bg-surface));
  text-align: center;
}

.big-number-label {
  display: block;
  margin-bottom: var(--space-3);
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  text-transform: uppercase;
}

.big-number-value {
  display: block;
  color: var(--green);
  font-family: var(--font-mono);
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  font-weight: 900;
  line-height: 1;
}

.big-number-sub {
  display: block;
  margin-top: var(--space-2);
  color: var(--text-tertiary);
  font-size: var(--text-xs);
}

.scenario-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.scenario-card {
  padding: var(--space-5);
}

.scenario-card.card-base { background: var(--bg-panel); }
.scenario-card.card-optimistic { background: var(--green-soft); border-color: color-mix(in srgb, var(--green) 28%, transparent); }
.scenario-card.card-pessimistic { background: var(--red-soft); border-color: color-mix(in srgb, var(--red) 28%, transparent); }

.scenario-header,
.sm-row,
.mb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
}

.scenario-header { margin-bottom: var(--space-4); }
.scenario-name { color: var(--text-primary); font-weight: 800; }
.scenario-sentiment,
.sm-value,
.mb-row strong { font-family: var(--font-mono); font-weight: 800; }

.scenario-metrics { display: grid; gap: var(--space-2); }
.sm-row { font-size: var(--text-sm); }
.sm-label { color: var(--text-tertiary); }
.sm-row.highlight { padding-top: var(--space-2); border-top: 1px solid var(--border-subtle); color: var(--text-primary); }
.sm-row.positive .sm-value { color: var(--green); }
.sm-row.negative .sm-value { color: var(--red); }

.recommendation-box,
.monthly-box {
  padding: var(--space-5);
  margin-bottom: var(--space-5);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.recommendation-box {
  background: var(--accent-subtle);
  border-color: var(--border-accent);
}

.monthly-box {
  display: grid;
  gap: var(--space-3);
  margin-bottom: 0;
  background: var(--bg-panel);
}

.text-red { color: var(--red); }

@media (max-width: 980px) {
  .impact-header,
  .impact-layout { grid-template-columns: 1fr; }
  .impact-header { flex-direction: column; }
  .input-panel { position: static; max-height: none; }
  .scenario-cards { grid-template-columns: 1fr; }
}
</style>
