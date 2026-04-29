<template>
  <div class="campaigns-page">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-brand">MIROFISH CAMPAIGNS</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">{{ $t('nav.home') }}</router-link>
        <router-link to="/campaigns" class="nav-link active">Campaigns</router-link>
        <router-link to="/settings" class="nav-link">{{ $t('nav.settings') }}</router-link>
      </div>
    </nav>

    <!-- Header Section -->
    <header class="page-header">
      <div class="header-left">
        <h1 class="page-title">Campaigns</h1>
        <p class="page-subtitle">{{ campaigns.length }} campaign{{ campaigns.length !== 1 ? 's' : '' }} configured</p>
      </div>
      <div class="header-right">
        <button class="btn-new-campaign" @click="openCreateModal">
          <span class="btn-icon">+</span>
          New Campaign
        </button>
      </div>
    </header>

    <!-- Campaign Grid -->
    <div class="campaigns-body">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>Loading campaigns...</span>
      </div>

      <!-- Empty State -->
      <div v-else-if="campaigns.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h2>No Campaigns Yet</h2>
        <p>Create your first campaign to start simulating public opinion.</p>
        <button class="btn-new-campaign" @click="openCreateModal">
          <span class="btn-icon">+</span>
          New Campaign
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
              {{ formatPlatform(campaign.platform) }}
            </span>
          </div>

          <!-- Card Description -->
          <p v-if="campaign.description" class="card-desc">{{ truncate(campaign.description, 120) }}</p>

          <!-- Card Meta Footer -->
          <div class="card-footer">
            <div class="card-meta">
              <span class="meta-item">
                <span class="meta-icon">👤</span>
                {{ campaign.persona_count || 0 }} personas
              </span>
              <span class="meta-item">
                <span class="meta-icon">🔄</span>
                {{ campaign.max_rounds || 10 }} rounds
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
            <span class="pipeline-label">{{ campaign.pipeline.current_step || 'Waiting' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== NEW CAMPAIGN MODAL ==================== -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2 class="modal-title">New Campaign</h2>
          <button class="modal-close" @click="closeModal">✕</button>
        </div>

        <div class="modal-body">
          <!-- Campaign Name -->
          <div class="form-group">
            <label>Campaign Name <span class="required">*</span></label>
            <input
              v-model="form.name"
              type="text"
              placeholder="e.g. Product Launch Q2 2026"
              class="form-input"
              :disabled="submitting"
            />
          </div>

          <!-- Description -->
          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="form.description"
              placeholder="Brief description of the campaign objectives..."
              rows="3"
              class="form-input"
              :disabled="submitting"
            ></textarea>
          </div>

          <!-- Objective -->
          <div class="form-group">
            <label>Objective <span class="required">*</span></label>
            <select v-model="form.objective" class="form-input" :disabled="submitting">
              <option value="">— Select Objective —</option>
              <option value="message_testing">Message Testing</option>
              <option value="crisis_simulation">Crisis Simulation</option>
              <option value="product_launch">Product Launch</option>
              <option value="competitor_response">Competitor Response</option>
              <option value="brand_perception">Brand Perception</option>
            </select>
          </div>

          <!-- Target Audience Section -->
          <div class="form-section">
            <h3 class="section-label">Target Audience</h3>

            <div class="form-row">
              <!-- Segment Name -->
              <div class="form-group flex-1">
                <label>Segment Name</label>
                <input
                  v-model="form.audience.segment_name"
                  type="text"
                  placeholder="e.g. Thai Urban Millennials"
                  class="form-input"
                  :disabled="submitting"
                />
              </div>

              <!-- Persona Count -->
              <div class="form-group flex-1">
                <label>Persona Count</label>
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
              <label>Age Range: {{ form.audience.age_min }} – {{ form.audience.age_max }}</label>
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
              <label>Gender</label>
              <div class="chip-group">
                <button
                  v-for="g in genderOptions"
                  :key="g.value"
                  :class="['chip', { active: form.audience.gender === g.value }]"
                  @click="form.audience.gender = g.value"
                  :disabled="submitting"
                  type="button"
                >{{ g.label }}</button>
              </div>
            </div>

            <!-- Regions (Multi-select) -->
            <div class="form-group">
              <label>Regions</label>
              <div class="chip-group">
                <button
                  v-for="r in regionOptions"
                  :key="r.value"
                  :class="['chip', { active: form.audience.regions.includes(r.value) }]"
                  @click="toggleRegion(r.value)"
                  :disabled="submitting"
                  type="button"
                >{{ r.label }}</button>
              </div>
            </div>
          </div>

          <!-- Platform -->
          <div class="form-group">
            <label>Platform <span class="required">*</span></label>
            <div class="chip-group">
              <button
                v-for="p in platformOptions"
                :key="p.value"
                :class="['chip', { active: form.platform === p.value }]"
                @click="form.platform = p.value"
                :disabled="submitting"
                type="button"
              >{{ p.label }}</button>
            </div>
          </div>

          <!-- Max Rounds -->
          <div class="form-group">
            <label>Max Rounds</label>
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
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal" :disabled="submitting">Cancel</button>
          <button
            class="btn-submit"
            @click="submitCampaign"
            :disabled="!canSubmit || submitting"
          >
            <span v-if="submitting" class="spinner-small"></span>
            {{ submitting ? 'Creating...' : 'Create & Start Pipeline' }}
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
          <h2 class="modal-title">Pipeline Progress</h2>
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
          <p class="pipeline-percent">{{ activePipelinePercent }}% Complete</p>

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
            <p>✅ Pipeline complete! Your simulation results are ready.</p>
            <button class="btn-submit" @click="goToDashboard">View Dashboard</button>
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
import {
  createCampaign,
  listCampaigns,
  startPipeline,
  getPipelineStatus
} from '@/api/campaign'

const router = useRouter()
const { t } = useI18n()

// ── State ──────────────────────────────────────────
const campaigns = ref([])
const loading = ref(true)
const showModal = ref(false)
const showPipelineModal = ref(false)
const submitting = ref(false)
const modalError = ref('')
const activePipelineCampaign = ref('')
const activePipelineStatus = ref(null)
const activePipelineCampaignId = ref(null)
let pipelinePollInterval = null

// ── Form State ─────────────────────────────────────
const form = ref({
  name: '',
  description: '',
  objective: '',
  platform: 'both',
  max_rounds: 10,
  audience: {
    segment_name: '',
    persona_count: 50,
    age_min: 18,
    age_max: 65,
    gender: 'all',
    regions: []
  }
})

// ── Options ────────────────────────────────────────
const genderOptions = [
  { value: 'all', label: 'All' },
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'non_binary', label: 'Non-Binary' }
]

const regionOptions = [
  { value: 'th', label: 'Thailand' },
  { value: 'sea', label: 'Southeast Asia' },
  { value: 'east_asia', label: 'East Asia' },
  { value: 'south_asia', label: 'South Asia' },
  { value: 'mena', label: 'MENA' },
  { value: 'eu', label: 'Europe' },
  { value: 'na', label: 'North America' },
  { value: 'latam', label: 'Latin America' },
  { value: 'africa', label: 'Africa' },
  { value: 'global', label: 'Global' }
]

const platformOptions = [
  { value: 'twitter', label: 'Twitter/X' },
  { value: 'reddit', label: 'Reddit' },
  { value: 'both', label: 'Both' }
]

const pipelineSteps = [
  { key: 'persona_generation', label: 'Persona Generation', desc: 'Generating AI agent personas with unique traits' },
  { key: 'graph_building', label: 'Graph Building', desc: 'Constructing knowledge graph from documents' },
  { key: 'simulation_running', label: 'Simulation Running', desc: 'Agents interacting in simulated platforms' },
  { key: 'report_generation', label: 'Report Generation', desc: 'Analyzing results and generating insights' }
]

// ── Computed ───────────────────────────────────────
const canSubmit = computed(() => {
  return form.value.name.trim() !== '' && form.value.objective !== ''
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
    message_testing: 'Message Testing',
    crisis_simulation: 'Crisis Simulation',
    product_launch: 'Product Launch',
    competitor_response: 'Competitor Response',
    brand_perception: 'Brand Perception'
  }
  return map[obj] || obj || 'Unknown'
}

function formatPlatform(platform) {
  const map = {
    twitter: '🐦 Twitter',
    reddit: '🤖 Reddit',
    both: '🐦🤖 Both'
  }
  return map[platform] || platform || 'Both'
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
  form.value = {
    name: '',
    description: '',
    objective: '',
    platform: 'both',
    max_rounds: 10,
    audience: {
      segment_name: '',
      persona_count: 50,
      age_min: 18,
      age_max: 65,
      gender: 'all',
      regions: []
    }
  }
  showModal.value = true
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

function openDashboard(campaignId) {
  router.push({ name: 'Dashboard', params: { campaignId } })
}

async function submitCampaign() {
  if (!canSubmit.value || submitting.value) return
  submitting.value = true
  modalError.value = ''

  try {
    // 1. Create campaign
    const payload = {
      name: form.value.name.trim(),
      description: form.value.description.trim(),
      objective: form.value.objective,
      platform: form.value.platform,
      max_rounds: form.value.max_rounds,
      audience: { ...form.value.audience }
    }

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
      campaigns.value = [
        {
          id: 'demo-1',
          name: 'Bank Digital Wallet Launch',
          description: 'Market sentiment simulation for new digital wallet feature targeting Thai urban population.',
          objective: 'product_launch',
          status: 'complete',
          platform: 'both',
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
          persona_count: 200,
          max_rounds: 15,
          created_at: '2026-04-28T08:15:00Z',
          pipeline: null
        }
      ]
    }
  } finally {
    loading.value = false
  }
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

.nav-link:hover,
.nav-link.active {
  color: #FF4500;
}

/* ====================== HEADER ====================== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px 40px 24px;
  border-bottom: 1px solid #1a1a1a;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 6px 0;
}

.page-subtitle {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: #666;
  margin: 0;
}

.btn-new-campaign {
  background: #FF4500;
  color: #fff;
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
  background: #ff5722;
  transform: translateY(-1px);
}

.btn-new-campaign:active {
  transform: translateY(0);
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
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-state h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #ccc;
  margin: 0 0 8px 0;
}

.empty-state p {
  color: #666;
  margin: 0 0 24px 0;
  font-size: 0.9rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #1a1a1a;
  border-top-color: #FF4500;
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
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  padding: 20px 22px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.15s;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.campaign-card:hover {
  border-color: #FF4500;
  transform: translateY(-2px);
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.card-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: #fff;
  margin: 0;
  flex: 1;
  min-width: 0;
}

/* Status Pills */
.status-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
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
  background: rgba(255, 255, 255, 0.06);
  color: #888;
}
.status-draft .status-dot { background: #888; }

.status-active {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}
.status-active .status-dot { background: #22c55e; }

.status-running {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
}
.status-running .status-dot { background: #818cf8; animation: pulse 1.5s infinite; }

.status-complete {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}
.status-complete .status-dot { background: #22c55e; }

.status-failed {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}
.status-failed .status-dot { background: #ef4444; }

.status-paused {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}
.status-paused .status-dot { background: #f59e0b; }

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
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.obj-message { background: rgba(99, 102, 241, 0.12); color: #a5b4fc; }
.obj-crisis { background: rgba(239, 68, 68, 0.12); color: #fca5a5; }
.obj-launch { background: rgba(34, 197, 94, 0.12); color: #86efac; }
.obj-competitor { background: rgba(245, 158, 11, 0.12); color: #fcd34d; }
.obj-brand { background: rgba(168, 85, 247, 0.12); color: #c4b5fd; }
.obj-default { background: rgba(255, 255, 255, 0.06); color: #999; }

.platform-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: #888;
  padding: 3px 10px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.04);
}

/* Card Description */
.card-desc {
  font-size: 0.82rem;
  color: #888;
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
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-icon {
  font-size: 0.75rem;
}

.card-date {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: #555;
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
  background: #1a1a1a;
  border-radius: 2px;
  overflow: hidden;
}

.pipeline-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF4500, #ff7f50);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.pipeline-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: #FF4500;
  white-space: nowrap;
}

/* ====================== MODAL ====================== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 12px;
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #1a1a1a;
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.modal-close {
  background: none;
  border: none;
  color: #666;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #fff;
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
  border-top: 1px solid #1a1a1a;
}

.modal-error {
  margin: 0 24px 16px;
  padding: 10px 14px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
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
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.required {
  color: #FF4500;
}

.form-input {
  padding: 10px 12px;
  background: #0a0a0a;
  border: 1px solid #1a1a1a;
  color: #e0e0e0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  outline: none;
  border-radius: 6px;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #FF4500;
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
  background: #111;
  color: #e0e0e0;
}

.form-section {
  border-top: 1px solid #1a1a1a;
  padding-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: #FF4500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
}

.form-row {
  display: flex;
  gap: 12px;
}

.flex-1 {
  flex: 1;
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
  background: #1a1a1a;
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: #FF4500;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #111;
}

.range-input::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: #FF4500;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #111;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: #444;
}

/* Chip Group */
.chip-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chip {
  padding: 6px 14px;
  background: #0a0a0a;
  border: 1px solid #1a1a1a;
  border-radius: 20px;
  color: #888;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  cursor: pointer;
  transition: all 0.2s;
}

.chip:hover {
  border-color: #444;
  color: #bbb;
}

.chip.active {
  background: rgba(255, 69, 0, 0.12);
  border-color: #FF4500;
  color: #FF4500;
}

.chip:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Buttons */
.btn-cancel {
  background: transparent;
  color: #888;
  border: 1px solid #1a1a1a;
  padding: 10px 24px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-cancel:hover {
  border-color: #444;
  color: #ccc;
}

.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit {
  background: #FF4500;
  color: #fff;
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
  background: #ff5722;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
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
  color: #ccc;
  margin: 0 0 20px 0;
}

.pipeline-progress-bar {
  height: 6px;
  background: #1a1a1a;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.pipeline-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF4500, #ff7f50);
  border-radius: 3px;
  transition: width 0.8s ease;
}

.pipeline-percent {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #888;
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
  border-left: 2px solid #1a1a1a;
  margin-left: 11px;
  transition: border-color 0.3s;
}

.pipeline-step.done {
  border-left-color: #22c55e;
}

.pipeline-step.active {
  border-left-color: #FF4500;
}

.pipeline-step.pending {
  border-left-color: #1a1a1a;
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
  background: rgba(34, 197, 94, 0.12);
}

.pipeline-step.active .step-indicator {
  background: rgba(255, 69, 0, 0.12);
}

.pipeline-step.pending .step-indicator {
  background: #0a0a0a;
  border: 1px solid #1a1a1a;
}

.step-check {
  color: #22c55e;
  font-weight: 700;
}

.step-spinner {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 69, 0, 0.3);
  border-top-color: #FF4500;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.step-circle {
  color: #555;
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.step-name {
  font-size: 0.82rem;
  font-weight: 500;
  color: #ccc;
}

.pipeline-step.done .step-name {
  color: #22c55e;
}

.pipeline-step.active .step-name {
  color: #FF4500;
}

.pipeline-step.pending .step-name {
  color: #666;
}

.step-desc {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: #555;
}

.pipeline-complete {
  margin-top: 20px;
  padding: 16px;
  background: rgba(34, 197, 94, 0.06);
  border: 1px solid rgba(34, 197, 94, 0.2);
  border-radius: 8px;
  text-align: center;
}

.pipeline-complete p {
  color: #86efac;
  margin: 0 0 14px 0;
  font-size: 0.88rem;
}

/* ====================== RESPONSIVE ====================== */
@media (max-width: 768px) {
  .navbar { padding: 0 16px; }
  .page-header { padding: 24px 16px 16px; flex-direction: column; gap: 16px; }
  .campaigns-body { padding: 20px 16px 40px; }
  .campaign-grid { grid-template-columns: 1fr; }
  .form-row { flex-direction: column; }
  .modal-container { max-width: 100%; margin: 0 8px; }
}
</style>
