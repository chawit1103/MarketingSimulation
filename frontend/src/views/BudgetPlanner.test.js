import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import BudgetPlanner from './BudgetPlanner.vue'
import { flushPromises, testI18n } from '@/test/helpers'

vi.mock('@/api/budget', () => ({
  runBudgetScenario: vi.fn(() => Promise.resolve({
    data: {
      objective: 'conversion',
      total_budget: 2500000,
      duration_weeks: 8,
      disclaimer: 'Directional planning only. Not exact ROI or ROAS prediction.',
      source: {
        type: 'demo_mode',
        warning: 'Demo Mode fixture for planning.',
      },
      confidence_level: 'medium',
      confidence_score: 70,
      recommended_validation_step: 'Validate with a small media test.',
      allocation_ranges: [],
      assumptions: ['Uses demo-safe assumptions.'],
      limitations: ['Not connected to live ad costs.'],
    },
  })),
}))

vi.mock('@/services/analytics', () => ({
  sourceModeFromValue: (value) => value || 'unknown',
  trackEvent: vi.fn(),
}))

describe('Budget Planner disclaimers', () => {
  it('shows assumption-based planning and not exact ROI/ROAS wording', async () => {
    const wrapper = mount(BudgetPlanner, {
      global: { plugins: [testI18n()] },
    })

    await flushPromises()
    await flushPromises()

    const text = wrapper.text()
    expect(text).toContain('This is assumption-based planning, not exact ROI or ROAS prediction.')
    expect(text).toContain('Directional planning only. Not exact ROI or ROAS prediction.')
    expect(text).toContain('Demo Mode')
  })
})
