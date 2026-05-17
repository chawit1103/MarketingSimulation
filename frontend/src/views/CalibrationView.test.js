import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import CalibrationView from './CalibrationView.vue'
import { testI18n } from '@/test/helpers'

vi.mock('@/api/calibration', () => ({
  importActualResults: vi.fn(),
}))

describe('Calibration privacy warnings', () => {
  it('keeps aggregate-only privacy guidance visible before import', () => {
    const wrapper = mount(CalibrationView, {
      global: { plugins: [testI18n()] },
    })

    const text = wrapper.text()
    expect(text).toContain('No PII or raw posts')
    expect(text).toContain('Use only campaign-level summaries')
    expect(text).toContain('Analyst/admin access is required because actual campaign data may be sensitive.')
    expect(wrapper.find('textarea').attributes('placeholder')).toBe('Anonymized aggregate summary only')
  })
})
