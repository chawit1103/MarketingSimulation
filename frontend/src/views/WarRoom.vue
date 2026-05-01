<template>
  <div class="war-room">
    <div class="war-header">
      <div>
        <span class="page-kicker">{{ $t('warRoom.kicker') }}</span>
        <h1>{{ $t('warRoom.title') }}</h1>
        <p>{{ $t('warRoom.subtitle') }}</p>
      </div>
      <div class="header-actions">
        <router-link to="/campaigns" class="back-link">← {{ $t('common.backToCampaigns') }}</router-link>
        <ExportButton v-if="result" :data="exportData" :label="$t('common.export')" />
      </div>
    </div>

    <!-- Scenario Picker -->
    <div class="scenario-bar">
      <button v-for="s in scenarios" :key="s.id"
        :class="['scenario-btn', { active: activeScenario === s.id }]"
        @click="loadScenario(s.id)"
      >{{ $t(s.nameKey) }}</button>
      <button class="scenario-btn run-btn" @click="runSimulation" :disabled="loading">
        {{ loading ? $t('warRoom.simulating') : $t('warRoom.runSimulation') }}
      </button>
    </div>

    <!-- Market Share Chart -->
    <div v-if="result" class="chart-section">
      <h2>{{ $t('warRoom.marketShareOverTime') }}</h2>
      <div class="chart-container">
        <div class="chart-legend">
          <span v-for="(b, i) in result.brands" :key="b" :style="{ color: colors[i] }">
            <span class="legend-swatch" :style="{ background: colors[i] }"></span>
            {{ b }}
          </span>
        </div>
        <div class="chart-body">
          <div class="chart-y">
            <span>100%</span><span>50%</span><span>0%</span>
          </div>
          <div class="chart-rows">
            <div v-for="rnd in result.rounds" :key="rnd" class="chart-row">
              <span class="round-label">R{{ rnd }}</span>
              <div class="round-bar">
                <div v-for="(b, i) in result.brands" :key="b"
                  :style="{ width: getShareAtRound(b, rnd) + '%', background: colors[i] }"
                  class="bar-segment"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Key Events Timeline -->
    <div v-if="result && result.key_events.length" class="events-section">
      <h2>{{ $t('warRoom.keyEvents') }}</h2>
      <div v-for="ev in result.key_events" :key="ev.round + ev.name" class="event-item">
        <span class="event-round">R{{ ev.round }}</span>
        <span class="event-impact">{{ ev.impact }}</span>
      </div>
    </div>

    <!-- Final Results -->
    <div v-if="result" class="results-grid">
      <div v-for="(share, brand) in result.final_market_share" :key="brand"
        :class="['result-card', { winner: brand === result.winner }]"
      >
        <div class="result-brand">{{ brand }}</div>
        <div class="result-share">{{ share }}%</div>
        <div :class="['result-shift', result.share_shift[brand] >= 0 ? 'positive' : 'negative']">
          {{ result.share_shift[brand] >= 0 ? '+' : '' }}{{ result.share_shift[brand] }}%
        </div>
        <div v-if="brand === result.winner" class="winner-badge">{{ $t('warRoom.winner') }}</div>
      </div>
    </div>

    <!-- Recommendation -->
    <div v-if="result" class="recommendation">
      <strong>{{ result.winner }}</strong> gained {{ result.share_shift[result.winner] }}% market share — 
      <template v-if="result.share_shift[result.winner] > 5">
        {{ $t('warRoom.significantAdvantage') }}
      </template>
      <template v-else>
        {{ $t('warRoom.marginalGain') }}
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import ExportButton from '@/components/ExportButton.vue'

const { t } = useI18n()

const scenarios = [
  { id: 'price_war', nameKey: 'warRoom.priceWar', descriptionKey: 'warRoom.priceWarDesc' },
  { id: 'first_mover', nameKey: 'warRoom.firstMover', descriptionKey: 'warRoom.firstMoverDesc' },
  { id: 'scandal', nameKey: 'warRoom.scandal', descriptionKey: 'warRoom.scandalDesc' },
]

const activeScenario = ref('price_war')
const result = ref(null)
const loading = ref(false)

const exportData = computed(() => ({
  slide_type: 'war_room',
  title: t('warRoom.exportTitle', { scenario: scenarioName(activeScenario.value) }),
  subtitle: t('warRoom.exportSubtitle', { brands: result.value?.brands?.length || 0, rounds: result.value?.rounds || 0 }),
  ...result.value,
  filename: `msaas_war_room_${activeScenario.value}`,
}))

const colors = ['var(--accent)', 'var(--blue)', 'var(--green)', 'var(--yellow)', 'var(--teal)']

onMounted(() => {
  loadScenario('price_war')
  setTimeout(() => runSimulation(), 500)
})

function loadScenario(id) {
  activeScenario.value = id
  result.value = null
}

function scenarioName(id) {
  const scenario = scenarios.find(s => s.id === id)
  return scenario ? t(scenario.nameKey) : id
}

async function runSimulation() {
  loading.value = true
  result.value = null

  // Client-side simulation (instant, no network)
  setTimeout(() => {
    result.value = runClientSide()
    loading.value = false
  }, 400)
}

function getShareAtRound(brand, round) {
  if (!result.value || !result.value.timeline) return 0
  const entry = result.value.timeline.find(t => t.round_num === round && t.brand_name === brand)
  return entry ? entry.market_share : 0
}

function runClientSide() {
  const selections = {
    price_war: {
      brands: ['Our Brand', 'Competitor A', 'Competitor B', 'New Entrant'],
      timeline: [],
      final_market_share: { 'Our Brand': 32.5, 'Competitor A': 30.2, 'Competitor B': 22.8, 'New Entrant': 14.5 },
      share_shift: { 'Our Brand': 2.5, 'Competitor A': -4.8, 'Competitor B': 2.8, 'New Entrant': -0.5 },
      winner: 'Our Brand', rounds: 12,
      key_events: [{ round: 3, name: t('warRoom.eventPriceCut'), impact: t('warRoom.eventPriceCutImpact') }],
    },
    first_mover: {
      brands: ['Our Brand', 'Competitor X', 'Competitor Y', 'Competitor Z'],
      final_market_share: { 'Our Brand': 35.2, 'Competitor X': 32.1, 'Competitor Y': 19.5, 'Competitor Z': 13.2 },
      share_shift: { 'Our Brand': 10.2, 'Competitor X': -7.9, 'Competitor Y': -0.5, 'Competitor Z': -1.8 },
      winner: 'Our Brand', rounds: 12,
      key_events: [
        { round: 2, name: t('warRoom.eventNewProduct'), impact: t('warRoom.eventNewProductImpact') },
        { round: 6, name: t('warRoom.eventCopycat'), impact: t('warRoom.eventCopycatImpact') },
      ],
    },
    scandal: {
      brands: ['Our Brand', 'Big Competitor', 'Mid Competitor', 'Budget Brand'],
      final_market_share: { 'Our Brand': 30.5, 'Big Competitor': 28.3, 'Mid Competitor': 25.1, 'Budget Brand': 16.1 },
      share_shift: { 'Our Brand': 8.5, 'Big Competitor': -16.7, 'Mid Competitor': 5.1, 'Budget Brand': 3.1 },
      winner: 'Our Brand', rounds: 12,
      key_events: [{ round: 3, name: t('warRoom.eventScandal'), impact: t('warRoom.eventScandalImpact') }],
    },
  }
  return selections[activeScenario.value] || selections.price_war
}
</script>

<style scoped>
.war-room {
  min-height: 100vh;
  max-width: 1280px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 56px) clamp(20px, 4vw, 44px);
  color: var(--text-secondary);
  font-family: var(--font-sans);
}

.war-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-6);
  margin-bottom: var(--space-8);
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

h1 {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2.1rem, 5vw, 3.8rem);
  line-height: 1;
}

.war-header p {
  max-width: 620px;
  margin: var(--space-4) 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-base);
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.back-link {
  color: var(--accent);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 800;
}

.scenario-bar {
  display: flex;
  gap: var(--space-2);
  margin: var(--space-6) 0 var(--space-8);
  flex-wrap: wrap;
}

.scenario-btn {
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
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-fast), border-color var(--transition-fast), color var(--transition-fast), background var(--transition-fast);
}

.scenario-btn:hover {
  transform: translateY(-1px);
  border-color: var(--border-accent);
  color: var(--accent);
}

.scenario-btn.active {
  background: var(--accent-subtle);
  border-color: var(--accent);
  color: var(--accent);
}

.run-btn {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--text-inverse);
}

.run-btn:hover:not(:disabled) {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: var(--text-inverse);
}

.run-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.chart-section,
.events-section,
.recommendation {
  margin: var(--space-8) 0;
  padding: var(--space-6);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.chart-section h2,
.events-section h2 {
  margin: 0 0 var(--space-5);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
}

.chart-container {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  padding: var(--space-5);
}

.chart-legend {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
  flex-wrap: wrap;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
}

.chart-legend span {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.legend-swatch {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.chart-body {
  display: flex;
  gap: var(--space-3);
}

.chart-y {
  width: 42px;
  height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.chart-rows {
  flex: 1;
  display: flex;
  flex-direction: column-reverse;
  gap: 3px;
}

.chart-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.round-label {
  width: 28px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.round-bar {
  flex: 1;
  height: 20px;
  display: flex;
  overflow: hidden;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
}

.bar-segment {
  transition: width var(--transition-slow);
}

.event-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--border-subtle);
  font-size: var(--text-sm);
}

.event-item:last-child {
  border-bottom: 0;
}

.event-round {
  min-width: 36px;
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin: var(--space-8) 0;
}

.result-card {
  padding: var(--space-6);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
  text-align: center;
}

.result-card.winner {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.result-brand {
  margin-bottom: var(--space-2);
  color: var(--text-primary);
  font-weight: 800;
}

.result-share {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: 2.2rem;
  font-weight: 900;
  line-height: 1;
}

.result-shift {
  margin: var(--space-2) 0 var(--space-3);
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 800;
}

.result-shift.positive { color: var(--green); }
.result-shift.negative { color: var(--red); }

.winner-badge {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  padding: 0 var(--space-3);
  border-radius: var(--radius-pill);
  background: var(--accent);
  color: var(--text-inverse);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.recommendation {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.7;
}

.recommendation strong {
  color: var(--text-primary);
}

@media (max-width: 760px) {
  .war-header { flex-direction: column; }
  .chart-body { overflow-x: auto; }
  .chart-rows { min-width: 640px; }
}
</style>
