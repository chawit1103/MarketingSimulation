import { describe, expect, it } from 'vitest'

import {
  buildExecutiveDecisionBrief,
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

  it('builds an executive decision brief with report scope and safety guardrails', () => {
    const brief = buildExecutiveDecisionBrief({
      campaign: {
        name: 'Premium Water Launch',
        description: 'Launch message test',
        target: { persona_count: 120 },
        sim_config: { max_rounds: 8 },
      },
      campaignBrief: {
        objective: 'Product launch',
        audience: 'Thai urban millennials',
        channels: 'LINE, TikTok',
        platform: 'Both',
        platformMode: 'Creator feed',
      },
      kpis: {
        overall_sentiment: 34,
        conversion_probability: 68,
        social_influence: 71,
        message_resonance: 74,
        crisis_risk: 22,
      },
      source: { type: 'local_estimate', warning: 'Backend unavailable' },
      trustPanel: { runId: 'demo-run', confidenceLevel: '78%', knownLimitations: ['No live ad platform data.'] },
      platformComparison: [
        { label: 'TikTok', engagementScore: 82, sentiment: 40, conversion: 72, risk: 18, evidenceCount: 3, role: 'primary' },
        { label: 'LINE', engagementScore: 70, sentiment: 24, conversion: 64, risk: 25, evidenceCount: 2, role: 'support' },
      ],
      polarityBreakdown: [{ key: 'negative', share: 12, avgSentiment: -22, drivers: ['Skeptics'] }],
      timeline: [{ round_num: 1, sentiment: 18, action_count: 9 }, { round_num: 2, sentiment: 38, action_count: 11 }],
      segments: [{ name: 'Advocates', sentiment: 62, conversion: 76 }],
      influencers: [{ agent_name: 'Creator A' }],
      assumptions: ['Directional synthetic sample.'],
      scoreExplanations: ['Strong positive modeled response.'],
      riskDrivers: ['Claim proof needs validation.'],
      simulatedQuotes: ['I would try this if the benefit is clear.'],
      nextAction: 'Run a controlled validation test.',
    })

    expect(brief.user_input.campaign_name).toBe('Premium Water Launch')
    expect(brief.scale.personas).toBe(120)
    expect(brief.platform_allocation[0].platform).toBe('TikTok')
    expect(brief.synthetic_results.conversion_probability).toBe(68)
    expect(brief.charts_summary.sentiment_timeline).toHaveLength(2)
    expect(brief.assumptions).toContain('Directional synthetic sample.')
    expect(brief.limitations).toContain('No live ad platform data.')
    expect(brief.safety_notices.join(' ')).toContain('synthetic/offline decision support')
    expect(brief.decision_options.map((item) => item.option)).toContain('Controlled pilot')
    expect(brief.recommended_next_action).toBe('Run a controlled validation test.')
  })
})
