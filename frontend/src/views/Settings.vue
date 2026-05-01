<template>
  <div class="settings-page">
    <nav class="navbar">
      <div class="nav-brand">3C SIMULATOR</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">{{ $t('nav.home') }}</router-link>
        <router-link to="/settings" class="nav-link active">{{ $t('nav.settings') }}</router-link>
      </div>
    </nav>

    <div class="settings-content">
      <h1 class="page-title">{{ $t('settings.title') }}</h1>

      <!-- Setup Wizard -->
      <section class="config-section setup-wizard">
        <div class="section-heading-row">
          <div>
            <h2 class="section-title">{{ $t('settings.wizardTitle') }}</h2>
            <p class="section-desc">{{ $t('settings.wizardDesc') }}</p>
          </div>
          <button class="btn-secondary compact" @click="runReadinessCheck" :disabled="wizardLoading">
            {{ wizardLoading ? $t('common.loading') : $t('settings.checkReadiness') }}
          </button>
        </div>

        <div class="wizard-modes">
          <button
            v-for="mode in wizardModes"
            :key="mode.id"
            :class="['wizard-mode', { active: wizardMode === mode.id }]"
            type="button"
            @click="selectWizardMode(mode.id)"
          >
            <strong>{{ $t(mode.labelKey) }}</strong>
            <span>{{ $t(mode.descKey) }}</span>
          </button>
        </div>

        <div class="wizard-steps">
          <button
            v-for="(step, idx) in wizardSteps"
            :key="step.key"
            :class="['wizard-step', { active: wizardStep === idx, done: readinessStatus(step.key) === 'ready' || readinessStatus(step.key) === 'skipped' }]"
            type="button"
            @click="wizardStep = idx"
          >
            <span>{{ idx + 1 }}</span>
            <strong>{{ $t(step.labelKey) }}</strong>
          </button>
        </div>

        <div class="wizard-panel">
          <div>
            <span class="wizard-kicker">{{ $t(activeWizardStep.kickerKey) }}</span>
            <h3>{{ $t(activeWizardStep.labelKey) }}</h3>
            <p>{{ $t(activeWizardStep.helpKey) }}</p>
          </div>

          <div v-if="activeWizardStep.key === 'mode'" class="wizard-readiness">
            <article>
              <strong>{{ $t('settings.currentSetupMode') }}</strong>
              <p>{{ setupModeLabel }}</p>
            </article>
            <article>
              <strong>{{ $t('settings.costEstimate') }}</strong>
              <p>{{ costEstimateText }}</p>
              <small>{{ readiness.cost_estimate?.disclaimer || $t('settings.costEstimateDisclaimer') }}</small>
            </article>
          </div>

          <div v-else-if="activeWizardStep.key === 'llm'" class="wizard-test-row">
            <article class="readiness-card">
              <strong>{{ $t('settings.llm') }}</strong>
              <span :class="['status-dot-label', statusClass(readiness.checks.llm.status)]">{{ readinessLabel(readiness.checks.llm.status) }}</span>
              <p>{{ readiness.checks.llm.safe_detail }}</p>
              <ul v-if="readiness.checks.llm.issues?.length">
                <li v-for="issue in readiness.checks.llm.issues" :key="issue">{{ issue }}</li>
              </ul>
            </article>
            <button class="btn-secondary" type="button" @click="testLLMProvider" :disabled="testingProvider || wizardMode === 'demo'">
              {{ testingProvider ? $t('common.loading') : $t('settings.testLlmProvider') }}
            </button>
          </div>

          <div v-else-if="activeWizardStep.key === 'embedding'" class="wizard-test-row">
            <article class="readiness-card">
              <strong>{{ $t('settings.embedding') }}</strong>
              <span :class="['status-dot-label', statusClass(readiness.checks.embedding.status)]">{{ readinessLabel(readiness.checks.embedding.status) }}</span>
              <p>{{ readiness.checks.embedding.safe_detail }}</p>
              <ul v-if="readiness.checks.embedding.issues?.length">
                <li v-for="issue in readiness.checks.embedding.issues" :key="issue">{{ issue }}</li>
              </ul>
            </article>
            <p class="wizard-note">{{ $t('settings.embeddingReadinessNote') }}</p>
          </div>

          <div v-else-if="activeWizardStep.key === 'neo4j'" class="wizard-test-row">
            <article class="readiness-card">
              <strong>{{ $t('settings.graphdb') }}</strong>
              <span :class="['status-dot-label', statusClass(readiness.checks.neo4j.status)]">{{ readinessLabel(readiness.checks.neo4j.status) }}</span>
              <p>{{ readiness.checks.neo4j.safe_detail }}</p>
              <ul v-if="readiness.checks.neo4j.issues?.length">
                <li v-for="issue in readiness.checks.neo4j.issues" :key="issue">{{ issue }}</li>
              </ul>
            </article>
            <button class="btn-secondary" type="button" @click="loadSystemStatus" :disabled="statusLoading || wizardMode === 'demo'">
              {{ statusLoading ? $t('common.loading') : $t('settings.testNeo4jStatus') }}
            </button>
          </div>

          <div v-else class="wizard-readiness">
            <article>
              <strong>{{ readiness.sample_simulation?.label || $t('settings.sampleSimulation') }}</strong>
              <p>{{ readiness.sample_simulation?.detail || $t('settings.sampleSimulationDesc') }}</p>
            </article>
            <article>
              <strong>{{ $t('settings.readinessResult') }}</strong>
              <p :class="readiness.ready ? 'is-ok-text' : 'is-warning-text'">
                {{ readiness.ready ? $t('settings.readyToSimulate') : $t('settings.needsAttentionBeforeSimulation') }}
              </p>
            </article>
          </div>

          <div v-if="wizardMessage" :class="['message inline-message', wizardMessageType]">{{ wizardMessage }}</div>
        </div>
      </section>

      <!-- System Health -->
      <section class="config-section system-health">
        <div class="section-heading-row">
          <div>
            <h2 class="section-title">{{ $t('settings.systemHealth') }}</h2>
            <p class="section-desc">{{ $t('settings.systemHealthDesc') }}</p>
          </div>
          <button class="btn-secondary compact" @click="loadSystemStatus" :disabled="statusLoading">
            {{ statusLoading ? $t('common.loading') : $t('settings.refreshStatus') }}
          </button>
        </div>

        <div class="health-summary">
          <div>
            <span>{{ $t('settings.overallStatus') }}</span>
            <strong :class="statusClass(systemStatus.status)">{{ statusLabel(systemStatus.status) }}</strong>
          </div>
          <div>
            <span>{{ $t('settings.costEstimate') }}</span>
            <strong>${{ systemStatus.estimate?.cost_per_100_personas_usd ?? '—' }} / 100 personas</strong>
          </div>
          <div>
            <span>{{ $t('settings.defaultModel') }}</span>
            <strong>{{ systemStatus.estimate?.default_model || '—' }}</strong>
          </div>
        </div>

        <div class="health-grid">
          <article v-for="service in systemStatus.services" :key="service.key" class="health-card">
            <div class="health-card-top">
              <strong>{{ service.label }}</strong>
              <span :class="['status-dot-label', statusClass(service.status)]">{{ statusLabel(service.status) }}</span>
            </div>
            <p>{{ service.detail }}</p>
            <small v-if="service.meta?.free_gb !== undefined">Free disk: {{ service.meta.free_gb }} GB</small>
          </article>
        </div>
      </section>

      <!-- LLM Configuration -->
      <section class="config-section">
        <h2 class="section-title">{{ $t('settings.llm') }}</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>{{ $t('settings.provider') }}</label>
            <select v-model="config.llm.provider">
              <option value="ollama">Ollama</option>
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
              <option value="deepseek">DeepSeek</option>
            </select>
          </div>
          <div class="form-group">
            <label>{{ $t('settings.model') }}</label>
            <input v-model="config.llm.model" type="text" placeholder="e.g. llama3" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.apiKey') }}</label>
            <input v-model="config.llm.apiKey" type="password" placeholder="sk-..." />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.baseUrl') }}</label>
            <input v-model="config.llm.baseUrl" type="text" placeholder="http://localhost:11434" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.temperature') }}</label>
            <input v-model.number="config.llm.temperature" type="number" min="0" max="2" step="0.1" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.maxTokens') }}</label>
            <input v-model.number="config.llm.maxTokens" type="number" min="1" max="32768" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.timeout') }}</label>
            <input v-model.number="config.llm.timeout" type="number" min="1" max="600" />
          </div>
        </div>
      </section>

      <!-- Embedding Configuration -->
      <section class="config-section">
        <h2 class="section-title">{{ $t('settings.embedding') }}</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>{{ $t('settings.provider') }}</label>
            <select v-model="config.embedding.provider">
              <option value="ollama">Ollama</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>
          <div class="form-group">
            <label>{{ $t('settings.model') }}</label>
            <input v-model="config.embedding.model" type="text" placeholder="e.g. nomic-embed-text" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.apiKey') }}</label>
            <input v-model="config.embedding.apiKey" type="password" placeholder="sk-..." />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.baseUrl') }}</label>
            <input v-model="config.embedding.baseUrl" type="text" placeholder="http://localhost:11434" />
          </div>
        </div>
      </section>

      <!-- Task-Specific Overrides -->
      <section class="config-section">
        <h2 class="section-title">{{ $t('settings.taskOverrides') }}</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>{{ $t('settings.ner') }}</label>
            <input v-model="config.tasks.ner" type="text" placeholder="llama3" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.report') }}</label>
            <input v-model="config.tasks.report" type="text" placeholder="llama3" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.simulation') }}</label>
            <input v-model="config.tasks.simulation" type="text" placeholder="llama3" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.ontology') }}</label>
            <input v-model="config.tasks.ontology" type="text" placeholder="llama3" />
          </div>
        </div>
      </section>

      <!-- Graph Database Configuration -->
      <section class="config-section">
        <h2 class="section-title">{{ $t('settings.graphdb') }}</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>{{ $t('settings.graphMode') }}</label>
            <select v-model="config.graphdb.mode">
              <option value="local">Local Neo4j</option>
              <option value="cloud">Neo4j AuraDB</option>
            </select>
          </div>
          <div class="form-group">
            <label>{{ $t('settings.graphUri') }}</label>
            <input v-model="config.graphdb.uri" type="text" placeholder="bolt://localhost:7687" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.graphUser') }}</label>
            <input v-model="config.graphdb.user" type="text" placeholder="neo4j" />
          </div>
          <div class="form-group">
            <label>{{ $t('settings.graphPassword') }}</label>
            <input v-model="config.graphdb.password" type="password" placeholder="password" />
          </div>
        </div>
      </section>

      <!-- Language Selection -->
      <section class="config-section">
        <h2 class="section-title">{{ $t('settings.language') }}</h2>
        <div class="form-group">
          <select v-model="selectedLanguage" @change="changeLanguage">
            <option value="en">English</option>
            <option value="zh-CN">中文 (简体)</option>
            <option value="th">ภาษาไทย</option>
            <option value="es">Español</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
            <option value="pt">Português</option>
            <option value="ru">Русский</option>
            <option value="hi">हिन्दी</option>
            <option value="bn">বাংলা</option>
            <option value="ur">اردو</option>
          </select>
        </div>
      </section>

      <!-- Industry Template Import -->
      <section class="config-section">
        <TemplateImportDropZone @template-imported="onTemplateImported" />
      </section>

      <!-- Action Buttons -->
      <div class="action-row">
        <button class="btn-primary" @click="saveSettings" :disabled="saving">
          {{ saving ? $t('common.saving') : $t('settings.save') }}
        </button>
        <button class="btn-secondary" @click="testConnection" :disabled="testing">
          {{ testing ? $t('common.saving') : $t('settings.test') }}
        </button>
      </div>

      <div v-if="message" :class="['message', messageType]">{{ message }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import TemplateImportDropZone from '@/components/TemplateImportDropZone.vue'
import { getSystemStatus } from '@/api/status'
import { checkSettingsReadiness, getProviders, testLLMConnection, updateSettings } from '@/api/settings'

const { locale, t } = useI18n()

const config = reactive({
  llm: {
    provider: 'ollama',
    model: '',
    apiKey: '',
    baseUrl: 'http://localhost:11434',
    temperature: 0.7,
    maxTokens: 4096,
    timeout: 120
  },
  embedding: {
    provider: 'ollama',
    model: '',
    apiKey: '',
    baseUrl: 'http://localhost:11434'
  },
  tasks: {
    ner: '',
    report: '',
    simulation: '',
    ontology: ''
  },
  graphdb: {
    mode: 'local',
    uri: 'bolt://localhost:7687',
    user: 'neo4j',
    password: ''
  }
})

const selectedLanguage = ref(locale.value)
const saving = ref(false)
const testing = ref(false)
const message = ref('')
const messageType = ref('success')
const statusLoading = ref(false)
const wizardMode = ref('demo')
const wizardStep = ref(0)
const wizardLoading = ref(false)
const testingProvider = ref(false)
const wizardMessage = ref('')
const wizardMessageType = ref('success')
const providerCatalog = ref({ llm_providers: [], embedding_providers: [], graph_db_modes: [] })
const systemStatus = reactive({
  status: 'degraded',
  services: [],
  estimate: {}
})
const readiness = reactive(defaultReadiness())

const wizardModes = [
  { id: 'demo', labelKey: 'settings.modeDemoOnly', descKey: 'settings.modeDemoOnlyDesc' },
  { id: 'local', labelKey: 'settings.modeLocalModel', descKey: 'settings.modeLocalModelDesc' },
  { id: 'cloud', labelKey: 'settings.modeCloudApi', descKey: 'settings.modeCloudApiDesc' },
]

const wizardSteps = [
  { key: 'mode', labelKey: 'settings.wizardStepMode', kickerKey: 'settings.wizardKickerStart', helpKey: 'settings.wizardStepModeHelp' },
  { key: 'llm', labelKey: 'settings.wizardStepLlm', kickerKey: 'settings.wizardKickerProvider', helpKey: 'settings.wizardStepLlmHelp' },
  { key: 'embedding', labelKey: 'settings.wizardStepEmbedding', kickerKey: 'settings.wizardKickerProvider', helpKey: 'settings.wizardStepEmbeddingHelp' },
  { key: 'neo4j', labelKey: 'settings.wizardStepNeo4j', kickerKey: 'settings.wizardKickerStorage', helpKey: 'settings.wizardStepNeo4jHelp' },
  { key: 'sample', labelKey: 'settings.wizardStepSample', kickerKey: 'settings.wizardKickerReady', helpKey: 'settings.wizardStepSampleHelp' },
]

const activeWizardStep = computed(() => wizardSteps[wizardStep.value] || wizardSteps[0])
const setupModeLabel = computed(() => t(wizardModes.find(mode => mode.id === wizardMode.value)?.labelKey || 'settings.modeDemoOnly'))
const costEstimateText = computed(() => {
  const value = readiness.cost_estimate?.per_100_personas
  if (value == null) return t('settings.costEstimateUnknown')
  return `$${value} / 100 personas (${readiness.cost_estimate?.label || t('settings.estimateOnly')})`
})

function changeLanguage() {
  locale.value = selectedLanguage.value
  localStorage.setItem('3c-lang', selectedLanguage.value)
}

async function saveSettings() {
  saving.value = true
  message.value = ''
  try {
    const settings = {
      llm: { ...config.llm },
      embedding: { ...config.embedding },
      tasks: { ...config.tasks },
      graphdb: { ...config.graphdb },
      language: selectedLanguage.value
    }
    localStorage.setItem('3c-settings', JSON.stringify(settings))
    message.value = t('settings.saveSuccess')
    messageType.value = 'success'
    if (wizardMode.value !== 'demo' && readiness.ready) {
      await updateSettings(toBackendSettings(settings))
    } else if (wizardMode.value !== 'demo' && !readiness.ready) {
      message.value = t('settings.localSaveNeedsReadiness')
    }
  } catch (e) {
    console.warn('Settings save failed:', e.message)
    message.value = wizardMode.value === 'demo' ? t('settings.saveFailed') : t('settings.localSaveBackendFailed')
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

async function testConnection() {
  testing.value = true
  message.value = ''
  try {
    await runReadinessCheck()
    message.value = readiness.ready ? t('settings.connectionSuccess') : t('settings.connectionNeedsAttention')
    messageType.value = readiness.ready ? 'success' : 'error'
  } catch (e) {
    message.value = t('settings.connectionFailed')
    messageType.value = 'error'
  } finally {
    testing.value = false
  }
}

async function loadSystemStatus() {
  statusLoading.value = true
  try {
    const res = await getSystemStatus()
    const data = res.data || res
    systemStatus.status = data.status || 'degraded'
    systemStatus.services = data.services || []
    systemStatus.estimate = data.estimate || {}
  } catch (e) {
    systemStatus.status = 'degraded'
    systemStatus.services = [
      { key: 'api', label: 'Backend API', status: 'warning', detail: e.message || 'Unable to reach status API' }
    ]
  } finally {
    statusLoading.value = false
  }
}

function statusLabel(status) {
  const labels = {
    ok: t('settings.statusOk'),
    configured: t('settings.statusConfigured'),
    warning: t('settings.statusWarning'),
    degraded: t('settings.statusDegraded')
  }
  return labels[status] || status || t('settings.statusWarning')
}

function statusClass(status) {
  if (status === 'ok' || status === 'configured' || status === 'ready' || status === 'skipped') return 'is-ok'
  return 'is-warning'
}

function defaultReadiness() {
  return {
    mode: 'demo',
    ready: true,
    checks: {
      llm: { status: 'skipped', safe_detail: 'Demo mode does not require an LLM provider.', issues: [] },
      embedding: { status: 'skipped', safe_detail: 'Demo mode does not require an embedding provider.', issues: [] },
      neo4j: { status: 'skipped', safe_detail: 'Demo mode does not require Neo4j.', issues: [] },
    },
    sample_simulation: { status: 'available', label: 'Try Sample Campaign', detail: 'Use a deterministic demo campaign.' },
    cost_estimate: { per_100_personas: 0, label: 'Directional estimate only', disclaimer: '' },
  }
}

function selectWizardMode(mode) {
  wizardMode.value = mode
  if (mode === 'demo') {
    wizardStep.value = 0
  } else if (mode === 'local') {
    config.llm.provider = 'ollama'
    config.embedding.provider = 'ollama'
    config.graphdb.mode = 'local'
    config.llm.baseUrl = config.llm.baseUrl || 'http://localhost:11434/v1'
    config.embedding.baseUrl = config.embedding.baseUrl || 'http://localhost:11434'
  } else if (mode === 'cloud') {
    if (config.llm.provider === 'ollama') config.llm.provider = 'openai'
    if (config.embedding.provider === 'ollama') config.embedding.provider = 'openai'
    config.graphdb.mode = 'cloud'
  }
  runReadinessCheck()
}

async function loadProviderCatalog() {
  try {
    const res = await getProviders()
    providerCatalog.value = res.data || res
  } catch (e) {
    console.warn('Provider catalog unavailable:', e.message)
  }
}

function readinessStatus(key) {
  if (key === 'mode' || key === 'sample') return readiness.ready ? 'ready' : 'needs_attention'
  return readiness.checks[key]?.status || 'needs_attention'
}

function readinessLabel(status) {
  const labels = {
    ready: t('settings.statusReady'),
    skipped: t('settings.statusSkipped'),
    needs_attention: t('settings.statusNeedsAttention'),
    ok: t('settings.statusOk'),
    configured: t('settings.statusConfigured'),
    warning: t('settings.statusWarning'),
  }
  return labels[status] || status || t('settings.statusWarning')
}

async function runReadinessCheck() {
  wizardLoading.value = true
  wizardMessage.value = ''
  try {
    const res = await checkSettingsReadiness(toReadinessPayload())
    Object.assign(readiness, res.data || res)
    wizardMessage.value = readiness.ready ? t('settings.readinessReady') : t('settings.readinessNeedsAttention')
    wizardMessageType.value = readiness.ready ? 'success' : 'error'
  } catch (e) {
    wizardMessage.value = safeClientError(e)
    wizardMessageType.value = 'error'
  } finally {
    wizardLoading.value = false
  }
}

async function testLLMProvider() {
  testingProvider.value = true
  wizardMessage.value = ''
  try {
    const res = await testLLMConnection(toBackendSettings({ llm: config.llm }).llm)
    wizardMessage.value = res.message || t('settings.connectionSuccess')
    wizardMessageType.value = 'success'
  } catch (e) {
    wizardMessage.value = safeClientError(e)
    wizardMessageType.value = 'error'
  } finally {
    testingProvider.value = false
  }
}

function toReadinessPayload() {
  const backend = toBackendSettings({
    llm: config.llm,
    embedding: config.embedding,
    graphdb: config.graphdb,
  })
  return {
    mode: wizardMode.value,
    llm: {
      provider: backend.llm.provider,
      model: backend.llm.model,
      base_url: backend.llm.base_url,
      api_key_present: Boolean(backend.llm.api_key),
    },
    embedding: {
      provider: backend.embedding.provider,
      model: backend.embedding.model,
      base_url: backend.embedding.base_url,
      api_key_present: Boolean(backend.embedding.api_key),
    },
    graph_db: {
      mode: backend.graph_db.mode,
      uri: backend.graph_db.uri,
      user: backend.graph_db.user,
      password_present: Boolean(backend.graph_db.password),
    },
  }
}

function toBackendSettings(settings) {
  return {
    language: selectedLanguage.value,
    llm: {
      provider: settings.llm?.provider || 'ollama',
      model: settings.llm?.model || 'qwen2.5:7b',
      api_key: unmaskedSecret(settings.llm?.apiKey),
      base_url: settings.llm?.baseUrl || null,
      temperature: settings.llm?.temperature ?? 0.7,
      max_tokens: settings.llm?.maxTokens ?? 4096,
      timeout: settings.llm?.timeout ?? 600,
    },
    embedding: {
      provider: settings.embedding?.provider || 'ollama',
      model: settings.embedding?.model || 'nomic-embed-text',
      api_key: unmaskedSecret(settings.embedding?.apiKey),
      base_url: settings.embedding?.baseUrl || null,
    },
    graph_db: {
      mode: normalizeGraphMode(settings.graphdb?.mode),
      uri: settings.graphdb?.uri || 'bolt://localhost:7687',
      user: settings.graphdb?.user || 'neo4j',
      password: unmaskedSecret(settings.graphdb?.password),
    },
    task_llm: {},
  }
}

function normalizeGraphMode(mode) {
  if (mode === 'neo4j' || mode === 'bolt') return 'local'
  return mode || 'local'
}

function unmaskedSecret(value) {
  if (!value || String(value).includes('••••') || String(value).includes('****')) return ''
  return value
}

function safeClientError(error) {
  const raw = error?.message || String(error || '')
  return raw.replace(/sk-[A-Za-z0-9_-]{8,}/g, 'sk-***').slice(0, 180) || t('settings.connectionFailed')
}

// Load saved settings on mount
try {
  const saved = localStorage.getItem('3c-settings')
  if (saved) {
    const parsed = JSON.parse(saved)
    Object.assign(config.llm, parsed.llm || {})
    Object.assign(config.embedding, parsed.embedding || {})
    Object.assign(config.tasks, parsed.tasks || {})
    Object.assign(config.graphdb, parsed.graphdb || {})
    config.graphdb.mode = normalizeGraphMode(config.graphdb.mode)
    if (parsed.language) {
      selectedLanguage.value = parsed.language
      locale.value = parsed.language
    }
  }
} catch (e) {
  // ignore parse errors
}

onMounted(() => {
  loadProviderCatalog()
  loadSystemStatus()
  runReadinessCheck()
})
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background: var(--bg-canvas);
  font-family: var(--font-sans);
  color: var(--text-secondary);
}

.navbar {
  min-height: 64px;
  background: rgba(var(--bg-canvas-rgb), 0.78);
  color: var(--text-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 clamp(18px, 4vw, 48px);
  border-bottom: 1px solid var(--border-subtle);
}

.nav-brand {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0;
  font-size: var(--text-lg);
}

.nav-links {
  display: flex;
  gap: var(--space-3);
  min-width: 0;
  flex-wrap: nowrap;
}

.nav-link {
  flex: 0 0 auto;
  color: var(--text-tertiary);
  text-decoration: none;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 700;
  line-height: 1;
  padding: 8px 10px;
  border-radius: var(--radius-md);
  white-space: nowrap;
  transition: color var(--transition-fast), background var(--transition-fast);
}

.nav-link:hover,
.nav-link.active {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.settings-content {
  max-width: 980px;
  margin: 0 auto;
  padding: clamp(32px, 5vw, 58px) clamp(18px, 4vw, 40px) 72px;
}

.page-title {
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 5vw, 3.3rem);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-8);
}

.config-section {
  margin-bottom: var(--space-5);
  padding: var(--space-6);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: var(--shadow-card);
}

.setup-wizard {
  border-color: var(--border-accent);
}

.wizard-modes,
.wizard-steps,
.wizard-readiness {
  display: grid;
  gap: var(--space-3);
}

.wizard-modes {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-bottom: var(--space-5);
}

.wizard-mode {
  min-height: 112px;
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  color: var(--text-secondary);
  text-align: left;
  cursor: pointer;
}

.wizard-mode.active {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.wizard-mode strong,
.readiness-card strong,
.wizard-readiness strong {
  display: block;
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 900;
}

.wizard-mode span {
  display: block;
  margin-top: var(--space-2);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.wizard-steps {
  grid-template-columns: repeat(5, minmax(0, 1fr));
  margin-bottom: var(--space-5);
}

.wizard-step {
  min-height: 64px;
  padding: var(--space-3);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
  color: var(--text-secondary);
  cursor: pointer;
  text-align: left;
}

.wizard-step span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  margin-right: 6px;
  border-radius: 50%;
  background: var(--bg-elevated);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
}

.wizard-step strong {
  color: var(--text-primary);
  font-size: var(--text-xs);
}

.wizard-step.active {
  border-color: var(--accent);
}

.wizard-step.done span {
  background: var(--green-soft);
  color: var(--green);
}

.wizard-panel {
  padding: var(--space-5);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
}

.wizard-kicker {
  display: block;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.wizard-panel h3 {
  margin: var(--space-2) 0;
  color: var(--text-primary);
  font-size: var(--text-lg);
}

.wizard-panel p,
.wizard-note {
  margin: 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.wizard-readiness {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: var(--space-4);
}

.wizard-readiness article,
.readiness-card {
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.readiness-card {
  display: grid;
  gap: var(--space-2);
}

.readiness-card ul {
  margin: 0;
  padding-left: var(--space-5);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.wizard-test-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: var(--space-4);
  align-items: start;
  margin-top: var(--space-4);
}

.inline-message {
  margin-top: var(--space-4);
}

.is-ok-text {
  color: var(--green) !important;
}

.is-warning-text {
  color: var(--yellow) !important;
}

.section-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-5);
  color: var(--text-primary);
}

.section-heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

.section-heading-row .section-title {
  margin-bottom: var(--space-2);
}

.section-desc {
  margin: 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.55;
}

.health-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1px;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--border-subtle);
  margin-bottom: var(--space-4);
}

.health-summary div {
  min-width: 0;
  padding: var(--space-4);
  background: var(--bg-panel);
}

.health-summary span {
  display: block;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.66rem;
  font-weight: 800;
  text-transform: uppercase;
}

.health-summary strong {
  display: block;
  margin-top: 8px;
  color: var(--text-primary);
  font-size: var(--text-base);
  line-height: 1.25;
  overflow-wrap: anywhere;
}

.health-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-3);
}

.health-card {
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-panel);
}

.health-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.health-card-top strong {
  color: var(--text-primary);
}

.status-dot-label {
  flex: 0 0 auto;
  padding: 4px 8px;
  border-radius: 999px;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 800;
  text-transform: uppercase;
}

.is-ok {
  color: var(--green);
  background: var(--green-soft);
}

.is-warning {
  color: var(--yellow);
  background: var(--yellow-soft);
}

.health-card p,
.health-card small {
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.health-card p {
  margin: 10px 0 0;
}

.health-card small {
  display: block;
  margin-top: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin: 0;
}

.form-group label {
  font-size: 0.68rem;
  font-family: var(--font-mono);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0;
}

.form-group input,
.form-group select {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  background: var(--bg-panel);
  color: var(--text-primary);
  outline: none;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-group input:focus,
.form-group select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}

.action-row {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-6);
  flex-wrap: wrap;
}

.btn-primary {
  background: var(--text-primary);
  color: var(--text-inverse);
  border: 1px solid var(--text-primary);
  border-radius: var(--radius-md);
  padding: 12px 24px;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 800;
  cursor: pointer;
  letter-spacing: 0;
}

.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: #fff;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-surface);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 12px 24px;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 800;
  cursor: pointer;
}

.btn-secondary:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-sm);
}

.btn-secondary.compact {
  flex: 0 0 auto;
  padding: 9px 14px;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message {
  margin-top: 20px;
  padding: 12px 16px;
  font-family: var(--font-sans);
  font-size: 0.85rem;
  border-radius: var(--radius-md);
}

.message.success {
  background: var(--green-soft);
  color: var(--green);
  border: 1px solid color-mix(in srgb, var(--green) 28%, transparent);
}

.message.error {
  background: var(--red-soft);
  color: var(--red);
  border: 1px solid color-mix(in srgb, var(--red) 28%, transparent);
}

@media (max-width: 600px) {
  .form-grid,
  .wizard-modes,
  .wizard-steps,
  .wizard-readiness,
  .wizard-test-row {
    grid-template-columns: 1fr;
  }
  .section-heading-row {
    flex-direction: column;
  }
  .health-summary,
  .health-grid {
    grid-template-columns: 1fr;
  }
  .settings-content {
    padding: 24px 16px;
  }
  .navbar {
    padding: 0 16px;
  }
}
</style>
