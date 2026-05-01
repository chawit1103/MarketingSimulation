<template>
  <div class="import-section">
    <!-- Header -->
    <h2 class="section-title">{{ $t('industry.importTitle') }}</h2>
    <p class="section-desc">{{ $t('industry.importDesc') }}</p>

    <!-- Drop Zone -->
    <div
      :class="['drop-zone', { 'drop-active': isDragOver, 'drop-error': importError }]"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".json"
        @change="handleFileSelect"
        style="display: none"
        :disabled="importing"
      />

      <div v-if="!importing && !importSuccess" class="drop-content">
        <div class="drop-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 4v10m0 0 4-4m-4 4-4-4" />
            <path d="M5 17.5V20h14v-2.5" />
          </svg>
        </div>
        <div class="drop-text">{{ $t('industry.dropHere') }}</div>
        <div class="drop-hint">{{ $t('industry.dropHint') }}</div>
      </div>

      <div v-else-if="importing" class="drop-content">
        <div class="spinner"></div>
        <div class="drop-text">{{ $t('industry.importing') }}</div>
      </div>

      <div v-else class="drop-content success">
        <div class="success-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="m6 12.5 3.7 3.7L18.5 7" />
          </svg>
        </div>
        <div class="drop-text">{{ $t('industry.importSuccess') }}</div>
        <div class="imported-name">{{ importedName }}</div>
      </div>
    </div>

    <!-- Error message -->
    <div v-if="importError" class="import-error">
      <span class="error-icon">!</span>
      <span>{{ importError }}</span>
    </div>

    <!-- Currently imported templates -->
    <div v-if="uploadedTemplates.length > 0" class="uploaded-list">
      <h3 class="list-title">{{ $t('industry.yourTemplates') }} ({{ uploadedTemplates.length }})</h3>
      <div v-for="tmpl in uploadedTemplates" :key="tmpl.id" class="uploaded-item">
        <span class="uploaded-icon">{{ templateInitial(tmpl) }}</span>
        <span class="uploaded-name">{{ locale === 'th' ? tmpl.name_th : tmpl.name_en }}</span>
        <span class="uploaded-segments">{{ tmpl.persona_segment_count }} segments</span>
        <button class="delete-btn" @click="deleteTemplate(tmpl.id)" :disabled="deleting === tmpl.id">
          {{ deleting === tmpl.id ? '...' : '✕' }}
        </button>
      </div>
    </div>

    <!-- Template schema reference link -->
    <div class="schema-link">
      <a href="#" @click.prevent="$emit('show-schema')">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 4.5h9a3 3 0 0 1 3 3V20H8a3 3 0 0 0-3-3z" />
          <path d="M5 4.5V17" />
          <path d="M9 8h4M9 11h4" />
        </svg>
        <span>{{ $t('industry.viewSchema') }}</span>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import service from '@/api'

const { locale } = useI18n()
const emit = defineEmits(['template-imported', 'show-schema'])

const fileInput = ref(null)
const isDragOver = ref(false)
const importing = ref(false)
const importSuccess = ref(false)
const importError = ref('')
const importedName = ref('')
const deleting = ref(null)
const uploadedTemplates = ref([])

onMounted(loadUploadedTemplates)

async function loadUploadedTemplates() {
  try {
    const res = await service.get('/api/industry/templates')
    const all = res.templates || res || []
    uploadedTemplates.value = all.filter(t => t.source === 'upload')
  } catch (e) {
    // silently fail — templates from API aren't critical
  }
}

function triggerFileInput() {
  if (!importing.value) fileInput.value?.click()
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) processFile(file)
}

function handleDrop(event) {
  isDragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file) processFile(file)
}

function templateInitial(template) {
  const name = locale.value === 'th' ? template.name_th : template.name_en
  return (name || template.id || 'T').trim().charAt(0).toUpperCase()
}

async function processFile(file) {
  importError.value = ''
  importSuccess.value = false

  if (!file.name.toLowerCase().endsWith('.json')) {
    importError.value = 'กรุณาอัปโหลดไฟล์ .json เท่านั้น / Please upload a .json file'
    return
  }

  importing.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)

    const res = await service.post('/api/industry/templates/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    if (res.success || res.template_id) {
      importSuccess.value = true
      importedName.value = res.metadata?.name_th || file.name.replace('.json', '')
      emit('template-imported', res.metadata || {})
      await loadUploadedTemplates()
    } else {
      importError.value = res.error || 'Import failed'
    }
  } catch (e) {
    const msg = e.response?.data?.error || e.message || 'Import failed'
    importError.value = msg
  } finally {
    importing.value = false
  }
}

async function deleteTemplate(id) {
  const name = uploadedTemplates.value.find(t => t.id === id)?.name_th || id
  if (!confirm(`ลบ template "${name}"? / Delete "${name}"?`)) return

  deleting.value = id
  try {
    await service.delete(`/api/industry/templates/${id}`)
    uploadedTemplates.value = uploadedTemplates.value.filter(t => t.id !== id)
  } catch (e) {
    const msg = e.response?.data?.error || 'Delete failed'
    importError.value = msg
  } finally {
    deleting.value = null
  }

  // Reset success to re-show drop zone
  importSuccess.value = false
  importedName.value = ''
}
</script>

<style scoped>
.import-section { margin-bottom: 36px; padding-bottom: 36px; border-bottom: 1px solid var(--border-subtle); }
.section-title { font-size: var(--text-lg); font-weight: 700; margin-bottom: 8px; color: var(--text-primary); }
.section-desc { color: var(--text-secondary); font-size: var(--text-sm); margin-bottom: 20px; }

.drop-zone {
  border: 1px dashed var(--border-strong); border-radius: var(--radius-lg);
  padding: 40px 20px; text-align: center;
  cursor: pointer; transition: all 0.2s;
  background: var(--bg-surface);
  box-shadow: var(--shadow-sm);
}
.drop-zone:hover, .drop-zone.drop-active {
  border-color: var(--accent);
  background: var(--accent-subtle);
  box-shadow: var(--shadow-card);
}
.drop-zone.drop-error { border-color: var(--red); background: var(--red-soft); }

.drop-icon,
.success-icon {
  width: 42px;
  height: 42px;
  margin: 0 auto 12px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  color: var(--accent);
  background: var(--accent-subtle);
}

.drop-icon svg,
.success-icon svg,
.schema-link svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.drop-text { font-weight: 700; font-size: var(--text-sm); margin-bottom: 4px; color: var(--text-primary); }
.drop-hint { font-size: var(--text-xs); color: var(--text-tertiary); }

.spinner {
  width: 28px; height: 28px; border: 3px solid var(--border-default);
  border-top-color: var(--accent); border-radius: 50%;
  animation: spin 0.7s linear infinite; margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }

.success-icon { color: var(--green); background: var(--green-soft); }
.imported-name { font-size: var(--text-sm); color: var(--accent); font-weight: 700; margin-top: 4px; }

.import-error {
  margin-top: 12px; padding: 10px 14px; background: var(--red-soft);
  border: 1px solid color-mix(in srgb, var(--red) 36%, transparent); border-radius: var(--radius-md);
  color: var(--red); font-size: var(--text-sm); display: flex; gap: 8px; align-items: flex-start;
}
.error-icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  display: inline-grid;
  place-items: center;
  border-radius: 50%;
  border: 1px solid currentColor;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 800;
}

.uploaded-list { margin-top: 24px; }
.list-title { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0; margin-bottom: 12px; }

.uploaded-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; border: 1px solid var(--border-default); border-radius: var(--radius-md);
  margin-bottom: 6px; font-size: var(--text-sm); background: var(--bg-surface);
}
.uploaded-icon {
  width: 28px;
  height: 28px;
  display: inline-grid;
  place-items: center;
  border-radius: var(--radius-md);
  background: var(--accent-subtle);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
}
.uploaded-name { flex: 1; font-weight: 700; color: var(--text-primary); }
.uploaded-segments { font-size: var(--text-xs); color: var(--text-tertiary); font-family: var(--font-mono); }
.delete-btn {
  background: transparent; border: none; color: var(--text-quaternary);
  cursor: pointer; font-size: 1rem; padding: 2px 6px;
}
.delete-btn:hover { color: var(--red); }
.delete-btn:disabled { color: var(--text-quaternary); cursor: not-allowed; }

.schema-link { margin-top: 16px; font-size: 0.85rem; }
.schema-link a {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--accent);
  text-decoration: none;
  font-weight: 700;
}
.schema-link svg {
  width: 16px;
  height: 16px;
}
.schema-link a:hover { text-decoration: underline; }
</style>
