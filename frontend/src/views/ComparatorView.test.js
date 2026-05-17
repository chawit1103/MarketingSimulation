import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import ComparatorView from './ComparatorView.vue'
import { flushPromises, testI18n } from '@/test/helpers'

vi.mock('@/components/ExportButton.vue', () => ({
  default: { template: '<button>Export</button>' },
}))

vi.mock('@/api/authStorage', () => ({
  hasBrowserAuth: vi.fn(() => false),
}))

vi.mock('@/api/campaign', () => ({
  listCampaigns: vi.fn(() => Promise.resolve({ data: [] })),
}))

vi.mock('@/api/comparator', () => ({
  listDemoComparatorCampaigns: vi.fn(),
  compareDemoCampaigns: vi.fn(),
  compareCampaigns: vi.fn(),
}))

vi.mock('@/services/analytics', () => ({
  sourceModeFromValue: (value) => value || 'unknown',
  trackEvent: vi.fn(),
}))

function comparison(sourceMode) {
  return {
    source: { source_mode: sourceMode, data_basis: sourceMode === 'demo_mode' ? 'demo_fixture' : 'backend_generated' },
    campaign_count: 2,
    overall_winner: { campaign_id: 'a', campaign_name: 'Campaign A', metric_wins: 4, total_metrics: 7 },
    campaign_summaries: [
      { campaign_id: 'a', campaign_name: 'Campaign A', metric_wins: 4, is_overall_winner: true, recommended_use_case: 'Lead', trade_offs: [] },
      { campaign_id: 'b', campaign_name: 'Campaign B', metric_wins: 3, is_overall_winner: false, recommended_use_case: 'Backup', trade_offs: [] },
    ],
    ranked_recommendation: [{ campaign_id: 'a', campaign_name: 'Campaign A', reason: 'Best balance.' }],
    metrics_comparison: [
      {
        key: 'sentiment',
        label: 'Sentiment',
        unit: '',
        max_diff: 8,
        higher_is_better: true,
        winner_campaign_id: 'a',
        values: [
          { campaign_id: 'a', value: 62 },
          { campaign_id: 'b', value: 54 },
        ],
      },
    ],
  }
}

async function mountComparator() {
  const wrapper = mount(ComparatorView, {
    global: { plugins: [testI18n()] },
  })
  await flushPromises()
  await flushPromises()
  return wrapper
}

describe('Comparator source labels', () => {
  beforeEach(async () => {
    const auth = await import('@/api/authStorage')
    const comparatorApi = await import('@/api/comparator')
    auth.hasBrowserAuth.mockReturnValue(false)
    comparatorApi.listDemoComparatorCampaigns.mockResolvedValue({
      data: [
        { id: 'a', campaign_id: 'a', name: 'Campaign A' },
        { id: 'b', campaign_id: 'b', name: 'Campaign B' },
      ],
    })
    comparatorApi.compareDemoCampaigns.mockResolvedValue({ data: comparison('demo_mode') })
    comparatorApi.compareCampaigns.mockResolvedValue({ data: comparison('live_backend') })
  })

  it('labels demo backend comparator fixtures as Demo Mode', async () => {
    const wrapper = await mountComparator()

    expect(wrapper.text()).toContain('Demo Mode')
    expect(wrapper.text()).toContain('Demo campaign options are being shown')

    await wrapper.findAll('.campaign-chip')[0].trigger('click')
    await wrapper.findAll('.campaign-chip')[1].trigger('click')
    await wrapper.find('.btn-compare').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Demo Mode')
    expect(wrapper.text()).toContain('deterministic backend demo fixtures')
  })

  it('requires explicit Local Estimate after backend comparison failure', async () => {
    const comparatorApi = await import('@/api/comparator')
    comparatorApi.compareDemoCampaigns.mockRejectedValueOnce(new Error('backend down'))
    const wrapper = await mountComparator()

    await wrapper.findAll('.campaign-chip')[0].trigger('click')
    await wrapper.findAll('.campaign-chip')[1].trigger('click')
    await wrapper.find('.btn-compare').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Backend comparison unavailable')
    expect(wrapper.find('.results-section').exists()).toBe(false)

    await wrapper.find('.btn-fallback').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Local Estimate')
    expect(wrapper.text()).toContain('not backend-verified simulation results')
  })

  it('labels authenticated backend comparator output as Live Backend', async () => {
    const auth = await import('@/api/authStorage')
    const campaignApi = await import('@/api/campaign')
    auth.hasBrowserAuth.mockReturnValue(true)
    campaignApi.listCampaigns.mockResolvedValue({
      data: [
        { id: 'a', campaign_id: 'a', name: 'Campaign A' },
        { id: 'b', campaign_id: 'b', name: 'Campaign B' },
      ],
    })
    const wrapper = await mountComparator()

    await wrapper.findAll('.campaign-chip')[0].trigger('click')
    await wrapper.findAll('.campaign-chip')[1].trigger('click')
    await wrapper.find('.btn-compare').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Live Backend')
    expect(wrapper.text()).toContain('backend comparator API')
  })
})
