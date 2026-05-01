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
              <option value="neo4j">Neo4j</option>
              <option value="bolt">Bolt</option>
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
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import TemplateImportDropZone from '@/components/TemplateImportDropZone.vue'

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
    mode: 'neo4j',
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

function changeLanguage() {
  locale.value = selectedLanguage.value
  localStorage.setItem('3c-lang', selectedLanguage.value)
}

function saveSettings() {
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
  } catch (e) {
    message.value = t('settings.saveFailed')
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

async function testConnection() {
  testing.value = true
  message.value = ''
  try {
    // Placeholder for actual connection test
    await new Promise(resolve => setTimeout(resolve, 1500))
    message.value = t('settings.connectionSuccess')
    messageType.value = 'success'
  } catch (e) {
    message.value = t('settings.connectionFailed')
    messageType.value = 'error'
  } finally {
    testing.value = false
  }
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
    if (parsed.language) {
      selectedLanguage.value = parsed.language
      locale.value = parsed.language
    }
  }
} catch (e) {
  // ignore parse errors
}
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

.section-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-5);
  color: var(--text-primary);
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
  .form-grid {
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
