<template>
  <div class="template-selector">
    <div v-if="!selectedTemplate && !loading">
      <!-- Step 1: Choose Industry Template -->
      <div class="template-header">
        <h3 class="template-title">{{ $t('industry.chooseTemplate') }}</h3>
        <p class="template-subtitle">{{ $t('industry.chooseTemplateDesc') }}</p>
      </div>

      <div class="template-grid">
        <div
          v-for="tmpl in templates"
          :key="tmpl.id"
          :class="['template-card', { selected: hoveredTemplate === tmpl.id }]"
          @click="selectTemplate(tmpl.id)"
          @mouseenter="hoveredTemplate = tmpl.id"
          @mouseleave="hoveredTemplate = null"
        >
          <div class="template-icon">
            {{ templateInitial(tmpl) }}
          </div>
          <div class="template-info">
            <h4 class="template-name">{{ locale === 'th' ? tmpl.name_th : tmpl.name_en }}</h4>
            <p class="template-desc">{{ locale === 'th' ? tmpl.description_th : tmpl.description_en }}</p>
            <div class="template-meta">
              <span class="meta-badge">{{ tmpl.persona_segment_count }} {{ $t('industry.segmentsShort') }}</span>
              <span class="meta-badge">{{ tmpl.crisis_scenario_count }} {{ $t('industry.crisesShort') }}</span>
              <span class="meta-badge">{{ tmpl.document_seed_count }} {{ $t('industry.docsShort') }}</span>
            </div>
          </div>
          <div class="template-arrow">→</div>
        </div>
      </div>
    </div>

    <!-- Step 2: Template Details (after selection) -->
    <div v-else-if="selectedTemplate && !loading" class="template-detail-view">
      <button class="back-btn" @click="clearSelection">
        ← {{ $t('industry.backToTemplates') }}
      </button>

      <div class="detail-header">
        <div class="detail-icon">
          {{ templateInitial(selectedTemplate) }}
        </div>
        <div>
          <h3>{{ locale === 'th' ? selectedTemplate.name_th : selectedTemplate.name_en }}</h3>
          <p>{{ locale === 'th' ? selectedTemplate.description_th : selectedTemplate.description_en }}</p>
        </div>
      </div>

      <div v-if="deepPreset" class="detail-section deep-preset-panel">
        <h4>Deep Preset / Industry Assumptions</h4>
        <div class="deep-grid">
          <div>
            <strong>Common objections</strong>
            <ul>
              <li v-for="item in deepPreset.common_objections?.slice(0, 4)" :key="item">{{ item }}</li>
            </ul>
          </div>
          <div>
            <strong>Proof required</strong>
            <ul>
              <li v-for="item in deepPreset.proof_point_requirements?.slice(0, 4)" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>
        <div class="assumption-list">
          <span
            v-for="item in [...(deepPreset.assumptions || []), ...(deepPreset.limitations || [])].slice(0, 4)"
            :key="item"
            class="assumption-chip"
          >
            {{ item }}
          </span>
        </div>
      </div>

      <!-- Persona Segments -->
      <div class="detail-section">
        <h4>{{ $t('industry.personaSegments') }} ({{ selectedTemplate.persona_segments.length }})</h4>
        <div class="segment-list">
          <div
            v-for="(seg, idx) in selectedTemplate.persona_segments"
            :key="seg.id"
            class="segment-item"
          >
            <div class="segment-number">{{ String(idx + 1).padStart(2, '0') }}</div>
            <div class="segment-info">
              <strong>{{ locale === 'th' ? seg.name_th : seg.name_en }}</strong>
              <span class="segment-count">{{ seg.archetypes?.length || 0 }} {{ $t('campaigns.personasUnit') }}</span>
              <p class="segment-interests">{{ (seg.interests || []).join(' · ') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Crisis Scenarios -->
      <div class="detail-section">
        <h4>{{ $t('industry.crisisScenarios') }} ({{ selectedTemplate.crisis_scenarios.length }})</h4>
        <div class="crisis-list">
          <div
            v-for="crisis in selectedTemplate.crisis_scenarios"
            :key="crisis.id"
            :class="['crisis-item', `intensity-${crisis.intensity}`]"
          >
            <span :class="['crisis-impact', `impact-${crisis.impact || 'mixed'}`]">{{ crisisImpactLabel(crisis.impact) }}</span>
            <div>
              <strong>{{ locale === 'th' ? crisis.name_th : crisis.name_en }}</strong>
              <p class="crisis-trigger">{{ crisis.trigger }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Document Seeds -->
      <div class="detail-section">
        <h4>{{ $t('industry.documentSeeds') }} ({{ selectedTemplate.document_seeds.length }})</h4>
        <div class="seed-list">
          <div
            v-for="seed in selectedTemplate.document_seeds"
            :key="seed.id"
            class="seed-item"
            @click="toggleSeedSelection(seed.id)"
            :class="{ active: selectedSeeds.has(seed.id) }"
          >
            <span class="seed-check">{{ selectedSeeds.has(seed.id) ? '✓' : '○' }}</span>
            <div>
              <strong>{{ locale === 'th' ? seed.name_th : seed.name_en }}</strong>
              <p>{{ locale === 'th' ? seed.description_th : seed.description_en }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action -->
      <div class="detail-actions">
        <button class="btn-cancel" @click="clearSelection">
          {{ $t('common.cancel') }}
        </button>
        <button class="btn-apply" @click="applyTemplate">
          {{ $t('industry.useThisTemplate') }}
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="template-loading">
      <div class="spinner"></div>
      <span>{{ $t('common.loading') }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import service from '@/api'

const { locale } = useI18n()

const emit = defineEmits(['template-selected', 'cancel'])

const templates = ref([])
const selectedTemplate = ref(null)
const selectedSeeds = ref(new Set())
const hoveredTemplate = ref(null)
const loading = ref(true)
const deepPreset = computed(() => selectedTemplate.value?.deep_preset || null)

onMounted(async () => {
  try {
    const response = await service.get('/api/industry/templates')
    templates.value = response.data?.templates || response.templates || []
  } catch (e) {
    console.warn('Failed to load industry templates:', e)
  } finally {
    loading.value = false
  }
})

async function selectTemplate(id) {
  loading.value = true
  try {
    const response = await service.get(`/api/industry/templates/${id}/preset`)
    const data = response.data || response
    selectedTemplate.value = data
    // Pre-select all seeds
    selectedSeeds.value = new Set((data.document_seeds || []).map(s => s.id))
  } catch (e) {
    console.error('Failed to load template details:', e)
  } finally {
    loading.value = false
  }
}

function clearSelection() {
  selectedTemplate.value = null
  selectedSeeds.value = new Set()
}

function toggleSeedSelection(seedId) {
  const newSet = new Set(selectedSeeds.value)
  if (newSet.has(seedId)) {
    newSet.delete(seedId)
  } else {
    newSet.add(seedId)
  }
  selectedSeeds.value = newSet
}

function applyTemplate() {
  emit('template-selected', {
    template: selectedTemplate.value,
    selectedSeeds: [...selectedSeeds.value],
  })
}

function templateInitial(template) {
  const name = locale.value === 'th' ? template?.name_th : template?.name_en
  return (name || template?.id || 'T').trim().charAt(0).toUpperCase()
}

function crisisImpactLabel(impact) {
  if (impact === 'negative') return 'NEG'
  if (impact === 'positive') return 'POS'
  return 'MIX'
}
</script>

<style scoped>
.template-selector { padding: 8px 0; }
.template-header { margin-bottom: 24px; }
.template-title { color: var(--text-primary); font-size: var(--text-lg); font-weight: 800; margin-bottom: 8px; }
.template-subtitle { color: var(--text-tertiary); font-size: var(--text-sm); }

.template-grid { display: grid; grid-template-columns: 1fr; gap: 12px; max-height: 400px; overflow-y: auto; }
.template-card {
  display: flex; align-items: center; gap: 16px;
  padding: 16px; border: 1px solid var(--border-default); border-radius: var(--radius-lg);
  cursor: pointer; transition: all 0.2s;
  background: var(--bg-surface);
}
.template-card:hover, .template-card.selected {
  border-color: var(--accent); background: var(--accent-subtle);
}
.template-icon {
  width: 48px; height: 48px; border-radius: var(--radius-lg);
  display: flex; align-items: center; justify-content: center;
  border: 1px solid var(--border-accent);
  background: var(--accent-subtle);
  color: var(--accent);
  flex-shrink: 0;
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 900;
}
.template-info { flex: 1; }
.template-name { color: var(--text-primary); font-size: var(--text-sm); font-weight: 800; margin-bottom: 4px; }
.template-desc { font-size: var(--text-xs); color: var(--text-tertiary); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.template-meta { display: flex; gap: 6px; margin-top: 8px; }
.meta-badge {
  font-size: 0.7rem; padding: 2px 8px; background: var(--bg-elevated); border-radius: var(--radius-pill);
  font-family: var(--font-mono); color: var(--text-tertiary);
}
.template-arrow { color: var(--text-tertiary); font-size: 1.2rem; }

/* Detail View */
.template-detail-view { max-height: 500px; overflow-y: auto; }
.back-btn { background: none; border: none; color: var(--accent); cursor: pointer; font-size: var(--text-sm); padding: 0; margin-bottom: 16px; font-weight: 800; }
.detail-header { display: flex; gap: 16px; align-items: center; margin-bottom: 24px; }
.detail-icon { width: 56px; height: 56px; border: 1px solid var(--border-accent); border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; font-family: var(--font-mono); font-size: var(--text-xl); font-weight: 900; color: var(--accent); background: var(--accent-subtle); flex-shrink: 0; }
.detail-section { margin-bottom: 24px; }
.detail-section h4 { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0; margin-bottom: 12px; }
.deep-preset-panel { padding: 14px; border: 1px solid var(--border-default); border-radius: var(--radius-lg); background: var(--bg-elevated); }
.deep-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.deep-grid strong { display: block; color: var(--text-primary); font-size: var(--text-xs); margin-bottom: 6px; }
.deep-grid ul { margin: 0; padding-left: 18px; color: var(--text-secondary); font-size: var(--text-xs); line-height: 1.55; }
.assumption-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
.assumption-chip { display: inline-flex; padding: 5px 8px; border: 1px solid var(--border-default); border-radius: var(--radius-sm); color: var(--text-secondary); background: var(--bg-surface); font-size: 11px; line-height: 1.35; }
.segment-list { display: flex; flex-direction: column; gap: 8px; }
.segment-item { display: flex; gap: 12px; align-items: flex-start; padding: 10px; background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); }
.segment-number { font-family: var(--font-mono); font-weight: 800; color: var(--accent); font-size: var(--text-sm); }
.segment-info strong { color: var(--text-primary); font-size: var(--text-sm); display: block; }
.segment-count { font-size: 0.7rem; color: var(--text-tertiary); font-family: var(--font-mono); }
.segment-interests { font-size: var(--text-xs); color: var(--text-tertiary); margin-top: 4px; }

.crisis-list { display: flex; flex-direction: column; gap: 8px; }
.crisis-item { display: flex; gap: 10px; align-items: flex-start; padding: 10px; border-radius: var(--radius-md); border-left: 3px solid var(--border-default); background: var(--bg-panel); }
.crisis-item.intensity-10, .crisis-item.intensity-9 { border-left-color: var(--red); background: var(--red-soft); }
.crisis-item.intensity-8, .crisis-item.intensity-7 { border-left-color: var(--yellow); background: var(--yellow-soft); }
.crisis-item.intensity-6 { border-left-color: var(--green); background: var(--green-soft); }
.crisis-item strong { color: var(--text-primary); font-size: var(--text-sm); }
.crisis-trigger { font-size: var(--text-xs); color: var(--text-tertiary); margin-top: 3px; }
.crisis-impact { min-width: 34px; font-family: var(--font-mono); font-size: 0.64rem; font-weight: 900; }

.seed-list { display: flex; flex-direction: column; gap: 6px; }
.seed-item {
  display: flex; gap: 10px; align-items: flex-start;
  padding: 10px; border: 1px solid var(--border-default); border-radius: var(--radius-md);
  cursor: pointer; transition: all 0.15s;
  background: var(--bg-surface);
}
.seed-item:hover, .seed-item.active { border-color: var(--accent); background: var(--accent-subtle); }
.seed-check { font-family: var(--font-mono); font-size: 1rem; color: var(--accent); }
.seed-item strong { color: var(--text-primary); font-size: var(--text-sm); }
.seed-item p { font-size: var(--text-xs); color: var(--text-tertiary); margin-top: 2px; }

.detail-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-subtle); }
.btn-cancel {
  padding: 12px 24px; background: transparent; border: 1px solid var(--border-default); color: var(--text-secondary);
  font-family: var(--font-mono); font-size: var(--text-sm); cursor: pointer; border-radius: var(--radius-md);
}
.btn-apply {
  padding: 12px 24px; background: var(--accent); color: var(--text-inverse); border: none;
  font-family: var(--font-mono); font-size: var(--text-sm); font-weight: 800;
  cursor: pointer; border-radius: var(--radius-md);
}
.template-loading { text-align: center; padding: 40px; }
.spinner { width: 32px; height: 32px; border: 3px solid var(--border-default); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 12px; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
