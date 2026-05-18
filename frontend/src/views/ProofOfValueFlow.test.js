import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import ProofOfValueFlow from './ProofOfValueFlow.vue'
import { testI18n } from '@/test/helpers'

function mountView() {
  return mount(ProofOfValueFlow, {
    global: {
      plugins: [testI18n()],
    },
  })
}

describe('ProofOfValueFlow', () => {
  it('renders proof-of-value guardrails and source labels', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('Approved Brief to Strategy Pack')
    expect(text).toContain('มีแค่โจทย์ดิบ?')
    expect(text).toContain('AI Research Prompt Pack')
    expect(text).toContain('Intake Import Template')
    expect(text).toContain('Resources Hub')
    expect(text).toContain('Local Estimate')
    expect(text).toContain('No PII')
    expect(text).toContain('No raw CRM records')
    expect(text).toContain('No customer lists')
    expect(text).toContain('No secrets')
    expect(text).toContain('No live integrations')
    expect(text).toContain('Decision-support estimate, not a guaranteed prediction')
    expect(text).not.toMatch(/production[- ]ready/i)
    expect(text).not.toMatch(/exact roi prediction/i)
  })

  it('flags unsafe intake text and redacts it from generated payload', async () => {
    const wrapper = mountView()
    const textareas = wrapper.findAll('textarea')

    await textareas[2].setValue('Market note includes person@example.test from a CRM export')
    await textareas[10].setValue('Operator suggested an API key for live integration')

    expect(wrapper.text()).toContain('Unsafe Intake Signals')
    expect(wrapper.text()).toContain('Email-like text is not allowed')
    expect(wrapper.text()).toContain('Raw CRM, contact, or customer-list language must be removed')
    expect(wrapper.text()).toContain('Secrets or credential language must be removed')

    const payload = wrapper.find('.payload-preview').text()
    expect(payload).toContain('[blocked: unsafe intake signal]')
    expect(payload).not.toContain('person@example.test')
    expect(payload).not.toContain('API key')
  })
})
