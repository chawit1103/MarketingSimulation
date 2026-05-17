import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import Settings from './Settings.vue'
import { flushPromises, testI18n } from '@/test/helpers'

vi.mock('@/components/TemplateImportDropZone.vue', () => ({
  default: { template: '<div data-test="template-import"></div>' },
}))

vi.mock('@/api/status', () => ({
  getSystemStatus: vi.fn(() => Promise.resolve({
    status: 'ready',
    estimate: { cost_per_100_personas_usd: 0, default_model: 'demo' },
    services: [],
  })),
}))

vi.mock('@/api/settings', () => ({
  getSettings: vi.fn(),
  updateSettings: vi.fn(() => Promise.resolve({ success: true })),
  getProviders: vi.fn(() => Promise.resolve({
    llm_providers: [],
    embedding_providers: [],
    graph_db_modes: [],
  })),
  testLLMConnection: vi.fn(() => Promise.resolve({ success: true })),
  checkSettingsReadiness: vi.fn(() => Promise.resolve({
    ready: true,
    checks: {
      llm: { status: 'ready', safe_detail: 'LLM configured.', issues: [] },
      embedding: { status: 'ready', safe_detail: 'Embedding configured.', issues: [] },
      neo4j: { status: 'ready', safe_detail: 'Neo4j configured.', issues: [] },
    },
    cost_estimate: {
      per_100_personas: 0,
      label: 'estimate only',
      disclaimer: 'Estimate only.',
    },
    sample_simulation: {
      label: 'Sample Simulation',
      detail: 'Safe demo run.',
    },
  })),
}))

vi.mock('@/services/analytics', () => ({
  trackEvent: vi.fn(),
}))

describe('Settings secret presence display', () => {
  beforeEach(async () => {
    const settingsApi = await import('@/api/settings')
    settingsApi.getSettings.mockResolvedValue({
      settings: {
        language: 'en',
        llm: {
          provider: 'openai',
          model: 'gpt-test',
          base_url: 'https://api.example.test',
          api_key_present: true,
        },
        embedding: {
          provider: 'openai',
          model: 'text-embedding-test',
          base_url: 'https://api.example.test',
          api_key_present: false,
        },
        graph_db: {
          mode: 'local',
          uri: 'bolt://localhost:7687',
          user: 'neo4j',
          password_present: true,
        },
      },
    })
  })

  it('shows presence flags without rendering raw secrets', async () => {
    const wrapper = mount(Settings, {
      global: { plugins: [testI18n()] },
    })

    await flushPromises()
    await flushPromises()

    const text = wrapper.text()
    expect(text).toContain('Saved secret present. Leave blank to keep it.')
    expect(text).toContain('No saved secret. Enter a value to save one.')
    expect(text).not.toContain('sk-live')
    expect(text).not.toContain('password-secret')

    const presentHints = wrapper.findAll('.secret-hint.is-present')
    expect(presentHints).toHaveLength(2)
  })
})
