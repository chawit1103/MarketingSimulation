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

    <section class="command-grid">
      <div class="control-panel">
        <div class="panel-heading">
          <span>{{ $t('warRoom.battleSetup') }}</span>
          <strong>{{ $t('warRoom.roundsLabel', { rounds }) }}</strong>
        </div>

        <label class="field-block">
          <span>{{ $t('warRoom.campaignInPlay') }}</span>
          <select v-model="selectedCampaignId">
            <option v-for="campaign in campaignOptions" :key="campaign.id" :value="campaign.id">
              {{ campaign.name }}
            </option>
          </select>
        </label>
        <ResultSourceBadge
          v-if="campaignListSource.source !== 'live_backend'"
          :source="campaignListSource.source"
          :warning="campaignListSource.warning"
        />

        <div class="scenario-grid">
          <button
            v-for="scenario in scenarios"
            :key="scenario.id"
            :class="['choice-card', { active: activeScenario === scenario.id }]"
            @click="loadScenario(scenario.id)"
          >
            <span>{{ $t(scenario.nameKey) }}</span>
            <small>{{ $t(scenario.descriptionKey) }}</small>
          </button>
        </div>

        <div class="strategy-section">
          <div class="section-label">{{ $t('warRoom.responseStrategy') }}</div>
          <div class="strategy-grid">
            <button
              v-for="strategy in strategies"
              :key="strategy.id"
              :class="['strategy-btn', { active: selectedStrategy === strategy.id }]"
              @click="selectedStrategy = strategy.id"
            >
              <span>{{ $t(strategy.nameKey) }}</span>
              <small>{{ $t(strategy.descriptionKey) }}</small>
            </button>
          </div>
        </div>

        <div class="slider-grid">
          <label class="range-field">
            <span>{{ $t('warRoom.ourBudget') }}</span>
            <strong>{{ formatCurrency(ourBudget) }}</strong>
            <input v-model.number="ourBudget" type="range" min="20" max="120" step="5" />
          </label>
          <label class="range-field">
            <span>{{ $t('warRoom.competitorIntensity') }}</span>
            <strong>{{ competitorIntensity }}%</strong>
            <input v-model.number="competitorIntensity" type="range" min="35" max="100" step="5" />
          </label>
        </div>

        <button class="run-btn" @click="runSimulation" :disabled="loading">
          {{ loading ? $t('warRoom.simulating') : $t('warRoom.runSimulation') }}
        </button>
        <div v-if="simulationWarning" class="backend-warning">
          <strong>{{ $t('warRoom.backendWarningTitle') }}</strong>
          <p>{{ simulationWarning }}</p>
          <button
            v-if="localFallbackAvailable"
            class="local-fallback-btn"
            type="button"
            @click="runLocalEstimate"
            :disabled="loading"
          >
            {{ $t('warRoom.runLocalEstimate') }}
          </button>
        </div>
      </div>

      <div class="competitor-panel">
        <div class="panel-heading">
          <span>{{ $t('warRoom.competitorProfiles') }}</span>
          <strong>{{ competitors.length }} {{ $t('warRoom.brands') }}</strong>
        </div>
        <div class="competitor-list">
          <div v-for="(competitor, index) in competitors" :key="competitor.id" class="competitor-row">
            <div class="competitor-main">
              <span class="competitor-color" :style="{ background: colors[index + 1] }"></span>
              <input v-model="competitor.name" :aria-label="$t('warRoom.competitorName')" />
            </div>
            <div class="mini-controls">
              <label>
                <span>{{ $t('warRoom.budget') }}</span>
                <input v-model.number="competitor.budget" type="range" min="30" max="120" step="5" />
                <strong>{{ competitor.budget }}</strong>
              </label>
              <label>
                <span>{{ $t('warRoom.aggression') }}</span>
                <input v-model.number="competitor.aggression" type="range" min="20" max="100" step="5" />
                <strong>{{ competitor.aggression }}</strong>
              </label>
            </div>
            <p>{{ $t(competitor.vulnerabilityKey) }}</p>
          </div>
        </div>
      </div>
    </section>

    <section v-if="result" class="decision-console">
      <div>
        <ResultSourceBadge
          :source="result.source.type"
          :warning="result.source.warning"
        />
        <span class="section-label">{{ $t('warRoom.decisionConsole') }}</span>
        <h2>{{ result.decision.headline }}</h2>
        <p>{{ result.decision.rationale }}</p>
      </div>
      <div class="decision-metrics">
        <div>
          <span>{{ $t('warRoom.confidence') }}</span>
          <strong>{{ formatPercentOrNA(result.decision.confidence) }}</strong>
        </div>
        <div>
          <span>{{ $t('warRoom.revenueUpside') }}</span>
          <strong>{{ formatMoneyOrNA(result.business.revenueUpside) }}</strong>
        </div>
        <div>
          <span>{{ $t('warRoom.crisisExposure') }}</span>
          <strong>{{ formatMoneyOrNA(result.business.crisisExposure) }}</strong>
        </div>
      </div>
    </section>

    <section v-if="result" class="intelligence-grid">
      <div class="intel-card">
        <span class="section-label">{{ $t('warRoom.sentimentMovement') }}</span>
        <div class="sentiment-list">
          <div v-for="[brand, movement] in sentimentMovementRows" :key="brand">
            <span>{{ brand }}</span>
            <strong :class="movement >= 0 ? 'positive' : 'negative'">
              {{ movement >= 0 ? '+' : '' }}{{ movement }}
            </strong>
          </div>
        </div>
      </div>
      <div class="intel-card">
        <span class="section-label">{{ $t('warRoom.affectedSegments') }}</span>
        <ul>
          <li v-for="segment in result.affected_segments" :key="segment">{{ segment }}</li>
        </ul>
      </div>
      <div class="intel-card">
        <span class="section-label">{{ $t('warRoom.amplificationChannels') }}</span>
        <ul>
          <li v-for="channel in result.amplification_channels" :key="channel">{{ channel }}</li>
        </ul>
      </div>
      <div class="intel-card">
        <span class="section-label">{{ $t('warRoom.keyDrivers') }}</span>
        <ul>
          <li v-for="driver in result.key_drivers" :key="driver">{{ driver }}</li>
        </ul>
      </div>
    </section>

    <section v-if="result" class="chart-section">
      <div class="section-head">
        <div>
          <span class="section-label">{{ $t('warRoom.marketShareOverTime') }}</span>
          <h2>{{ $t('warRoom.shareMovement') }}</h2>
        </div>
        <div class="chart-legend">
          <span v-for="(brand, i) in result.brands" :key="brand" :style="{ color: colors[i] }">
            <span class="legend-swatch" :style="{ background: colors[i] }"></span>
            {{ brand }}
          </span>
        </div>
      </div>
      <div class="chart-container">
        <div class="chart-body">
          <div class="chart-y">
            <span>100%</span><span>50%</span><span>0%</span>
          </div>
          <div class="chart-rows">
            <div v-for="round in result.rounds" :key="round" class="chart-row">
              <span class="round-label">R{{ round }}</span>
              <div class="round-bar">
                <div
                  v-for="(brand, i) in result.brands"
                  :key="brand"
                  :style="{ width: getShareAtRound(brand, round) + '%', background: colors[i] }"
                  class="bar-segment"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="result" class="war-grid">
      <div class="events-section">
        <div class="section-label">{{ $t('warRoom.keyEvents') }}</div>
        <div v-for="event in result.key_events" :key="event.round + event.name" class="event-item">
          <span class="event-round">R{{ event.round }}</span>
          <div>
            <strong>{{ event.name }}</strong>
            <p>{{ event.impact }}</p>
          </div>
        </div>
      </div>

      <div class="playbook-section">
        <div class="section-label">{{ $t('warRoom.responsePlaybook') }}</div>
        <div v-for="step in responsePlaybookRows" :key="step.stage || step.round" class="playbook-item">
          <span>{{ step.stageLabel || `R${step.round}` }}</span>
          <div>
            <strong>{{ step.title || step.move }}</strong>
            <p>{{ step.reason }}</p>
            <ul v-if="step.actions?.length" class="playbook-actions">
              <li v-for="action in step.actions" :key="action">{{ action }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section v-if="result" class="results-grid">
      <div
        v-for="brand in result.brands"
        :key="brand"
        :class="['result-card', { winner: brand === result.winner }]"
      >
        <div class="result-brand">{{ brand }}</div>
        <div class="result-share">{{ result.final_market_share[brand] }}%</div>
        <div :class="['result-shift', result.share_shift[brand] >= 0 ? 'positive' : 'negative']">
          {{ result.share_shift[brand] >= 0 ? '+' : '' }}{{ result.share_shift[brand] }}%
        </div>
        <div v-if="brand === result.winner" class="winner-badge">{{ $t('warRoom.winner') }}</div>
      </div>
    </section>

    <section v-if="result" class="recommendation">
      <div>
        <span class="section-label">{{ $t('warRoom.immediateAction') }}</span>
        <h2>{{ result.recommendation.title }}</h2>
        <p>{{ result.recommendation.summary }}</p>
        <p v-if="result.recommended_response" class="recommended-response">
          {{ result.recommended_response }}
        </p>
      </div>
      <ol>
        <li v-for="action in result.recommendation.actions" :key="action">{{ action }}</li>
      </ol>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import ExportButton from '@/components/ExportButton.vue'
import ResultSourceBadge from '@/components/ResultSourceBadge.vue'
import { listCampaigns } from '@/api/campaign'
import { runCompetitorSimulation } from '@/api/competitor'

const { t } = useI18n()

const rounds = 12
const colors = ['var(--accent)', 'var(--blue)', 'var(--green)', 'var(--yellow)', 'var(--teal)']

const scenarios = [
  {
    id: 'price_war',
    nameKey: 'warRoom.priceWar',
    descriptionKey: 'warRoom.priceWarDesc',
    baseRisk: 44,
    pressure: 1.1,
    ourBase: 29,
    events: [
      { round: 3, nameKey: 'warRoom.eventPriceCut', impactKey: 'warRoom.eventPriceCutImpact', effects: { our: -2.8, competitor0: 3.8, risk: 10 } },
      { round: 8, nameKey: 'warRoom.eventMarginPressure', impactKey: 'warRoom.eventMarginPressureImpact', effects: { our: -0.8, allCompetitors: -0.5, risk: 5 } },
    ],
    competitors: [
      competitor('cmp-a', 'Competitor A', 86, 78, 'warRoom.vulnerabilityMargin'),
      competitor('cmp-b', 'Competitor B', 70, 66, 'warRoom.vulnerabilityTrust'),
      competitor('entrant', 'New Entrant', 54, 58, 'warRoom.vulnerabilityReach'),
    ],
  },
  {
    id: 'first_mover',
    nameKey: 'warRoom.firstMover',
    descriptionKey: 'warRoom.firstMoverDesc',
    baseRisk: 36,
    pressure: 0.85,
    ourBase: 31,
    events: [
      { round: 2, nameKey: 'warRoom.eventNewProduct', impactKey: 'warRoom.eventNewProductImpact', effects: { our: 4.5, allCompetitors: -1.2, risk: -3 } },
      { round: 6, nameKey: 'warRoom.eventCopycat', impactKey: 'warRoom.eventCopycatImpact', effects: { our: -2.2, competitor1: 2.8, risk: 4 } },
    ],
    competitors: [
      competitor('cmp-x', 'Competitor X', 76, 64, 'warRoom.vulnerabilitySpeed'),
      competitor('cmp-y', 'Competitor Y', 68, 82, 'warRoom.vulnerabilityOriginality'),
      competitor('cmp-z', 'Competitor Z', 50, 45, 'warRoom.vulnerabilityAwareness'),
    ],
  },
  {
    id: 'scandal',
    nameKey: 'warRoom.scandal',
    descriptionKey: 'warRoom.scandalDesc',
    baseRisk: 58,
    pressure: 0.75,
    ourBase: 28,
    events: [
      { round: 3, nameKey: 'warRoom.eventScandal', impactKey: 'warRoom.eventScandalImpact', effects: { our: 3.8, competitor0: -9.5, risk: 8 } },
      { round: 7, nameKey: 'warRoom.eventApology', impactKey: 'warRoom.eventApologyImpact', effects: { our: -1.2, competitor0: 3.1, risk: -6 } },
    ],
    competitors: [
      competitor('big-cmp', 'Big Competitor', 92, 74, 'warRoom.vulnerabilityReputation'),
      competitor('mid-cmp', 'Mid Competitor', 64, 48, 'warRoom.vulnerabilityScale'),
      competitor('budget', 'Budget Brand', 46, 42, 'warRoom.vulnerabilityPremium'),
    ],
  },
  {
    id: 'influencer_backlash',
    nameKey: 'warRoom.influencerBacklash',
    descriptionKey: 'warRoom.influencerBacklashDesc',
    baseRisk: 66,
    pressure: 1,
    ourBase: 30,
    events: [
      { round: 4, nameKey: 'warRoom.eventInfluencerBacklash', impactKey: 'warRoom.eventInfluencerBacklashImpact', effects: { our: -6, competitor0: 2.6, risk: 16 } },
      { round: 9, nameKey: 'warRoom.eventCreatorRepair', impactKey: 'warRoom.eventCreatorRepairImpact', effects: { our: 3.6, allCompetitors: -0.8, risk: -10 } },
    ],
    competitors: [
      competitor('social-cmp', 'Social Challenger', 72, 86, 'warRoom.vulnerabilityProof'),
      competitor('legacy-cmp', 'Legacy Brand', 84, 52, 'warRoom.vulnerabilityCulture'),
      competitor('nano-cmp', 'Creator Network', 58, 78, 'warRoom.vulnerabilityConsistency'),
    ],
  },
  {
    id: 'product_recall',
    nameKey: 'warRoom.productRecall',
    descriptionKey: 'warRoom.productRecallDesc',
    baseRisk: 72,
    pressure: 0.9,
    ourBase: 31,
    events: [
      { round: 2, nameKey: 'warRoom.eventRecall', impactKey: 'warRoom.eventRecallImpact', effects: { our: -7.5, competitor0: 3.8, risk: 18 } },
      { round: 7, nameKey: 'warRoom.eventRecallRepair', impactKey: 'warRoom.eventRecallRepairImpact', effects: { our: 3.2, allCompetitors: -0.7, risk: -11 } },
    ],
    competitors: [
      competitor('trusted', 'Trusted Incumbent', 88, 58, 'warRoom.vulnerabilityProof'),
      competitor('value', 'Value Rival', 62, 72, 'warRoom.vulnerabilityTrust'),
      competitor('private-label', 'Retail Private Label', 52, 48, 'warRoom.vulnerabilityDistribution'),
    ],
  },
  {
    id: 'regulatory_issue',
    nameKey: 'warRoom.regulatoryIssue',
    descriptionKey: 'warRoom.regulatoryIssueDesc',
    baseRisk: 68,
    pressure: 0.95,
    ourBase: 32,
    events: [
      { round: 3, nameKey: 'warRoom.eventRegulatoryReview', impactKey: 'warRoom.eventRegulatoryReviewImpact', effects: { our: -5.4, competitor0: 2.4, risk: 14 } },
      { round: 8, nameKey: 'warRoom.eventCompliantRelaunch', impactKey: 'warRoom.eventCompliantRelaunchImpact', effects: { our: 2.5, risk: -9 } },
    ],
    competitors: [
      competitor('compliant', 'Compliant Incumbent', 86, 48, 'warRoom.vulnerabilitySpeed'),
      competitor('fast', 'Fast Challenger', 64, 82, 'warRoom.vulnerabilityConsistency'),
      competitor('expert', 'Niche Expert', 46, 42, 'warRoom.vulnerabilityAwareness'),
    ],
  },
  {
    id: 'esg_controversy',
    nameKey: 'warRoom.esgControversy',
    descriptionKey: 'warRoom.esgControversyDesc',
    baseRisk: 70,
    pressure: 1,
    ourBase: 34,
    events: [
      { round: 3, nameKey: 'warRoom.eventEsgAllegation', impactKey: 'warRoom.eventEsgAllegationImpact', effects: { our: -6.4, competitor0: 2.9, risk: 17 } },
      { round: 8, nameKey: 'warRoom.eventAuditCommitment', impactKey: 'warRoom.eventAuditCommitmentImpact', effects: { our: 2.9, risk: -8 } },
    ],
    competitors: [
      competitor('ethical', 'Ethical Challenger', 66, 74, 'warRoom.vulnerabilityScale'),
      competitor('mass', 'Mass Competitor', 92, 54, 'warRoom.vulnerabilityCulture'),
      competitor('budget-sub', 'Budget Substitute', 48, 44, 'warRoom.vulnerabilityPremium'),
    ],
  },
  {
    id: 'fake_news',
    nameKey: 'warRoom.fakeNews',
    descriptionKey: 'warRoom.fakeNewsDesc',
    baseRisk: 64,
    pressure: 1.05,
    ourBase: 30,
    events: [
      { round: 2, nameKey: 'warRoom.eventRumorSpike', impactKey: 'warRoom.eventRumorSpikeImpact', effects: { our: -5.8, competitor0: 2.3, risk: 15 } },
      { round: 6, nameKey: 'warRoom.eventTrustedCorrection', impactKey: 'warRoom.eventTrustedCorrectionImpact', effects: { our: 3, risk: -10 } },
    ],
    competitors: [
      competitor('opportunist', 'Opportunist Rival', 62, 78, 'warRoom.vulnerabilityReputation'),
      competitor('trusted-leader', 'Trusted Leader', 88, 46, 'warRoom.vulnerabilityEfficiency'),
      competitor('low-price', 'Low-price Alternative', 44, 52, 'warRoom.vulnerabilityReach'),
    ],
  },
  {
    id: 'competitor_launch',
    nameKey: 'warRoom.competitorLaunch',
    descriptionKey: 'warRoom.competitorLaunchDesc',
    baseRisk: 45,
    pressure: 1.2,
    ourBase: 33,
    events: [
      { round: 2, nameKey: 'warRoom.eventCompetitorLaunch', impactKey: 'warRoom.eventCompetitorLaunchImpact', effects: { our: -3.8, competitor0: 5.4, risk: 5 } },
      { round: 6, nameKey: 'warRoom.eventDifferentiatedResponse', impactKey: 'warRoom.eventDifferentiatedResponseImpact', effects: { our: 3.4, allCompetitors: -0.8, risk: -4 } },
    ],
    competitors: [
      competitor('launch-rival', 'Launch Rival', 92, 78, 'warRoom.vulnerabilityEfficiency'),
      competitor('category-leader', 'Category Leader', 100, 52, 'warRoom.vulnerabilityMessage'),
      competitor('niche-challenger', 'Niche Challenger', 50, 58, 'warRoom.vulnerabilityDistribution'),
    ],
  },
]

const strategies = [
  { id: 'proof', nameKey: 'warRoom.strategyProof', descriptionKey: 'warRoom.strategyProofDesc', shareLift: 1.15, lateLift: 0.75, disruption: 0.4, riskReduction: 13, conversionLift: 6, confidence: 8 },
  { id: 'price_match', nameKey: 'warRoom.strategyPriceMatch', descriptionKey: 'warRoom.strategyPriceMatchDesc', shareLift: 1.35, lateLift: -0.1, disruption: 0.7, riskReduction: 4, conversionLift: 9, confidence: 2 },
  { id: 'creator', nameKey: 'warRoom.strategyCreator', descriptionKey: 'warRoom.strategyCreatorDesc', shareLift: 1, lateLift: 1.25, disruption: 0.5, riskReduction: 8, conversionLift: 7, confidence: 5 },
  { id: 'defensive', nameKey: 'warRoom.strategyDefensive', descriptionKey: 'warRoom.strategyDefensiveDesc', shareLift: 0.55, lateLift: 0.4, disruption: 0.25, riskReduction: 18, conversionLift: 1, confidence: 7 },
]

const activeScenario = ref('price_war')
const selectedStrategy = ref('proof')
const selectedCampaignId = ref('demo-premium-water')
const campaignOptions = ref(fallbackCampaigns())
const competitors = ref([])
const competitorIntensity = ref(70)
const ourBudget = ref(80)
const result = ref(null)
const loading = ref(false)
const campaignListSource = ref({ source: 'unknown', warning: '' })
const simulationWarning = ref('')
const localFallbackAvailable = ref(false)

const activeScenarioData = computed(() => scenarios.find(s => s.id === activeScenario.value) || scenarios[0])
const activeStrategyData = computed(() => strategies.find(s => s.id === selectedStrategy.value) || strategies[0])
const selectedCampaign = computed(() => campaignOptions.value.find(c => c.id === selectedCampaignId.value) || campaignOptions.value[0])
const sentimentMovementRows = computed(() => Object.entries(result.value?.expected_sentiment_movement || {}))
const responsePlaybookRows = computed(() => {
  const rows = result.value?.response_playbook?.length ? result.value.response_playbook : result.value?.playbook || []
  return rows.map(step => ({
    ...step,
    stageLabel: step.stage ? t(`warRoom.${step.stage}`) : null,
    reason: step.reason || (Array.isArray(step.actions) ? step.actions.join(' / ') : ''),
  }))
})

const exportData = computed(() => ({
  slide_type: 'war_room',
  title: t('warRoom.exportTitle', { scenario: scenarioName(activeScenario.value) }),
  subtitle: t('warRoom.exportSubtitle', { brands: result.value?.brands?.length || 0, rounds: result.value?.rounds || 0 }),
  recommendation: result.value?.recommendation?.summary,
  ...result.value,
  filename: `msaas_war_room_${activeScenario.value}`,
}))

onMounted(async () => {
  await loadCampaignOptions()
  loadScenario('price_war')
  setTimeout(() => runSimulation(), 350)
})

function competitor(id, name, budget, aggression, vulnerabilityKey) {
  return { id, name, budget, aggression, vulnerabilityKey }
}

async function loadCampaignOptions() {
  try {
    const res = await listCampaigns()
    const campaigns = Array.isArray(res) ? res : res.campaigns || []
    if (campaigns.length) {
      campaignOptions.value = campaigns.map(item => ({
        id: item.id || item.campaign_id,
        name: item.name || item.campaign_name || t('warRoom.untitledCampaign'),
        objective: item.objective || 'competitor_response',
      }))
      selectedCampaignId.value = campaignOptions.value[0].id
      campaignListSource.value = { source: 'live_backend', warning: '' }
      return
    }
    campaignListSource.value = {
      source: 'demo_mode',
      warning: t('warRoom.demoCampaignWarning'),
    }
  } catch (error) {
    campaignOptions.value = fallbackCampaigns()
    campaignListSource.value = {
      source: 'demo_mode',
      warning: t('warRoom.demoCampaignWarning'),
    }
  }
}

function fallbackCampaigns() {
  return [
    { id: 'demo-premium-water', name: 'Premium Water Launch', objective: 'product_launch' },
    { id: 'demo-crisis', name: 'Energy Crisis Response', objective: 'crisis_simulation' },
    { id: 'demo-fmcg', name: 'FMCG Value Campaign', objective: 'competitor_response' },
  ]
}

function loadScenario(id) {
  activeScenario.value = id
  const scenario = scenarios.find(s => s.id === id) || scenarios[0]
  competitors.value = scenario.competitors.map(item => ({ ...item }))
  competitorIntensity.value = ['competitor_launch', 'fake_news'].includes(id) ? 82 : id === 'influencer_backlash' ? 76 : 70
  result.value = null
  simulationWarning.value = ''
  localFallbackAvailable.value = false
}

function scenarioName(id) {
  const scenario = scenarios.find(s => s.id === id)
  return scenario ? t(scenario.nameKey) : id
}

async function runSimulation() {
  loading.value = true
  result.value = null
  simulationWarning.value = ''
  localFallbackAvailable.value = false
  try {
    const res = await runCompetitorSimulation(buildBackendPayload())
    result.value = normalizeBackendResult(res.data || res)
  } catch (error) {
    console.warn('Backend War Room simulation failed:', error.message)
    simulationWarning.value = t('warRoom.backendSimulationFailed')
    localFallbackAvailable.value = true
  } finally {
    loading.value = false
  }
}

function runLocalEstimate() {
  loading.value = true
  result.value = null
  simulationWarning.value = t('warRoom.localEstimateWarning')
  localFallbackAvailable.value = false
  setTimeout(() => {
    result.value = runWarGame()
    loading.value = false
  }, 250)
}

function buildBackendPayload() {
  return {
    scenario: activeScenario.value,
    rounds,
    response_strategy: selectedStrategy.value,
    our_budget_index: ourBudget.value,
    competitor_intensity: competitorIntensity.value,
    campaign_name: selectedCampaign.value?.name || t('warRoom.ourBrand'),
    campaign: selectedCampaign.value || null,
  }
}

function normalizeBackendResult(data) {
  const brands = data.brands || []
  const ourBrand = selectedCampaign.value?.name || brands[0] || t('warRoom.ourBrand')
  const ourShift = Number(data.share_shift?.[ourBrand] ?? data.share_shift?.[brands[0]] ?? 0)
  const recommendation = backendRecommendation(data, ourBrand, ourShift)

  return {
    ...data,
    source: data.source || {
      type: 'live_backend',
      warning: t('warRoom.backendDeterministicWarning'),
    },
    expected_sentiment_movement: data.expected_sentiment_movement || {},
    affected_segments: data.affected_segments || [],
    amplification_channels: data.amplification_channels || [],
    key_drivers: data.key_drivers || [],
    recommended_response: data.recommended_response || '',
    response_playbook: data.response_playbook || [],
    business: {
      revenueUpside: null,
      crisisExposure: null,
      marketShareShift: roundToOne(ourShift),
      projectedConversion: null,
    },
    decision: {
      headline: recommendation.title,
      rationale: recommendation.summary,
      confidence: null,
    },
    recommendation,
  }
}

function backendRecommendation(data, ourBrand, ourShift) {
  if (data.recommended_response) {
    return {
      title: t('warRoom.backendRecommendedResponse'),
      summary: data.recommended_response,
      actions: data.response_playbook?.flatMap(step => step.actions || []).slice(0, 3) || [],
    }
  }
  if (data.winner === ourBrand && ourShift > 0) {
    return {
      title: t('warRoom.recommendAttack'),
      summary: t('warRoom.recommendAttackSummary'),
      actions: [t('warRoom.actionIncreaseBudget'), t('warRoom.actionMonitorCompetitor')],
    }
  }
  return {
    title: t('warRoom.recommendPilot'),
    summary: t('warRoom.recommendPilotSummary'),
    actions: [t('warRoom.actionRetestMessage'), t('warRoom.actionPrepareCounter')],
  }
}

function runWarGame() {
  const scenario = activeScenarioData.value
  const strategy = activeStrategyData.value
  const ourBrand = selectedCampaign.value?.name || t('warRoom.ourBrand')
  const brands = [ourBrand, ...competitors.value.map(c => c.name || t('warRoom.competitorName'))]
  const startShares = initialShares(ourBrand, competitors.value, scenario.ourBase)
  const current = { ...startShares }
  const timeline = []
  let risk = scenario.baseRisk
  const eventRows = []
  const playbook = []

  for (let round = 1; round <= rounds; round += 1) {
    const pressure = average(competitors.value.map(c => c.aggression)) * (competitorIntensity.value / 100) * scenario.pressure
    const budgetAdvantage = (ourBudget.value - average(competitors.value.map(c => c.budget))) * 0.018
    const objectiveBoost = selectedCampaign.value?.objective === 'product_launch' ? 0.22 : selectedCampaign.value?.objective === 'crisis_simulation' ? -0.08 : 0.14
    current[ourBrand] += strategy.shareLift + strategy.lateLift * (round > 6 ? 1 : 0) + budgetAdvantage + objectiveBoost - pressure * 0.006

    competitors.value.forEach((comp, index) => {
      current[comp.name] += (comp.aggression * competitorIntensity.value * 0.00018) + ((comp.budget - ourBudget.value) * 0.008) - (strategy.disruption * (index === 0 ? 0.7 : 0.35))
    })

    scenario.events.filter(event => event.round === round).forEach(event => {
      applyEvent(current, ourBrand, competitors.value, event.effects)
      risk += event.effects.risk || 0
      eventRows.push({
        round,
        name: t(event.nameKey),
        impact: t(event.impactKey),
      })
    })

    risk -= strategy.riskReduction / rounds
    normalizeShares(current)
    brands.forEach(brand => {
      timeline.push({ round_num: round, brand_name: brand, market_share: roundToOne(current[brand]) })
    })

    if ([1, 4, 8, 12].includes(round)) {
      playbook.push(playbookStep(round, strategy, scenario))
    }
  }

  const finalShares = Object.fromEntries(brands.map(brand => [brand, roundToOne(current[brand])]))
  const shareShift = Object.fromEntries(brands.map(brand => [brand, roundToOne(finalShares[brand] - startShares[brand])]))
  const winner = brands.reduce((best, brand) => finalShares[brand] > finalShares[best] ? brand : best, brands[0])
  const ourShift = shareShift[ourBrand]
  const finalRisk = clamp(risk + (competitorIntensity.value - 70) * 0.18, 8, 92)
  const conversion = clamp(51 + ourShift * 1.65 + strategy.conversionLift - finalRisk * 0.08, 10, 88)
  const confidence = clamp(58 + Math.abs(ourShift) * 1.8 + strategy.confidence - finalRisk * 0.12, 35, 91)
  const business = {
    revenueUpside: Math.round(ourShift * 430000 + conversion * 18000 - finalRisk * 9500),
    crisisExposure: Math.round(finalRisk * 32000 + competitorIntensity.value * 6500),
    marketShareShift: roundToOne(ourShift),
    projectedConversion: roundToOne(conversion),
  }

  return {
    brands,
    timeline,
    rounds,
    final_market_share: finalShares,
    share_shift: shareShift,
    winner,
    key_events: eventRows,
    playbook,
    response_playbook: localResponsePlaybook(strategy, scenario),
    expected_sentiment_movement: localSentimentMovement(brands, shareShift, finalRisk),
    affected_segments: localAffectedSegments(scenario),
    amplification_channels: localAmplificationChannels(scenario),
    key_drivers: localKeyDrivers(scenario, strategy),
    recommended_response: localRecommendedResponse(winner === ourBrand, finalRisk),
    business,
    source: {
      type: 'local_estimate',
      warning: t('warRoom.localEstimateWarning'),
    },
    decision: decisionReadout(ourBrand, winner, ourShift, finalRisk, confidence, business),
    recommendation: recommendationReadout(ourBrand, winner, ourShift, finalRisk),
  }
}

function localResponsePlaybook(strategy, scenario) {
  const middleMove = strategy.id === 'price_match' ? t('warRoom.playbookPrice') : t('warRoom.playbookProof')
  const lateMove = scenario.id === 'influencer_backlash' ? t('warRoom.playbookCreatorRepair') : t('warRoom.playbookRetarget')
  return [
    { stage: 'first_2_hours', title: t('warRoom.playbookRound1'), actions: [t('warRoom.playbookRound1Reason')] },
    { stage: 'first_24_hours', title: middleMove, actions: [t('warRoom.playbookMidReason'), lateMove] },
    { stage: 'first_72_hours', title: t('warRoom.playbookScale'), actions: [t('warRoom.playbookScaleReason')] },
  ]
}

function localSentimentMovement(brands, shareShift, risk) {
  return Object.fromEntries(brands.map((brand, index) => {
    const shift = shareShift[brand] || 0
    const riskPenalty = index === 0 ? risk * 0.05 : 0
    return [brand, roundToOne(shift * 1.6 - riskPenalty)]
  }))
}

function localAffectedSegments(scenario) {
  const map = {
    price_war: ['Price-sensitive families', 'Retail shoppers', 'Value seekers'],
    influencer_backlash: ['Gen Z creators', 'Trust-sensitive buyers', 'High-intent social shoppers'],
    product_recall: ['Existing customers', 'Parents/families', 'Retail partners'],
    regulatory_issue: ['Compliance-sensitive buyers', 'Enterprise customers', 'Trade media'],
    esg_controversy: ['Purpose-led buyers', 'Urban professionals', 'Employees'],
    fake_news: ['Low-trust audiences', 'Community group members', 'Older buyers'],
    competitor_launch: ['Switchable buyers', 'Category explorers', 'Retail shoppers'],
  }
  return map[scenario.id] || ['Switchable buyers', 'High-intent audiences']
}

function localAmplificationChannels(scenario) {
  const map = {
    price_war: ['Facebook', 'TikTok', 'Retail media', 'LINE'],
    influencer_backlash: ['TikTok', 'Instagram Reels', 'X/Twitter', 'Facebook groups'],
    product_recall: ['Facebook groups', 'LINE communities', 'News sites', 'TikTok'],
    regulatory_issue: ['News sites', 'LinkedIn', 'X/Twitter', 'Industry forums'],
    esg_controversy: ['X/Twitter', 'LinkedIn', 'News sites', 'Facebook groups'],
    fake_news: ['LINE', 'Facebook groups', 'TikTok', 'X/Twitter'],
    competitor_launch: ['TikTok', 'YouTube', 'Retail media', 'Instagram'],
  }
  return map[scenario.id] || ['TikTok', 'Facebook', 'News sites']
}

function localKeyDrivers(scenario, strategy) {
  return [
    t(`warRoom.driver_${scenario.id}`),
    t(`warRoom.driver_strategy_${strategy.id}`),
    t('warRoom.driverChannelVelocity'),
  ]
}

function localRecommendedResponse(isWinning, risk) {
  if (risk >= 62) return t('warRoom.localRecommendedContain')
  if (isWinning) return t('warRoom.localRecommendedScale')
  return t('warRoom.localRecommendedPilot')
}

function initialShares(ourBrand, competitorRows, ourBase) {
  const shares = { [ourBrand]: ourBase }
  const remaining = 100 - ourBase
  const totalWeight = competitorRows.reduce((sum, comp) => sum + comp.budget + comp.aggression * 0.35, 0)
  competitorRows.forEach(comp => {
    shares[comp.name] = remaining * ((comp.budget + comp.aggression * 0.35) / totalWeight)
  })
  normalizeShares(shares)
  return Object.fromEntries(Object.entries(shares).map(([brand, share]) => [brand, roundToOne(share)]))
}

function applyEvent(current, ourBrand, competitorRows, effects) {
  current[ourBrand] += effects.our || 0
  competitorRows.forEach((comp, index) => {
    current[comp.name] += effects[`competitor${index}`] || 0
    current[comp.name] += effects.allCompetitors || 0
  })
}

function normalizeShares(shares) {
  Object.keys(shares).forEach(brand => {
    shares[brand] = Math.max(4, shares[brand])
  })
  const total = Object.values(shares).reduce((sum, value) => sum + value, 0) || 1
  Object.keys(shares).forEach(brand => {
    shares[brand] = shares[brand] / total * 100
  })
}

function playbookStep(round, strategy, scenario) {
  const map = {
    1: [t('warRoom.playbookRound1'), t('warRoom.playbookRound1Reason')],
    4: [t(strategy.id === 'price_match' ? 'warRoom.playbookPrice' : 'warRoom.playbookProof'), t('warRoom.playbookMidReason')],
    8: [t(scenario.id === 'creator_backlash' ? 'warRoom.playbookCreatorRepair' : 'warRoom.playbookRetarget'), t('warRoom.playbookLateReason')],
    12: [t('warRoom.playbookScale'), t('warRoom.playbookScaleReason')],
  }
  return { round, move: map[round][0], reason: map[round][1] }
}

function decisionReadout(ourBrand, winner, ourShift, risk, confidence, business) {
  if (winner === ourBrand && ourShift >= 5 && risk < 55) {
    return {
      headline: t('warRoom.decisionScale'),
      rationale: t('warRoom.decisionScaleReason', { brand: ourBrand, shift: roundToOne(ourShift), conversion: business.projectedConversion }),
      confidence: roundToOne(confidence),
    }
  }
  if (risk >= 62) {
    return {
      headline: t('warRoom.decisionContain'),
      rationale: t('warRoom.decisionContainReason', { risk: roundToOne(risk), exposure: formatMoney(business.crisisExposure) }),
      confidence: roundToOne(confidence),
    }
  }
  return {
    headline: t('warRoom.decisionPilot'),
    rationale: t('warRoom.decisionPilotReason', { shift: roundToOne(ourShift), conversion: business.projectedConversion }),
    confidence: roundToOne(confidence),
  }
}

function recommendationReadout(ourBrand, winner, ourShift, risk) {
  if (risk >= 62) {
    return {
      title: t('warRoom.recommendContain'),
      summary: t('warRoom.recommendContainSummary'),
      actions: [t('warRoom.actionCrisisCell'), t('warRoom.actionRewriteClaim'), t('warRoom.actionHoldSpend')],
    }
  }
  if (winner === ourBrand && ourShift >= 5) {
    return {
      title: t('warRoom.recommendAttack'),
      summary: t('warRoom.recommendAttackSummary'),
      actions: [t('warRoom.actionIncreaseBudget'), t('warRoom.actionLockCreators'), t('warRoom.actionMonitorCompetitor')],
    }
  }
  return {
    title: t('warRoom.recommendPilot'),
    summary: t('warRoom.recommendPilotSummary'),
    actions: [t('warRoom.actionRetestMessage'), t('warRoom.actionSegmentOffer'), t('warRoom.actionPrepareCounter')],
  }
}

function getShareAtRound(brand, round) {
  if (!result.value?.timeline) return 0
  const entry = result.value.timeline.find(item => item.round_num === round && item.brand_name === brand)
  return entry ? entry.market_share : 0
}

function average(values) {
  return values.reduce((sum, value) => sum + value, 0) / (values.length || 1)
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value))
}

function roundToOne(value) {
  return Math.round(value * 10) / 10
}

function formatMoney(value) {
  return new Intl.NumberFormat('th-TH', { maximumFractionDigits: 0 }).format(value)
}

function formatMoneyOrNA(value) {
  return value == null ? t('warRoom.notAvailable') : formatMoney(value)
}

function formatPercentOrNA(value) {
  return value == null ? t('warRoom.notAvailable') : `${value}%`
}

function formatCurrency(value) {
  return `${formatMoney(value * 10000)}`
}
</script>

<style scoped>
.war-room {
  min-height: 100vh;
  max-width: 1360px;
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
  margin-bottom: var(--space-7);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-subtle);
}

.page-kicker,
.section-label {
  display: block;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  letter-spacing: 0;
  text-transform: uppercase;
}

h1,
h2 {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-display);
}

h1 {
  font-size: clamp(2.1rem, 5vw, 3.8rem);
  line-height: 1;
}

h2 {
  font-size: clamp(1.35rem, 2.4vw, 2rem);
  line-height: 1.1;
}

.war-header p {
  max-width: 660px;
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

.command-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
  gap: var(--space-5);
  align-items: start;
}

.control-panel,
.competitor-panel,
.decision-console,
.chart-section,
.events-section,
.playbook-section,
.recommendation,
.result-card {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.control-panel,
.competitor-panel,
.chart-section,
.events-section,
.playbook-section,
.recommendation {
  padding: var(--space-6);
}

.panel-heading,
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

.panel-heading span {
  color: var(--text-primary);
  font-size: var(--text-lg);
  font-weight: 900;
}

.panel-heading strong {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
}

.field-block {
  display: grid;
  gap: var(--space-2);
  margin-bottom: var(--space-5);
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

select,
.competitor-main input {
  width: 100%;
  min-height: 44px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  color: var(--text-primary);
  font: inherit;
  font-size: var(--text-sm);
  font-weight: 800;
}

select {
  padding: 0 var(--space-4);
}

.scenario-grid,
.strategy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(168px, 1fr));
  gap: var(--space-3);
}

.choice-card,
.strategy-btn {
  min-height: 92px;
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  color: var(--text-secondary);
  text-align: left;
  cursor: pointer;
  transition: transform var(--transition-fast), border-color var(--transition-fast), background var(--transition-fast);
}

.choice-card:hover,
.strategy-btn:hover {
  transform: translateY(-1px);
  border-color: var(--border-accent);
}

.choice-card.active,
.strategy-btn.active {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.choice-card span,
.strategy-btn span {
  display: block;
  margin-bottom: var(--space-2);
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 900;
}

.choice-card small,
.strategy-btn small {
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  line-height: 1.5;
}

.strategy-section,
.slider-grid {
  margin-top: var(--space-5);
}

.slider-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.range-field {
  display: grid;
  gap: var(--space-2);
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
}

.range-field span,
.mini-controls span {
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.range-field strong,
.mini-controls strong {
  color: var(--text-primary);
  font-family: var(--font-mono);
}

input[type="range"] {
  width: 100%;
  accent-color: var(--accent);
}

.run-btn {
  width: 100%;
  min-height: 48px;
  margin-top: var(--space-5);
  border: 1px solid var(--accent);
  border-radius: var(--radius-md);
  background: var(--accent);
  color: var(--text-inverse);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 900;
}

.run-btn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.backend-warning {
  margin-top: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--yellow);
  border-radius: var(--radius-md);
  background: color-mix(in srgb, var(--yellow) 10%, transparent);
}

.backend-warning strong {
  color: var(--text-primary);
  font-size: var(--text-sm);
}

.backend-warning p {
  margin: var(--space-2) 0 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.local-fallback-btn {
  min-height: 38px;
  margin-top: var(--space-3);
  padding: 0 var(--space-4);
  border: 1px solid var(--yellow);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--yellow);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 900;
}

.competitor-list {
  display: grid;
  gap: var(--space-4);
}

.competitor-row {
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
}

.competitor-main {
  display: grid;
  grid-template-columns: 12px 1fr;
  gap: var(--space-3);
  align-items: center;
}

.competitor-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.competitor-main input {
  min-height: 38px;
  padding: 0 var(--space-3);
}

.mini-controls {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-3);
  margin-top: var(--space-3);
}

.mini-controls label {
  display: grid;
  gap: var(--space-1);
}

.competitor-row p {
  margin: var(--space-3) 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  line-height: 1.6;
}

.decision-console {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
  gap: var(--space-5);
  align-items: center;
  margin: var(--space-6) 0;
  padding: var(--space-6);
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.decision-console p,
.recommendation p {
  margin: var(--space-3) 0 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.decision-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-3);
}

.decision-metrics div {
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.decision-metrics span {
  display: block;
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.decision-metrics strong {
  display: block;
  margin-top: var(--space-2);
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: var(--text-lg);
}

.intelligence-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-4);
  margin: var(--space-6) 0;
}

.intel-card {
  min-height: 180px;
  padding: var(--space-5);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.intel-card ul,
.playbook-actions {
  margin: var(--space-3) 0 0;
  padding-left: var(--space-5);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.7;
}

.sentiment-list {
  display: grid;
  gap: var(--space-2);
  margin-top: var(--space-3);
}

.sentiment-list div {
  display: flex;
  justify-content: space-between;
  gap: var(--space-3);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.sentiment-list strong.positive {
  color: var(--green);
}

.sentiment-list strong.negative {
  color: var(--red);
}

.chart-section {
  margin: var(--space-6) 0;
}

.chart-legend {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-4);
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

.chart-container {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  padding: var(--space-5);
}

.chart-body {
  display: flex;
  gap: var(--space-3);
}

.chart-y {
  width: 42px;
  height: 312px;
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
  gap: 4px;
}

.chart-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.round-label {
  width: 32px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.round-bar {
  flex: 1;
  height: 22px;
  display: flex;
  overflow: hidden;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
}

.bar-segment {
  transition: width var(--transition-slow);
}

.war-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-5);
  margin: var(--space-6) 0;
}

.event-item,
.playbook-item {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: var(--space-3);
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--border-subtle);
}

.event-item:last-child,
.playbook-item:last-child {
  border-bottom: 0;
}

.event-round,
.playbook-item > span {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
}

.event-item strong,
.playbook-item strong {
  color: var(--text-primary);
  font-size: var(--text-sm);
}

.event-item p,
.playbook-item p {
  margin: var(--space-1) 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.playbook-actions {
  margin-top: var(--space-2);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin: var(--space-6) 0;
}

.result-card {
  padding: var(--space-6);
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
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(320px, 1.1fr);
  gap: var(--space-5);
  align-items: start;
}

.recommendation ol {
  margin: 0;
  padding-left: var(--space-5);
  color: var(--text-secondary);
  line-height: 1.8;
}

.recommended-response {
  color: var(--text-primary);
  font-weight: 800;
}

@media (max-width: 980px) {
  .war-header,
  .command-grid,
  .decision-console,
  .war-grid,
  .intelligence-grid,
  .recommendation {
    grid-template-columns: 1fr;
    flex-direction: column;
  }

  .decision-metrics,
  .slider-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .chart-body {
    overflow-x: auto;
  }

  .chart-rows {
    min-width: 680px;
  }

  .mini-controls {
    grid-template-columns: 1fr;
  }
}
</style>
