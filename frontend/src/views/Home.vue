<template>
  <div class="home-page">
    <nav class="home-nav">
      <router-link to="/" class="nav-brand">{{ $t('home.brand') }}</router-link>
      <div class="nav-right">
        <router-link to="/campaigns" class="nav-link">{{ $t('home.navCampaigns') }}</router-link>
        <router-link to="/settings" class="nav-link">{{ $t('home.navSettings') }}</router-link>
        <select v-model="currentLanguage" class="language-select" @change="changeLanguage" :aria-label="$t('home.languageLabel')">
          <option value="en">{{ $t('home.languageEn') }}</option>
          <option value="th">{{ $t('home.languageTh') }}</option>
          <option value="zh-CN">{{ $t('home.languageZh') }}</option>
        </select>
      </div>
    </nav>

    <main>
      <section class="hero-section reveal is-visible">
        <div class="hero-inner">
          <div class="hero-copy-stack">
            <div class="hero-badge">{{ $t('home.heroBadge') }}</div>
            <h1 class="hero-title">
              <span>{{ $t('home.heroPunch1') }}</span>
              <span class="hero-shift">{{ $t('home.heroPunch2') }}</span>
              <span class="hero-shift hero-shift-large">{{ $t('home.heroPunch3') }}</span>
            </h1>
            <p class="hero-copy">{{ $t('home.heroCopy') }}</p>

            <div class="hero-actions">
              <router-link to="/campaigns" class="btn-hero btn-primary">
                <span>{{ $t('home.primaryCta') }}</span>
                <span class="btn-arrow">→</span>
              </router-link>
              <router-link to="/war-room" class="btn-hero btn-secondary">
                <span>{{ $t('home.demoCta') }}</span>
                <span class="btn-arrow">→</span>
              </router-link>
            </div>

            <div ref="statsSection" class="stats-row">
              <div v-for="stat in stats" :key="stat.key" class="stat-item">
                <strong>{{ stat.display }}</strong>
                <span>{{ stat.label }}</span>
              </div>
            </div>
          </div>

          <aside class="hero-proof" :aria-label="$t('home.previewAria')">
            <div class="proof-chrome">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div class="proof-command">
              <span class="command-prefix">⌘K</span>
              <span>{{ $t('home.previewCommand') }}</span>
            </div>
            <div class="proof-grid">
              <div class="proof-score">
                <span>{{ $t('home.previewWinner') }}</span>
                <strong>Variant B</strong>
                <small>+18.4% {{ $t('home.previewLift') }}</small>
              </div>
              <div class="proof-score muted">
                <span>{{ $t('home.previewRisk') }}</span>
                <strong>Low</strong>
                <small>3 / 10</small>
              </div>
            </div>
            <div class="proof-section">
              <div class="proof-header">
                <span>{{ $t('home.previewSentiment') }}</span>
                <strong>74%</strong>
              </div>
              <div class="sentiment-bars">
                <span class="bar-positive"></span>
                <span class="bar-neutral"></span>
                <span class="bar-negative"></span>
              </div>
            </div>
            <div class="proof-section">
              <div class="proof-header">
                <span>{{ $t('home.previewPersonas') }}</span>
                <strong>500</strong>
              </div>
              <div class="persona-table">
                <div v-for="row in previewRows" :key="row.segment" class="persona-row">
                  <span>{{ row.segment }}</span>
                  <div class="mini-meter"><i :style="{ width: row.width }"></i></div>
                  <strong>{{ row.value }}</strong>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>

      <section class="section-block flow-section reveal">
        <div class="section-heading">
          <span>{{ $t('home.workflowEyebrow') }}</span>
          <h2>{{ $t('home.workflowHeading') }}</h2>
        </div>
        <div class="flow-grid">
          <article v-for="step in flowSteps" :key="step.no" class="flow-card">
            <div class="flow-top">
              <span class="flow-number">{{ step.no }}</span>
              <span class="icon-shell flow-icon" :class="`icon-${step.kind}`">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path v-if="step.kind === 'template'" d="M4 5h16M4 12h16M4 19h16M8 3v18M16 3v18" />
                  <path v-else-if="step.kind === 'compare'" d="M5 6h6v12H5zM13 6h6v12h-6zM11 12h2" />
                  <path v-else-if="step.kind === 'impact'" d="M5 19V9M12 19V5M19 19v-7M3 19h18" />
                  <path v-else-if="step.kind === 'war'" d="M12 3v18M3 12h18M6.4 6.4l11.2 11.2M17.6 6.4L6.4 17.6" />
                  <path v-else d="M12 4v10M8 10l4 4 4-4M5 20h14" />
                </svg>
              </span>
            </div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </article>
        </div>
      </section>

      <section class="section-block feature-section reveal">
        <div class="section-heading wide">
          <span>{{ $t('home.featuresEyebrow') }}</span>
          <h2>{{ $t('home.featuresHeading') }}</h2>
        </div>
        <div class="feature-grid">
          <router-link v-for="feature in features" :key="feature.title" :to="feature.to" class="feature-card">
            <span class="icon-shell feature-icon" :class="`icon-${feature.kind}`">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path v-if="feature.kind === 'template'" d="M4 5h16M4 12h16M4 19h16M8 3v18M16 3v18" />
                <path v-else-if="feature.kind === 'compare'" d="M5 6h6v12H5zM13 6h6v12h-6zM11 12h2" />
                <path v-else-if="feature.kind === 'impact'" d="M5 19V9M12 19V5M19 19v-7M3 19h18" />
                <path v-else-if="feature.kind === 'war'" d="M12 3v18M3 12h18M6.4 6.4l11.2 11.2M17.6 6.4L6.4 17.6" />
                <path v-else-if="feature.kind === 'export'" d="M12 4v10M8 10l4 4 4-4M5 20h14" />
                <path v-else d="M4 7h16M7 4v16M17 4v16M4 17h16" />
              </svg>
            </span>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
            <span class="try-link">{{ $t('home.tryIt') }} →</span>
          </router-link>
        </div>
      </section>

      <section class="trust-strip reveal">
        <div>
          <h2>{{ $t('home.trustTitle') }}</h2>
          <p>{{ $t('home.trustCopy') }}</p>
        </div>
        <div class="logo-row" aria-hidden="true">
          <span v-for="logo in trustLogos" :key="logo">{{ logo }}</span>
        </div>
      </section>

      <section class="repeat-cta reveal">
        <h2>{{ $t('home.repeatHeading') }}</h2>
        <router-link to="/campaigns" class="btn-hero btn-primary">
          <span>{{ $t('home.repeatCta') }}</span>
          <span class="btn-arrow">→</span>
        </router-link>
      </section>

      <section class="legacy-console reveal">
        <div class="legacy-heading">
          <span>{{ $t('home.legacyEyebrow') }}</span>
          <h2>{{ $t('home.legacyTitle') }}</h2>
          <p>{{ $t('home.legacyDesc') }}</p>
        </div>

        <div class="console-grid">
          <aside class="console-guide">
            <div class="status-header">
              <span class="status-dot"></span>
              <span>{{ $t('home.systemStatus') }}</span>
            </div>
            <div class="engine-card">
              <strong>{{ $t('home.ready') }}</strong>
              <p>{{ $t('home.readyDesc') }}</p>
            </div>
            <div class="mini-metrics">
              <div>
                <strong>{{ $t('home.metricProviders') }}</strong>
                <span>{{ $t('home.metricProvidersLabel') }}</span>
              </div>
              <div>
                <strong>{{ $t('home.metricLanguages') }}</strong>
                <span>{{ $t('home.metricLanguagesLabel') }}</span>
              </div>
            </div>
          </aside>

          <div class="console-panel">
            <div class="console-header">
              <span>01 / {{ $t('home.consoleRealitySeeds') }}</span>
              <small>{{ $t('home.consoleSupported') }}</small>
            </div>
            <div class="drop-zone" :class="{ 'is-dragging': isDragOver }" @dragover.prevent="handleDragOver" @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop" @click="triggerFileInput">
              <input ref="fileInput" type="file" multiple accept=".pdf,.md,.txt" hidden :disabled="loading" @change="handleFileSelect" />
              <div v-if="files.length === 0" class="upload-placeholder">
                <div class="upload-icon">+</div>
                <h3>{{ $t('home.uploadTitle') }}</h3>
                <p>{{ $t('home.uploadHint') }}</p>
              </div>
              <div v-else class="file-inventory">
                <div v-for="(file, index) in files" :key="file.name + index" class="file-chip">
                  <span>{{ file.name }}</span>
                  <button type="button" class="remove-file" @click.stop="removeFile(index)" :aria-label="$t('home.removeFile')">×</button>
                </div>
              </div>
            </div>

            <div class="console-header border-top">
              <span>02 / {{ $t('home.consoleSimPrompt') }}</span>
            </div>
            <textarea v-model="formData.simulationRequirement" class="terminal-textarea" :placeholder="$t('home.simPromptPlaceholder')" rows="7" :disabled="loading"></textarea>
            <button class="start-btn" type="button" :disabled="!canSubmit || loading" @click="startSimulation">
              <span>{{ loading ? $t('home.initializing') : $t('home.startEngine') }}</span>
              <span>→</span>
            </button>
          </div>
        </div>

        <HistoryDatabase />
      </section>
    </main>

    <footer class="home-footer">
      <span>{{ $t('home.footerVersion') }}</span>
      <a href="https://github.com/chawit1103/3c-simulator" target="_blank" rel="noreferrer">{{ $t('home.footerGithub') }}</a>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const { locale, t } = useI18n()
const router = useRouter()

const savedLanguage = localStorage.getItem('3c-lang')
const currentLanguage = ref(savedLanguage || locale.value || 'en')

const changeLanguage = () => {
  locale.value = currentLanguage.value
  localStorage.setItem('3c-lang', currentLanguage.value)
}

const statValues = [
  { key: 'models', value: 17, labelKey: 'home.statModels' },
  { key: 'languages', value: 11, labelKey: 'home.statLanguages' },
  { key: 'industries', value: 4, labelKey: 'home.statIndustries' },
  { key: 'archetypes', value: 25, labelKey: 'home.statArchetypes' }
]

const statsStarted = ref(false)
const animatedCounts = ref({ models: 0, languages: 0, industries: 0, archetypes: 0 })
const statsSection = ref(null)

const stats = computed(() => statValues.map((stat) => ({
  ...stat,
  display: animatedCounts.value[stat.key],
  label: t(stat.labelKey)
})))

const flowSteps = computed(() => [
  { no: '01', kind: 'template', title: t('home.flow1Title'), desc: t('home.flow1Desc') },
  { no: '02', kind: 'compare', title: t('home.flow2Title'), desc: t('home.flow2Desc') },
  { no: '03', kind: 'impact', title: t('home.flow3Title'), desc: t('home.flow3Desc') },
  { no: '04', kind: 'war', title: t('home.flow4Title'), desc: t('home.flow4Desc') },
  { no: '05', kind: 'export', title: t('home.flow5Title'), desc: t('home.flow5Desc') }
])

const features = computed(() => [
  { kind: 'template', title: t('home.featureIndustryTitle'), desc: t('home.featureIndustryDesc'), to: '/campaigns' },
  { kind: 'compare', title: t('home.featureComparatorTitle'), desc: t('home.featureComparatorDesc'), to: '/comparator' },
  { kind: 'impact', title: t('home.featureImpactTitle'), desc: t('home.featureImpactDesc'), to: '/impact' },
  { kind: 'war', title: t('home.featureWarRoomTitle'), desc: t('home.featureWarRoomDesc'), to: '/war-room' },
  { kind: 'export', title: t('home.featureExportTitle'), desc: t('home.featureExportDesc'), to: '/campaigns' },
  { kind: 'language', title: t('home.featureLanguageTitle'), desc: t('home.featureLanguageDesc'), to: '/settings' }
])

const trustLogos = ['NOVA', 'ATLAS', 'ORBIT', 'SUMMIT', 'KAI']

const previewRows = computed(() => [
  { segment: t('home.previewSegment1'), value: '82', width: '82%' },
  { segment: t('home.previewSegment2'), value: '68', width: '68%' },
  { segment: t('home.previewSegment3'), value: '41', width: '41%' }
])

let statsObserver
let revealObserver

const animateStats = () => {
  if (statsStarted.value) return
  statsStarted.value = true
  const duration = 900
  const start = performance.now()

  const tick = (now) => {
    const progress = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    const next = {}
    statValues.forEach((stat) => {
      next[stat.key] = Math.round(stat.value * eased)
    })
    animatedCounts.value = next
    if (progress < 1) requestAnimationFrame(tick)
  }

  requestAnimationFrame(tick)
}

onMounted(() => {
  locale.value = currentLanguage.value

  statsObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) animateStats()
    })
  }, { threshold: 0.4 })

  if (statsSection.value) statsObserver.observe(statsSection.value)

  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('is-visible')
    })
  }, { threshold: 0.12 })

  document.querySelectorAll('.reveal').forEach((el) => revealObserver.observe(el))
})

onUnmounted(() => {
  statsObserver?.disconnect()
  revealObserver?.disconnect()
})

const formData = ref({ simulationRequirement: '' })
const files = ref([])
const loading = ref(false)
const isDragOver = ref(false)
const fileInput = ref(null)

const canSubmit = computed(() => formData.value.simulationRequirement.trim() !== '' && files.value.length > 0)

const triggerFileInput = () => {
  if (!loading.value) fileInput.value?.click()
}

const handleFileSelect = (event) => {
  addFiles(Array.from(event.target.files || []))
  event.target.value = ''
}

const handleDragOver = () => {
  isDragOver.value = true
}

const handleDragLeave = () => {
  isDragOver.value = false
}

const handleDrop = (event) => {
  isDragOver.value = false
  addFiles(Array.from(event.dataTransfer.files || []))
}

const addFiles = (newFiles) => {
  const allowed = ['.pdf', '.md', '.txt']
  const valid = newFiles.filter((file) => allowed.some((ext) => file.name.toLowerCase().endsWith(ext)))
  files.value = [...files.value, ...valid]
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    router.push({ name: 'Process', params: { projectId: 'new' } })
  })
}
</script>

<style scoped>
.home-page {
  --home-bg: #08090a;
  --home-surface: rgba(255, 255, 255, 0.045);
  --home-surface-strong: rgba(255, 255, 255, 0.075);
  --home-border: rgba(255, 255, 255, 0.11);
  --home-border-strong: rgba(255, 255, 255, 0.2);
  --home-text: rgba(255, 255, 255, 0.96);
  --home-muted: rgba(255, 255, 255, 0.62);
  --home-faint: rgba(255, 255, 255, 0.38);
  --home-accent: #FF4500;
  min-height: 100vh;
  color: var(--home-text);
  background:
    radial-gradient(circle at 50% -10%, rgba(255, 255, 255, 0.08), transparent 34rem),
    linear-gradient(180deg, rgba(255, 255, 255, 0.025), transparent 24rem),
    var(--home-bg);
}

:global([data-theme="light"] .home-page) {
  --home-bg: #f7f8fb;
  --home-surface: rgba(255, 255, 255, 0.78);
  --home-surface-strong: rgba(255, 255, 255, 0.92);
  --home-border: rgba(12, 18, 28, 0.1);
  --home-border-strong: rgba(12, 18, 28, 0.18);
  --home-text: rgba(12, 18, 28, 0.94);
  --home-muted: rgba(12, 18, 28, 0.62);
  --home-faint: rgba(12, 18, 28, 0.42);
  background:
    radial-gradient(circle at 18% 0%, rgba(255, 69, 0, 0.1), transparent 28rem),
    radial-gradient(circle at 82% 8%, rgba(38, 99, 235, 0.08), transparent 30rem),
    linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(247, 248, 251, 0.9) 42rem),
    var(--home-bg);
}

.home-page :where(h1, h2, h3, p) {
  margin: 0;
  color: inherit;
  font-family: var(--font-sans);
}

.home-page::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(var(--home-border) 1px, transparent 1px),
    linear-gradient(90deg, var(--home-border) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.42), transparent 52%);
  opacity: 0.28;
}

.home-nav {
  position: sticky;
  top: 0;
  z-index: 20;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-width: 0;
  padding: 0 clamp(20px, 4vw, 48px);
  background: color-mix(in srgb, var(--home-bg) 88%, transparent);
  border-bottom: 1px solid var(--home-border);
  backdrop-filter: blur(18px);
}

:global([data-theme="light"] .home-nav) {
  box-shadow: 0 10px 34px rgba(12, 18, 28, 0.06);
}

.nav-brand,
.language-select,
.section-heading span,
.flow-number,
.try-link,
.status-header,
.console-header,
.home-footer {
  font-family: var(--font-mono);
  letter-spacing: 0;
  text-transform: uppercase;
}

.nav-brand {
  flex: 0 0 auto;
  color: var(--home-muted);
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  line-height: 1;
  white-space: nowrap;
}

.nav-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: clamp(10px, 1.8vw, 18px);
  min-width: 0;
  flex: 0 1 auto;
  flex-wrap: nowrap;
}

.nav-link {
  flex: 0 0 auto;
  color: var(--home-muted);
  font-size: 13px;
  font-weight: 500;
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  transition: color 170ms ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--home-text);
}

.language-select {
  flex: 0 0 auto;
  width: 92px;
  color: var(--home-muted);
  background: var(--home-surface);
  border: 1px solid var(--home-border);
  border-radius: 6px;
  padding: 6px 26px 6px 10px;
  font-size: 11px;
  line-height: 1;
  outline: none;
  white-space: nowrap;
}

.hero-section {
  padding: clamp(110px, 14vw, 156px) 24px 96px;
}

.hero-inner,
.section-block,
.trust-strip,
.repeat-cta,
.legacy-console {
  width: min(1200px, calc(100% - 40px));
  margin: 0 auto;
}

.hero-inner {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(340px, 0.72fr);
  gap: clamp(48px, 6vw, 84px);
  align-items: center;
}

.hero-copy-stack {
  min-width: 0;
}

.hero-badge {
  display: inline-flex;
  margin-bottom: 28px;
  padding: 8px 12px;
  border: 1px solid var(--home-border);
  border-radius: 999px;
  color: var(--home-muted);
  background: rgba(255, 255, 255, 0.035);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

.hero-title {
  max-width: 1040px;
  font-size: clamp(50px, 7vw, 82px);
  font-weight: 650;
  line-height: 0.95;
  letter-spacing: -0.04em;
}

.hero-title span {
  display: block;
}

.hero-shift {
  transform: translateX(clamp(16px, 4vw, 52px));
}

.hero-shift-large {
  transform: translateX(clamp(30px, 8vw, 104px));
}

.hero-copy {
  max-width: 660px;
  margin-top: 30px;
  color: var(--home-muted);
  font-size: clamp(18px, 2vw, 20px);
  line-height: 1.55;
}

.hero-proof {
  position: relative;
  min-height: 520px;
  padding: 18px;
  border: 1px solid var(--home-border);
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.105), rgba(255, 255, 255, 0.035)),
    rgba(255, 255, 255, 0.035);
  box-shadow: 0 34px 110px rgba(0, 0, 0, 0.42), inset 0 1px rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

.hero-proof::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent),
    radial-gradient(circle at 80% 16%, rgba(255, 69, 0, 0.12), transparent 14rem);
  pointer-events: none;
}

:global([data-theme="light"] .hero-proof) {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.76)),
    rgba(255, 255, 255, 0.8);
  box-shadow: 0 26px 86px rgba(12, 18, 28, 0.13), inset 0 1px rgba(255, 255, 255, 0.9);
}

.proof-chrome {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 7px;
  margin-bottom: 16px;
}

.proof-chrome span {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--home-border-strong);
}

.proof-command {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  padding: 0 12px;
  border: 1px solid var(--home-border);
  border-radius: 8px;
  color: var(--home-muted);
  background: rgba(255, 255, 255, 0.045);
  font-size: 13px;
}

.command-prefix {
  color: var(--home-accent);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
}

.proof-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 14px;
}

.proof-score,
.proof-section {
  border: 1px solid var(--home-border);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.045);
}

.proof-score {
  padding: 16px;
}

.proof-score span,
.proof-header span {
  display: block;
  color: var(--home-faint);
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}

.proof-score strong {
  display: block;
  margin-top: 18px;
  color: var(--home-text);
  font-size: 25px;
  line-height: 1;
  letter-spacing: -0.03em;
}

.proof-score small {
  display: block;
  margin-top: 8px;
  color: var(--home-accent);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
}

.proof-score.muted small {
  color: var(--home-muted);
}

.proof-section {
  position: relative;
  z-index: 1;
  margin-top: 10px;
  padding: 16px;
}

.proof-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.proof-header strong {
  color: var(--home-text);
  font-size: 18px;
}

.sentiment-bars {
  display: grid;
  grid-template-columns: 74fr 18fr 8fr;
  gap: 6px;
}

.sentiment-bars span {
  height: 64px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.08);
}

.bar-positive {
  background: linear-gradient(180deg, rgba(85, 214, 143, 0.9), rgba(85, 214, 143, 0.28)) !important;
}

.bar-neutral {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0.08)) !important;
}

.bar-negative {
  background: linear-gradient(180deg, rgba(255, 69, 0, 0.78), rgba(255, 69, 0, 0.18)) !important;
}

.persona-table {
  display: grid;
  gap: 10px;
}

.persona-row {
  display: grid;
  grid-template-columns: 118px minmax(0, 1fr) 34px;
  gap: 10px;
  align-items: center;
  color: var(--home-muted);
  font-size: 12px;
}

.persona-row strong {
  color: var(--home-text);
  font-family: var(--font-mono);
  font-size: 11px;
  text-align: right;
}

.mini-meter {
  height: 6px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
}

.mini-meter i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--home-accent);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 34px;
}

.btn-hero {
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 18px;
  border-radius: 7px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease, color 180ms ease;
}

.btn-hero:hover {
  transform: translateY(-2px);
}

.btn-hero:active {
  transform: translateY(0) scale(0.98);
}

.btn-primary {
  color: rgba(255, 250, 247, 0.98);
  background: var(--home-accent);
  border: 1px solid var(--home-accent);
  box-shadow: 0 18px 40px rgba(255, 69, 0, 0.24);
}

.btn-primary:hover {
  border-color: rgba(255, 255, 255, 0.8);
}

.btn-secondary {
  color: var(--home-text);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--home-border);
}

.btn-secondary:hover {
  border-color: var(--home-accent);
  color: var(--home-accent);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  max-width: 760px;
  margin-top: 58px;
  border-top: 1px solid var(--home-border);
  border-bottom: 1px solid var(--home-border);
}

.stat-item {
  padding: 20px 24px;
  border-right: 1px solid var(--home-border);
}

.stat-item:last-child {
  border-right: 0;
}

.stat-item strong {
  display: block;
  font-size: 28px;
  line-height: 1;
}

.stat-item span {
  display: block;
  margin-top: 8px;
  color: var(--home-faint);
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
}

.section-block {
  padding: 88px 0;
}

.section-heading {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 40px;
  align-items: end;
  margin-bottom: 32px;
}

.section-heading.wide {
  grid-template-columns: 260px minmax(0, 1fr);
}

.section-heading span {
  color: var(--home-faint);
  font-size: 11px;
  font-weight: 700;
}

.section-heading h2 {
  max-width: 760px;
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 640;
  line-height: 1;
  letter-spacing: -0.035em;
}

.flow-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}

.flow-card,
.feature-card,
.console-panel,
.console-guide {
  position: relative;
  border: 1px solid var(--home-border);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.075), rgba(255, 255, 255, 0.03)),
    var(--home-surface);
  box-shadow: 0 20px 70px rgba(0, 0, 0, 0.34), inset 0 1px rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(18px);
  transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}

:global([data-theme="light"] .flow-card),
:global([data-theme="light"] .feature-card),
:global([data-theme="light"] .console-panel),
:global([data-theme="light"] .console-guide) {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.74)),
    var(--home-surface);
  box-shadow: 0 18px 58px rgba(12, 18, 28, 0.09), inset 0 1px rgba(255, 255, 255, 0.9);
}

.flow-card {
  min-height: 210px;
  padding: 18px;
  border-radius: 8px;
}

.flow-card::after {
  content: '';
  position: absolute;
  top: 34px;
  right: -12px;
  width: 12px;
  height: 1px;
  background: var(--home-border-strong);
}

.flow-card:last-child::after {
  display: none;
}

.flow-card:hover,
.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 69, 0, 0.72);
  box-shadow: 0 28px 90px rgba(0, 0, 0, 0.46), 0 0 34px rgba(255, 69, 0, 0.09);
}

:global([data-theme="light"] .flow-card:hover),
:global([data-theme="light"] .feature-card:hover) {
  box-shadow: 0 24px 72px rgba(12, 18, 28, 0.14), 0 0 34px rgba(255, 69, 0, 0.12);
}

.flow-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 42px;
}

.flow-number {
  color: var(--home-faint);
  font-size: 11px;
  font-weight: 700;
}

.icon-shell {
  display: inline-grid;
  place-items: center;
  border: 1px solid var(--home-border);
  border-radius: 8px;
  color: var(--home-text);
  background: rgba(255, 255, 255, 0.045);
}

.icon-shell svg {
  width: 22px;
  height: 22px;
}

.icon-shell path {
  fill: none;
  stroke: currentColor;
  stroke-width: 1.65;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.flow-icon {
  width: 42px;
  height: 42px;
}

.flow-card h3,
.feature-card h3 {
  margin-bottom: 10px;
  font-size: 20px;
  font-weight: 650;
  letter-spacing: -0.01em;
}

.flow-card p,
.feature-card p,
.trust-strip p,
.legacy-heading p,
.engine-card p {
  color: var(--home-muted);
  font-size: 15px;
  line-height: 1.55;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.feature-card {
  min-height: 252px;
  display: flex;
  flex-direction: column;
  padding: 24px;
  border-radius: 8px;
  color: var(--home-text);
  text-decoration: none;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  inset: auto 18px -46px 18px;
  height: 86px;
  border-radius: 999px;
  background: rgba(255, 69, 0, 0.12);
  filter: blur(28px);
  opacity: 0;
  transition: opacity 180ms ease;
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 52px;
  height: 52px;
  margin-bottom: 40px;
  color: var(--home-accent);
}

.feature-icon svg {
  width: 25px;
  height: 25px;
}

.feature-card p {
  flex: 1;
}

.try-link {
  margin-top: 18px;
  color: var(--home-accent);
  font-size: 11px;
  font-weight: 800;
}

.trust-strip {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 520px);
  gap: 32px;
  align-items: center;
  margin-top: 56px;
  padding: 32px;
  border-top: 1px solid var(--home-border);
  border-bottom: 1px solid var(--home-border);
  background: rgba(255, 255, 255, 0.025);
}

.trust-strip h2,
.repeat-cta h2,
.legacy-heading h2 {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 640;
  letter-spacing: -0.03em;
}

.trust-strip p {
  margin-top: 12px;
}

.logo-row {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
}

.logo-row span {
  display: grid;
  min-height: 54px;
  place-items: center;
  border: 1px solid var(--home-border);
  color: var(--home-faint);
  filter: grayscale(1);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
  transition: color 170ms ease, border-color 170ms ease, filter 170ms ease;
}

.logo-row span:hover {
  color: var(--home-accent);
  border-color: rgba(255, 69, 0, 0.5);
  filter: grayscale(0);
}

.repeat-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 112px 0;
}

.legacy-console {
  padding: 80px 0 100px;
  border-top: 1px solid var(--home-border);
}

.legacy-heading {
  max-width: 720px;
  margin-bottom: 28px;
}

.legacy-heading span {
  display: block;
  margin-bottom: 14px;
  color: var(--home-faint);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
}

.legacy-heading p {
  margin-top: 14px;
}

.console-grid {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 18px;
  margin-bottom: 28px;
}

.console-guide,
.console-panel {
  border-radius: 8px;
}

.console-guide {
  padding: 20px;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--home-faint);
  font-size: 10px;
  font-weight: 800;
  margin-bottom: 24px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #55d68f;
  box-shadow: 0 0 0 5px rgba(85, 214, 143, 0.12);
}

.engine-card strong,
.mini-metrics strong {
  display: block;
  color: var(--home-text);
  font-size: 22px;
  line-height: 1;
}

.engine-card p {
  margin-top: 12px;
}

.mini-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  margin-top: 24px;
  overflow: hidden;
  border: 1px solid var(--home-border);
  border-radius: 8px;
  background: var(--home-border);
}

.mini-metrics div {
  padding: 16px;
  background: rgba(8, 9, 10, 0.7);
}

:global([data-theme="light"] .mini-metrics div) {
  background: rgba(255, 255, 255, 0.82);
}

.mini-metrics span {
  display: block;
  margin-top: 8px;
  color: var(--home-faint);
  font-family: var(--font-mono);
  font-size: 10px;
  text-transform: uppercase;
}

.console-panel {
  overflow: hidden;
}

.console-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 18px;
  color: var(--home-muted);
  font-size: 11px;
  font-weight: 800;
}

.console-header small {
  color: var(--home-faint);
  font-size: 11px;
}

.border-top {
  border-top: 1px solid var(--home-border);
}

.drop-zone {
  min-height: 178px;
  display: grid;
  place-items: center;
  margin: 0 18px 18px;
  border: 1px dashed var(--home-border-strong);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.035);
  cursor: pointer;
  transition: border-color 170ms ease, background 170ms ease;
}

.drop-zone:hover,
.drop-zone.is-dragging {
  border-color: var(--home-accent);
  background: rgba(255, 69, 0, 0.055);
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  margin: 0 auto 12px;
  border: 1px solid var(--home-border);
  border-radius: 8px;
  color: var(--home-accent);
  font-size: 28px;
}

.upload-placeholder h3 {
  font-size: 15px;
  font-weight: 700;
}

.upload-placeholder p {
  margin-top: 4px;
  color: var(--home-faint);
  font-size: 12px;
}

.file-inventory {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 18px;
}

.file-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 100%;
  padding: 7px 10px;
  border: 1px solid var(--home-border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: var(--home-text);
  font-family: var(--font-mono);
  font-size: 11px;
}

.file-chip span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-file {
  border: 0;
  background: transparent;
  color: var(--home-faint);
  cursor: pointer;
}

.remove-file:hover {
  color: var(--home-accent);
}

.terminal-textarea {
  width: calc(100% - 36px);
  margin: 0 18px 18px;
  padding: 16px;
  resize: vertical;
  border: 1px solid var(--home-border);
  border-radius: 8px;
  outline: none;
  color: var(--home-text);
  background: rgba(255, 255, 255, 0.035);
  font-size: 14px;
  line-height: 1.7;
}

.terminal-textarea:focus {
  border-color: rgba(255, 69, 0, 0.7);
}

.start-btn {
  width: calc(100% - 36px);
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 18px 18px;
  padding: 0 18px;
  border: 1px solid var(--home-accent);
  border-radius: 8px;
  color: rgba(255, 250, 247, 0.98);
  background: var(--home-accent);
  font-weight: 800;
  cursor: pointer;
  transition: transform 170ms ease, opacity 170ms ease, border-color 170ms ease;
}

.start-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.8);
}

.start-btn:disabled {
  cursor: not-allowed;
  opacity: 0.46;
}

.home-footer {
  min-height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 clamp(20px, 4vw, 48px);
  border-top: 1px solid var(--home-border);
  color: var(--home-faint);
  font-size: 11px;
}

.home-footer a {
  color: var(--home-muted);
  text-decoration: none;
  transition: color 170ms ease;
}

.home-footer a:hover {
  color: var(--home-accent);
}

.reveal {
  opacity: 0;
  transform: translateY(26px);
  transition: opacity 520ms ease, transform 520ms ease;
}

.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .reveal,
  .btn-hero,
  .flow-card,
  .feature-card,
  .start-btn {
    transition: none;
  }
}

@media (max-width: 1024px) {
  .hero-inner,
  .flow-grid,
  .feature-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hero-inner {
    grid-template-columns: 1fr;
  }

  .hero-proof {
    min-height: auto;
  }

  .flow-card::after {
    display: none;
  }

  .trust-strip,
  .console-grid,
  .section-heading,
  .section-heading.wide {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .home-nav {
    padding: 0 16px;
  }

  .nav-right {
    gap: 10px;
  }

  .nav-link {
    display: none;
  }

  .hero-section {
    padding: 92px 0 70px;
  }

  .hero-title {
    font-size: clamp(46px, 14vw, 64px);
  }

  .hero-shift,
  .hero-shift-large {
    transform: translateX(0);
  }

  .hero-actions,
  .repeat-cta {
    align-items: stretch;
    flex-direction: column;
  }

  .stats-row,
  .proof-grid,
  .flow-grid,
  .feature-grid,
  .logo-row {
    grid-template-columns: 1fr;
  }

  .persona-row {
    grid-template-columns: 1fr;
  }

  .persona-row strong {
    text-align: left;
  }

  .stat-item {
    border-right: 0;
    border-bottom: 1px solid var(--home-border);
  }

  .stat-item:last-child {
    border-bottom: 0;
  }

  .section-block {
    padding: 64px 0;
  }

  .trust-strip {
    padding: 28px 0;
  }
}
</style>
