<template>
  <div class="app-wrapper">
    <!-- Global Controls: Language & Theme -->
    <div class="global-controls glass">
      <div class="control-group">
        <select v-model="currentLanguage" @change="changeLanguage" class="minimal-select">
          <option value="en">EN</option>
          <option value="zh-CN">中文</option>
          <option value="th">TH</option>
          <option value="es">ES</option>
          <option value="fr">FR</option>
          <option value="ar">AR</option>
          <option value="pt">PT</option>
          <option value="ru">RU</option>
          <option value="hi">HI</option>
          <option value="bn">BN</option>
          <option value="ur">UR</option>
        </select>
      </div>
      <div class="control-divider"></div>
      <select
        v-model="themeMode"
        @change="changeTheme"
        class="minimal-select theme-select"
        :title="$t('common.theme')"
        :aria-label="$t('common.theme')"
      >
        <option value="system">{{ $t('common.themeSystem') }}</option>
        <option value="dark">{{ $t('common.themeDark') }}</option>
        <option value="light">{{ $t('common.themeLight') }}</option>
      </select>
    </div>

    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <FeedbackWidget />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import FeedbackWidget from '@/components/FeedbackWidget.vue'

const { locale } = useI18n()

// Language Logic
const savedLang = localStorage.getItem('3c-lang')
const currentLanguage = ref(savedLang || 'en')
if (savedLang) {
  locale.value = savedLang
}

function changeLanguage() {
  locale.value = currentLanguage.value
  localStorage.setItem('3c-lang', currentLanguage.value)
}

watch(locale, (newVal) => {
  if (currentLanguage.value !== newVal) {
    currentLanguage.value = newVal
  }
})

// Theme Logic
const savedTheme = localStorage.getItem('3c-theme')
const themeMode = ref(['light', 'dark', 'system'].includes(savedTheme) ? savedTheme : 'system')
const systemDarkQuery = window.matchMedia('(prefers-color-scheme: dark)')

function resolveTheme(mode) {
  if (mode === 'system') {
    return systemDarkQuery.matches ? 'dark' : 'light'
  }
  return mode
}

function applyTheme(mode) {
  const resolvedTheme = resolveTheme(mode)
  document.documentElement.setAttribute('data-theme', resolvedTheme)
  document.documentElement.setAttribute('data-theme-mode', mode)
  localStorage.setItem('3c-theme', mode)
}

function changeTheme() {
  applyTheme(themeMode.value)
}

function handleSystemThemeChange() {
  if (themeMode.value === 'system') {
    applyTheme('system')
  }
}

onMounted(() => {
  applyTheme(themeMode.value)
  systemDarkQuery.addEventListener('change', handleSystemThemeChange)
})

onUnmounted(() => {
  systemDarkQuery.removeEventListener('change', handleSystemThemeChange)
})
</script>

<style>
@import './assets/design-system.css';

.app-wrapper {
  min-height: 100vh;
}

/* Global Controls Floating Pill */
.global-controls {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: var(--radius-pill);
}

.control-divider {
  width: 1px;
  height: 12px;
  background: var(--border-subtle);
}

.minimal-select {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  padding: 4px 8px;
  width: auto;
  appearance: none;
  text-align: center;
  transition: color var(--transition-fast);
}
.minimal-select:hover {
  color: var(--text-primary);
}
.minimal-select:focus {
  box-shadow: none;
}

.theme-select {
  min-width: 70px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
  padding: 5px 10px;
  text-transform: uppercase;
}
.theme-select:hover {
  background: var(--accent-subtle);
  border-color: var(--border-accent);
}

.app-wrapper:has(.modal-overlay) .global-controls {
  opacity: 0;
  pointer-events: none;
}

/* Common Page Layouts (Used by router-view) */
.page-container {
  min-height: 100vh;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Global Utility Overrides for Premium feel */
.section-title {
  color: var(--text-primary);
  font-size: var(--text-base);
  font-weight: 600;
  margin-bottom: var(--space-2);
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border-default);
  border-top-color: var(--text-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: var(--space-20) var(--space-6);
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.page-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-12);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-subtle);
}

@media (max-width: 640px) {
  .global-controls {
    right: 14px;
    bottom: 14px;
  }
}
</style>
