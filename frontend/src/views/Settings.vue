<template>
  <div class="settings-page">
    <nav class="navbar">
      <div class="nav-brand">MIROFISH OFFLINE</div>
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

const { locale } = useI18n()

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
  localStorage.setItem('mirofish-lang', selectedLanguage.value)
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
    localStorage.setItem('mirofish-settings', JSON.stringify(settings))
    message.value = 'Settings saved successfully'
    messageType.value = 'success'
  } catch (e) {
    message.value = 'Failed to save settings'
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
    message.value = 'Connection successful'
    messageType.value = 'success'
  } catch (e) {
    message.value = 'Connection failed'
    messageType.value = 'error'
  } finally {
    testing.value = false
  }
}

// Load saved settings on mount
try {
  const saved = localStorage.getItem('mirofish-settings')
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
  background: #fff;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  color: #000;
}

.navbar {
  height: 60px;
  background: #000;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: #999;
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: #FF4500;
}

.settings-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.page-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 32px;
}

.config-section {
  margin-bottom: 36px;
  padding-bottom: 36px;
  border-bottom: 1px solid #eee;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #000;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.8rem;
  font-family: 'JetBrains Mono', monospace;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  background: #fafafa;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #FF4500;
}

.action-row {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.btn-primary {
  background: #000;
  color: #fff;
  border: none;
  padding: 14px 32px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.5px;
}

.btn-primary:hover {
  background: #333;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: transparent;
  color: #000;
  border: 1px solid #ddd;
  padding: 14px 32px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  cursor: pointer;
}

.btn-secondary:hover {
  border-color: #000;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message {
  margin-top: 20px;
  padding: 12px 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
}

.message.success {
  background: #f0fff4;
  color: #2f855a;
  border: 1px solid #c6f6d5;
}

.message.error {
  background: #fff5f5;
  color: #c53030;
  border: 1px solid #fed7d7;
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
