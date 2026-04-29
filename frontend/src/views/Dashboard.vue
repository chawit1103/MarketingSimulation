<template>
  <div class="dashboard">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-brand">MIROFISH EXECUTIVE DASHBOARD</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">{{ $t('nav.home') }}</router-link>
        <router-link to="/settings" class="nav-link">{{ $t('nav.settings') }}</router-link>
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
          <span class="meta-rounds">{{ totalRounds }} Simulation Rounds</span>
        </p>
      </div>
      <div class="header-right">
        <div :class="['grade-badge', gradeClass]">
          <span class="grade-letter">{{ overallGrade }}</span>
          <span class="grade-label">Overall Score</span>
        </div>
      </div>
    </header>

    <div class="dash-body">
      <!-- KPI Cards Row -->
      <section class="kpi-row">
        <div class="kpi-card sentiment-card">
          <div class="kpi-icon">📊</div>
          <div class="kpi-content">
            <span class="kpi-label">Overall Sentiment</span>
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
          <div class="kpi-icon">🎯</div>
          <div class="kpi-content">
            <span class="kpi-label">Conversion Probability</span>
            <span class="kpi-value big">{{ kpis.conversion_probability }}%</span>
            <div class="kpi-bar">
              <div class="kpi-bar-fill conversion" :style="{ width: kpis.conversion_probability + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">🌐</div>
          <div class="kpi-content">
            <span class="kpi-label">Social Influence Index</span>
            <span class="kpi-value big">{{ kpis.social_influence }}/100</span>
            <div class="kpi-bar">
              <div class="kpi-bar-fill influence" :style="{ width: kpis.social_influence + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">💬</div>
          <div class="kpi-content">
            <span class="kpi-label">Message Resonance</span>
            <span class="kpi-value big">{{ kpis.message_resonance }}%</span>
            <div class="kpi-bar">
              <div class="kpi-bar-fill resonance" :style="{ width: kpis.message_resonance + '%' }"></div>
            </div>
          </div>
        </div>

        <div :class="['kpi-card', 'crisis-card', crisisClass]">
          <div class="kpi-icon">⚠️</div>
          <div class="kpi-content">
            <span class="kpi-label">Crisis Risk</span>
            <span class="kpi-value big">{{ crisisLabel }}</span>
            <div class="crisis-indicator">
              <span class="crisis-dot" :style="{ background: crisisColor }"></span>
              <span class="crisis-text">Level {{ crisisLevel }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Sentiment Timeline + Segment Breakdown -->
      <section class="mid-row">
        <!-- Sentiment Timeline Chart -->
        <div class="panel chart-panel">
          <h2 class="panel-title">Sentiment Timeline by Round</h2>
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
          <h2 class="panel-title">Persona Segment Breakdown</h2>
          <table class="segment-table">
            <thead>
              <tr>
                <th>Segment</th>
                <th>Sentiment</th>
                <th>Conv. Est.</th>
                <th>Size</th>
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

      <!-- Top Influencers -->
      <section class="panel">
        <h2 class="panel-title">Top Influencers &amp; Impact</h2>
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
                <span class="inf-metric-label">Impact</span>
                <span class="inf-metric-val">{{ inf.impact_score }}/100</span>
              </div>
              <div class="inf-metric">
                <span class="inf-metric-label">Reach</span>
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
      <section class="action-plan">
        <h2 class="panel-title">Action Plan — Think to Finish</h2>

        <div class="action-grid">
          <!-- Winning Strategy -->
          <div class="action-box winning">
            <div class="action-box-header">
              <span class="action-icon">🏆</span>
              <h3>Winning Strategy</h3>
            </div>
            <p class="action-box-text">{{ winningStrategy }}</p>
            <ul class="winning-highlights">
              <li v-for="(pt, idx) in winningHighlights" :key="idx">{{ pt }}</li>
            </ul>
          </div>

          <!-- Risk Areas -->
          <div class="action-box risk">
            <div class="action-box-header">
              <span class="action-icon">🚨</span>
              <h3>Risk Areas</h3>
            </div>
            <p class="action-box-text">{{ riskSummary }}</p>
            <ul class="risk-list">
              <li v-for="(r, idx) in riskAreas" :key="idx">
                <span class="risk-severity" :style="{ color: r.severity === 'high' ? '#ef4444' : '#f59e0b' }">
                  {{ r.severity === 'high' ? 'HIGH' : 'MED' }}
                </span>
                {{ r.description }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Action Items -->
        <div class="action-items">
          <h3 class="action-items-title">Priority Action Items</h3>
          <div class="action-item-list">
            <div v-for="(item, idx) in actionItems" :key="idx" class="action-item">
              <span class="action-item-num">{{ idx + 1 }}</span>
              <div class="action-item-body">
                <span class="action-item-priority" :style="{ color: priorityColor(item.priority) }">
                  {{ item.priority.toUpperCase() }}
                </span>
                <span class="action-item-desc">{{ item.description }}</span>
                <span class="action-item-timeline">{{ item.timeline }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Executive Summary -->
      <section class="panel summary-panel">
        <div class="summary-header" @click="showSummary = !showSummary">
          <h2 class="panel-title">Executive Summary ภาษาไทย</h2>
          <span class="summary-toggle">{{ showSummary ? '▲' : '▼' }}</span>
        </div>
        <div v-if="showSummary" class="summary-content">
          <p class="summary-thai">{{ executiveSummaryTH }}</p>
        </div>
      </section>

      <!-- Data Info -->
      <div class="data-info">
        <span>{{ $t('common.loading') }}...</span>
        <span v-if="loading">Fetching latest data...</span>
        <span v-else>Last updated: {{ lastUpdated }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getKPIs, getTimeline, getSegments, getInfluencers } from '@/api/dashboard'

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
const executiveSummaryTH = ref('')

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
  if (r === 'high') return 3
  if (r === 'medium') return 2
  return 1
})
const crisisLabel = computed(() => {
  const r = kpis.value.crisis_risk
  if (r === 'high') return 'HIGH'
  if (r === 'medium') return 'MEDIUM'
  return 'LOW'
})
const crisisColor = computed(() => {
  const r = kpis.value.crisis_risk
  if (r === 'high') return '#ef4444'
  if (r === 'medium') return '#f59e0b'
  return '#22c55e'
})
const crisisClass = computed(() => `crisis-${kpis.value.crisis_risk}`)

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

function barHeight(val) {
  const pct = Math.max(0, Math.min(100, ((val + 100) / 200) * 100))
  return pct + '%'
}

function priorityColor(p) {
  if (p === 'critical') return '#ef4444'
  if (p === 'high') return '#FF4500'
  if (p === 'medium') return '#f59e0b'
  return '#22c55e'
}

// --- Load data ---
async function loadDashboard() {
  loading.value = true
  try {
    const cid = campaignId.value

    // Fetch KPIs
    try {
      const kpiRes = await getKPIs(cid)
      if (kpiRes && kpiRes.data) {
        Object.assign(kpis.value, kpiRes.data)
      }
      if (kpiRes && kpiRes.campaign_name) campaignName.value = kpiRes.campaign_name
      if (kpiRes && kpiRes.grade) overallGrade.value = kpiRes.grade
    } catch (e) {
      console.warn('KPIs fetch failed, using defaults:', e.message)
    }

    // Fetch Timeline
    try {
      const tlRes = await getTimeline(cid)
      if (tlRes && tlRes.rounds) {
        timeline.value = tlRes.rounds
        totalRounds.value = tlRes.rounds.length
      }
    } catch (e) {
      console.warn('Timeline fetch failed:', e.message)
    }

    // Fetch Segments
    try {
      const segRes = await getSegments(cid)
      if (segRes && segRes.segments) {
        segments.value = segRes.segments
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
      { name: '@TechReviewTH', platform: 'Twitter', impact_score: 92, sentiment: 68, reach: 245000 },
      { name: 'SomsakD', platform: 'Reddit', impact_score: 85, sentiment: 45, reach: 180000 },
      { name: '@DigitalNomadBKK', platform: 'Twitter', impact_score: 78, sentiment: 55, reach: 120000 },
      { name: 'PraewMedia', platform: 'Facebook', impact_score: 71, sentiment: 30, reach: 310000 },
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

onMounted(async () => {
  await loadDashboard()
  seedDemoData()
})
</script>

<style scoped>
/* ====================== BASE ====================== */
.dashboard {
  min-height: 100vh;
  background: #0a0a0a;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  color: #e0e0e0;
}

/* ====================== NAVBAR ====================== */
.navbar {
  height: 60px;
  background: #000;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  border-bottom: 1px solid #1a1a1a;
}

.nav-brand {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1rem;
}

.nav-links {
  display: flex;
  gap: 24px;
  align-items: center;
}

.nav-link {
  color: #999;
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #FF4500;
}

.nav-campaign {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #FF4500;
  background: rgba(255, 69, 0, 0.12);
  padding: 3px 10px;
  border-radius: 3px;
}

/* ====================== HEADER ====================== */
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px 40px 24px;
  border-bottom: 1px solid #1a1a1a;
}

.campaign-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 6px 0;
}

.campaign-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: #666;
  margin: 0;
}

.meta-sep {
  margin: 0 10px;
  color: #333;
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
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.08);
}

.grade-badge.grade-ok {
  border-color: #f59e0b;
  background: rgba(245, 158, 11, 0.08);
}

.grade-badge.grade-bad {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.08);
}

.grade-letter {
  font-size: 2.4rem;
  font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  color: #fff;
  line-height: 1;
}

.grade-label {
  font-size: 0.6rem;
  font-family: 'JetBrains Mono', monospace;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ====================== BODY ====================== */
.dash-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 40px 60px;
}

/* ====================== KPI ROW ====================== */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.kpi-card {
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  padding: 18px 16px;
  display: flex;
  gap: 14px;
  align-items: flex-start;
  transition: border-color 0.2s;
}

.kpi-card:hover {
  border-color: #333;
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
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: block;
  margin-bottom: 6px;
}

.kpi-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  display: block;
}

.kpi-value.big {
  font-size: 1.8rem;
  margin-bottom: 6px;
}

/* KPI Bars */
.kpi-bar {
  height: 4px;
  background: #1a1a1a;
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
  background: linear-gradient(90deg, #FF4500, #f59e0b, #22c55e);
}

.kpi-bar-fill.influence {
  background: linear-gradient(90deg, #FF4500, #ff7f50);
}

.kpi-bar-fill.resonance {
  background: linear-gradient(90deg, #6366f1, #FF4500);
}

/* Sentiment Gauge */
.sentiment-gauge {
  margin: 4px 0;
}

.gauge-track {
  height: 6px;
  background: #1a1a1a;
  border-radius: 3px;
  display: flex;
  overflow: hidden;
}

.gauge-fill-negative {
  background: #ef4444;
  height: 100%;
  transition: width 0.6s ease;
}

.gauge-fill-positive {
  background: #22c55e;
  height: 100%;
  transition: width 0.6s ease;
}

.gauge-scale {
  display: flex;
  justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.55rem;
  color: #444;
  margin-top: 2px;
}

.sentiment-positive { color: #22c55e !important; }
.sentiment-negative { color: #ef4444 !important; }
.sentiment-neutral { color: #f59e0b !important; }

/* Crisis Card States */
.crisis-card.crisis-low {
  border-left: 3px solid #22c55e;
}

.crisis-card.crisis-medium {
  border-left: 3px solid #f59e0b;
}

.crisis-card.crisis-high {
  border-left: 3px solid #ef4444;
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
  color: #888;
}

/* ====================== MID ROW (Chart + Table) ====================== */
.mid-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 28px;
}

.panel {
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  padding: 20px 22px;
}

.panel-title {
  font-size: 0.9rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: #fff;
  margin: 0 0 16px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  color: #444;
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
  color: #888;
  margin-bottom: 2px;
}

.bar-wrapper {
  width: 100%;
  max-width: 40px;
  height: 150px;
  background: #1a1a1a;
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
  background: linear-gradient(180deg, #22c55e, #16a34a);
}

.bar-negative {
  background: linear-gradient(180deg, #ef4444, #dc2626);
}

.bar-round-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: #555;
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
  color: #555;
  text-transform: uppercase;
  padding-bottom: 10px;
  font-weight: 500;
  border-bottom: 1px solid #1a1a1a;
}

.segment-table td {
  padding: 10px 0;
  font-size: 0.82rem;
  border-bottom: 1px solid #0f0f0f;
}

.seg-name {
  font-weight: 500;
  color: #ccc;
}

.sentiment-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 3px;
  font-weight: 600;
}

.tag-positive {
  background: rgba(34, 197, 94, 0.12);
  color: #22c55e;
}

.tag-negative {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
}

.mini-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mini-bar {
  height: 6px;
  background: linear-gradient(90deg, #ef4444, #f59e0b, #22c55e);
  border-radius: 3px;
  min-width: 4px;
  transition: width 0.6s ease;
}

.mini-bar-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #aaa;
  flex-shrink: 0;
}

.seg-size {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #888;
}

/* ====================== INFLUENCERS ====================== */
.influencer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.influencer-card {
  background: #0d0d0d;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  transition: border-color 0.2s;
}

.influencer-card:hover {
  border-color: #333;
}

.inf-rank {
  position: absolute;
  top: 10px;
  right: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #FF4500;
  font-weight: 700;
}

.inf-avatar {
  width: 36px;
  height: 36px;
  background: #FF4500;
  color: #fff;
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
  color: #fff;
}

.inf-platform {
  font-size: 0.65rem;
  font-family: 'JetBrains Mono', monospace;
  color: #666;
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
  color: #555;
  text-transform: uppercase;
}

.inf-metric-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  font-weight: 700;
  color: #ddd;
}

.inf-sentiment {
  margin-top: 2px;
}

/* ====================== ACTION PLAN ====================== */
.action-plan {
  margin-bottom: 28px;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.action-box {
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  padding: 20px 22px;
}

.action-box.winning {
  background: rgba(34, 197, 94, 0.03);
  border-left: 3px solid #22c55e;
}

.action-box.risk {
  background: rgba(239, 68, 68, 0.03);
  border-left: 3px solid #ef4444;
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
  color: #fff;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-box-text {
  font-size: 0.82rem;
  color: #aaa;
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
  color: #86efac;
  padding: 3px 0;
  padding-left: 14px;
  position: relative;
}

.winning-highlights li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #22c55e;
  font-weight: 700;
}

.risk-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.risk-list li {
  font-size: 0.78rem;
  color: #aaa;
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

/* Action Items */
.action-items {
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  padding: 20px 22px;
}

.action-items-title {
  font-size: 0.85rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #fff;
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
  border-bottom: 1px solid #0f0f0f;
}

.action-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.action-item-num {
  width: 28px;
  height: 28px;
  background: #1a1a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: #FF4500;
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
  background: rgba(255, 255, 255, 0.04);
  padding: 2px 8px;
  border-radius: 3px;
  flex-shrink: 0;
}

.action-item-desc {
  font-size: 0.82rem;
  color: #ccc;
  flex: 1;
  min-width: 200px;
}

.action-item-timeline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: #555;
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
  color: #666;
  transition: color 0.2s;
}

.summary-header:hover .summary-toggle {
  color: #FF4500;
}

.summary-content {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #1a1a1a;
}

.summary-thai {
  font-size: 0.9rem;
  color: #bbb;
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
  color: #444;
  display: flex;
  justify-content: center;
  gap: 8px;
}

/* ====================== RESPONSIVE ====================== */
@media (max-width: 1100px) {
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
  .mid-row {
    grid-template-columns: 1fr;
  }
  .action-grid {
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
}
</style>
