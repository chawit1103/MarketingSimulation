<template>
  <div :class="['source-badge-wrap', toneClass]">
    <span class="source-badge">{{ label }}</span>
    <p v-if="warning" class="source-warning">{{ warning }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  source: {
    type: String,
    default: 'unknown',
  },
  warning: {
    type: String,
    default: '',
  },
})

const { t } = useI18n()

const sourceMap = {
  demo_mode: { key: 'resultSource.demoMode', tone: 'demo' },
  local_estimate: { key: 'resultSource.localEstimate', tone: 'warning' },
  live_backend: { key: 'resultSource.liveBackend', tone: 'live' },
  backend_verified: { key: 'resultSource.backendVerified', tone: 'verified' },
  unknown: { key: 'resultSource.unknownSource', tone: 'unknown' },
}

const resolved = computed(() => sourceMap[props.source] || sourceMap.unknown)
const label = computed(() => t(resolved.value.key))
const toneClass = computed(() => `source-${resolved.value.tone}`)
</script>

<style scoped>
.source-badge-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
  margin: var(--space-4) 0;
}

.source-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  background: var(--bg-panel);
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.source-warning {
  flex: 1;
  min-width: min(100%, 280px);
  margin: 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.source-demo .source-badge {
  border-color: var(--border-accent);
  background: var(--accent-subtle);
  color: var(--accent);
}

.source-warning .source-badge {
  border-color: var(--yellow);
  color: var(--yellow);
}

.source-live .source-badge,
.source-verified .source-badge {
  border-color: var(--green);
  color: var(--green);
}

.source-unknown .source-badge {
  color: var(--text-tertiary);
}
</style>
