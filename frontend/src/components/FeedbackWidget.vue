<template>
  <div class="feedback-widget">
    <button
      v-if="!open"
      class="feedback-trigger"
      type="button"
      @click="open = true"
    >
      {{ $t('feedback.trigger') }}
    </button>

    <aside v-else class="feedback-panel" aria-live="polite">
      <div class="feedback-header">
        <div>
          <span>{{ $t('feedback.kicker') }}</span>
          <h2>{{ submitted ? $t('feedback.thanksTitle') : $t('feedback.title') }}</h2>
        </div>
        <button class="feedback-close" type="button" :aria-label="$t('common.cancel')" @click="open = false">×</button>
      </div>

      <p class="feedback-copy">
        {{ submitted ? $t('feedback.thanksCopy') : $t('feedback.copy') }}
      </p>

      <form v-if="!submitted" class="feedback-form" @submit.prevent="submitFeedback">
        <div class="rating-row" :aria-label="$t('feedback.ratingLabel')">
          <button
            v-for="value in ratings"
            :key="value"
            type="button"
            :class="['rating-button', { active: rating === value }]"
            @click="rating = value"
          >
            {{ value }}
          </button>
        </div>

        <label class="feedback-label" for="feedback-confusion">{{ $t('feedback.confusionLabel') }}</label>
        <select id="feedback-confusion" v-model="confusionArea" class="feedback-select">
          <option value="none">{{ $t('feedback.none') }}</option>
          <option value="source_labels">{{ $t('feedback.sourceLabels') }}</option>
          <option value="brief_quality">{{ $t('feedback.briefQuality') }}</option>
          <option value="dashboard">{{ $t('feedback.dashboard') }}</option>
          <option value="war_room">{{ $t('feedback.warRoom') }}</option>
          <option value="settings">{{ $t('feedback.settings') }}</option>
          <option value="export">{{ $t('feedback.export') }}</option>
          <option value="other">{{ $t('feedback.other') }}</option>
        </select>

        <label class="feedback-label" for="feedback-missing">{{ $t('feedback.missingLabel') }}</label>
        <select id="feedback-missing" v-model="missingNeed" class="feedback-select">
          <option value="none">{{ $t('feedback.missingNone') }}</option>
          <option value="better_evidence">{{ $t('feedback.missingEvidence') }}</option>
          <option value="clearer_actions">{{ $t('feedback.missingActions') }}</option>
          <option value="export_storyline">{{ $t('feedback.missingExport') }}</option>
          <option value="calibration">{{ $t('feedback.missingCalibration') }}</option>
          <option value="collaboration">{{ $t('feedback.missingCollaboration') }}</option>
          <option value="other">{{ $t('feedback.other') }}</option>
        </select>

        <label class="feedback-label" for="feedback-source-clear">{{ $t('feedback.sourceConfidenceLabel') }}</label>
        <select id="feedback-source-clear" v-model="sourceConfidenceClear" class="feedback-select">
          <option value="yes">{{ $t('feedback.yes') }}</option>
          <option value="partial">{{ $t('feedback.partial') }}</option>
          <option value="no">{{ $t('feedback.no') }}</option>
        </select>

        <button class="feedback-submit" type="submit" :disabled="!rating">
          {{ $t('feedback.submit') }}
        </button>
      </form>
    </aside>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { routeBucket, trackEvent } from '@/services/analytics'

const route = useRoute()
const open = ref(false)
const submitted = ref(false)
const rating = ref(null)
const confusionArea = ref('none')
const missingNeed = ref('none')
const sourceConfidenceClear = ref('yes')
const ratings = [1, 2, 3, 4, 5]

function submitFeedback() {
  trackEvent('feedback_submitted', {
    rating: rating.value,
    confusion_area: confusionArea.value,
    missing_need: missingNeed.value,
    source_confidence_clear: sourceConfidenceClear.value,
    useful_for_decision: Number(rating.value || 0) >= 4,
    route_bucket: routeBucket(route),
  })
  submitted.value = true
  setTimeout(() => {
    open.value = false
    submitted.value = false
    rating.value = null
    confusionArea.value = 'none'
    missingNeed.value = 'none'
    sourceConfidenceClear.value = 'yes'
  }, 1800)
}
</script>

<style scoped>
.feedback-widget {
  position: fixed;
  left: 24px;
  bottom: 24px;
  z-index: 9998;
  font-family: var(--font-sans);
}

.feedback-trigger,
.feedback-submit,
.feedback-close,
.rating-button {
  border: 1px solid var(--border-default);
  background: var(--bg-surface);
  color: var(--text-primary);
  cursor: pointer;
  transition: background var(--transition-fast), border-color var(--transition-fast), transform var(--transition-fast);
}

.feedback-trigger {
  min-height: 38px;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-sm);
  color: var(--text-secondary);
  font-size: var(--text-xs);
  font-weight: 800;
}

.feedback-trigger:hover,
.feedback-submit:hover,
.rating-button:hover {
  border-color: var(--border-accent);
  background: var(--accent-subtle);
  transform: translateY(-1px);
}

.feedback-panel {
  width: min(330px, calc(100vw - 32px));
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  box-shadow: var(--shadow-elevated);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  gap: var(--space-3);
}

.feedback-header span {
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.feedback-header h2 {
  margin: 4px 0 0;
  color: var(--text-primary);
  font-size: var(--text-base);
}

.feedback-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: var(--text-lg);
  line-height: 1;
}

.feedback-copy {
  margin: var(--space-3) 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.feedback-form {
  display: grid;
  gap: var(--space-3);
}

.rating-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-2);
}

.rating-button {
  min-height: 36px;
  border-radius: var(--radius-md);
  font-weight: 900;
}

.rating-button.active {
  border-color: var(--accent);
  background: var(--accent-subtle);
  color: var(--accent);
}

.feedback-label {
  color: var(--text-secondary);
  font-size: var(--text-xs);
  font-weight: 800;
}

.feedback-select {
  width: 100%;
  min-height: 38px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-primary);
  padding: 8px 10px;
}

.feedback-submit {
  min-height: 38px;
  border-radius: var(--radius-pill);
  font-weight: 900;
}

.feedback-submit:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 680px) {
  .feedback-widget {
    left: 16px;
    bottom: 76px;
  }
}
</style>
