<template>
  <div class="campaigns-page">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-brand">{{ $t('campaigns.brand') }}</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">{{ $t('nav.home') }}</router-link>
        <router-link to="/campaigns" class="nav-link active">{{ $t('campaigns.title') }}</router-link>
        <router-link to="/settings" class="nav-link">{{ $t('nav.settings') }}</router-link>
      </div>
    </nav>

    <!-- Header Section -->
    <header class="page-header">
      <div class="header-left">
        <h1 class="page-title">{{ $t('campaigns.title') }}</h1>
        <p class="page-subtitle">{{ $t('campaigns.campaignCount', campaigns.length) }}</p>
      </div>
      <div class="header-right">
        <router-link to="/war-room" class="btn-warroom-nav">
          {{ $t('warRoom.title') }}
        </router-link>
        <router-link to="/impact" class="btn-impact-nav">
          {{ $t('impact.title') }}
        </router-link>
        <router-link to="/comparator" class="btn-compare-nav">
          {{ $t('comparator.navLink') }}
        </router-link>
        <button class="btn-new-campaign" @click="openCreateModal">
          <span class="btn-icon">+</span>
          {{ $t('campaigns.newCampaign') }}
          </button>
        </div>
      </header>

    <!-- Campaign Grid -->
    <div class="campaigns-body">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>{{ $t('campaigns.loading') }}</span>
      </div>

      <!-- Empty State -->
      <div v-else-if="campaigns.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M6 4h12v16H6zM9 8h6M9 12h6M9 16h4" />
          </svg>
        </div>
        <h2>{{ $t('campaigns.emptyTitle') }}</h2>
        <p>{{ $t('campaigns.emptyDesc') }}</p>
        <button class="btn-new-campaign" @click="openCreateModal">
          <span class="btn-icon">+</span>
          {{ $t('campaigns.newCampaign') }}
        </button>
      </div>

      <!-- Campaign Cards Grid -->
      <div v-else class="campaign-grid">
        <div
          v-for="campaign in campaigns"
          :key="campaign.id"
          class="campaign-card"
          @click="openDashboard(campaign.id)"
        >
          <!-- Card Header -->
          <div class="card-header">
            <h3 class="card-name">{{ campaign.name }}</h3>
            <span :class="['status-pill', statusClass(campaign.status)]">
              <span class="status-dot"></span>
              {{ campaign.status || 'draft' }}
            </span>
          </div>

          <!-- Card Objective Badge -->
          <div class="card-badges">
            <span :class="['objective-badge', objectiveClass(campaign.objective)]">
              {{ formatObjective(campaign.objective) }}
            </span>
            <span class="platform-badge">
              {{ formatPlatform(campaignPlatform(campaign)) }}
            </span>
            <span class="platform-badge mode-badge">
              {{ formatPlatformMode(campaignPlatformMode(campaign)) }}
            </span>
          </div>
          <div v-if="campaignChannels(campaign).length" class="channel-strip">
            <span
              v-for="channel in campaignChannels(campaign).slice(0, 4)"
              :key="channel"
              class="channel-pill"
            >
              {{ formatChannel(channel) }}
            </span>
            <span v-if="campaignChannels(campaign).length > 4" class="channel-pill muted">
              +{{ campaignChannels(campaign).length - 4 }}
            </span>
          </div>

          <!-- Card Description -->
          <p v-if="campaign.description" class="card-desc">{{ truncate(campaign.description, 120) }}</p>

          <!-- Card Meta Footer -->
          <div class="card-footer">
            <div class="card-meta">
              <span class="meta-item">
                <span class="meta-icon">AG</span>
                {{ campaignPersonaCount(campaign) }} personas
              </span>
              <span class="meta-item">
                <span class="meta-icon">RD</span>
                {{ campaignMaxRounds(campaign) }} rounds
              </span>
            </div>
            <div class="card-date">{{ formatDate(campaign.created_at) }}</div>
          </div>

          <!-- Pipeline Progress (if active) -->
          <div v-if="campaign.pipeline && campaign.pipeline.status !== 'complete'" class="pipeline-bar-mini">
            <div class="pipeline-track">
              <div
                class="pipeline-fill"
                :style="{ width: pipelinePercent(campaign.pipeline) + '%' }"
              ></div>
            </div>
            <span class="pipeline-label">{{ campaign.pipeline.current_step || $t('campaigns.waiting') }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== NEW CAMPAIGN MODAL ==================== -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2 class="modal-title">
            {{ modalStep === 1 ? $t('campaigns.modalTitle') : $t('industry.chooseTemplate') }}
          </h2>
          <button class="modal-close" @click="closeModal">✕</button>
        </div>

        <!-- Step 0: Industry Template Selector -->
        <div v-if="modalStep === 0" class="modal-body">
          <div class="wizard-intro">
            <div>
              <span class="wizard-kicker">{{ $t('campaigns.guidedStartTitle') }}</span>
              <p>{{ $t('campaigns.guidedStartDesc') }}</p>
            </div>
            <button class="btn-quick-start" type="button" @click="applyRecommendedSetup">
              {{ $t('campaigns.useRecommendedSetup') }}
            </button>
          </div>

          <div class="wizard-summary">
            <div class="wizard-step active">
              <span>01</span>
              <strong>{{ $t('campaigns.wizardTemplate') }}</strong>
            </div>
            <div class="wizard-step">
              <span>02</span>
              <strong>{{ $t('campaigns.wizardConfigure') }}</strong>
            </div>
            <div class="wizard-step">
              <span>03</span>
              <strong>{{ $t('campaigns.wizardLaunch') }}</strong>
            </div>
          </div>

          <p v-if="skipAvailable" class="skip-link" @click="skipTemplate">
            {{ $t('industry.skipTemplate') }} →
          </p>
          <IndustryTemplateSelector
            @template-selected="onTemplateSelected"
            @cancel="closeModal"
          />
        </div>

        <!-- Step 1: Campaign Form -->
        <div v-if="modalStep === 1" class="modal-body">
          <!-- Template indicator (if template applied) -->
          <div v-if="appliedTemplate" class="template-applied-badge">
            <span class="template-badge-icon">{{ templateInitial(appliedTemplate) }}</span>
            <span>
              <strong>{{ $t('campaigns.selectedTemplate') }}</strong>
              {{ locale === 'th' ? appliedTemplate.name_th : appliedTemplate.name_en }}
            </span>
            <button class="template-remove-btn" @click="removeTemplate">✕</button>
          </div>

          <div class="wizard-summary">
            <div class="wizard-step done">
              <span>01</span>
              <strong>{{ $t('campaigns.wizardTemplate') }}</strong>
            </div>
            <div class="wizard-step active">
              <span>02</span>
              <strong>{{ $t('campaigns.wizardConfigure') }}</strong>
            </div>
            <div class="wizard-step">
              <span>03</span>
              <strong>{{ $t('campaigns.wizardLaunch') }}</strong>
            </div>
          </div>

          <!-- Campaign Name -->
          <div class="form-group">
            <label>{{ $t('campaigns.campaignName') }} <span class="required">{{ $t('campaigns.campaignNameRequired') }}</span></label>
            <input
              v-model="form.name"
              type="text"
              :placeholder="$t('campaigns.campaignNamePlaceholder')"
              class="form-input"
              :disabled="submitting"
            />
          </div>

          <!-- Description -->
          <div class="form-group">
            <label>{{ $t('campaigns.description') }}</label>
            <textarea
              v-model="form.description"
              :placeholder="$t('campaigns.descriptionPlaceholder')"
              rows="3"
              class="form-input"
              :disabled="submitting"
            ></textarea>
          </div>

          <!-- Objective -->
          <div class="form-group">
            <label>{{ $t('campaigns.objective') }} <span class="required">{{ $t('campaigns.objectiveRequired') }}</span></label>
            <select v-model="form.objective" class="form-input" :disabled="submitting">
              <option value="">{{ $t('campaigns.objectivePlaceholder') }}</option>
              <option value="message_testing">{{ $t('campaigns.objectiveMessageTesting') }}</option>
              <option value="crisis_simulation">{{ $t('campaigns.objectiveCrisisSimulation') }}</option>
              <option value="product_launch">{{ $t('campaigns.objectiveProductLaunch') }}</option>
              <option value="competitor_response">{{ $t('campaigns.objectiveCompetitorResponse') }}</option>
              <option value="brand_perception">{{ $t('campaigns.objectiveBrandPerception') }}</option>
            </select>
          </div>

          <!-- Target Audience Section -->
          <div class="form-section">
            <h3 class="section-label">{{ $t('campaigns.targetAudience') }}</h3>

            <div class="form-row">
              <!-- Segment Name -->
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.segmentName') }}</label>
                <input
                  v-model="form.audience.segment_name"
                  type="text"
                  :placeholder="$t('campaigns.segmentNamePlaceholder')"
                  class="form-input"
                  :disabled="submitting"
                />
              </div>

              <!-- Persona Count -->
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.personaCount') }}</label>
                <input
                  v-model.number="form.audience.persona_count"
                  type="number"
                  min="5"
                  max="500"
                  placeholder="50"
                  class="form-input"
                  :disabled="submitting"
                />
              </div>
            </div>

            <!-- Age Range Slider -->
            <div class="form-group">
              <label>{{ $t('campaigns.ageRange') }}: {{ form.audience.age_min }} – {{ form.audience.age_max }}</label>
              <div class="range-slider">
                <input
                  v-model.number="form.audience.age_min"
                  type="range"
                  min="13"
                  max="100"
                  class="range-input"
                  :disabled="submitting"
                />
                <input
                  v-model.number="form.audience.age_max"
                  type="range"
                  min="13"
                  max="100"
                  class="range-input"
                  :disabled="submitting"
                />
              </div>
              <div class="range-labels">
                <span>13</span>
                <span>30</span>
                <span>50</span>
                <span>70</span>
                <span>100</span>
              </div>
            </div>

            <!-- Gender -->
            <div class="form-group">
              <label>{{ $t('campaigns.gender') }}</label>
              <div class="chip-group">
                <button
                  v-for="g in genderOptions"
                  :key="g.value"
                  :class="['chip', { active: form.audience.gender === g.value }]"
                  @click="form.audience.gender = g.value"
                  :disabled="submitting"
                  type="button"
                >{{ $t(g.labelKey) }}</button>
              </div>
            </div>

            <!-- Regions (Multi-select) -->
            <div class="form-group">
              <label>{{ $t('campaigns.regions') }}</label>
              <div class="chip-group">
                <button
                  v-for="r in regionOptions"
                  :key="r.value"
                  :class="['chip', { active: form.audience.regions.includes(r.value) }]"
                  @click="toggleRegion(r.value)"
                  :disabled="submitting"
                  type="button"
                >{{ $t(r.labelKey) }}</button>
              </div>
            </div>

            <!-- Campaign Channels -->
            <div class="form-group">
              <label>{{ $t('campaigns.audienceChannels') }}</label>
              <p class="field-hint">{{ $t('campaigns.audienceChannelsHint') }}</p>
              <div class="chip-group channel-chip-group">
                <button
                  v-for="c in channelOptions"
                  :key="c.value"
                  :class="['chip', 'channel-chip', { active: form.audience.channels.includes(c.value) }]"
                  @click="toggleChannel(c.value)"
                  :disabled="submitting"
                  type="button"
                >
                  <span class="channel-code">{{ c.code }}</span>
                  {{ $t(c.labelKey) }}
                </button>
              </div>
            </div>
          </div>

          <!-- Behavior Model -->
          <div class="form-group">
            <label>{{ $t('campaigns.platformMode') }}</label>
            <p class="field-hint">{{ $t('campaigns.platformModeHint') }}</p>
            <div class="mode-grid">
              <button
                v-for="mode in platformModeOptions"
                :key="mode.value"
                :class="['mode-option', { active: form.platform_mode === mode.value }]"
                @click="form.platform_mode = mode.value"
                :disabled="submitting"
                type="button"
              >
                <span class="mode-code">{{ mode.code }}</span>
                <strong>{{ $t(mode.labelKey) }}</strong>
                <small>{{ $t(mode.descKey) }}</small>
              </button>
            </div>
          </div>

          <!-- Advanced Engine Settings -->
          <details class="advanced-settings">
            <summary>
              <span>{{ $t('campaigns.advancedSettings') }}</span>
              <strong>{{ formatPlatform(form.platform) }}</strong>
            </summary>
            <div class="advanced-body">
              <div class="form-group">
                <label>{{ $t('campaigns.simulationEngine') }} <span class="required">{{ $t('campaigns.platformRequired') }}</span></label>
                <p class="field-hint">{{ $t('campaigns.simulationEngineHint') }}</p>
                <div class="chip-group">
                  <button
                    v-for="p in platformOptions"
                    :key="p.value"
                    :class="['chip', { active: form.platform === p.value }]"
                    @click="form.platform = p.value"
                    :disabled="submitting"
                    type="button"
                  >{{ $t(p.labelKey) }}</button>
                </div>
              </div>
            </div>
          </details>

          <!-- Max Rounds -->
          <div class="form-group">
            <label>{{ $t('campaigns.maxRounds') }}</label>
            <input
              v-model.number="form.max_rounds"
              type="number"
              min="1"
              max="100"
              placeholder="10"
              class="form-input"
              :disabled="submitting"
            />
          </div>

          <div class="form-section trust-section">
            <h3 class="section-label">{{ $t('campaigns.briefQualityTitle') }}</h3>
            <p class="field-hint">{{ $t('campaigns.briefQualityDesc') }}</p>

            <div class="form-row">
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.campaignDuration') }}</label>
                <input v-model="form.campaign_duration" class="form-input" :placeholder="$t('campaigns.campaignDurationPlaceholder')" :disabled="submitting" />
              </div>
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.budgetRange') }}</label>
                <input v-model="form.budget_range" class="form-input" :placeholder="$t('campaigns.budgetRangePlaceholder')" :disabled="submitting" />
              </div>
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.primaryKpi') }}</label>
                <input v-model="form.primary_kpi" class="form-input" :placeholder="$t('campaigns.primaryKpiPlaceholder')" :disabled="submitting" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.competitorContext') }}</label>
                <textarea v-model="form.competitor_context" rows="2" class="form-input" :placeholder="$t('campaigns.competitorContextPlaceholder')" :disabled="submitting"></textarea>
              </div>
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.brandConstraints') }}</label>
                <textarea v-model="form.brand_constraints" rows="2" class="form-input" :placeholder="$t('campaigns.brandConstraintsPlaceholder')" :disabled="submitting"></textarea>
              </div>
              <div class="form-group flex-1">
                <label>{{ $t('campaigns.riskLegalNotes') }}</label>
                <textarea v-model="form.risk_legal_notes" rows="2" class="form-input" :placeholder="$t('campaigns.riskLegalNotesPlaceholder')" :disabled="submitting"></textarea>
              </div>
            </div>

            <div class="brief-quality-panel">
              <div class="brief-score" :class="briefQualityScoreClass">
                <span>{{ $t('campaigns.briefQualityScore') }}</span>
                <strong>{{ briefQuality ? briefQuality.score : '—' }}%</strong>
              </div>
              <div class="brief-quality-copy">
                <strong>{{ briefQualityLevelLabel }}</strong>
                <p>{{ briefQualityImpactLabel }}</p>
                <ul v-if="briefQuality?.missing_fields?.length" class="brief-missing-list">
                  <li v-for="field in briefQuality.missing_fields.slice(0, 4)" :key="field.key">
                    {{ field.label }}
                  </li>
                </ul>
              </div>
              <button class="btn-quality" type="button" @click="refreshBriefQuality" :disabled="briefQualityLoading || submitting">
                {{ briefQualityLoading ? $t('campaigns.checkingBriefQuality') : $t('campaigns.checkBriefQuality') }}
              </button>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal" :disabled="submitting">{{ $t('campaigns.cancel') }}</button>
          <button
            class="btn-submit"
            @click="submitCampaign"
            :disabled="!canSubmit || submitting"
          >
            <span v-if="submitting" class="spinner-small"></span>
            {{ submitting ? $t('campaigns.creating') : $t('campaigns.createAndStart') }}
          </button>
        </div>

        <!-- Error / Message -->
        <div v-if="modalError" class="modal-error">{{ modalError }}</div>
      </div>
    </div>

    <!-- ==================== PIPELINE PROGRESS MODAL ==================== -->
    <div v-if="showPipelineModal" class="modal-overlay" @click.self="closePipelineModal">
      <div class="modal-container pipeline-modal">
        <div class="modal-header">
          <h2 class="modal-title">{{ $t('campaigns.pipelineTitle') }}</h2>
          <button class="modal-close" @click="closePipelineModal">✕</button>
        </div>

        <div class="modal-body">
          <p class="pipeline-campaign-name">{{ activePipelineCampaign }}</p>

          <!-- Progress Bar -->
          <div class="pipeline-progress-bar">
            <div
              class="pipeline-progress-fill"
              :style="{ width: activePipelinePercent + '%' }"
            ></div>
          </div>
          <p class="pipeline-percent">{{ $t('campaigns.completePercent', { percent: activePipelinePercent }) }}</p>

          <!-- Steps -->
          <div class="pipeline-steps">
            <div
              v-for="(step, idx) in pipelineSteps"
              :key="idx"
              :class="['pipeline-step', stepStatus(step.key)]"
            >
              <div class="step-indicator">
                <span v-if="stepStatus(step.key) === 'done'" class="step-check">✓</span>
                <span v-else-if="stepStatus(step.key) === 'active'" class="step-spinner"></span>
                <span v-else class="step-circle">{{ idx + 1 }}</span>
              </div>
              <div class="step-content">
                <span class="step-name">{{ step.label }}</span>
                <span class="step-desc">{{ step.desc }}</span>
              </div>
            </div>
          </div>

          <!-- Action -->
          <div v-if="pipelineComplete" class="pipeline-complete">
            <p>{{ $t('campaigns.pipelineCompleteMsg') }}</p>
            <button class="btn-submit" @click="goToDashboard">{{ $t('campaigns.viewDashboard') }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import IndustryTemplateSelector from '@/components/IndustryTemplateSelector.vue'
import {
  createCampaign,
  hasCampaignAuth,
  listCampaigns,
  startPipeline,
  getPipelineStatus
} from '@/api/campaign'
import { listDemoCampaigns } from '@/api/demo'
import { scoreBriefQuality } from '@/api/brief'

const router = useRouter()
const { t } = useI18n()
const { locale } = useI18n()

// ── State ──────────────────────────────────────────
const campaigns = ref([])
const loading = ref(true)
const showModal = ref(false)
const showPipelineModal = ref(false)
const submitting = ref(false)
const modalError = ref('')
const modalStep = ref(0)  // 0: template picker, 1: form
const appliedTemplate = ref(null)
const skipAvailable = ref(true)  // Allows skipping template step
const activePipelineCampaign = ref('')
const activePipelineStatus = ref(null)
const activePipelineCampaignId = ref(null)
const briefQuality = ref(null)
const briefQualityLoading = ref(false)
let pipelinePollInterval = null

// ── Form State ─────────────────────────────────────
const form = ref({
  name: '',
  description: '',
  objective: '',
  campaign_duration: '',
  budget_range: '',
  primary_kpi: '',
  competitor_context: '',
  brand_constraints: '',
  risk_legal_notes: '',
  platform: 'both',
  platform_mode: 'auto',
  max_rounds: 10,
  audience: {
    segment_name: '',
    persona_count: 50,
    age_min: 18,
    age_max: 65,
    gender: 'all',
    regions: [],
    channels: ['facebook', 'instagram', 'tiktok']
  }
})

// ── Options ────────────────────────────────────────
const genderOptions = [
  { value: 'all', labelKey: 'campaigns.genderAll' },
  { value: 'male', labelKey: 'campaigns.genderMale' },
  { value: 'female', labelKey: 'campaigns.genderFemale' },
  { value: 'non_binary', labelKey: 'campaigns.genderNonBinary' }
]

const regionOptions = [
  { value: 'th', labelKey: 'regions.thailand' },
  { value: 'sea', labelKey: 'regions.southeastAsia' },
  { value: 'east_asia', labelKey: 'regions.eastAsia' },
  { value: 'south_asia', labelKey: 'regions.southAsia' },
  { value: 'mena', labelKey: 'regions.mena' },
  { value: 'eu', labelKey: 'regions.europe' },
  { value: 'na', labelKey: 'regions.northAmerica' },
  { value: 'latam', labelKey: 'regions.latinAmerica' },
  { value: 'africa', labelKey: 'regions.africa' },
  { value: 'global', labelKey: 'regions.global' }
]

const platformOptions = [
  { value: 'twitter', labelKey: 'campaigns.platformTwitter' },
  { value: 'reddit', labelKey: 'campaigns.platformReddit' },
  { value: 'both', labelKey: 'campaigns.platformBoth' }
]

const channelOptions = [
  { value: 'facebook', code: 'FB', labelKey: 'campaigns.channelFacebook' },
  { value: 'instagram', code: 'IG', labelKey: 'campaigns.channelInstagram' },
  { value: 'tiktok', code: 'TT', labelKey: 'campaigns.channelTikTok' },
  { value: 'youtube', code: 'YT', labelKey: 'campaigns.channelYouTube' },
  { value: 'line', code: 'LN', labelKey: 'campaigns.channelLine' },
  { value: 'twitter_x', code: 'X', labelKey: 'campaigns.channelTwitterX' },
  { value: 'reddit', code: 'RD', labelKey: 'campaigns.channelReddit' },
  { value: 'linkedin', code: 'IN', labelKey: 'campaigns.channelLinkedIn' }
]

const platformModeOptions = [
  { value: 'auto', code: 'AI', labelKey: 'campaigns.modeAuto', descKey: 'campaigns.modeAutoDesc' },
  { value: 'microblog', code: 'MB', labelKey: 'campaigns.modeMicroblog', descKey: 'campaigns.modeMicroblogDesc' },
  { value: 'community_forum', code: 'CF', labelKey: 'campaigns.modeCommunityForum', descKey: 'campaigns.modeCommunityForumDesc' },
  { value: 'group_chat', code: 'GC', labelKey: 'campaigns.modeGroupChat', descKey: 'campaigns.modeGroupChatDesc' },
  { value: 'creator_feed', code: 'CR', labelKey: 'campaigns.modeCreatorFeed', descKey: 'campaigns.modeCreatorFeedDesc' },
  { value: 'commerce_intent', code: 'CI', labelKey: 'campaigns.modeCommerceIntent', descKey: 'campaigns.modeCommerceIntentDesc' }
]

const pipelineSteps = computed(() => [
  { key: 'persona_generation', label: t('campaigns.personaGeneration'), desc: t('campaigns.personaGenerationDesc') },
  { key: 'graph_building', label: t('campaigns.graphBuilding'), desc: t('campaigns.graphBuildingDesc') },
  { key: 'simulation_running', label: t('campaigns.simulationRunning'), desc: t('campaigns.simulationRunningDesc') },
  { key: 'report_generation', label: t('campaigns.reportGeneration'), desc: t('campaigns.reportGenerationDesc') }
])

// ── Computed ───────────────────────────────────────
const canSubmit = computed(() => {
  return form.value.name.trim() !== '' && form.value.objective !== ''
})

const briefQualityScoreClass = computed(() => {
  const level = briefQuality.value?.level || 'unknown'
  return `brief-${level}`
})

const briefQualityLevelLabel = computed(() => {
  const level = briefQuality.value?.level
  const map = {
    strong: t('campaigns.briefQualityStrong'),
    usable: t('campaigns.briefQualityUsable'),
    thin: t('campaigns.briefQualityThin'),
    weak: t('campaigns.briefQualityWeak')
  }
  return map[level] || t('campaigns.briefQualityUnknown')
})

const briefQualityImpactLabel = computed(() => {
  const impact = briefQuality.value?.confidence_impact
  const map = {
    low_negative_impact: t('campaigns.confidenceImpactLow'),
    moderate_negative_impact: t('campaigns.confidenceImpactModerate'),
    high_negative_impact: t('campaigns.confidenceImpactHigh')
  }
  return map[impact] || t('campaigns.confidenceImpactUnknown')
})

const activePipelinePercent = computed(() => {
  if (!activePipelineStatus.value) return 0
  return pipelinePercent(activePipelineStatus.value)
})

const pipelineComplete = computed(() => {
  return activePipelineStatus.value && activePipelineStatus.value.status === 'complete'
})

// ── Methods: Formatting ────────────────────────────
function statusClass(status) {
  const map = {
    draft: 'status-draft',
    active: 'status-active',
    running: 'status-running',
    complete: 'status-complete',
    failed: 'status-failed',
    paused: 'status-paused'
  }
  return map[status] || 'status-draft'
}

function objectiveClass(obj) {
  const map = {
    message_testing: 'obj-message',
    crisis_simulation: 'obj-crisis',
    product_launch: 'obj-launch',
    competitor_response: 'obj-competitor',
    brand_perception: 'obj-brand'
  }
  return map[obj] || 'obj-default'
}

function formatObjective(obj) {
  const map = {
    message_testing: t('campaigns.objectiveMessageTesting'),
    crisis_simulation: t('campaigns.objectiveCrisisSimulation'),
    product_launch: t('campaigns.objectiveProductLaunch'),
    competitor_response: t('campaigns.objectiveCompetitorResponse'),
    brand_perception: t('campaigns.objectiveBrandPerception')
  }
  return map[obj] || obj || 'Unknown'
}

function formatPlatform(platform) {
  const map = {
    twitter: t('campaigns.platformTwitter'),
    reddit: t('campaigns.platformReddit'),
    both: t('campaigns.platformBoth')
  }
  return map[platform] || platform || t('campaigns.platformBoth')
}

function formatPlatformMode(mode) {
  const map = {
    auto: t('campaigns.modeAuto'),
    microblog: t('campaigns.modeMicroblog'),
    community_forum: t('campaigns.modeCommunityForum'),
    group_chat: t('campaigns.modeGroupChat'),
    creator_feed: t('campaigns.modeCreatorFeed'),
    commerce_intent: t('campaigns.modeCommerceIntent')
  }
  return map[mode] || mode || t('campaigns.modeAuto')
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
    shopee_live: 'Shopee Live'
  }
  return map[channel] || channel
}

function campaignChannels(campaign) {
  return normalizeChannels(
    campaign?.target?.channels ||
    campaign?.audience?.channels ||
    campaign?.channels ||
    campaign?.sim_config?.audience_channels ||
    []
  )
}

function campaignPlatform(campaign) {
  return campaign?.platform || campaign?.sim_config?.platform || 'both'
}

function campaignPlatformMode(campaign) {
  return campaign?.platform_mode || campaign?.sim_config?.platform_mode || campaign?.sim_config?.oasis_preset?.resolved_mode || 'auto'
}

function campaignPersonaCount(campaign) {
  return campaign?.persona_count || campaign?.target?.persona_count || campaign?.audience?.persona_count || 0
}

function campaignMaxRounds(campaign) {
  return campaign?.max_rounds || campaign?.sim_config?.max_rounds || 10
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return dateStr
  }
}

function truncate(text, max) {
  if (!text) return ''
  return text.length > max ? text.slice(0, max) + '...' : text
}

function pipelinePercent(pipeline) {
  if (!pipeline) return 0
  const stepWeights = {
    persona_generation: 25,
    graph_building: 50,
    simulation_running: 75,
    report_generation: 95,
    complete: 100
  }
  if (pipeline.status === 'complete') return 100
  const base = stepWeights[pipeline.current_step] || 0
  if (pipeline.current_step === 'complete') return 100
  const progressInStep = pipeline.step_progress || 0
  return Math.min(100, base + progressInStep * 0.25)
}

function stepStatus(stepKey) {
  if (!activePipelineStatus.value) return 'pending'
  const current = activePipelineStatus.value.current_step
  const stepOrder = ['persona_generation', 'graph_building', 'simulation_running', 'report_generation']
  const currentIdx = stepOrder.indexOf(current)
  const stepIdx = stepOrder.indexOf(stepKey)

  if (activePipelineStatus.value.status === 'complete') return 'done'
  if (stepIdx < currentIdx) return 'done'
  if (stepIdx === currentIdx) return 'active'
  return 'pending'
}

// ── Methods: Actions ───────────────────────────────
function openCreateModal() {
  modalError.value = ''
  modalStep.value = 0  // Start with template selector
  appliedTemplate.value = null
  briefQuality.value = null
  form.value = {
    name: '',
    description: '',
	    objective: '',
    campaign_duration: '',
    budget_range: '',
    primary_kpi: '',
    competitor_context: '',
    brand_constraints: '',
    risk_legal_notes: '',
	    platform: 'both',
	    platform_mode: 'auto',
	    max_rounds: 10,
    audience: {
      segment_name: '',
      persona_count: 50,
      age_min: 18,
      age_max: 65,
      gender: 'all',
      regions: [],
      channels: ['facebook', 'instagram', 'tiktok']
    }
  }
  showModal.value = true
}

function skipTemplate() {
  modalStep.value = 1  // Go directly to form
}

function applyRecommendedSetup() {
  form.value.name = t('campaigns.campaignNamePlaceholder')
  form.value.description = t('campaigns.quickStartDesc')
	  form.value.objective = 'message_testing'
  form.value.campaign_duration = ''
  form.value.budget_range = ''
  form.value.primary_kpi = ''
  form.value.competitor_context = ''
  form.value.brand_constraints = ''
  form.value.risk_legal_notes = ''
	  form.value.platform = 'both'
	  form.value.platform_mode = 'auto'
	  form.value.max_rounds = 10
  form.value.audience = {
    segment_name: t('campaigns.segmentNamePlaceholder'),
    persona_count: 80,
    age_min: 18,
    age_max: 55,
    gender: 'all',
    regions: ['th'],
    channels: ['facebook', 'instagram', 'tiktok', 'line']
  }
  modalStep.value = 1
}

function onTemplateSelected({ template, selectedSeeds }) {
  appliedTemplate.value = template
  modalStep.value = 1
  briefQuality.value = null

  // Pre-fill form from template
  const t = template
  form.value.objective = t.default_objective || 'crisis_simulation'
  form.value.platform = (t.sim_config && t.sim_config.platform) || t.default_platform || 'both'
  form.value.platform_mode = (t.sim_config && t.sim_config.platform_mode) || 'auto'
  form.value.max_rounds = (t.sim_config && t.sim_config.max_rounds) || t.default_max_rounds || 20
  form.value.campaign_duration = t.campaign_duration || ''
  form.value.budget_range = t.budget_range || ''
  form.value.primary_kpi = t.primary_kpi || ''
  form.value.competitor_context = t.competitor_context || ''
  form.value.brand_constraints = t.brand_constraints || ''
  form.value.risk_legal_notes = t.risk_legal_notes || ''
  const target = t.target || t.target_audience || {}
  if (target) {
    form.value.audience.age_min = (target.age_range && target.age_range[0]) || 18
    form.value.audience.age_max = (target.age_range && target.age_range[1]) || 65
    form.value.audience.persona_count = target.persona_count || 100
    form.value.audience.gender = target.gender || 'all'
    form.value.audience.regions = target.regions || []
    form.value.audience.channels = inferTemplateChannels(t)
  }
  if (t.name_th) {
    form.value.name = t.name_th + ' — ' + new Date().toLocaleDateString('th-TH')
  }

  // Store selected seeds for campaign creation
  form.value._template_id = t.template_id
  form.value._selected_seeds = selectedSeeds
}

function removeTemplate() {
  appliedTemplate.value = null
  form.value._template_id = null
  form.value._selected_seeds = []
  modalStep.value = 0  // Back to template selector
}

function templateInitial(template) {
  const name = locale.value === 'th' ? template?.name_th : template?.name_en
  return (name || template?.template_id || 'T').trim().charAt(0).toUpperCase()
}

function closeModal() {
  if (submitting.value) return
  showModal.value = false
  modalError.value = ''
}

function toggleRegion(region) {
  const regions = form.value.audience.regions
  const idx = regions.indexOf(region)
  if (idx >= 0) {
    regions.splice(idx, 1)
  } else {
    regions.push(region)
	  }
	}

function toggleChannel(channel) {
  const channels = form.value.audience.channels
  const idx = channels.indexOf(channel)
  if (idx >= 0) {
    channels.splice(idx, 1)
  } else {
    channels.push(channel)
  }
}

function normalizeChannels(channels) {
  const values = Array.isArray(channels) ? channels : []
  return [...new Set(values.map((channel) => {
    if (channel === 'twitter') return 'twitter_x'
    return String(channel || '').trim()
  }).filter(Boolean))]
}

function inferTemplateChannels(template) {
  const targetChannels = template?.target?.channels || template?.target_audience?.channels
  if (Array.isArray(targetChannels) && targetChannels.length) {
    return normalizeChannels(targetChannels).slice(0, 6)
  }

  const archetypeChannels = (template?.persona_segments || [])
    .flatMap((segment) => segment.archetypes || [])
    .flatMap((archetype) => archetype.channels || [])

  const counts = archetypeChannels.reduce((acc, channel) => {
    const normalized = channel === 'twitter' ? 'twitter_x' : channel
    acc[normalized] = (acc[normalized] || 0) + 1
    return acc
  }, {})

  const inferred = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .map(([channel]) => channel)
    .slice(0, 6)

  return inferred.length ? inferred : ['facebook', 'instagram', 'tiktok']
}

function openDashboard(campaignId) {
  router.push({ name: 'Dashboard', params: { campaignId } })
}

async function submitCampaign() {
  if (!canSubmit.value || submitting.value) return
  submitting.value = true
  modalError.value = ''

  try {
    await refreshBriefQuality()

    // 1. Create campaign
    const payload = buildCampaignPayload()
    payload.brief_quality = briefQuality.value

    const res = await createCampaign(payload)
    const campaignId = res.data?.id || res.id

    // 2. Start pipeline
    try {
      await startPipeline(campaignId)
    } catch (pipeErr) {
      console.warn('Pipeline start warning:', pipeErr.message)
    }

    // 3. Close modal, refresh list, and show pipeline progress
    showModal.value = false

    // Refresh campaign list
    await loadCampaigns()

    // Show pipeline progress for this campaign
    activePipelineCampaign.value = payload.name
    activePipelineCampaignId.value = campaignId
    activePipelineStatus.value = { current_step: 'persona_generation', status: 'running', step_progress: 0 }
    showPipelineModal.value = true
    startPipelinePolling(campaignId)
  } catch (err) {
    modalError.value = err.response?.data?.error || err.message || 'Failed to create campaign'
  } finally {
    submitting.value = false
  }
}

function buildCampaignPayload() {
  return {
    name: form.value.name.trim(),
    description: form.value.description.trim(),
    objective: form.value.objective,
    platform: form.value.platform,
    platform_mode: form.value.platform_mode,
    max_rounds: form.value.max_rounds,
    campaign_duration: form.value.campaign_duration,
    budget_range: form.value.budget_range,
    primary_kpi: form.value.primary_kpi,
    competitor_context: form.value.competitor_context,
    brand_constraints: form.value.brand_constraints,
    risk_legal_notes: form.value.risk_legal_notes,
    brief_metadata: {
      campaign_duration: form.value.campaign_duration,
      budget_range: form.value.budget_range,
      primary_kpi: form.value.primary_kpi,
      competitor_context: form.value.competitor_context,
      brand_constraints: form.value.brand_constraints,
      risk_legal_notes: form.value.risk_legal_notes
    },
    audience: { ...form.value.audience },
    target: {
      segment_name: form.value.audience.segment_name || 'General',
      age_range: [form.value.audience.age_min, form.value.audience.age_max],
      gender: form.value.audience.gender,
      regions: [...form.value.audience.regions],
      channels: [...form.value.audience.channels],
      persona_count: form.value.audience.persona_count
    },
    sim_config: {
      platform: form.value.platform,
      platform_mode: form.value.platform_mode,
      max_rounds: form.value.max_rounds,
      audience_channels: [...form.value.audience.channels]
    }
  }
}

async function refreshBriefQuality() {
  briefQualityLoading.value = true
  try {
    const res = await scoreBriefQuality(buildCampaignPayload())
    briefQuality.value = res.data || res
  } catch (err) {
    console.warn('Brief quality scoring failed:', err.message)
    briefQuality.value = {
      score: 0,
      level: 'unknown',
      confidence_impact: 'unknown',
      missing_fields: [],
      recommendations: [t('campaigns.briefQualityUnavailable')],
      known_limitations: [t('campaigns.briefQualityUnavailable')]
    }
  } finally {
    briefQualityLoading.value = false
  }
}

function closePipelineModal() {
  showPipelineModal.value = false
  stopPipelinePolling()
}

function goToDashboard() {
  closePipelineModal()
  if (activePipelineCampaignId.value) {
    router.push({ name: 'Dashboard', params: { campaignId: activePipelineCampaignId.value } })
  }
}

function startPipelinePolling(campaignId) {
  stopPipelinePolling()
  pipelinePollInterval = setInterval(async () => {
    try {
      const res = await getPipelineStatus(campaignId)
      if (res && res.data) {
        activePipelineStatus.value = res.data
      } else if (res) {
        activePipelineStatus.value = res
      }
    } catch (e) {
      console.warn('Pipeline status poll failed:', e.message)
    }
  }, 3000)
}

function stopPipelinePolling() {
  if (pipelinePollInterval) {
    clearInterval(pipelinePollInterval)
    pipelinePollInterval = null
  }
}

// ── Load Data ──────────────────────────────────────
async function loadCampaigns() {
  loading.value = true
  try {
    if (shouldUseDemoCampaigns()) {
      try {
        const demoRes = await listDemoCampaigns()
        campaigns.value = demoRes.data || demoRes || demoCampaigns()
      } catch (demoErr) {
        console.warn('Demo campaign API unavailable, using local fallback:', demoErr.message)
        campaigns.value = demoCampaigns()
      }
      return
    }

    const res = await listCampaigns()
    if (res && res.data) {
      campaigns.value = Array.isArray(res.data) ? res.data : (res.data.campaigns || [])
    } else if (Array.isArray(res)) {
      campaigns.value = res
    } else if (res && res.campaigns) {
      campaigns.value = res.campaigns
    }
  } catch (err) {
    console.warn('Failed to load campaigns:', err.message)
    campaigns.value = []
    // Seed some demo data for development
    if (import.meta.env.DEV) {
      campaigns.value = demoCampaigns()
    }
  } finally {
    loading.value = false
  }
}

function shouldUseDemoCampaigns() {
  return !hasCampaignAuth()
}

function demoCampaigns() {
  return [
    {
      id: 'demo-1',
      name: 'Bank Digital Wallet Launch',
      description: 'Market sentiment simulation for new digital wallet feature targeting Thai urban population.',
      objective: 'product_launch',
      status: 'complete',
	      platform: 'both',
	      platform_mode: 'creator_feed',
	      target: { channels: ['facebook', 'instagram', 'tiktok', 'twitter_x', 'reddit'] },
	      sim_config: { platform: 'both', platform_mode: 'creator_feed', audience_channels: ['facebook', 'instagram', 'tiktok', 'twitter_x', 'reddit'] },
	      persona_count: 120,
	      max_rounds: 8,
      created_at: '2026-04-20T10:00:00Z',
      pipeline: { status: 'complete', current_step: 'complete', step_progress: 1 }
    },
    {
      id: 'demo-2',
      name: 'Crisis Response: Data Breach',
      description: 'Simulate public reaction to a hypothetical data breach scenario and test response strategies.',
      objective: 'crisis_simulation',
      status: 'running',
	      platform: 'twitter',
	      platform_mode: 'microblog',
	      target: { channels: ['twitter_x', 'facebook', 'line'] },
	      sim_config: { platform: 'twitter', platform_mode: 'microblog', audience_channels: ['twitter_x', 'facebook', 'line'] },
	      persona_count: 85,
      max_rounds: 12,
      created_at: '2026-04-25T14:30:00Z',
      pipeline: { status: 'running', current_step: 'simulation_running', step_progress: 0.6 }
    },
    {
      id: 'demo-3',
      name: 'Competitor Messaging Analysis',
      description: 'Analyze how competitor product launch messaging resonates across different demographics.',
      objective: 'competitor_response',
      status: 'draft',
	      platform: 'reddit',
	      platform_mode: 'community_forum',
	      target: { channels: ['reddit', 'youtube', 'linkedin'] },
	      sim_config: { platform: 'reddit', platform_mode: 'community_forum', audience_channels: ['reddit', 'youtube', 'linkedin'] },
	      persona_count: 200,
      max_rounds: 15,
      created_at: '2026-04-28T08:15:00Z',
      pipeline: null
    }
  ]
}

onMounted(() => {
  loadCampaigns()
})

onUnmounted(() => {
  stopPipelinePolling()
})
</script>

<style scoped>
/* ====================== BASE ====================== */
.campaigns-page {
  min-height: 100vh;
  background: var(--bg-canvas);
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  color: var(--text-secondary);
}

/* ====================== NAVBAR ====================== */
.navbar {
  height: 60px;
  background: var(--text-primary);
  color: var(--text-inverse);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  border-bottom: 1px solid var(--border-subtle);
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
  min-width: 0;
  flex-wrap: nowrap;
}

.nav-link {
  flex: 0 0 auto;
  color: var(--text-tertiary);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  line-height: 1;
  white-space: nowrap;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: var(--accent);
}

/* ====================== HEADER ====================== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px 40px 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-inverse);
  margin: 0 0 6px 0;
}

.page-subtitle {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: var(--text-tertiary);
  margin: 0;
}

.btn-new-campaign {
  background: var(--accent);
  color: var(--text-inverse);
  border: none;
  padding: 12px 24px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s, transform 0.15s;
}

.btn-new-campaign:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
}

.btn-new-campaign:active {
  transform: translateY(0);
}

.btn-compare-nav, .btn-impact-nav, .btn-warroom-nav {
  padding: 10px 18px; border: 1px solid var(--border-default); border-radius: 6px;
  text-decoration: none; font-size: 0.85rem; color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace; margin-right: 10px;
  transition: all 0.15s;
}
.btn-compare-nav:hover, .btn-impact-nav:hover {
  border-color: var(--accent); color: var(--accent); background: var(--accent-subtle);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1;
}

/* ====================== BODY ====================== */
.campaigns-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 40px 60px;
}

/* ====================== LOADING / EMPTY ====================== */
.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  margin-bottom: 16px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  color: var(--accent);
  background: var(--accent-subtle);
}

.empty-icon svg {
  width: 28px;
  height: 28px;
}

.empty-icon path {
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.empty-state h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-state p {
  color: var(--text-tertiary);
  margin: 0 0 24px 0;
  font-size: 0.9rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ====================== CAMPAIGN GRID ====================== */
.campaign-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}

.campaign-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-5);
  cursor: pointer;
  transition: border-color var(--transition-fast), transform var(--transition-fast);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  box-shadow: var(--shadow-card);
}

.campaign-card:hover {
  border-color: var(--border-accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-elevated);
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.card-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
  min-width: 0;
  letter-spacing: -0.01em;
}

/* Status Pills */
.status-pill {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  padding: 2px 10px;
  border-radius: var(--radius-pill);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  white-space: nowrap;
  flex-shrink: 0;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}

.status-draft {
  background: var(--bg-elevated);
  color: var(--text-tertiary);
}
.status-draft .status-dot { background: var(--text-tertiary); }

.status-active {
  background: var(--green-soft);
  color: var(--green);
}
.status-active .status-dot { background: var(--green); }

.status-running {
  background: var(--blue-soft);
  color: var(--blue);
}
.status-running .status-dot { background: var(--blue); animation: pulse 1.5s infinite; }

.status-complete {
  background: var(--green-soft);
  color: var(--green);
}
.status-complete .status-dot { background: var(--green); }

.status-failed {
  background: var(--red-soft);
  color: var(--red);
}
.status-failed .status-dot { background: var(--red); }

.status-paused {
  background: var(--yellow-soft);
  color: var(--yellow);
}
.status-paused .status-dot { background: var(--yellow); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* Card Badges */
.card-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.objective-badge {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.obj-message { background: var(--blue-soft); color: var(--blue); }
.obj-crisis { background: var(--red-soft); color: var(--red); }
.obj-launch { background: var(--green-soft); color: var(--green); }
.obj-competitor { background: var(--yellow-soft); color: var(--yellow); }
.obj-brand { background: var(--accent-subtle); color: var(--accent); }
.obj-default { background: var(--bg-elevated); color: var(--text-tertiary); }

.platform-badge {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
}

.mode-badge {
  color: var(--accent);
  background: var(--accent-subtle);
}

.channel-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.channel-pill {
  display: inline-flex;
  align-items: center;
  min-height: 20px;
  padding: 2px 8px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
  color: var(--text-secondary);
  background: var(--bg-panel);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
}

.channel-pill.muted {
  color: var(--text-tertiary);
}

/* Card Description */
.card-desc {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  margin: 0;
  line-height: 1.5;
}

/* Card Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.card-meta {
  display: flex;
  gap: 16px;
}

.meta-item {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.meta-icon {
  display: inline-grid;
  place-items: center;
  width: 22px;
  height: 18px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.58rem;
  font-weight: 900;
}

.card-date {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-quaternary);
}

/* Mini Pipeline Bar on Card */
.pipeline-bar-mini {
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.pipeline-track {
  flex: 1;
  height: 3px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.pipeline-fill {
  height: 100%;
  background: var(--accent);
  border-radius: var(--radius-sm);
  transition: width var(--transition-slow);
}

.pipeline-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--accent);
  white-space: nowrap;
}

/* ====================== MODAL ====================== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(var(--bg-canvas-rgb), 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-modal);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--border-subtle);
}

.modal-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  font-family: var(--font-mono);
}

/* Template Applied Badge */
.template-applied-badge {
  display: inline-flex; align-items: center; gap: var(--space-3);
  padding: var(--space-2) var(--space-4); background: var(--accent-subtle);
  border: 1px solid var(--border-accent); border-radius: var(--radius-md);
  margin-bottom: var(--space-5); font-size: var(--text-sm); color: var(--accent);
}
.template-applied-badge strong {
  display: block;
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
}
.template-badge-icon {
  width: 30px;
  height: 30px;
  display: inline-grid;
  place-items: center;
  border: 1px solid var(--border-accent);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
}
.template-remove-btn {
  background: none; border: none; color: var(--text-tertiary);
  cursor: pointer; font-size: 1rem; margin-left: 8px;
}
.template-remove-btn:hover { color: var(--text-primary); }

.wizard-intro {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-5);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
}

.wizard-kicker {
  display: block;
  margin-bottom: var(--space-1);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.wizard-intro p {
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.55;
}

.btn-quick-start {
  min-height: 36px;
  padding: 0 var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  color: var(--text-primary);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 800;
  white-space: nowrap;
  transition: border-color var(--transition-fast), color var(--transition-fast), background var(--transition-fast);
}

.btn-quick-start:hover {
  border-color: var(--border-accent);
  color: var(--accent);
  background: var(--accent-subtle);
}

.wizard-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.wizard-step {
  min-width: 0;
  padding: var(--space-3);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  color: var(--text-tertiary);
}

.wizard-step span {
  display: block;
  margin-bottom: var(--space-1);
  font-family: var(--font-mono);
  font-size: 0.64rem;
  font-weight: 900;
}

.wizard-step strong {
  display: block;
  color: inherit;
  font-size: var(--text-xs);
  font-weight: 900;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wizard-step.active,
.wizard-step.done {
  border-color: var(--border-accent);
  background: var(--accent-subtle);
  color: var(--accent);
}

.modal-close {
  background: none;
  border: none;
  color: var(--text-tertiary);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.2s;
}

.modal-close:hover {
  color: var(--text-inverse);
}

.modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
}

.modal-error {
  margin: 0 24px 16px;
  padding: 10px 14px;
  background: var(--red-soft);
  border: 1px solid color-mix(in srgb, var(--red) 34%, transparent);
  color: var(--red);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  border-radius: 6px;
}

/* ====================== FORM ELEMENTS ====================== */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.field-hint {
  margin: -2px 0 4px;
  color: var(--text-quaternary);
  font-size: var(--text-xs);
  line-height: 1.45;
}

.required {
  color: var(--accent);
}

.form-input {
  padding: 10px 12px;
  background: var(--bg-canvas);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  outline: none;
  border-radius: 6px;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: var(--accent);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

textarea.form-input {
  resize: vertical;
  min-height: 60px;
}

select.form-input {
  cursor: pointer;
}

select.form-input option {
  background: var(--bg-surface);
  color: var(--text-secondary);
}

.form-section {
  border-top: 1px solid var(--border-subtle);
  padding-top: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.section-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
  font-weight: 600;
}

.form-row {
  display: flex;
  gap: 12px;
}

.flex-1 {
  flex: 1;
}

.trust-section {
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
}

.brief-quality-panel {
  display: grid;
  grid-template-columns: 140px 1fr auto;
  gap: var(--space-4);
  align-items: center;
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.brief-score {
  display: grid;
  gap: var(--space-1);
  text-align: center;
}

.brief-score span {
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  text-transform: uppercase;
}

.brief-score strong {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: 2rem;
  line-height: 1;
}

.brief-score.brief-strong strong { color: var(--green); }
.brief-score.brief-usable strong { color: var(--accent); }
.brief-score.brief-thin strong { color: var(--yellow); }
.brief-score.brief-weak strong { color: var(--red); }

.brief-quality-copy strong {
  color: var(--text-primary);
}

.brief-quality-copy p {
  margin: var(--space-1) 0 var(--space-2);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.brief-missing-list {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin: 0;
  padding: 0;
  list-style: none;
}

.brief-missing-list li {
  padding: 4px 8px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
  color: var(--text-tertiary);
  font-size: var(--text-xs);
}

.btn-quality {
  min-height: 40px;
  padding: 0 var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 800;
}

.btn-quality:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.btn-quality:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* Range Slider */
.range-slider {
  display: flex;
  gap: 8px;
  align-items: center;
}

.range-input {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  outline: none;
  cursor: pointer;
}

.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: var(--accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid var(--bg-surface);
}

.range-input::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: var(--accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid var(--bg-surface);
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-quaternary);
}

/* Chip Group */
.chip-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chip {
  padding: var(--space-1) var(--space-4);
  background: var(--bg-canvas);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.chip:hover {
  border-color: var(--border-strong);
  color: var(--text-secondary);
}

.chip.active {
  background: var(--accent-subtle);
  border-color: var(--accent);
  color: var(--accent);
}

.channel-chip-group {
  gap: 8px;
}

.channel-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.channel-code {
  display: inline-grid;
  place-items: center;
  min-width: 22px;
  height: 18px;
  border: 1px solid currentColor;
  border-radius: var(--radius-sm);
  font-size: 0.58rem;
  font-weight: 900;
  opacity: 0.75;
}

.mode-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.mode-option {
  min-width: 0;
  padding: var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-canvas);
  color: var(--text-secondary);
  text-align: left;
  cursor: pointer;
  transition: border-color var(--transition-fast), background var(--transition-fast), transform var(--transition-fast);
}

.mode-option:hover {
  border-color: var(--border-strong);
  transform: translateY(-1px);
}

.mode-option.active {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.mode-option:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.mode-code {
  display: inline-grid;
  place-items: center;
  width: 28px;
  height: 22px;
  margin-bottom: 8px;
  border: 1px solid currentColor;
  border-radius: var(--radius-sm);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 900;
}

.mode-option strong,
.mode-option small {
  display: block;
}

.mode-option strong {
  color: var(--text-primary);
  font-size: var(--text-sm);
  line-height: 1.25;
}

.mode-option small {
  margin-top: 4px;
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  line-height: 1.35;
}

.advanced-settings {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
}

.advanced-settings summary {
  min-height: 44px;
  padding: 0 var(--space-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  cursor: pointer;
  list-style: none;
}

.advanced-settings summary::-webkit-details-marker {
  display: none;
}

.advanced-settings summary::before {
  content: '+';
  width: 18px;
  height: 18px;
  display: inline-grid;
  place-items: center;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--accent);
}

.advanced-settings[open] summary::before {
  content: '-';
}

.advanced-settings summary span {
  flex: 1;
}

.advanced-settings summary strong {
  color: var(--text-primary);
  font-size: var(--text-xs);
}

.advanced-body {
  padding: 0 var(--space-4) var(--space-4);
}

.chip:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Buttons */
.btn-cancel {
  background: transparent;
  color: var(--text-tertiary);
  border: 1px solid var(--border-default);
  padding: var(--space-2) var(--space-6);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.btn-cancel:hover {
  border-color: var(--border-strong);
  color: var(--text-primary);
}

.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit {
  background: var(--accent);
  color: var(--text-inverse);
  border: none;
  padding: 10px 28px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.5px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.btn-submit:hover {
  background: var(--accent-hover);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid color-mix(in srgb, var(--text-inverse) 30%, transparent);
  border-top-color: var(--text-inverse);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  display: inline-block;
}

/* ====================== PIPELINE MODAL ====================== */
.pipeline-modal {
  max-width: 560px;
}

.pipeline-campaign-name {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0 0 20px 0;
}

.pipeline-progress-bar {
  height: 6px;
  background: var(--border-subtle);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.pipeline-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-hover));
  border-radius: 3px;
  transition: width 0.8s ease;
}

.pipeline-percent {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-tertiary);
  margin: 0 0 24px 0;
}

.pipeline-steps {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.pipeline-step {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 12px;
  border-left: 2px solid var(--border-subtle);
  margin-left: 11px;
  transition: border-color 0.3s;
}

.pipeline-step.done {
  border-left-color: var(--green);
}

.pipeline-step.active {
  border-left-color: var(--accent);
}

.pipeline-step.pending {
  border-left-color: var(--border-subtle);
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  margin-left: -25px;
}

.pipeline-step.done .step-indicator {
  background: var(--green-soft);
}

.pipeline-step.active .step-indicator {
  background: var(--accent-subtle);
}

.pipeline-step.pending .step-indicator {
  background: var(--bg-canvas);
  border: 1px solid var(--border-subtle);
}

.step-check {
  color: var(--green);
  font-weight: 700;
}

.step-spinner {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 69, 0, 0.3);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.step-circle {
  color: var(--text-tertiary);
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.step-name {
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.pipeline-step.done .step-name {
  color: var(--green);
}

.pipeline-step.active .step-name {
  color: var(--accent);
}

.pipeline-step.pending .step-name {
  color: var(--text-tertiary);
}

.step-desc {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
}

.pipeline-complete {
  margin-top: 20px;
  padding: 16px;
  background: var(--green-soft);
  border: 1px solid color-mix(in srgb, var(--green) 24%, transparent);
  border-radius: 8px;
  text-align: center;
}

.pipeline-complete p {
  color: var(--green);
  margin: 0 0 14px 0;
  font-size: 0.88rem;
}

/* ====================== PREMIUM RESTYLE ====================== */
.campaigns-page {
  background: var(--bg-canvas);
  color: var(--text-secondary);
  font-family: var(--font-sans);
}

.campaigns-page .navbar {
  min-height: 64px;
  background: rgba(var(--bg-canvas-rgb), 0.78);
  border-bottom-color: var(--border-subtle);
  padding: 0 clamp(18px, 4vw, 48px);
}

.campaigns-page .nav-brand {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  letter-spacing: 0;
}

.campaigns-page .nav-link:hover,
.campaigns-page .nav-link.active {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.page-header {
  max-width: 1280px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 52px) clamp(20px, 4vw, 44px) 28px;
  border-bottom-color: var(--border-subtle);
}

.page-title {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3.3rem);
  letter-spacing: 0;
}

.page-subtitle,
.card-date,
.meta-item,
.pipeline-label,
.modal-error,
.form-group label,
.range-labels,
.pipeline-percent,
.step-desc {
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  letter-spacing: 0;
}

.header-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.btn-new-campaign,
.btn-submit {
  background: var(--text-primary);
  color: var(--text-inverse);
  border: 1px solid var(--text-primary);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-weight: 800;
  letter-spacing: 0;
  box-shadow: var(--shadow-sm);
}

.btn-new-campaign:hover,
.btn-submit:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: var(--text-inverse);
}

.btn-compare-nav,
.btn-impact-nav,
.btn-warroom-nav {
  margin-right: 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-secondary);
  font-family: var(--font-sans);
  font-weight: 800;
  box-shadow: var(--shadow-sm);
}

.btn-compare-nav:hover,
.btn-impact-nav:hover,
.btn-warroom-nav:hover {
  border-color: var(--border-accent);
  color: var(--accent);
  background: var(--accent-soft);
}

.campaigns-body {
  max-width: 1280px;
  padding: 28px clamp(20px, 4vw, 44px) 70px;
}

.empty-state h2 {
  color: var(--text-primary);
  font-family: var(--font-display);
}

.empty-state p {
  color: var(--text-tertiary);
}

.spinner {
  border-color: var(--border-default);
  border-top-color: var(--accent);
}

.campaign-grid {
  gap: var(--space-4);
}

.campaign-card {
  background: var(--bg-surface);
  border-color: var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.campaign-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-elevated);
}

.card-name {
  color: var(--text-primary);
}

.status-draft,
.platform-badge {
  background: var(--bg-elevated);
  color: var(--text-tertiary);
}

.status-active,
.status-complete {
  background: var(--green-soft);
  color: var(--green);
}

.status-running {
  background: var(--blue-soft);
  color: var(--blue);
}

.status-failed {
  background: var(--red-soft);
  color: var(--red);
}

.status-paused {
  background: var(--yellow-soft);
  color: var(--yellow);
}

.status-draft .status-dot { background: var(--text-tertiary); }
.status-active .status-dot,
.status-complete .status-dot { background: var(--green); }
.status-running .status-dot { background: var(--blue); }
.status-failed .status-dot { background: var(--red); }
.status-paused .status-dot { background: var(--yellow); }

.obj-message { background: var(--blue-soft); color: var(--blue); }
.obj-crisis { background: var(--red-soft); color: var(--red); }
.obj-launch { background: var(--green-soft); color: var(--green); }
.obj-competitor { background: var(--yellow-soft); color: var(--yellow); }
.obj-brand,
.obj-default { background: var(--teal-soft); color: var(--teal); }

.pipeline-track,
.pipeline-progress-bar {
  background: var(--bg-elevated);
}

.pipeline-fill,
.pipeline-progress-fill {
  background: linear-gradient(90deg, var(--accent), var(--teal));
}

.modal-overlay {
  background: rgba(var(--bg-canvas-rgb), 0.42);
  backdrop-filter: blur(10px);
}

.modal-container {
  background: var(--bg-surface);
  border-color: var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-modal);
}

.modal-header,
.modal-footer {
  border-color: var(--border-subtle);
}

.modal-title {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
}

.modal-close {
  color: var(--text-tertiary);
  border-radius: var(--radius-md);
}

.modal-close:hover {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.template-remove-btn:hover {
  color: var(--text-primary);
}

.modal-error {
  background: var(--red-soft);
  border-color: color-mix(in srgb, var(--red) 30%, transparent);
  color: var(--red);
}

.form-input {
  background: var(--bg-panel);
  border-color: var(--border-default);
  color: var(--text-primary);
  font-family: var(--font-sans);
}

.form-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}

select.form-input option {
  background: var(--bg-surface);
  color: var(--text-primary);
}

.required {
  color: var(--accent);
}

.section-label {
  color: var(--text-tertiary);
  letter-spacing: 0;
}

.range-input::-webkit-slider-thumb {
  background: var(--accent);
  border-color: var(--bg-surface);
}

.range-input::-moz-range-thumb {
  background: var(--accent);
  border-color: var(--bg-surface);
}

.chip {
  background: var(--bg-panel);
}

.btn-cancel {
  background: var(--bg-surface);
  color: var(--text-secondary);
  font-family: var(--font-sans);
  font-weight: 800;
}

.pipeline-campaign-name,
.step-name {
  color: var(--text-primary);
}

.pipeline-step {
  border-left-color: var(--border-default);
}

.pipeline-step.done {
  border-left-color: var(--green);
}

.pipeline-step.active {
  border-left-color: var(--accent);
}

.pipeline-step.pending {
  border-left-color: var(--border-default);
}

.pipeline-step.done .step-indicator {
  background: var(--green-soft);
}

.pipeline-step.active .step-indicator {
  background: var(--accent-subtle);
}

.pipeline-step.pending .step-indicator {
  background: var(--bg-panel);
  border-color: var(--border-default);
}

.step-check,
.pipeline-step.done .step-name {
  color: var(--green);
}

.step-spinner {
  border-color: var(--accent-subtle);
  border-top-color: var(--accent);
}

.step-circle,
.pipeline-step.pending .step-name {
  color: var(--text-tertiary);
}

.pipeline-step.active .step-name {
  color: var(--accent);
}

.pipeline-complete {
  background: var(--green-soft);
  border-color: color-mix(in srgb, var(--green) 28%, transparent);
}

.pipeline-complete p {
  color: var(--green);
}

/* ====================== RESPONSIVE ====================== */
@media (max-width: 768px) {
  .navbar { padding: 0 16px; }
  .page-header { padding: 24px 16px 16px; flex-direction: column; gap: 16px; }
  .campaigns-body { padding: 20px 16px 40px; }
  .campaign-grid { grid-template-columns: 1fr; }
  .form-row { flex-direction: column; }
  .brief-quality-panel { grid-template-columns: 1fr; }
  .modal-container { max-width: 100%; margin: 0 8px; }
  .wizard-intro { flex-direction: column; align-items: stretch; }
	  .btn-quick-start { width: 100%; }
	  .wizard-summary { grid-template-columns: 1fr; }
	  .mode-grid { grid-template-columns: 1fr; }
	}
</style>
