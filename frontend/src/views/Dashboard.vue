<template>
  <div class="dashboard">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-brand">{{ $t('dashboard.brand') }}</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">{{ $t('nav.home') }}</router-link>
        <router-link to="/settings" class="nav-link">{{ $t('nav.settings') }}</router-link>
        <ExportButton :data="exportData" :label="$t('common.export')" :filename="exportData.filename" />
        <span class="nav-campaign">#{{ campaignId }}</span>
      </div>
    </nav>

    <!-- Header Section -->
    <header class="dash-header">
      <div class="header-left">
        <h1 class="campaign-name">{{ campaignName }}</h1>
        <p class="campaign-meta">
          <span class="meta-date">{{ reportDate }}</span>
          <span class="meta-sep">|</span>
          <span class="meta-rounds">{{ totalRounds }} {{ $t('dashboard.simulationRounds') }}</span>
        </p>
      </div>
      <div class="header-right">
        <div :class="['grade-badge', gradeClass]">
          <span class="grade-letter">{{ overallGrade }}</span>
          <span class="grade-label">{{ $t('dashboard.overallScore') }}</span>
        </div>
      </div>
    </header>

    <div class="dash-body">
      <section class="decision-console panel">
        <div class="decision-main">
          <span class="brief-kicker">{{ $t('dashboard.decisionConsole') }}</span>
          <h2>{{ decisionHeadline }}</h2>
          <p>{{ decisionRationale }}</p>
          <div class="decision-actions-row">
            <span :class="['decision-verdict', `verdict-${decisionStrategy.verdict || 'controlled_pilot'}`]">
              {{ formatDecisionVerdict(decisionStrategy.verdict) }}
            </span>
            <span class="decision-confidence">
              {{ $t('dashboard.confidenceScore') }} {{ Math.round(decisionStrategy.confidence || confidenceScore) }}%
            </span>
          </div>
        </div>
        <div class="decision-side">
          <div class="next-action-card">
            <span>{{ $t('dashboard.nextBestAction') }}</span>
            <strong>{{ decisionNextAction }}</strong>
          </div>
          <div class="money-grid">
            <div>
              <span>{{ $t('dashboard.revenueImpact') }}</span>
              <strong>{{ formatCurrency(businessImpact.estimated_revenue_impact) }}</strong>
            </div>
            <div>
              <span>{{ $t('dashboard.crisisLoss') }}</span>
              <strong>{{ formatCurrency(businessImpact.estimated_crisis_loss) }}</strong>
            </div>
            <div>
              <span>{{ $t('dashboard.marketShareShift') }}</span>
              <strong>{{ formatSigned(businessImpact.market_share_shift_pct) }} pts</strong>
            </div>
            <div>
              <span>{{ $t('dashboard.roi') }}</span>
              <strong>{{ formatSigned(businessImpact.roi_pct) }}%</strong>
            </div>
          </div>
        </div>
      </section>

      <section class="what-if-console panel">
        <div class="what-if-header">
          <div>
            <span class="brief-kicker">{{ $t('dashboard.strategySandbox') }}</span>
            <h2 class="panel-title">{{ $t('dashboard.whatIfTitle') }}</h2>
          </div>
          <span v-if="whatIfLoading" class="sandbox-status">{{ $t('common.loading') }}</span>
        </div>
        <div class="scenario-row">
          <button
            v-for="scenario in whatIfScenarios"
            :key="scenario.key"
            type="button"
            :class="['scenario-button', { active: activeScenario === scenario.key }]"
            @click="runScenario(scenario)"
          >
            <strong>{{ $t(scenario.labelKey) }}</strong>
            <span>{{ $t(scenario.descKey) }}</span>
          </button>
        </div>
        <div v-if="whatIfResult" class="what-if-result">
          <div>
            <span>{{ $t('dashboard.conversionDelta') }}</span>
            <strong>{{ formatSigned(whatIfResult.delta?.conversion_probability) }} pts</strong>
          </div>
          <div>
            <span>{{ $t('dashboard.sentimentDelta') }}</span>
            <strong>{{ formatSigned(whatIfResult.delta?.overall_sentiment) }} pts</strong>
          </div>
          <div>
            <span>{{ $t('dashboard.riskDelta') }}</span>
            <strong>{{ formatSigned(whatIfResult.delta?.crisis_risk) }} pts</strong>
          </div>
          <div>
            <span>{{ $t('dashboard.projectedRevenue') }}</span>
            <strong>{{ formatCurrency(whatIfResult.business_impact?.estimated_revenue_impact) }}</strong>
          </div>
        </div>
      </section>

      <!-- Campaign Brief -->
      <section class="campaign-brief panel">
        <div class="brief-main">
          <span class="brief-kicker">{{ $t('dashboard.campaignBrief') }}</span>
          <h2>{{ campaignName }}</h2>
          <p>{{ campaignBrief.description || $t('dashboard.noCampaignDescription') }}</p>
        </div>
        <div class="brief-grid">
          <div class="brief-item">
            <span>{{ $t('dashboard.briefObjective') }}</span>
            <strong>{{ campaignBrief.objective }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefPlatform') }}</span>
            <strong>{{ campaignBrief.platform }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefPlatformMode') }}</span>
            <strong>{{ campaignBrief.platformMode }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefChannels') }}</span>
            <strong>{{ campaignBrief.channels }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefAudience') }}</span>
            <strong>{{ campaignBrief.audience }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefPersonas') }}</span>
            <strong>{{ campaignBrief.personas }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefRounds') }}</span>
            <strong>{{ campaignBrief.rounds }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.briefStatus') }}</span>
            <strong>{{ campaignBrief.status }}</strong>
          </div>
        </div>
      </section>

      <section class="confidence-evidence panel">
        <div class="evidence-header">
          <div>
            <span class="brief-kicker">{{ $t('dashboard.confidenceEvidence') }}</span>
            <h2 class="panel-title">{{ $t('dashboard.confidenceEvidenceTitle') }}</h2>
          </div>
          <ResultSourceBadge :source="trustPanel.sourceType" :warning="trustPanel.sourceWarning" />
        </div>
        <div class="trust-grid">
          <div class="brief-item">
            <span>{{ $t('dashboard.trustRunId') }}</span>
            <strong>{{ trustPanel.runId }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.trustPersonaCount') }}</span>
            <strong>{{ trustPanel.personaCount }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.trustBriefCompleteness') }}</span>
            <strong>{{ trustPanel.briefCompleteness }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.trustProviderModel') }}</span>
            <strong>{{ trustPanel.providerModel }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.trustConfidenceLevel') }}</span>
            <strong>{{ trustPanel.confidenceLevel }}</strong>
          </div>
          <div class="brief-item">
            <span>{{ $t('dashboard.trustNextValidation') }}</span>
            <strong>{{ trustPanel.nextValidationStep }}</strong>
          </div>
        </div>
        <ul class="trust-limitations">
          <li v-for="item in trustPanel.knownLimitations" :key="item">{{ item }}</li>
        </ul>
      </section>

      <!-- KPI Cards Row -->
      <section class="kpi-row">
        <div class="kpi-card sentiment-card">
          <div class="kpi-icon">SI</div>
          <div class="kpi-content">
            <span class="kpi-label">{{ $t('dashboard.overallSentiment') }}</span>
            <div class="sentiment-gauge">
              <div class="gauge-track">
                <div class="gauge-fill-negative" :style="{ width: negativeGaugeWidth }"></div>
                <div class="gauge-fill-positive" :style="{ width: positiveGaugeWidth }"></div>
              </div>
              <div class="gauge-scale">
                <span>-100</span><span>0</span><span>+100</span>
              </div>
            </div>
            <span :class="['kpi-value', sentimentClass]">{{ formatSentiment(kpis.overall_sentiment) }}</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">CV</div>
          <div class="kpi-content">
            <span class="kpi-label">{{ $t('dashboard.conversionProbability') }}</span>
            <span class="kpi-value big">{{ kpis.conversion_probability }}%</span>
            <div class="kpi-bar">
              <div class="kpi-bar-fill conversion" :style="{ width: kpis.conversion_probability + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">IF</div>
          <div class="kpi-content">
            <span class="kpi-label">{{ $t('dashboard.socialInfluence') }}</span>
            <span class="kpi-value big">{{ kpis.social_influence }}/100</span>
            <div class="kpi-bar">
              <div class="kpi-bar-fill influence" :style="{ width: kpis.social_influence + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">MR</div>
          <div class="kpi-content">
            <span class="kpi-label">{{ $t('dashboard.messageResonance') }}</span>
            <span class="kpi-value big">{{ kpis.message_resonance }}%</span>
            <div class="kpi-bar">
              <div class="kpi-bar-fill resonance" :style="{ width: kpis.message_resonance + '%' }"></div>
            </div>
          </div>
        </div>

        <div :class="['kpi-card', 'crisis-card', crisisClass]">
          <div class="kpi-icon">CR</div>
          <div class="kpi-content">
            <span class="kpi-label">{{ $t('dashboard.crisisRisk') }}</span>
            <span class="kpi-value big">{{ crisisLabel }}</span>
            <div class="crisis-indicator">
              <span class="crisis-dot" :style="{ background: crisisColor }"></span>
              <span class="crisis-text">Level {{ crisisLevel }}</span>
            </div>
          </div>
        </div>
      </section>

      <section class="decision-evidence panel">
        <div class="evidence-header">
          <div>
            <span class="brief-kicker">{{ $t('dashboard.decisionEvidence') }}</span>
            <h2 class="panel-title">{{ $t('dashboard.whyTrustThis') }}</h2>
          </div>
          <div class="confidence-pill">
            <span>{{ $t('dashboard.confidenceScore') }}</span>
            <strong>{{ confidenceScore }}%</strong>
          </div>
        </div>
        <div class="evidence-grid">
          <article class="evidence-block">
            <h3>{{ $t('dashboard.whyThisScore') }}</h3>
            <ul>
              <li v-for="item in scoreExplanations" :key="item">{{ item }}</li>
            </ul>
          </article>
          <article class="evidence-block">
            <h3>{{ $t('dashboard.riskDrivers') }}</h3>
            <ul>
              <li v-for="item in riskDrivers" :key="item">{{ item }}</li>
            </ul>
          </article>
          <article class="evidence-block">
            <h3>{{ $t('dashboard.assumptions') }}</h3>
            <ul>
              <li v-for="item in assumptions" :key="item">{{ item }}</li>
            </ul>
          </article>
          <article class="evidence-block quotes">
            <h3>{{ $t('dashboard.simulatedQuotes') }}</h3>
            <blockquote v-for="quote in simulatedQuotes" :key="quote">{{ quote }}</blockquote>
          </article>
        </div>
        <div class="business-map">
          <article v-for="item in businessMapping" :key="item.kpi" class="business-map-item">
            <span>{{ item.kpi }}</span>
            <strong>{{ item.business_meaning }}</strong>
            <small>{{ item.interpretation }}</small>
          </article>
        </div>
      </section>

      <!-- Sentiment Timeline + Segment Breakdown -->
      <section class="mid-row">
        <!-- Sentiment Timeline Chart -->
        <div class="panel chart-panel">
          <h2 class="panel-title">{{ $t('dashboard.sentimentTimeline') }}</h2>
          <div class="chart-container">
            <div class="chart-y-axis">
              <span>+100</span>
              <span>0</span>
              <span>-100</span>
            </div>
            <div class="chart-bars">
              <div
                v-for="(round, idx) in timeline"
                :key="idx"
                class="chart-bar-group"
                :title="`Round ${round.round_num}: Sentiment ${formatSentiment(round.sentiment)}`"
              >
                <div class="bar-value-label">{{ formatSentiment(round.sentiment) }}</div>
                <div class="bar-wrapper">
                  <div
                    :class="['bar-fill', round.sentiment >= 0 ? 'bar-positive' : 'bar-negative']"
                    :style="{ height: barHeight(round.sentiment) }"
                  ></div>
                </div>
                <span class="bar-round-label">R{{ round.round_num }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Segment Breakdown Table -->
        <div class="panel table-panel">
          <h2 class="panel-title">{{ $t('dashboard.personaSegmentBreakdown') }}</h2>
          <table class="segment-table">
            <thead>
              <tr>
                <th>{{ $t('dashboard.tableSegment') }}</th>
                <th>{{ $t('dashboard.tableSentiment') }}</th>
                <th>{{ $t('dashboard.tableConvEst') }}</th>
                <th>{{ $t('dashboard.tableSize') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(seg, idx) in segments" :key="idx">
                <td class="seg-name">{{ seg.name }}</td>
                <td>
                  <span :class="['sentiment-tag', seg.sentiment >= 0 ? 'tag-positive' : 'tag-negative']">
                    {{ formatSentiment(seg.sentiment) }}
                  </span>
                </td>
                <td>
                  <div class="mini-bar-wrap">
                    <div class="mini-bar" :style="{ width: seg.conversion_estimate + '%' }"></div>
                    <span class="mini-bar-val">{{ seg.conversion_estimate }}%</span>
                  </div>
                </td>
                <td class="seg-size">{{ seg.size }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Simulated influence nodes -->
      <section class="panel">
        <h2 class="panel-title">{{ $t('dashboard.topInfluencers') }}</h2>
        <p class="panel-note">{{ $t('dashboard.syntheticInfluencerNote') }}</p>
        <div class="influencer-grid">
          <div v-for="(inf, idx) in influencers" :key="idx" class="influencer-card">
            <div class="inf-rank">#{{ idx + 1 }}</div>
            <div class="inf-avatar">{{ inf.name.charAt(0) }}</div>
            <div class="inf-info">
              <span class="inf-name">{{ inf.name }}</span>
              <span class="inf-platform">{{ inf.platform }}</span>
            </div>
            <div class="inf-metrics">
              <div class="inf-metric">
                <span class="inf-metric-label">{{ $t('dashboard.influencerImpact') }}</span>
                <span class="inf-metric-val">{{ inf.impact_score }}/100</span>
              </div>
              <div class="inf-metric">
                <span class="inf-metric-label">{{ $t('dashboard.influencerReach') }}</span>
                <span class="inf-metric-val">{{ formatNumber(inf.reach) }}</span>
              </div>
            </div>
            <div class="inf-sentiment">
              <span :class="['sentiment-tag', inf.sentiment >= 0 ? 'tag-positive' : 'tag-negative']">
                {{ formatSentiment(inf.sentiment) }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Action Plan: Think to Finish -->
      <section ref="actionPlanSection" class="action-plan">
        <div class="action-plan-head">
          <div>
            <h2 class="panel-title">{{ $t('dashboard.actionPlan') }}</h2>
            <p>{{ displayActionPlan.disclaimer }}</p>
          </div>
          <div class="action-plan-tools">
            <ResultSourceBadge
              :source="displayActionPlan.source.type"
              :warning="displayActionPlan.source.warning"
            />
            <button class="copy-action-plan" type="button" @click="copyActionPlan">
              {{ actionPlanCopied ? $t('dashboard.actionPlanCopied') : $t('dashboard.copyActionPlan') }}
            </button>
          </div>
        </div>

        <div class="action-grid">
          <!-- Winning Strategy -->
          <div class="action-box winning">
            <div class="action-box-header">
              <span class="action-icon">WS</span>
              <h3>{{ $t('dashboard.winningStrategy') }}</h3>
            </div>
            <p class="action-box-text">{{ winningStrategy }}</p>
            <ul class="winning-highlights">
              <li v-for="(pt, idx) in winningHighlights" :key="idx">{{ pt }}</li>
            </ul>
          </div>

          <!-- Risk Areas -->
          <div class="action-box risk">
            <div class="action-box-header">
              <span class="action-icon">RA</span>
              <h3>{{ $t('dashboard.riskAreas') }}</h3>
            </div>
            <p class="action-box-text">{{ riskSummary }}</p>
            <ul class="risk-list">
              <li v-for="(r, idx) in riskAreas" :key="idx">
                <span class="risk-severity" :style="{ color: severityColor(r.severity) }">
                  {{ r.severity === 'high' ? 'HIGH' : 'MED' }}
                </span>
                {{ r.description }}
              </li>
            </ul>
          </div>
        </div>

        <div class="structured-action-grid">
          <div
            v-for="section in actionPlanSections"
            :key="section.key"
            class="structured-action-section"
          >
            <div class="structured-section-head">
              <span class="section-label">{{ section.title }}</span>
            </div>
            <div
              v-for="(item, itemIdx) in section.items"
              :key="`${section.key}-${itemIdx}`"
              class="structured-action-item"
            >
              <strong>{{ item.recommendation }}</strong>
              <dl>
                <div>
                  <dt>{{ $t('dashboard.actionReason') }}</dt>
                  <dd>{{ item.reason }}</dd>
                </div>
                <div>
                  <dt>{{ $t('dashboard.actionExpectedImpact') }}</dt>
                  <dd>{{ item.expected_impact }}</dd>
                </div>
                <div>
                  <dt>{{ $t('dashboard.actionRisk') }}</dt>
                  <dd>{{ item.risk }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        <!-- Action Items -->
        <div class="action-items">
          <h3 class="action-items-title">{{ $t('dashboard.priorityActionItems') }}</h3>
          <div class="action-item-list">
            <div v-for="(item, idx) in actionItems" :key="idx" class="action-item">
              <span class="action-item-num">{{ idx + 1 }}</span>
              <div class="action-item-body">
                <span class="action-item-priority" :style="{ color: priorityColor(item.priority) }">
                  {{ item.priority.toUpperCase() }}
                </span>
                <span class="action-item-desc">{{ item.description || item.recommendation || item.action }}</span>
                <span class="action-item-timeline">{{ item.timeline }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Executive Summary -->
      <section class="panel summary-panel">
        <div class="summary-header" @click="showSummary = !showSummary">
          <h2 class="panel-title">{{ $t('dashboard.executiveSummaryTH') }}</h2>
          <span class="summary-toggle">{{ showSummary ? '▲' : '▼' }}</span>
        </div>
        <div v-if="showSummary" class="summary-content">
          <p class="summary-thai">{{ executiveSummaryTH }}</p>
        </div>
      </section>

      <!-- Data Info -->
      <div class="data-info">
        <span>{{ $t('common.loading') }}...</span>
        <span v-if="loading">{{ $t('dashboard.fetchingData') }}</span>
        <span v-else>{{ $t('dashboard.lastUpdated') }}: {{ lastUpdated }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getKPIs, getTimeline, getSegments, getInfluencers } from '@/api/dashboard'
import { getCampaign, hasCampaignAuth } from '@/api/campaign'
import { getDemoDashboard } from '@/api/demo'
import { analyzeDecision, runWhatIf } from '@/api/decision'
import ExportButton from '@/components/ExportButton.vue'
import ResultSourceBadge from '@/components/ResultSourceBadge.vue'
import { sourceModeFromValue, trackEvent } from '@/services/analytics'

const route = useRoute()
const { t } = useI18n()

const campaignId = computed(() => route.params.campaignId)
const campaignName = ref('Campaign Analysis')
const reportDate = ref('')
const totalRounds = ref(0)
const overallGrade = ref('B+')
const loading = ref(true)
const showSummary = ref(false)
const lastUpdated = ref('')
const campaignDetails = ref(null)
const resultSource = ref({ type: 'unknown', warning: '' })

// Export data (computed from current state)
const exportData = computed(() => ({
  slide_type: 'dashboard',
  title: `${campaignName.value} — Executive Summary`,
  subtitle: `${reportDate.value} | ${totalRounds.value} Rounds | Grade: ${overallGrade.value}`,
  kpis: {
    overall_sentiment: kpis.value.overall_sentiment,
    conversion_probability: kpis.value.conversion_probability,
    social_influence_index: kpis.value.social_influence,
    message_resonance: kpis.value.message_resonance,
    crisis_risk: crisisLabel.value,
    brand_perception_shift: kpis.value.brand_perception_shift || 12,
    opinion_polarization: kpis.value.opinion_polarization || 35,
    roi_pct: kpis.value.conversion_probability - 40,
  },
  timeline: timeline.value,
  action_plan: displayActionPlan.value,
  recommendation: executiveSummaryTH.value || winningStrategy.value || 'Review action plan for next steps.',
  revenue_projection: {
    monthly: kpis.value.conversion_probability * 10000,
    annual: kpis.value.conversion_probability * 120000,
    crisis_loss: crisisLevel.value * 500000,
  },
  filename: `msaas_${campaignName.value.replace(/\s+/g, '_').toLowerCase()}`,
}))

const campaignBrief = computed(() => {
  const campaign = campaignDetails.value || {}
  const target = campaign.target || campaign.audience || {}
  const simConfig = campaign.sim_config || {}
  const ageRange = target.age_range || [target.age_min, target.age_max].filter(Boolean)
  const channels = normalizeChannels(
    target.channels || simConfig.audience_channels || campaign.audience_channels || []
  )
  const regions = Array.isArray(target.regions) && target.regions.length
    ? target.regions.join(', ')
    : ''
  const audienceParts = [
    target.segment_name,
    Array.isArray(ageRange) && ageRange.length === 2 ? `${ageRange[0]}-${ageRange[1]}` : '',
    regions,
  ].filter(Boolean)

  return {
    description: campaign.description || '',
    objective: formatObjective(campaign.objective),
    platform: formatPlatform(simConfig.platform || campaign.platform),
    platformMode: formatPlatformMode(
      simConfig.platform_mode ||
      campaign.platform_mode ||
      simConfig.oasis_preset?.resolved_mode ||
      simConfig.oasis_preset?.mode
    ),
    channels: channels.length ? channels.map(formatChannel).join(', ') : t('dashboard.briefNotSpecified'),
    audience: audienceParts.join(' / ') || t('dashboard.briefNotSpecified'),
    personas: target.persona_count || campaign.persona_count || '—',
    rounds: simConfig.max_rounds || campaign.max_rounds || totalRounds.value || '—',
    status: formatStatus(campaign.status),
  }
})

const trustPanel = computed(() => {
  const campaign = campaignDetails.value || {}
  const simConfig = campaign.sim_config || {}
  const briefQuality = campaign.brief_quality || {}
  const completeness = briefQuality?.brief_completeness?.percent ?? briefQuality?.score
  const provider = simConfig.llm_provider || simConfig.provider || campaign.llm_provider
  const model = simConfig.llm_model || simConfig.model || campaign.llm_model
  const sourceType = resultSource.value?.type || 'unknown'
  const sourceWarning = resultSource.value?.warning || ''
  const limitations = [
    ...((resultSource.value && Array.isArray(resultSource.value.limitations)) ? resultSource.value.limitations : []),
    ...(briefQuality.known_limitations || []),
    ...(assumptions.value || []),
  ].filter(Boolean).slice(0, 4)

  return {
    sourceType,
    sourceWarning,
    runId: campaign.simulation_id || campaign.report_id || campaign.campaign_id || campaign.id || t('dashboard.trustNotAvailable'),
    personaCount: campaignBrief.value.personas || t('dashboard.trustNotAvailable'),
    briefCompleteness: completeness != null ? `${completeness}%` : t('dashboard.trustUnknown'),
    providerModel: provider || model ? [provider, model].filter(Boolean).join(' / ') : t('dashboard.trustNotAvailable'),
    confidenceLevel: confidenceScore.value ? `${confidenceScore.value}%` : t('dashboard.trustUnknown'),
    knownLimitations: limitations.length ? limitations : [t('dashboard.trustNoLimitationsAvailable')],
    nextValidationStep: briefQuality.score != null && briefQuality.score < 80
      ? t('dashboard.trustValidateBrief')
      : t('dashboard.trustValidateLiveMarket'),
  }
})

// KPI State
const kpis = ref({
  overall_sentiment: 42,
  conversion_probability: 67,
  social_influence: 78,
  message_resonance: 72,
  crisis_risk: 'low'
})

// Timeline State
const timeline = ref([])

// Segments State
const segments = ref([])

// Influencers State
const influencers = ref([])

// Action Plan State
const winningStrategy = ref('')
const winningHighlights = ref([])
const riskSummary = ref('')
const riskAreas = ref([])
const actionItems = ref([])
const structuredActionPlan = ref(null)
const actionPlanCopied = ref(false)
const executiveSummaryTH = ref('')
const confidenceScore = ref(78)
const assumptions = ref([])
const scoreExplanations = ref([])
const riskDrivers = ref([])
const simulatedQuotes = ref([])
const decisionStrategy = ref({})
const businessImpact = ref({})
const businessMapping = ref([])
const primaryRisk = ref({})
const whatIfResult = ref(null)
const whatIfLoading = ref(false)
const activeScenario = ref('')
const actionPlanSection = ref(null)
let actionPlanObserver = null
let actionPlanViewedTracked = false

const whatIfScenarios = [
  {
    key: 'proof',
    labelKey: 'dashboard.whatIfProof',
    descKey: 'dashboard.whatIfProofDesc',
    scenario: { proof_points: true, testimonials: true },
  },
  {
    key: 'discount',
    labelKey: 'dashboard.whatIfDiscount',
    descKey: 'dashboard.whatIfDiscountDesc',
    scenario: { price_discount_pct: 10, proof_points: true },
  },
  {
    key: 'competitor',
    labelKey: 'dashboard.whatIfCompetitor',
    descKey: 'dashboard.whatIfCompetitorDesc',
    scenario: { competitor_launch: true, budget_increase_pct: 20 },
  },
]

const displayActionPlan = computed(() => structuredActionPlan.value || buildLocalActionPlan())

const actionPlanSections = computed(() => {
  const plan = displayActionPlan.value
  const sections = plan.sections || {}
  return [
    'creative_adjustment',
    'channel_allocation',
    'crisis_prevention',
    'validation_plan',
  ].map(key => ({
    key,
    title: sections[key]?.title || t(`dashboard.actionSection_${key}`),
    items: sections[key]?.items || [],
  }))
})

// --- Computed: Grade class ---
const gradeClass = computed(() => {
  const g = overallGrade.value.charAt(0).toUpperCase()
  if (['A', 'B'].includes(g)) return 'grade-good'
  if (['C'].includes(g)) return 'grade-ok'
  return 'grade-bad'
})

// --- Computed: Sentiment gauge ---
const sentimentValue = computed(() => kpis.value.overall_sentiment)
const negativeGaugeWidth = computed(() => {
  if (sentimentValue.value >= 0) return '50%'
  return (50 + sentimentValue.value / 2) + '%'
})
const positiveGaugeWidth = computed(() => {
  if (sentimentValue.value <= 0) return '50%'
  return (50 + sentimentValue.value / 2) + '%'
})
const sentimentClass = computed(() => {
  if (sentimentValue.value > 20) return 'sentiment-positive'
  if (sentimentValue.value < -20) return 'sentiment-negative'
  return 'sentiment-neutral'
})

// --- Computed: Crisis ---
const crisisLevel = computed(() => {
  const r = kpis.value.crisis_risk
  if (typeof r === 'number') {
    if (r >= 65) return 3
    if (r >= 35) return 2
    return 1
  }
  if (r === 'high') return 3
  if (r === 'medium') return 2
  return 1
})
const crisisLabel = computed(() => {
  const r = kpis.value.crisis_risk
  if (typeof r === 'number') {
    if (r >= 65) return t('dashboard.crisisHigh')
    if (r >= 35) return t('dashboard.crisisMedium')
    return t('dashboard.crisisLow')
  }
  if (r === 'high') return t('dashboard.crisisHigh')
  if (r === 'medium') return t('dashboard.crisisMedium')
  return t('dashboard.crisisLow')
})
const crisisColor = computed(() => {
  const r = kpis.value.crisis_risk
  if (typeof r === 'number') {
    if (r >= 65) return 'var(--red)'
    if (r >= 35) return 'var(--yellow)'
    return 'var(--green)'
  }
  if (r === 'high') return 'var(--red)'
  if (r === 'medium') return 'var(--yellow)'
  return 'var(--green)'
})
const crisisClass = computed(() => {
  const r = kpis.value.crisis_risk
  if (typeof r === 'number') {
    if (r >= 65) return 'crisis-high'
    if (r >= 35) return 'crisis-medium'
    return 'crisis-low'
  }
  return `crisis-${r}`
})

const decisionHeadline = computed(() => {
  if (!decisionStrategy.value.verdict) return t('dashboard.decisionPending')
  const map = {
    launch_with_guardrails: t('dashboard.decisionHeadlineLaunch'),
    revise_before_launch: t('dashboard.decisionHeadlineRevise'),
    optimize_message: t('dashboard.decisionHeadlineOptimize'),
    controlled_pilot: t('dashboard.decisionHeadlinePilot'),
  }
  return map[decisionStrategy.value.verdict] || decisionStrategy.value.headline || t('dashboard.decisionPending')
})

const decisionRationale = computed(() => {
  if (!decisionStrategy.value.verdict) return t('dashboard.decisionPendingDesc')
  return t('dashboard.decisionRationale', {
    conversion: Math.round(kpis.value.conversion_probability || 0),
    risk: crisisLabel.value,
    segment: topPositiveSegmentLabel(),
  })
})

const decisionNextAction = computed(() => {
  const verdict = decisionStrategy.value.verdict
  const map = {
    launch_with_guardrails: t('dashboard.decisionNextLaunch'),
    revise_before_launch: t('dashboard.decisionNextRevise'),
    optimize_message: t('dashboard.decisionNextOptimize'),
    controlled_pilot: t('dashboard.decisionNextPilot'),
  }
  return map[verdict] || decisionStrategy.value.next_best_action || primaryRisk.value.recommended_action || t('dashboard.decisionPending')
})

// --- Helpers ---
function formatSentiment(val) {
  if (val == null) return '—'
  const prefix = val > 0 ? '+' : ''
  return prefix + Math.round(val)
}

function formatNumber(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return String(n)
}

function formatCurrency(value) {
  const n = Number(value || 0)
  const abs = Math.abs(n)
  const sign = n < 0 ? '-' : ''
  if (abs >= 1000000) return `${sign}฿${(abs / 1000000).toFixed(1)}M`
  if (abs >= 1000) return `${sign}฿${(abs / 1000).toFixed(0)}K`
  return `${sign}฿${abs.toFixed(0)}`
}

function formatSigned(value) {
  const n = Number(value || 0)
  if (n > 0) return `+${Number.isInteger(n) ? n : n.toFixed(1)}`
  if (n < 0) return Number.isInteger(n) ? String(n) : n.toFixed(1)
  return '0'
}

function formatDecisionVerdict(verdict) {
  const map = {
    launch_with_guardrails: t('dashboard.verdictLaunch'),
    revise_before_launch: t('dashboard.verdictRevise'),
    optimize_message: t('dashboard.verdictOptimize'),
    controlled_pilot: t('dashboard.verdictPilot'),
  }
  return map[verdict] || map.controlled_pilot
}

function barHeight(val) {
  const pct = Math.max(0, Math.min(100, ((val + 100) / 200) * 100))
  return pct + '%'
}

function priorityColor(p) {
  if (p === 'critical') return 'var(--red)'
  if (p === 'high') return 'var(--accent)'
  if (p === 'medium') return 'var(--yellow)'
  return 'var(--green)'
}

function severityColor(severity) {
  return severity === 'high' ? 'var(--red)' : 'var(--yellow)'
}

function formatObjective(objective) {
  const map = {
    message_testing: t('campaigns.objectiveMessageTesting'),
    crisis_simulation: t('campaigns.objectiveCrisisSimulation'),
    product_launch: t('campaigns.objectiveProductLaunch'),
    competitor_response: t('campaigns.objectiveCompetitorResponse'),
    brand_perception: t('campaigns.objectiveBrandPerception'),
  }
  return map[objective] || objective || t('dashboard.briefNotSpecified')
}

function formatPlatform(platform) {
  const map = {
    twitter: t('campaigns.platformTwitter'),
    reddit: t('campaigns.platformReddit'),
    both: t('campaigns.platformBoth'),
  }
  return map[platform] || platform || t('dashboard.briefNotSpecified')
}

function formatPlatformMode(mode) {
  const map = {
    auto: t('campaigns.modeAuto'),
    microblog: t('campaigns.modeMicroblog'),
    community_forum: t('campaigns.modeCommunityForum'),
    group_chat: t('campaigns.modeGroupChat'),
    creator_feed: t('campaigns.modeCreatorFeed'),
    commerce_intent: t('campaigns.modeCommerceIntent'),
  }
  return map[mode] || mode || t('dashboard.briefNotSpecified')
}

function formatChannel(channel) {
  const map = {
    facebook: t('campaigns.channelFacebook'),
    instagram: t('campaigns.channelInstagram'),
    tiktok: t('campaigns.channelTikTok'),
    youtube: t('campaigns.channelYouTube'),
    line: t('campaigns.channelLine'),
    twitter_x: t('campaigns.channelTwitterX'),
    twitter: t('campaigns.channelTwitterX'),
    reddit: t('campaigns.channelReddit'),
    linkedin: t('campaigns.channelLinkedIn'),
    whatsapp: 'WhatsApp',
    tv: 'TV',
    radio: 'Radio',
    shopee_live: 'Shopee Live',
  }
  return map[channel] || channel
}

function normalizeChannels(channels) {
  const values = Array.isArray(channels) ? channels : []
  return [...new Set(values.map((channel) => {
    if (channel === 'twitter') return 'twitter_x'
    return String(channel || '').trim()
  }).filter(Boolean))]
}

function formatStatus(status) {
  const map = {
    draft: t('campaigns.statusDraft'),
    active: t('campaigns.statusActive'),
    running: t('campaigns.statusRunning'),
    complete: t('campaigns.statusComplete'),
    completed: t('campaigns.statusComplete'),
    failed: t('campaigns.statusFailed'),
    paused: t('campaigns.statusPaused'),
    persona_building: t('campaigns.personaGeneration'),
    simulating: t('campaigns.simulationRunning'),
  }
  return map[status] || status || t('dashboard.briefNotSpecified')
}

async function loadCampaignDetails(cid) {
  if (shouldUseDemoCampaignDetails()) {
    campaignDetails.value = demoCampaignDetails(cid)
    if (campaignDetails.value?.name) campaignName.value = campaignDetails.value.name
    return
  }

  try {
    const campaignRes = await getCampaign(cid)
    const campaign = campaignRes.data || campaignRes
    campaignDetails.value = campaign
    if (campaign?.name) campaignName.value = campaign.name
  } catch (e) {
    console.warn('Campaign details fetch failed, using fallback:', e.message)
    campaignDetails.value = demoCampaignDetails(cid)
    if (campaignDetails.value?.name) campaignName.value = campaignDetails.value.name
  }
}

function shouldUseDemoCampaignDetails() {
  return String(campaignId.value || '').startsWith('demo-') || !hasCampaignAuth()
}

function demoCampaignDetails(cid) {
  const demos = {
    'demo-1': {
      name: 'Bank Digital Wallet Launch',
      description: 'Market sentiment simulation for a new digital wallet feature targeting Thai urban customers.',
      objective: 'product_launch',
      status: 'complete',
      target: { segment_name: 'Thai Urban Millennials', age_range: [22, 44], regions: ['Thailand'], persona_count: 120, channels: ['facebook', 'instagram', 'tiktok', 'twitter_x', 'reddit'] },
      sim_config: { platform: 'both', platform_mode: 'creator_feed', max_rounds: 8, audience_channels: ['facebook', 'instagram', 'tiktok', 'twitter_x', 'reddit'] },
    },
    'demo-2': {
      name: 'Crisis Response: Data Breach',
      description: 'Public reaction simulation for a hypothetical data breach and response-message test.',
      objective: 'crisis_simulation',
      status: 'running',
      target: { segment_name: 'Digital Banking Customers', age_range: [20, 58], regions: ['Thailand'], persona_count: 85, channels: ['twitter_x', 'facebook', 'line'] },
      sim_config: { platform: 'twitter', platform_mode: 'microblog', max_rounds: 12, audience_channels: ['twitter_x', 'facebook', 'line'] },
    },
    'demo-3': {
      name: 'Competitor Messaging Analysis',
      description: 'Test how competitor launch messaging resonates across audience segments.',
      objective: 'competitor_response',
      status: 'draft',
      target: { segment_name: 'Category Shoppers', age_range: [18, 55], regions: ['Thailand'], persona_count: 200, channels: ['reddit', 'youtube', 'linkedin'] },
      sim_config: { platform: 'reddit', platform_mode: 'community_forum', max_rounds: 15, audience_channels: ['reddit', 'youtube', 'linkedin'] },
    },
  }
  return demos[cid] || {
    name: campaignName.value,
    description: '',
    objective: 'message_testing',
    status: 'draft',
    target: { segment_name: t('dashboard.briefNotSpecified'), persona_count: 100 },
    sim_config: { platform: 'both', max_rounds: totalRounds.value || 10 },
  }
}

// --- Load data ---
async function loadDashboard() {
  loading.value = true
  try {
    const cid = campaignId.value
    const useDemoData = shouldUseDemoCampaignDetails()

    if (useDemoData) {
      await loadDemoDashboard(cid)
      lastUpdated.value = new Date().toLocaleString()
      reportDate.value = new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
      return
    }

    await loadCampaignDetails(cid)
    resultSource.value = { type: 'unknown', warning: t('dashboard.sourceUnknownPending') }

    // Fetch KPIs
    try {
      const kpiRes = await getKPIs(cid)
      if (kpiRes && kpiRes.data) {
        Object.assign(kpis.value, normalizeKpis(kpiRes.data))
        resultSource.value = normalizeResultSource(kpiRes.data.source || kpiRes.data)
        if (kpiRes.data.confidence != null) {
          confidenceScore.value = Math.round(kpiRes.data.confidence)
        }
        if (kpiRes.data.action_plan) {
          structuredActionPlan.value = normalizeActionPlan(kpiRes.data.action_plan)
        }
      }
      if (kpiRes && kpiRes.campaign_name) campaignName.value = kpiRes.campaign_name
      if (kpiRes && kpiRes.grade) overallGrade.value = kpiRes.grade
    } catch (e) {
      console.warn('KPIs fetch failed, using defaults:', e.message)
    }

    // Fetch Timeline
    try {
      const tlRes = await getTimeline(cid)
      const tlData = tlRes?.data || tlRes || {}
      if (tlData.source && resultSource.value?.type === 'unknown') {
        resultSource.value = normalizeResultSource(tlData.source)
      }
      const points = tlData.timeline || tlData.rounds || []
      if (points.length) {
        timeline.value = points.map(normalizeTimelinePoint)
        totalRounds.value = timeline.value.length
      }
    } catch (e) {
      console.warn('Timeline fetch failed:', e.message)
    }

    // Fetch Segments
    try {
      const segRes = await getSegments(cid)
      const segData = segRes?.data || segRes || {}
      if (segData.source && resultSource.value?.type === 'unknown') {
        resultSource.value = normalizeResultSource(segData.source)
      }
      const rows = segData.segments || segData
      if (Array.isArray(rows) && rows.length) {
        segments.value = rows.map(normalizeSegment)
      }
    } catch (e) {
      console.warn('Segments fetch failed:', e.message)
    }

    // Fetch Influencers
    try {
      const infRes = await getInfluencers(cid)
      if (infRes && infRes.influencers) {
        influencers.value = infRes.influencers
      }
    } catch (e) {
      console.warn('Influencers fetch failed:', e.message)
    }

    // If backend returned action plan data, use it
    if (typeof kpis.value.winning_strategy === 'string') {
      winningStrategy.value = kpis.value.winning_strategy
    }
    if (Array.isArray(kpis.value.winning_highlights)) {
      winningHighlights.value = kpis.value.winning_highlights
    }
    if (typeof kpis.value.risk_summary === 'string') {
      riskSummary.value = kpis.value.risk_summary
    }
    if (Array.isArray(kpis.value.risk_areas)) {
      riskAreas.value = kpis.value.risk_areas
    }
    if (Array.isArray(kpis.value.action_items)) {
      actionItems.value = kpis.value.action_items
    }
    if (typeof kpis.value.executive_summary_th === 'string') {
      executiveSummaryTH.value = kpis.value.executive_summary_th
    }

    buildEvidenceFromCurrentState()
    await loadDecisionEngine()

    lastUpdated.value = new Date().toLocaleString()
    reportDate.value = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    console.error('Dashboard load error:', e)
  } finally {
    loading.value = false
  }
}

async function loadDemoDashboard(cid) {
  const demoId = String(cid || '').startsWith('demo-') ? cid : 'demo-premium-water'
  try {
    const res = await getDemoDashboard(demoId)
    applyDemoDashboard(res.data || res)
  } catch (e) {
    console.warn('Demo dashboard API unavailable, using local fallback:', e.message)
    resultSource.value = { type: 'local_estimate', warning: t('dashboard.sourceLocalFallback') }
    campaignDetails.value = demoCampaignDetails(demoId)
    if (campaignDetails.value?.name) campaignName.value = campaignDetails.value.name
    buildEvidenceFromCurrentState()
  }
}

function applyDemoDashboard(data) {
  const campaign = data.campaign || demoCampaignDetails('demo-premium-water')
  resultSource.value = normalizeResultSource(data.source || { type: 'demo_mode', warning: t('dashboard.sourceDemoMode') })
  campaignDetails.value = campaign
  campaignName.value = campaign.name || campaignName.value
  Object.assign(kpis.value, normalizeKpis(data.kpis || {}))
  timeline.value = (data.timeline || []).map(normalizeTimelinePoint)
  segments.value = (data.segments || []).map(normalizeSegment)
  influencers.value = data.influencers || []
  totalRounds.value = timeline.value.length || campaign?.sim_config?.max_rounds || 0

  const evidence = data.evidence || {}
  confidenceScore.value = evidence.confidence_score || data.kpis?.confidence_score || 78
  assumptions.value = evidence.assumptions || []
  scoreExplanations.value = evidence.why_this_score || []
  riskDrivers.value = evidence.risk_drivers || []
  simulatedQuotes.value = evidence.quotes || []
  structuredActionPlan.value = data.action_plan ? normalizeActionPlan(data.action_plan) : null

  if (Array.isArray(evidence.recommended_actions)) {
    actionItems.value = evidence.recommended_actions
  }
  riskAreas.value = (evidence.risk_drivers || []).map((description, idx) => ({
    severity: idx === 0 ? 'high' : 'medium',
    description,
  }))
  winningStrategy.value = scoreExplanations.value[0] || winningStrategy.value
  winningHighlights.value = scoreExplanations.value.slice(0, 3)
  riskSummary.value = riskDrivers.value[0] || riskSummary.value
  executiveSummaryTH.value = scoreExplanations.value.join(' ') || executiveSummaryTH.value
  loadDecisionEngine()
}

async function loadDecisionEngine() {
  try {
    const res = await analyzeDecision({
      campaign: campaignDetails.value || {},
      kpis: kpis.value,
      segments: segments.value,
      evidence: {
        confidence_score: confidenceScore.value,
        risk_drivers: riskDrivers.value,
        why_this_score: scoreExplanations.value,
        assumptions: assumptions.value,
      },
    })
    applyDecision(res.data || res)
  } catch (e) {
    console.warn('Decision engine unavailable, using local fallback:', e.message)
    applyDecision(localDecisionFallback())
  }
}

function applyDecision(data) {
  decisionStrategy.value = data.recommended_strategy || {}
  businessImpact.value = data.business_impact || {}
  businessMapping.value = data.business_mapping || []
  primaryRisk.value = data.primary_risk || {}
  if (Array.isArray(data.actions) && data.actions.length) {
    actionItems.value = data.actions
  }
  if (data.action_plan) {
    structuredActionPlan.value = normalizeActionPlan(data.action_plan)
  }
  if (data.primary_risk?.driver && !riskDrivers.value.includes(data.primary_risk.driver)) {
    riskDrivers.value = [data.primary_risk.driver, ...riskDrivers.value].slice(0, 4)
  }
}

function normalizeActionPlan(plan) {
  const source = plan.source || resultSource.value || { type: 'unknown', warning: '' }
  const sections = plan.sections || {}
  return {
    version: plan.version || 'structured_action_plan_v1',
    source: {
      type: source.type || 'unknown',
      warning: source.warning || '',
    },
    headline: plan.headline || winningStrategy.value || t('dashboard.actionPlanDefaultHeadline'),
    disclaimer: plan.disclaimer || t('dashboard.actionPlanDisclaimer'),
    sections: {
      creative_adjustment: normalizeActionSection('creative_adjustment', sections.creative_adjustment),
      channel_allocation: normalizeActionSection('channel_allocation', sections.channel_allocation),
      crisis_prevention: normalizeActionSection('crisis_prevention', sections.crisis_prevention),
      validation_plan: normalizeActionSection('validation_plan', sections.validation_plan),
    },
    summary_items: Array.isArray(plan.summary_items) ? plan.summary_items : [],
  }
}

function normalizeActionSection(key, section) {
  const fallback = buildLocalActionSection(key)
  const items = Array.isArray(section?.items) && section.items.length ? section.items : fallback.items
  return {
    title: section?.title || t(`dashboard.actionSection_${key}`),
    items: items.map(normalizeActionItem),
  }
}

function normalizeActionItem(item) {
  return {
    recommendation: item.recommendation || item.action || item.description || t('dashboard.actionPlanMissingRecommendation'),
    reason: item.reason || item.rationale || t('dashboard.actionPlanMissingReason'),
    expected_impact: item.expected_impact || item.impact || t('dashboard.actionPlanMissingImpact'),
    risk: item.risk || t('dashboard.actionPlanMissingRisk'),
    priority: item.priority || 'medium',
  }
}

function buildLocalActionPlan() {
  return {
    version: 'structured_action_plan_v1',
    source: {
      type: resultSource.value?.type || 'unknown',
      warning: resultSource.value?.warning || '',
    },
    headline: decisionStrategy.value?.headline || winningStrategy.value || t('dashboard.actionPlanDefaultHeadline'),
    disclaimer: t('dashboard.actionPlanDisclaimer'),
    sections: {
      creative_adjustment: buildLocalActionSection('creative_adjustment'),
      channel_allocation: buildLocalActionSection('channel_allocation'),
      crisis_prevention: buildLocalActionSection('crisis_prevention'),
      validation_plan: buildLocalActionSection('validation_plan'),
    },
  }
}

function buildLocalActionSection(key) {
  const topPositive = topPositiveSegmentLabel()
  const topRisk = topNegativeSegmentLabel()
  const source = resultSource.value?.type || 'unknown'
  const mapping = {
    creative_adjustment: {
      title: t('dashboard.actionSection_creative_adjustment'),
      items: [{
        recommendation: kpis.value.message_resonance >= 70
          ? t('dashboard.actionCreativeKeep')
          : t('dashboard.actionCreativeRewrite'),
        reason: t('dashboard.actionCreativeReason', { resonance: kpis.value.message_resonance, segment: topPositive }),
        expected_impact: t('dashboard.actionCreativeImpact'),
        risk: t('dashboard.actionCreativeRisk'),
        priority: kpis.value.message_resonance >= 70 ? 'medium' : 'high',
      }],
    },
    channel_allocation: {
      title: t('dashboard.actionSection_channel_allocation'),
      items: [{
        recommendation: t('dashboard.actionChannelRecommendation', { channels: campaignBrief.value.channels }),
        reason: t('dashboard.actionChannelReason', { conversion: kpis.value.conversion_probability, influence: kpis.value.social_influence }),
        expected_impact: t('dashboard.actionChannelImpact'),
        risk: t('dashboard.actionChannelRisk'),
        priority: 'high',
      }],
    },
    crisis_prevention: {
      title: t('dashboard.actionSection_crisis_prevention'),
      items: [{
        recommendation: crisisLevel.value >= 3 ? t('dashboard.actionCrisisContain') : t('dashboard.actionCrisisPrepare'),
        reason: t('dashboard.actionCrisisReason', { risk: crisisLabel.value, driver: riskDrivers.value[0] || topRisk }),
        expected_impact: t('dashboard.actionCrisisImpact'),
        risk: t('dashboard.actionCrisisRisk'),
        priority: crisisLevel.value >= 3 ? 'critical' : 'medium',
      }],
    },
    validation_plan: {
      title: t('dashboard.actionSection_validation_plan'),
      items: [{
        recommendation: ['demo_mode', 'local_estimate', 'unknown'].includes(source)
          ? t('dashboard.actionValidationBackend')
          : t('dashboard.actionValidationLive'),
        reason: t('dashboard.actionValidationReason', { source, confidence: confidenceScore.value }),
        expected_impact: t('dashboard.actionValidationImpact'),
        risk: t('dashboard.actionValidationRisk'),
        priority: ['demo_mode', 'local_estimate', 'unknown'].includes(source) ? 'high' : 'medium',
      }],
    },
  }
  return mapping[key]
}

async function copyActionPlan() {
  const lines = actionPlanToLines(displayActionPlan.value)
  try {
    await navigator.clipboard.writeText(lines.join('\n'))
    actionPlanCopied.value = true
    setTimeout(() => { actionPlanCopied.value = false }, 1800)
  } catch (e) {
    console.warn('Copy action plan failed:', e.message)
  }
}

function actionPlanToLines(plan) {
  const lines = [
    `${t('dashboard.actionPlan')}: ${plan.headline}`,
    `${t('resultSource.unknownSource')}: ${plan.source.type}`,
    plan.disclaimer,
  ]
  for (const section of actionPlanSections.value) {
    lines.push('', section.title)
    section.items.forEach((item, idx) => {
      lines.push(`${idx + 1}. ${item.recommendation}`)
      lines.push(`   ${t('dashboard.actionReason')}: ${item.reason}`)
      lines.push(`   ${t('dashboard.actionExpectedImpact')}: ${item.expected_impact}`)
      lines.push(`   ${t('dashboard.actionRisk')}: ${item.risk}`)
    })
  }
  return lines
}

function localDecisionFallback() {
  const crisis = crisisLevel.value
  const verdict = crisis >= 3 ? 'revise_before_launch' : kpis.value.conversion_probability >= 65 ? 'launch_with_guardrails' : 'controlled_pilot'
  return {
    recommended_strategy: {
      verdict,
      headline: verdict === 'launch_with_guardrails' ? 'Launch with proof guardrails.' : 'Run a controlled pilot before scaling.',
      rationale: `Conversion ${kpis.value.conversion_probability}% with ${crisisLabel.value} crisis risk.`,
      next_best_action: riskDrivers.value[0] || 'Add proof points and retest one revised message.',
      confidence: confidenceScore.value,
    },
    business_impact: {
      estimated_revenue_impact: kpis.value.conversion_probability * 10000,
      estimated_crisis_loss: crisis * 500000,
      market_share_shift_pct: (kpis.value.brand_perception_shift || 8) * 0.08,
      roi_pct: kpis.value.conversion_probability - 40,
    },
    business_mapping: [],
    primary_risk: { recommended_action: riskDrivers.value[0] || '' },
  }
}

async function runScenario(scenario) {
  activeScenario.value = scenario.key
  whatIfLoading.value = true
  try {
    const res = await runWhatIf({
      kpis: kpis.value,
      scenario: scenario.scenario,
    })
    whatIfResult.value = res.data || res
  } catch (e) {
    console.warn('What-if API unavailable:', e.message)
    whatIfResult.value = null
  } finally {
    whatIfLoading.value = false
  }
}

function normalizeKpis(data) {
  const next = { ...data }
  if (next.social_influence == null && next.social_influence_index != null) {
    next.social_influence = next.social_influence_index
  }
  if (typeof next.crisis_risk === 'number') {
    next.crisis_risk = Math.round(next.crisis_risk)
  }
  return next
}

function normalizeResultSource(source) {
  const rawType = source?.type || source?.source_mode || 'unknown'
  const allowed = ['demo_mode', 'local_estimate', 'live_backend', 'backend_verified', 'unknown']
  const type = allowed.includes(rawType) ? rawType : 'unknown'
  const fallbackWarnings = {
    demo_mode: t('dashboard.sourceDemoMode'),
    local_estimate: t('dashboard.sourceLocalEstimate'),
    backend_verified: t('dashboard.sourceBackendVerified'),
    live_backend: t('dashboard.sourceLiveBackend'),
    unknown: t('dashboard.sourceUnknownPending'),
  }
  return {
    type,
    warning: source?.warning || fallbackWarnings[type],
    data_basis: source?.data_basis || 'unknown',
    run_id: source?.run_id,
    simulation_id: source?.simulation_id,
    campaign_id: source?.campaign_id,
    confidence: source?.confidence,
    limitations: Array.isArray(source?.limitations) ? source.limitations : [],
  }
}

function normalizeTimelinePoint(point) {
  return {
    round_num: point.round_num || point.round || 0,
    sentiment: point.sentiment ?? point.avg_sentiment ?? 0,
    posts_count: point.posts_count ?? point.action_count ?? 0,
    date: point.date,
  }
}

function normalizeSegment(segment) {
  return {
    name: segment.name || segment.segment_name || 'Segment',
    sentiment: segment.sentiment ?? segment.avg_sentiment ?? 0,
    conversion_estimate: segment.conversion_estimate ?? 0,
    size: segment.size || `${segment.persona_count || 0}`,
  }
}

function buildEvidenceFromCurrentState() {
  confidenceScore.value = Math.max(62, Math.min(88, Math.round((kpis.value.message_resonance || 65) * 0.55 + (segments.value.length ? 30 : 18))))
  assumptions.value = assumptions.value.length ? assumptions.value : [
    `${campaignBrief.value.personas} personas across ${campaignBrief.value.channels}`,
    `${campaignBrief.value.rounds} simulated rounds using ${campaignBrief.value.platformMode}`,
    'Scores are directional decision signals, not a replacement for live market measurement.',
  ]
  scoreExplanations.value = scoreExplanations.value.length ? scoreExplanations.value : [
    `Conversion is ${kpis.value.conversion_probability}% because the strongest segment response is ${topPositiveSegmentLabel()}.`,
    `Message resonance is ${kpis.value.message_resonance}% after discounting polarized or low-intent reactions.`,
    `Crisis level is ${crisisLabel.value} based on negative segment concentration and influencer amplification risk.`,
  ]
  riskDrivers.value = riskDrivers.value.length ? riskDrivers.value : [
    topNegativeSegmentLabel(),
    'High-reach voices can amplify uncertainty if proof points are missing.',
    'Price, trust, and claim substantiation remain the most sensitive message areas.',
  ]
  simulatedQuotes.value = simulatedQuotes.value.length ? simulatedQuotes.value : [
    'I like the idea, but I need a concrete reason to believe the claim.',
    'If the brand explains the trade-off clearly, I would consider trying it.',
    'The message feels stronger when it shows evidence rather than just emotion.',
  ]
}

function topPositiveSegmentLabel() {
  const best = [...segments.value].sort((a, b) => b.sentiment - a.sentiment)[0]
  return best ? `${best.name} (${formatSentiment(best.sentiment)})` : 'the strongest positive segment'
}

function topNegativeSegmentLabel() {
  const worst = [...segments.value].sort((a, b) => a.sentiment - b.sentiment)[0]
  return worst ? `${worst.name} remains a risk driver at ${formatSentiment(worst.sentiment)} sentiment.` : 'Negative reaction concentration is still unknown.'
}

// --- Seed demo data if backend returns nothing ---
function seedDemoData() {
  if (timeline.value.length === 0) {
    timeline.value = [
      { round_num: 1, sentiment: -12, posts_count: 24, date: '2026-04-20' },
      { round_num: 2, sentiment: 8, posts_count: 31, date: '2026-04-21' },
      { round_num: 3, sentiment: 21, posts_count: 28, date: '2026-04-22' },
      { round_num: 4, sentiment: 35, posts_count: 35, date: '2026-04-23' },
      { round_num: 5, sentiment: 42, posts_count: 40, date: '2026-04-24' },
    ]
    totalRounds.value = timeline.value.length
  }

  if (segments.value.length === 0) {
    segments.value = [
      { name: 'Early Adopters', sentiment: 55, conversion_estimate: 82, size: '12%' },
      { name: 'Skeptical Majority', sentiment: -18, conversion_estimate: 34, size: '38%' },
      { name: 'Influencers/KOL', sentiment: 70, conversion_estimate: 91, size: '8%' },
      { name: 'Passive Observers', sentiment: 10, conversion_estimate: 48, size: '25%' },
      { name: 'Hard Opposition', sentiment: -65, conversion_estimate: 5, size: '17%' },
    ]
  }

  if (influencers.value.length === 0) {
    influencers.value = [
      { name: 'Synthetic Tech Reviewer A', platform: 'X', impact_score: 92, sentiment: 68, reach: 245000 },
      { name: 'Synthetic Forum Voice B', platform: 'Reddit', impact_score: 85, sentiment: 45, reach: 180000 },
      { name: 'Synthetic Urban Creator C', platform: 'X', impact_score: 78, sentiment: 55, reach: 120000 },
      { name: 'Synthetic Family Page D', platform: 'Facebook', impact_score: 71, sentiment: 30, reach: 310000 },
    ]
  }

  if (!winningStrategy.value) {
    winningStrategy.value =
      'Message framing emphasizing economic benefits and national progress consistently outperformed fear-based narratives. Early Adopter segment showed strongest conversion trajectory when exposed to data-driven factual content.'
    winningHighlights.value = [
      'Data-driven posts got 2.3x more positive engagement than emotional appeals',
      'Early Adopters converted at 82% when shown ROI projections',
      'Influencer amplification multiplied reach by 4x per round',
    ]
    riskSummary.value =
      'Hard Opposition segment remains entrenched despite positive messaging. Crisis potential from misinformation spikes in Round 3 requires ongoing monitoring.'
    riskAreas.value = [
      { severity: 'high', description: 'Hard Opposition segment (17%) shows zero conversion — risk of coordinated backlash' },
      { severity: 'high', description: 'Round 3 sentiment dip correlated with misinformation spread about data privacy' },
      { severity: 'medium', description: 'Skeptical Majority conversion rate (34%) is below threshold — needs personalized approach' },
    ]
    actionItems.value = [
      { priority: 'critical', description: 'Deploy crisis response protocol for data privacy misinformation', timeline: 'Immediate (0-2 days)' },
      { priority: 'high', description: 'Launch influencer amplification campaign targeting Early Adopters', timeline: 'This week (2-5 days)' },
      { priority: 'high', description: 'Develop personalized messaging for Skeptical Majority segment', timeline: 'This week (3-7 days)' },
      { priority: 'medium', description: 'Schedule sentiment re-assessment for Passive Observers', timeline: 'Next week (7-10 days)' },
      { priority: 'low', description: 'Document winning message frameworks for future campaigns', timeline: 'Ongoing' },
    ]
    executiveSummaryTH.value =
      'จากการวิเคราะห์แคมเปญพบว่ากลุ่ม Early Adopters มีแนวโน้มการเปลี่ยนใจสูงสุดที่ 82% ในขณะที่กลุ่ม Hard Opposition ยังคงต่อต้านที่ -65 การใช้ข้อความที่เน้นข้อมูลเชิงเศรษฐกิจและความก้าวหน้าของประเทศให้ผลลัพธ์ดีกว่าการใช้ความกลัว ความเสี่ยงหลักคือการแพร่กระจายของข้อมูลเท็จเกี่ยวกับความเป็นส่วนตัวของข้อมูลซึ่งพบในรอบที่ 3 แผนปฏิบัติการแนะนำให้เร่งจัดการวิกฤตข้อมูลเท็จก่อนเป็นอันดับแรก ตามด้วยการขยายผลผ่าน Influencer และพัฒนาข้อความสำหรับกลุ่ม Skeptical Majority'
  }
}

function observeActionPlan() {
  if (!actionPlanSection.value || actionPlanViewedTracked || typeof IntersectionObserver === 'undefined') return
  actionPlanObserver = new IntersectionObserver((entries) => {
    if (entries.some(entry => entry.isIntersecting)) {
      actionPlanViewedTracked = true
      trackEvent('action_plan_viewed', {
        source_mode: sourceModeFromValue(displayActionPlan.value?.source?.type),
        section_count: actionPlanSections.value.length,
        has_structured_plan: Boolean(structuredActionPlan.value),
      })
      actionPlanObserver?.disconnect()
      actionPlanObserver = null
    }
  }, { threshold: 0.35 })
  actionPlanObserver.observe(actionPlanSection.value)
}

onMounted(async () => {
  await loadDashboard()
  seedDemoData()
  observeActionPlan()
})

onUnmounted(() => {
  if (actionPlanObserver) {
    actionPlanObserver.disconnect()
    actionPlanObserver = null
  }
})
</script>

<style scoped>
/* ====================== BASE ====================== */
.dashboard {
  min-height: 100vh;
  background: var(--bg-canvas);
  font-family: var(--font-sans);
  color: var(--text-secondary);
}

/* ====================== NAVBAR ====================== */
.navbar {
  height: 52px;
  background: var(--bg-panel);
  color: var(--text-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 var(--space-6);
  border-bottom: 1px solid var(--border-subtle);
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 600;
  letter-spacing: 0.04em;
  font-size: var(--text-sm);
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  gap: var(--space-4);
  align-items: center;
  min-width: 0;
  flex-wrap: nowrap;
}

.nav-link {
  flex: 0 0 auto;
  color: var(--text-tertiary);
  text-decoration: none;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 500;
  line-height: 1;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
  white-space: nowrap;
  transition: color var(--transition-fast);
}

.nav-link:hover {
  color: var(--accent);
}

.nav-link.active {
  color: var(--text-primary);
}

.nav-campaign {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--accent);
  background: var(--accent-subtle);
  padding: 3px 10px;
  border-radius: 3px;
}

/* ====================== HEADER ====================== */
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px 40px 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.campaign-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-inverse);
  margin: 0 0 6px 0;
}

.campaign-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: var(--text-tertiary);
  margin: 0;
}

.meta-sep {
  margin: 0 10px;
  color: var(--border-strong);
}

/* Grade Badge */
.grade-badge {
  width: 90px;
  height: 90px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid;
  gap: 2px;
}

.grade-badge.grade-good {
  border-color: var(--green);
  background: var(--green-soft);
}

.grade-badge.grade-ok {
  border-color: var(--yellow);
  background: var(--yellow-soft);
}

.grade-badge.grade-bad {
  border-color: var(--red);
  background: var(--red-soft);
}

.grade-letter {
font-size: var(--text-sm);
  font-weight: 600;
  margin: 0 0 var(--space-5) 0;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.grade-label {
  font-size: 0.6rem;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ====================== BODY ====================== */
.dash-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 40px 60px;
}

/* ====================== DECISION CONSOLE ====================== */
.decision-console {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  gap: var(--space-5);
  margin-bottom: 28px;
  border-color: color-mix(in srgb, var(--accent) 42%, var(--border-subtle));
}

.decision-main h2 {
  margin: 8px 0 10px;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.65rem, 3vw, 2.6rem);
  line-height: 1.02;
}

.decision-main p {
  max-width: 760px;
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--text-base);
  line-height: 1.6;
}

.decision-actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-top: var(--space-4);
}

.decision-verdict,
.decision-confidence,
.sandbox-status {
  display: inline-flex;
  min-height: 30px;
  align-items: center;
  padding: 0 10px;
  border-radius: 999px;
  font-family: var(--font-mono);
  font-size: 0.66rem;
  font-weight: 900;
  text-transform: uppercase;
}

.decision-verdict {
  color: var(--accent);
  background: var(--accent-subtle);
}

.verdict-launch_with_guardrails {
  color: var(--green);
  background: var(--green-soft);
}

.verdict-revise_before_launch {
  color: var(--red);
  background: var(--red-soft);
}

.verdict-optimize_message,
.verdict-controlled_pilot {
  color: var(--yellow);
  background: var(--yellow-soft);
}

.decision-confidence,
.sandbox-status {
  color: var(--text-tertiary);
  background: var(--bg-elevated);
}

.decision-side {
  display: grid;
  gap: var(--space-3);
}

.next-action-card,
.money-grid div {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
}

.next-action-card {
  padding: var(--space-4);
}

.next-action-card span,
.money-grid span,
.what-if-result span {
  display: block;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.64rem;
  font-weight: 900;
  text-transform: uppercase;
}

.next-action-card strong {
  display: block;
  margin-top: 8px;
  color: var(--text-primary);
  font-size: var(--text-base);
  line-height: 1.35;
}

.money-grid,
.what-if-result {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-2);
}

.money-grid div,
.what-if-result div {
  min-width: 0;
  padding: var(--space-3);
}

.money-grid strong,
.what-if-result strong {
  display: block;
  margin-top: 8px;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  line-height: 1;
}

.what-if-console {
  margin-bottom: 28px;
}

.what-if-header,
.evidence-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
}

.what-if-header {
  margin-bottom: var(--space-4);
}

.scenario-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-3);
}

.scenario-button {
  min-height: 96px;
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  background: var(--bg-panel);
  cursor: pointer;
  text-align: left;
  transition: border-color var(--transition-fast), background var(--transition-fast), transform var(--transition-fast);
}

.scenario-button:hover,
.scenario-button.active {
  border-color: var(--accent);
  background: var(--accent-subtle);
  transform: translateY(-1px);
}

.scenario-button strong,
.scenario-button span {
  display: block;
}

.scenario-button strong {
  color: var(--text-primary);
  font-size: var(--text-sm);
}

.scenario-button span {
  margin-top: 8px;
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  line-height: 1.45;
}

.what-if-result {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-subtle);
}

/* ====================== CAMPAIGN BRIEF ====================== */
.campaign-brief {
  margin-bottom: 28px;
}

.brief-main {
  display: grid;
  gap: 8px;
  margin-bottom: 20px;
}

.brief-kicker,
.brief-item span {
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0;
}

.brief-main h2 {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.35rem, 3vw, 2rem);
  line-height: 1.08;
}

.brief-main p {
  max-width: 860px;
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.65;
}

.brief-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
  gap: 1px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--border-subtle);
}

.brief-item {
  min-width: 0;
  padding: 14px;
  background: var(--bg-panel);
}

.brief-item span,
.brief-item strong {
  display: block;
}

.brief-item strong {
  margin-top: 6px;
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 800;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.confidence-evidence {
  margin-bottom: 28px;
}

.trust-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--border-subtle);
}

.trust-limitations {
  margin: var(--space-4) 0 0;
  padding-left: var(--space-5);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.7;
}

/* ====================== DECISION EVIDENCE ====================== */
.decision-evidence {
  margin: 28px 0;
}

.evidence-header { margin-bottom: var(--space-5); }

.confidence-pill {
  min-width: 128px;
  padding: 12px 14px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  text-align: right;
}

.confidence-pill span {
  display: block;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 800;
  text-transform: uppercase;
}

.confidence-pill strong {
  display: block;
  color: var(--green);
  font-family: var(--font-display);
  font-size: 1.7rem;
  line-height: 1;
  margin-top: 6px;
}

.evidence-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-3);
}

.evidence-block {
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
}

.evidence-block h3 {
  margin: 0 0 var(--space-3);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
}

.evidence-block ul {
  display: grid;
  gap: 10px;
  margin: 0;
  padding-left: 18px;
}

.evidence-block li,
.evidence-block blockquote {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.55;
}

.evidence-block blockquote {
  margin: 0 0 10px;
  padding-left: 12px;
  border-left: 2px solid var(--accent);
}

.business-map {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1px;
  overflow: hidden;
  margin-top: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--border-subtle);
}

.business-map-item {
  min-width: 0;
  padding: var(--space-3);
  background: var(--bg-panel);
}

.business-map-item span,
.business-map-item small {
  display: block;
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  line-height: 1.35;
}

.business-map-item span {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 900;
  text-transform: uppercase;
}

.business-map-item strong {
  display: block;
  margin: 8px 0 6px;
  color: var(--text-primary);
  font-size: var(--text-sm);
  line-height: 1.25;
}

/* ====================== KPI ROW ====================== */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.kpi-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 18px 16px;
  display: flex;
  gap: 14px;
  align-items: flex-start;
  transition: border-color 0.2s;
}

.kpi-card:hover {
  border-color: var(--border-strong);
}

.kpi-icon {
  font-size: 1.4rem;
  line-height: 1;
  flex-shrink: 0;
  margin-top: 2px;
}

.kpi-content {
  flex: 1;
  min-width: 0;
}

.kpi-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: block;
  margin-bottom: 6px;
}

.kpi-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-inverse);
  display: block;
}

.kpi-value.big {
  font-size: 1.8rem;
  margin-bottom: 6px;
}

/* KPI Bars */
.kpi-bar {
  height: 4px;
  background: var(--border-subtle);
  border-radius: 2px;
  margin-top: 6px;
  overflow: hidden;
}

.kpi-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.6s ease;
}

.kpi-bar-fill.conversion {
  background: linear-gradient(90deg, var(--accent), var(--yellow), var(--green));
}

.kpi-bar-fill.influence {
  background: linear-gradient(90deg, var(--accent), var(--accent-hover));
}

.kpi-bar-fill.resonance {
  background: linear-gradient(90deg, var(--blue), var(--accent));
}

/* Sentiment Gauge */
.sentiment-gauge {
  margin: 4px 0;
}

.gauge-track {
  height: 6px;
  background: var(--border-subtle);
  border-radius: 3px;
  display: flex;
  overflow: hidden;
}

.gauge-fill-negative {
  background: var(--red);
  height: 100%;
  transition: width 0.6s ease;
}

.gauge-fill-positive {
  background: var(--green);
  height: 100%;
  transition: width 0.6s ease;
}

.gauge-scale {
  display: flex;
  justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.55rem;
  color: var(--text-quaternary);
  margin-top: 2px;
}

.sentiment-positive { color: var(--green) !important; }
.sentiment-negative { color: var(--red) !important; }
.sentiment-neutral { color: var(--yellow) !important; }

/* Crisis Card States */
.crisis-card.crisis-low {
  border-left: 3px solid var(--green);
}

.crisis-card.crisis-medium {
  border-left: 3px solid var(--yellow);
}

.crisis-card.crisis-high {
  border-left: 3px solid var(--red);
}

.crisis-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.crisis-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.crisis-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
}

/* ====================== MID ROW (Chart + Table) ====================== */
.mid-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 28px;
}

.panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px 22px;
}

.panel-title {
  font-size: 0.9rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: var(--text-inverse);
  margin: 0 0 16px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.panel-note {
  margin: -8px 0 16px 0;
  max-width: 760px;
  color: var(--text-muted);
  font-size: 0.88rem;
  line-height: 1.55;
}

/* ====================== CHART ====================== */
.chart-container {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  height: 200px;
  position: relative;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 170px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-quaternary);
  padding-bottom: 22px;
  flex-shrink: 0;
}

.chart-bars {
  display: flex;
  gap: 24px;
  align-items: flex-end;
  height: 100%;
  flex: 1;
}

.chart-bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex: 1;
  height: 100%;
  justify-content: flex-end;
}

.bar-value-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-tertiary);
  margin-bottom: 2px;
}

.bar-wrapper {
  width: 100%;
  max-width: 40px;
  height: 150px;
  background: var(--border-subtle);
  border-radius: 3px 3px 0 0;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.bar-fill {
  width: 100%;
  border-radius: 3px 3px 0 0;
  transition: height 0.6s ease;
  min-height: 2px;
}

.bar-positive {
  background: linear-gradient(180deg, var(--green), var(--green));
}

.bar-negative {
  background: linear-gradient(180deg, var(--red), var(--red));
}

.bar-round-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-tertiary);
  margin-top: 4px;
}

/* ====================== SEGMENT TABLE ====================== */
.segment-table {
  width: 100%;
  border-collapse: collapse;
}

.segment-table th {
  text-align: left;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  padding-bottom: 10px;
  font-weight: 500;
  border-bottom: 1px solid var(--border-subtle);
}

.segment-table td {
  padding: 10px 0;
  font-size: 0.82rem;
  border-bottom: 1px solid var(--border-subtle);
}

.seg-name {
  font-weight: 500;
  color: var(--text-secondary);
}

.sentiment-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 3px;
  font-weight: 600;
}

.tag-positive {
  background: var(--green-soft);
  color: var(--green);
}

.tag-negative {
  background: var(--red-soft);
  color: var(--red);
}

.mini-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mini-bar {
  height: 6px;
  background: linear-gradient(90deg, var(--red), var(--yellow), var(--green));
  border-radius: 3px;
  min-width: 4px;
  transition: width 0.6s ease;
}

.mini-bar-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.seg-size {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-tertiary);
}

/* ====================== INFLUENCERS ====================== */
.influencer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.influencer-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  transition: border-color 0.2s;
}

.influencer-card:hover {
  border-color: var(--border-strong);
}

.inf-rank {
  position: absolute;
  top: 10px;
  right: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--accent);
  font-weight: 700;
}

.inf-avatar {
  width: 36px;
  height: 36px;
  background: var(--accent);
  color: var(--text-inverse);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}

.inf-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.inf-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-inverse);
}

.inf-platform {
  font-size: 0.65rem;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-tertiary);
}

.inf-metrics {
  display: flex;
  gap: 16px;
}

.inf-metric {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.inf-metric-label {
  font-size: 0.6rem;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

.inf-metric-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--border-default);
}

.inf-sentiment {
  margin-top: 2px;
}

/* ====================== ACTION PLAN ====================== */
.action-plan {
  margin-bottom: 28px;
}

.action-plan-head {
  display: flex;
  justify-content: space-between;
  gap: var(--space-5);
  align-items: flex-start;
  margin-bottom: 18px;
}

.action-plan-head p {
  max-width: 760px;
  margin: 6px 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.action-plan-tools {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.copy-action-plan {
  min-height: 36px;
  padding: 0 var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  background: var(--bg-surface);
  color: var(--text-secondary);
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
}

.copy-action-plan:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.action-box {
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px 22px;
}

.action-box.winning {
  background: var(--green-soft);
  border-left: 3px solid var(--green);
}

.action-box.risk {
  background: rgba(239, 68, 68, 0.03);
  border-left: 3px solid var(--red);
}

.action-box-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.action-icon {
  font-size: 1.1rem;
}

.action-box-header h3 {
  font-size: 0.9rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: var(--text-inverse);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-box-text {
  font-size: 0.82rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 10px 0;
}

.winning-highlights {
  list-style: none;
  padding: 0;
  margin: 0;
}

.winning-highlights li {
  font-size: 0.78rem;
  color: var(--green);
  padding: 3px 0;
  padding-left: 14px;
  position: relative;
}

.winning-highlights li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--green);
  font-weight: 700;
}

.risk-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.risk-list li {
  font-size: 0.78rem;
  color: var(--text-secondary);
  padding: 5px 0;
  display: flex;
  gap: 6px;
  align-items: baseline;
}

.risk-severity {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  font-weight: 700;
  flex-shrink: 0;
  min-width: 32px;
}

.structured-action-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.structured-action-section {
  padding: 18px;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  background: var(--bg-surface);
}

.structured-section-head {
  margin-bottom: 12px;
}

.structured-action-item strong {
  display: block;
  color: var(--text-primary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.structured-action-item dl {
  display: grid;
  gap: 10px;
  margin: 14px 0 0;
}

.structured-action-item dl div {
  display: grid;
  gap: 3px;
}

.structured-action-item dt {
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.structured-action-item dd {
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.55;
}

/* Action Items */
.action-items {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px 22px;
}

.action-items-title {
  font-size: 0.85rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: var(--text-inverse);
  margin: 0 0 14px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-item-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.action-item {
  display: flex;
  gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-subtle);
}

.action-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.action-item-num {
  width: 28px;
  height: 28px;
  background: var(--border-subtle);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent);
  flex-shrink: 0;
}

.action-item-body {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  flex: 1;
}

.action-item-priority {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  font-weight: 700;
  text-transform: uppercase;
  background: var(--bg-elevated);
  padding: 2px 8px;
  border-radius: 3px;
  flex-shrink: 0;
}

.action-item-desc {
  font-size: 0.82rem;
  color: var(--text-secondary);
  flex: 1;
  min-width: 200px;
}

.action-item-timeline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

/* ====================== SUMMARY ====================== */
.summary-panel {
  margin-bottom: 28px;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.summary-toggle {
  font-size: 0.7rem;
  color: var(--text-tertiary);
  transition: color 0.2s;
}

.summary-header:hover .summary-toggle {
  color: var(--accent);
}

.summary-content {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
}

.summary-thai {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.8;
  margin: 0;
  font-family: 'Noto Sans Thai', 'Space Grotesk', system-ui, sans-serif;
}

/* ====================== DATA INFO ====================== */
.data-info {
  text-align: center;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text-quaternary);
  display: flex;
  justify-content: center;
  gap: 8px;
}

/* ====================== PREMIUM RESTYLE ====================== */
.dashboard {
  background: var(--bg-canvas);
  color: var(--text-secondary);
}

.dashboard .navbar {
  min-height: 64px;
  background: rgba(var(--bg-canvas-rgb), 0.78);
  border-bottom-color: var(--border-subtle);
  padding: 0 clamp(18px, 4vw, 48px);
}

.dashboard .nav-brand {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  letter-spacing: 0;
  text-transform: none;
}

.dashboard .nav-link:hover,
.dashboard .nav-link.router-link-active {
  color: var(--text-primary);
}

.nav-campaign {
  color: var(--accent);
  background: var(--accent-subtle);
  border: 1px solid var(--border-accent);
  border-radius: var(--radius-pill);
}

.dash-header {
  max-width: 1280px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 52px) clamp(20px, 4vw, 44px) 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.campaign-name {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3.3rem);
  letter-spacing: 0;
}

.campaign-meta,
.grade-label,
.kpi-label,
.crisis-text,
.panel-title,
.segment-table th,
.inf-platform,
.inf-metric-label,
.action-box-header h3,
.action-items-title,
.action-item-priority,
.action-item-timeline,
.data-info {
  font-family: var(--font-mono);
  letter-spacing: 0;
}

.campaign-meta,
.grade-label,
.kpi-label,
.crisis-text,
.segment-table th,
.inf-platform,
.inf-metric-label,
.action-item-timeline,
.data-info,
.gauge-scale,
.chart-y-axis,
.bar-round-label {
  color: var(--text-tertiary);
}

.meta-sep {
  color: var(--border-strong);
}

.grade-badge {
  width: 96px;
  height: 96px;
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.grade-badge.grade-good {
  border-color: var(--green);
  background: var(--green-soft);
}

.grade-badge.grade-ok {
  border-color: var(--yellow);
  background: var(--yellow-soft);
}

.grade-badge.grade-bad {
  border-color: var(--red);
  background: var(--red-soft);
}

.grade-letter {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 700;
  line-height: 1;
  text-transform: none;
}

.dash-body {
  max-width: 1280px;
  padding: 28px clamp(20px, 4vw, 44px) 70px;
}

.kpi-row {
  gap: var(--space-4);
}

.kpi-card,
.panel,
.action-items {
  background: var(--bg-surface);
  border-color: var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.kpi-card {
  padding: var(--space-5);
  transition: transform var(--transition-fast), border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.kpi-card:hover,
.panel:hover,
.influencer-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-elevated);
}

.kpi-card:hover {
  transform: translateY(-2px);
}

.kpi-icon,
.action-icon {
  width: 34px;
  height: 34px;
  display: inline-grid;
  place-items: center;
  flex-shrink: 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--accent-subtle);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.64rem;
  font-weight: 800;
  letter-spacing: 0;
  line-height: 1;
}

.action-icon {
  width: 32px;
  height: 32px;
}

.kpi-value,
.kpi-value.big,
.panel-title,
.action-box-header h3,
.action-items-title,
.inf-name,
.inf-metric-val,
.seg-name {
  color: var(--text-primary);
}

.kpi-value.big {
  font-family: var(--font-display);
  font-size: 2rem;
  line-height: 1.1;
}

.kpi-bar,
.gauge-track,
.bar-wrapper {
  background: var(--bg-elevated);
}

.kpi-bar-fill.conversion,
.mini-bar {
  background: linear-gradient(90deg, var(--red), var(--yellow), var(--green));
}

.kpi-bar-fill.influence {
  background: linear-gradient(90deg, var(--teal), var(--blue));
}

.kpi-bar-fill.resonance {
  background: linear-gradient(90deg, var(--accent), var(--yellow));
}

.gauge-fill-negative,
.bar-negative {
  background: linear-gradient(180deg, var(--red), color-mix(in srgb, var(--red) 75%, var(--text-primary)));
}

.gauge-fill-positive,
.bar-positive {
  background: linear-gradient(180deg, var(--green), color-mix(in srgb, var(--green) 78%, var(--text-primary)));
}

.sentiment-positive { color: var(--green) !important; }
.sentiment-negative { color: var(--red) !important; }
.sentiment-neutral { color: var(--yellow) !important; }

.crisis-card.crisis-low { border-left-color: var(--green); }
.crisis-card.crisis-medium { border-left-color: var(--yellow); }
.crisis-card.crisis-high { border-left-color: var(--red); }

.mid-row {
  gap: var(--space-4);
}

.panel {
  padding: var(--space-6);
}

.panel-title {
  font-size: 0.78rem;
  font-weight: 700;
}

.segment-table th {
  border-bottom-color: var(--border-subtle);
}

.segment-table td {
  border-bottom-color: var(--border-subtle);
  color: var(--text-secondary);
}

.tag-positive {
  background: var(--green-soft);
  color: var(--green);
}

.tag-negative {
  background: var(--red-soft);
  color: var(--red);
}

.mini-bar-val,
.seg-size,
.bar-value-label {
  color: var(--text-tertiary);
}

.influencer-grid {
  gap: var(--space-4);
}

.influencer-card {
  background: var(--bg-panel);
  border-color: var(--border-subtle);
  border-radius: var(--radius-lg);
}

.inf-rank {
  color: var(--accent);
}

.inf-avatar {
  background: linear-gradient(145deg, var(--accent), var(--teal));
  color: var(--text-inverse);
}

.action-box {
  border-color: var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.action-box.winning {
  background: var(--green-soft);
  border-left-color: var(--green);
}

.action-box.risk {
  background: var(--red-soft);
  border-left-color: var(--red);
}

.action-box-text,
.risk-list li,
.action-item-desc,
.summary-thai {
  color: var(--text-secondary);
}

.winning-highlights li {
  color: var(--text-secondary);
}

.winning-highlights li::before {
  color: var(--green);
}

.action-item {
  border-bottom-color: var(--border-subtle);
}

.action-item-num {
  background: var(--accent-subtle);
  color: var(--accent);
}

.action-item-priority {
  background: var(--bg-elevated);
}

.summary-content {
  border-top-color: var(--border-subtle);
}

.summary-toggle {
  color: var(--text-tertiary);
}

.summary-header:hover .summary-toggle {
  color: var(--accent);
}

/* ====================== RESPONSIVE ====================== */
@media (max-width: 1100px) {
  .decision-console {
    grid-template-columns: 1fr;
  }
  .business-map {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .kpi-row {
    grid-template-columns: repeat(3, 1fr);
  }
  .influencer-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 16px;
  }
  .dash-header {
    flex-direction: column;
    gap: 16px;
    padding: 20px 16px;
  }
  .dash-body {
    padding: 16px;
  }
  .kpi-row {
    grid-template-columns: 1fr 1fr;
  }
  .scenario-row,
  .money-grid,
  .what-if-result {
    grid-template-columns: 1fr;
  }
  .brief-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .evidence-header {
    flex-direction: column;
  }
  .confidence-pill {
    width: 100%;
    text-align: left;
  }
  .evidence-grid {
    grid-template-columns: 1fr;
  }
  .mid-row {
    grid-template-columns: 1fr;
  }
  .action-plan-head {
    flex-direction: column;
  }
  .action-plan-tools {
    justify-content: flex-start;
  }
  .action-grid,
  .structured-action-grid {
    grid-template-columns: 1fr;
  }
  .influencer-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .kpi-row {
    grid-template-columns: 1fr;
  }
  .brief-grid {
    grid-template-columns: 1fr;
  }
  .business-map {
    grid-template-columns: 1fr;
  }
}
</style>
