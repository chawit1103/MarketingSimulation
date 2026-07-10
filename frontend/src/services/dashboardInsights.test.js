import { describe, expect, it } from 'vitest'

import {
  buildExplanationPanels,
  buildPlatformComparison,
  buildPolarityBreakdown,
  platformLabel,
} from './dashboardInsights'

describe('dashboard insight helpers', () => {
  it('builds ranked platform comparison from campaign channels and KPI evidence', () => {
    const rows = buildPlatformComparison({
      campaign: {
        target: { channels: ['facebook', 'tiktok', 'twitter'] },
        sim_config: { audience_channels: ['line'] },
      },
      kpis: {
        overall_sentiment: 32,
        conversion_probability: 68,
        social_influence: 74,
        message_resonance: 70,
        crisis_risk: 22,
      },
      timeline: [{ round_num: 1, sentiment: 18 }, { round_num: 2, sentiment: 38 }],
      segments: [{ name: 'A', sentiment: 55 }, { name: 'B', sentiment: -12 }],
      influencers: [{ platform: 'TikTok', impact_score: 91 }],
    })

    expect(rows).toHaveLength(4)
    expect(rows.map((row) => row.platform)).toContain('twitter_x')
    expect(rows[0].engagementScore).toBeGreaterThanOrEqual(rows[rows.length - 1].engagementScore)
    expect(rows.every((row) => row.engagementScore >= 0 && row.engagementScore <= 100)).toBe(true)
    expect(platformLabel('twitter_x')).toBe('X / Twitter')
  })

  it('summarizes polarity buckets without hiding negative concentration', () => {
    const buckets = buildPolarityBreakdown([
      { name: 'Advocates', sentiment: 64 },
      { name: 'Fence sitters', sentiment: 4 },
      { name: 'Skeptics', sentiment: -33 },
      { name: 'Opposition', sentiment: -61 },
    ])

    const negative = buckets.find((bucket) => bucket.key === 'negative')
    expect(negative.share).toBe(50)
    expect(negative.drivers).toEqual(['Skeptics', 'Opposition'])
  })

  it('keeps source transparency in explanation panels', () => {
    const panels = buildExplanationPanels({
      kpis: { conversion_probability: 54 },
      source: { type: 'local_estimate' },
      platformComparison: [{ label: 'LINE', engagementScore: 66, risk: 28 }],
      polarityBreakdown: [{ key: 'negative', share: 12 }],
    })

    expect(panels.map((panel) => panel.bodyKey)).toContain('dashboard.explainEstimatedBody')
    expect(panels.map((panel) => panel.bodyKey)).toContain('dashboard.explainPilotBody')
  })
})
