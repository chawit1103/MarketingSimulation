<template>
  <div class="export-wrapper">
    <button
      :class="['btn-export', { exporting: isExporting }]"
      @click="toggleMenu"
      :disabled="isExporting"
      :title="title"
    >
      <span v-if="!isExporting" class="export-label">
        <svg class="export-glyph" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M12 3v11m0 0 4-4m-4 4-4-4" />
          <path d="M5 17v2h14v-2" />
        </svg>
        <span>{{ label }}</span>
      </span>
      <span v-else class="export-label">
        <span class="export-spinner"></span>
        <span>{{ $t('common.exporting') }}</span>
      </span>
    </button>

    <div v-if="showMenu" class="export-menu" @click.stop>
      <button class="export-option" @click="download('pptx')">
        <span class="option-code">PPT</span>
        <span>{{ $t('common.exportPowerPoint') }}</span>
      </button>
      <button class="export-option" @click="download('csv')">
        <span class="option-code">CSV</span>
        <span>{{ $t('common.exportCsv') }}</span>
      </button>
      <button class="export-option" @click="downloadClientSide">
        <span class="option-code">DL</span>
        <span>{{ $t('common.quickDownload') }}</span>
      </button>
      <button class="export-option cancel" @click="showMenu = false">
        ✕ {{ $t('common.cancel') }}
      </button>
    </div>

    <div v-if="showMenu" class="export-backdrop" @click="showMenu = false"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: { type: String, default: 'Export' },
  title: { type: String, default: 'Export Report' },
  data: { type: Object, required: true },
  filename: { type: String, default: 'msaas_report' },
})

const showMenu = ref(false)
const isExporting = ref(false)

function toggleMenu() {
  showMenu.value = !showMenu.value
}

async function download(format) {
  isExporting.value = true
  showMenu.value = false

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 8000)

    const endpoint = format === 'pptx' ? '/api/export/pptx' : '/api/export/csv'

    const res = await fetch(endpoint, {
      method: 'POST',
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...props.data, filename: props.filename }),
    })
    clearTimeout(timeout)

    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.filename}.${format}`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    downloadClientSide()
  } finally {
    isExporting.value = false
  }
}

function downloadClientSide() {
  showMenu.value = false

  const rows = []
  rows.push([`MSaaS Report: ${props.data.title || 'Untitled'}`])
  rows.push([`Generated: ${new Date().toISOString()}`])
  rows.push([])

  const kpis = props.data.kpis || {}
  rows.push(['KPI', 'Value'])
  for (const [k, v] of Object.entries(kpis)) {
    rows.push([k, String(v)])
  }

  const timeline = props.data.timeline || []
  if (timeline.length) {
    rows.push([])
    rows.push(['Round', 'Sentiment', 'Actions'])
    for (const pt of timeline) {
      rows.push([String(pt.round_num || ''), String(pt.avg_sentiment || ''), String(pt.action_count || '')])
    }
  }

  const actionPlan = props.data.action_plan
  if (actionPlan?.sections) {
    rows.push([])
    rows.push(['Action Plan Source', actionPlan.source?.type || 'unknown'])
    rows.push(['Action Plan Disclaimer', actionPlan.disclaimer || ''])
    rows.push([])
    rows.push(['Section', 'Recommendation', 'Reason', 'Expected Impact', 'Risk'])
    for (const [sectionKey, section] of Object.entries(actionPlan.sections)) {
      for (const item of section.items || []) {
        rows.push([
          section.title || sectionKey,
          item.recommendation || '',
          item.reason || '',
          item.expected_impact || '',
          item.risk || '',
        ])
      }
    }
  }

  const csv = rows.map(r => r.map(c => `"${c}"`).join(',')).join('\n')
  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${props.filename}.csv`
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.export-wrapper { position: relative; display: inline-block; }

.btn-export {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 38px;
  padding: 9px 15px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  background: var(--bg-surface);
  color: var(--text-primary);
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0;
  box-shadow: var(--shadow-sm);
  transition: border-color var(--transition-fast), background var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast);
}
.btn-export:hover {
  border-color: var(--border-accent);
  background: var(--accent-subtle);
  color: var(--accent);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.btn-export.exporting { opacity: 0.6; cursor: not-allowed; }

.export-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.export-glyph {
  width: 15px;
  height: 15px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.export-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--border-default);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.export-backdrop { position: fixed; inset: 0; z-index: 99; }

.export-menu {
  position: absolute; top: 100%; right: 0; margin-top: 8px; z-index: 100;
  background: var(--bg-panel); border: 1px solid var(--border-default); border-radius: var(--radius-lg);
  box-shadow: var(--shadow-elevated); padding: 6px; min-width: 252px;
}

.export-option {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  text-align: left;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast), color var(--transition-fast);
}
.export-option:hover { background: var(--accent-subtle); color: var(--text-primary); }
.export-option.cancel { color: var(--text-tertiary); font-size: var(--text-xs); margin-top: 4px; border-top: 1px solid var(--border-subtle); border-radius: 0 0 var(--radius-md) var(--radius-md); }

.option-code {
  width: 34px;
  display: inline-flex;
  justify-content: center;
  padding: 2px 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--accent);
  background: var(--accent-subtle);
  font-family: var(--font-mono);
  font-size: 0.64rem;
  font-weight: 700;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
