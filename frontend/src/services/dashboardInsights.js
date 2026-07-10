const PLATFORM_LABELS = {
  facebook: 'Facebook',
  instagram: 'Instagram',
  tiktok: 'TikTok',
  youtube: 'YouTube',
  line: 'LINE',
  twitter: 'X / Twitter',
  twitter_x: 'X / Twitter',
  x: 'X / Twitter',
  reddit: 'Reddit',
  linkedin: 'LinkedIn',
  shopee_live: 'Shopee Live',
}

function clamp(value, min = 0, max = 100) {
  const n = Number(value)
  if (!Number.isFinite(n)) return min
  return Math.max(min, Math.min(max, n))
}

function round(value, digits = 0) {
  const factor = 10 ** digits
  return Math.round(Number(value || 0) * factor) / factor
}

function slug(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '_')
    .replace(/[^a-z0-9_]/g, '')
}

function normalizeChannels(campaign = {}, influencers = []) {
  const target = campaign.target || campaign.audience || {}
  const simConfig = campaign.sim_config || {}
  const raw = [
    ...(Array.isArray(target.channels) ? target.channels : []),
    ...(Array.isArray(simConfig.audience_channels) ? simConfig.audience_channels : []),
    ...(Array.isArray(campaign.audience_channels) ? campaign.audience_channels : []),
    ...(Array.isArray(campaign.channels) ? campaign.channels : []),
    ...influencers.map((item) => item.platform),
  ]

  const normalized = raw
    .map((channel) => slug(channel))
    .map((channel) => (channel === 'twitter' ? 'twitter_x' : channel))
    .filter(Boolean)

  return [...new Set(normalized)].slice(0, 6)
}

export function platformLabel(platform) {
  return PLATFORM_LABELS[slug(platform)] || String(platform || 'Channel')
}

export function buildPlatformComparison({ campaign = {}, kpis = {}, timeline = [], segments = [], influencers = [] } = {}) {
  const channels = normalizeChannels(campaign, influencers)
  const platforms = channels.length ? channels : ['facebook', 'instagram', 'tiktok']
  const sentimentBase = Number(kpis.overall_sentiment ?? 0)
  const conversionBase = Number(kpis.conversion_probability ?? 50)
  const resonanceBase = Number(kpis.message_resonance ?? 50)
  const influenceBase = Number(kpis.social_influence ?? kpis.social_influence_index ?? 50)
  const recentSentiment = timeline.length
    ? Number(timeline[timeline.length - 1].sentiment ?? timeline[timeline.length - 1].avg_sentiment ?? sentimentBase)
    : sentimentBase
  const segmentSpread = segments.length
    ? Math.max(...segments.map((s) => Number(s.sentiment ?? s.avg_sentiment ?? 0))) - Math.min(...segments.map((s) => Number(s.sentiment ?? s.avg_sentiment ?? 0)))
    : 0

  return platforms.map((platform, index) => {
    const relatedInfluencers = influencers.filter((item) => slug(item.platform) === platform)
    const influencerLift = relatedInfluencers.reduce((sum, item) => sum + Number(item.impact_score ?? item.influence_score ?? 0), 0) / Math.max(1, relatedInfluencers.length)
    const deterministicOffset = ((index % 3) - 1) * 6
    const engagementScore = clamp(resonanceBase * 0.42 + influenceBase * 0.34 + conversionBase * 0.18 + influencerLift * 0.06 + deterministicOffset)
    const sentiment = clamp(recentSentiment + deterministicOffset + (influencerLift ? (influencerLift - 50) * 0.08 : 0), -100, 100)
    const conversion = clamp(conversionBase + deterministicOffset * 0.7 + (engagementScore - 50) * 0.12)
    const risk = clamp(Number(kpis.crisis_risk ?? 0) + segmentSpread * 0.08 - engagementScore * 0.05 + index * 2)

    return {
      platform,
      label: platformLabel(platform),
      engagementScore: round(engagementScore),
      sentiment: round(sentiment),
      conversion: round(conversion),
      risk: round(risk),
      evidenceCount: relatedInfluencers.length || Math.max(1, Math.round((timeline.length || 3) / Math.max(1, platforms.length))),
      role: index === 0 ? 'primary' : index === 1 ? 'support' : 'test',
    }
  }).sort((a, b) => b.engagementScore - a.engagementScore)
}

export function buildPolarityBreakdown(segments = [], timeline = []) {
  const source = segments.length
    ? segments.map((item) => ({ label: item.name || item.segment_name || 'Segment', sentiment: Number(item.sentiment ?? item.avg_sentiment ?? 0) }))
    : timeline.map((item) => ({ label: `R${item.round_num || item.round || ''}`.trim(), sentiment: Number(item.sentiment ?? item.avg_sentiment ?? 0) }))

  const buckets = [
    { key: 'positive', min: 16, labelKey: 'dashboard.polarityPositive', color: 'var(--green)' },
    { key: 'neutral', min: -15, max: 15, labelKey: 'dashboard.polarityNeutral', color: 'var(--yellow)' },
    { key: 'negative', max: -16, labelKey: 'dashboard.polarityNegative', color: 'var(--red)' },
  ]

  return buckets.map((bucket) => {
    const items = source.filter((item) => {
      if (bucket.key === 'positive') return item.sentiment >= bucket.min
      if (bucket.key === 'negative') return item.sentiment <= bucket.max
      return item.sentiment >= bucket.min && item.sentiment <= bucket.max
    })
    const avg = items.length ? items.reduce((sum, item) => sum + item.sentiment, 0) / items.length : 0
    return {
      ...bucket,
      count: items.length,
      share: source.length ? round((items.length / source.length) * 100) : 0,
      avgSentiment: round(avg),
      drivers: items.slice(0, 3).map((item) => item.label),
    }
  })
}

export function buildExplanationPanels({ kpis = {}, source = {}, platformComparison = [], polarityBreakdown = [] } = {}) {
  const leader = platformComparison[0]
  const negative = polarityBreakdown.find((item) => item.key === 'negative')
  const sourceMode = source.type || source.source_mode || 'unknown'
  const isEstimated = ['demo_mode', 'local_estimate', 'unknown'].includes(sourceMode)

  return [
    {
      key: 'decision_use',
      titleKey: 'dashboard.explainDecisionUse',
      bodyKey: kpis.conversion_probability >= 65 ? 'dashboard.explainScaleBody' : 'dashboard.explainPilotBody',
      metric: `${round(kpis.conversion_probability)}%`,
    },
    {
      key: 'platform_focus',
      titleKey: 'dashboard.explainPlatformFocus',
      bodyKey: leader?.risk >= 45 ? 'dashboard.explainPlatformGuardrailBody' : 'dashboard.explainPlatformScaleBody',
      metric: leader ? `${leader.label} · ${leader.engagementScore}` : '—',
    },
    {
      key: 'evidence_quality',
      titleKey: 'dashboard.explainEvidenceQuality',
      bodyKey: isEstimated ? 'dashboard.explainEstimatedBody' : 'dashboard.explainVerifiedBody',
      metric: sourceMode,
    },
    {
      key: 'polarity_watch',
      titleKey: 'dashboard.explainPolarityWatch',
      bodyKey: negative?.share >= 30 ? 'dashboard.explainPolarityRiskBody' : 'dashboard.explainPolarityStableBody',
      metric: `${negative?.share || 0}%`,
    },
  ]
}

function valueOrDash(value) {
  if (value === null || value === undefined || value === '') return '—'
  return String(value)
}

function listFrom(value, fallback = []) {
  if (Array.isArray(value)) return value.filter(Boolean)
  if (value) return [value]
  return fallback
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (Array.isArray(value) && value.length) return value.filter(Boolean)
    if (value !== null && value !== undefined && value !== '') return value
  }
  return ''
}

export function buildExecutiveDecisionBrief({
  campaign = {},
  campaignBrief = {},
  kpis = {},
  source = {},
  trustPanel = {},
  platformComparison = [],
  polarityBreakdown = [],
  timeline = [],
  segments = [],
  influencers = [],
  actionPlan = {},
  decision = {},
  businessImpact = {},
  assumptions = [],
  scoreExplanations = [],
  riskDrivers = [],
  simulatedQuotes = [],
  summary = '',
  recommendation = '',
  nextAction = '',
} = {}) {
  const sourceType = source.type || source.source_mode || actionPlan?.source?.type || 'unknown'
  const sourceWarning = source.warning || source.recommended_next_validation_step || actionPlan?.source?.warning || ''
  const leader = platformComparison[0] || {}
  const negative = polarityBreakdown.find((item) => item.key === 'negative') || {}
  const latestTimeline = timeline[timeline.length - 1] || {}
  const actionSections = actionPlan?.sections || {}
  const channelItems = actionSections.channel_allocation?.items || []
  const validationItems = actionSections.validation_plan?.items || []
  const topSegments = [...segments]
    .sort((a, b) => Number(b.sentiment ?? b.avg_sentiment ?? 0) - Number(a.sentiment ?? a.avg_sentiment ?? 0))
    .slice(0, 3)
    .map((item) => ({
      name: item.name || item.segment_name || 'Segment',
      sentiment: round(item.sentiment ?? item.avg_sentiment ?? 0),
      conversion: round(item.conversion ?? item.conversion_estimate ?? 0),
    }))

  const scale = {
    personas: firstNonEmpty(campaignBrief.personas, campaign.target?.persona_count, campaign.persona_count, trustPanel.personaCount, '—'),
    rounds: firstNonEmpty(campaignBrief.rounds, campaign.sim_config?.max_rounds, timeline.length, '—'),
    timeline_points: timeline.length,
    segments: segments.length,
    influence_nodes: influencers.length,
    evidence_count: platformComparison.reduce((sum, item) => sum + Number(item.evidenceCount || 0), 0),
  }

  const syntheticResults = {
    overall_sentiment: round(kpis.overall_sentiment ?? 0),
    conversion_probability: round(kpis.conversion_probability ?? 0),
    social_influence_index: round(kpis.social_influence ?? kpis.social_influence_index ?? 0),
    message_resonance: round(kpis.message_resonance ?? 0),
    crisis_risk: valueOrDash(kpis.crisis_risk),
    latest_sentiment: round(latestTimeline.sentiment ?? latestTimeline.avg_sentiment ?? kpis.overall_sentiment ?? 0),
    negative_share: round(negative.share ?? 0),
  }

  const platformAllocation = platformComparison.map((item, index) => ({
    platform: item.label || platformLabel(item.platform),
    role: item.role || (index === 0 ? 'primary' : index === 1 ? 'support' : 'test'),
    engagement_score: round(item.engagementScore ?? 0),
    sentiment: round(item.sentiment ?? 0),
    conversion: round(item.conversion ?? 0),
    risk: round(item.risk ?? 0),
    evidence_count: item.evidenceCount || 0,
  }))

  const decisionOptions = [
    {
      option: 'Scale with guardrails',
      when: Number(syntheticResults.conversion_probability) >= 65 && Number(syntheticResults.negative_share) < 30,
      rationale: `Use ${leader.label || 'the leading platform'} as the primary channel while preserving validation and escalation gates.`,
    },
    {
      option: 'Controlled pilot',
      when: Number(syntheticResults.conversion_probability) < 65 || ['demo_mode', 'local_estimate', 'unknown'].includes(sourceType),
      rationale: 'Run a bounded pilot because the evidence is synthetic/offline and needs market validation before full spend.',
    },
    {
      option: 'Revise message before launch',
      when: Number(syntheticResults.negative_share) >= 30 || Number(leader.risk || 0) >= 45,
      rationale: 'Reduce claim, channel, or segment risk before approving broader activation.',
    },
  ]

  const limitations = [
    ...listFrom(trustPanel.knownLimitations),
    ...listFrom(source.limitations),
    ...listFrom(assumptions),
  ].filter(Boolean)

  const safetyNotices = [
    'Results are synthetic/offline decision support, not measured ad-platform performance or guaranteed market outcomes.',
    'Do not treat modeled engagement, conversion, or platform ranking as a launch winner without controlled validation.',
    'No live CRM, PII, scraping, credentials, or external social-listening data is required for this report.',
  ]

  if (['demo_mode', 'local_estimate', 'unknown'].includes(sourceType)) {
    safetyNotices.unshift(`Offline notice: source mode is ${sourceType}; keep provenance visible in exports and executive screenshots.`)
  }

  return {
    title: `${campaign.name || campaignBrief.description || 'Campaign'} — Executive Decision Brief`,
    generated_at: new Date().toISOString(),
    user_input: {
      campaign_name: campaign.name || '—',
      description: campaignBrief.description || campaign.description || '—',
      objective: campaignBrief.objective || campaign.objective || '—',
      audience: campaignBrief.audience || '—',
      channels: campaignBrief.channels || '—',
      platform: campaignBrief.platform || '—',
      behavior_model: campaignBrief.platformMode || '—',
      status: campaignBrief.status || campaign.status || '—',
    },
    workflow: {
      source_mode: sourceType,
      source_warning: sourceWarning,
      run_id: trustPanel.runId || campaign.simulation_id || campaign.campaign_id || '—',
      confidence: trustPanel.confidenceLevel || `${round(trustPanel.confidence ?? 0)}%`,
      next_validation_step: trustPanel.nextValidationStep || source.recommended_next_validation_step || '',
      chart_inputs: {
        timeline_points: timeline.length,
        platform_rows: platformComparison.length,
        polarity_buckets: polarityBreakdown.length,
      },
    },
    scale,
    synthetic_results: syntheticResults,
    platform_allocation: platformAllocation,
    evidence: {
      summary: summary || scoreExplanations[0] || actionPlan.headline || 'Review synthetic evidence before approving the next action.',
      score_explanations: listFrom(scoreExplanations).slice(0, 5),
      risk_drivers: listFrom(riskDrivers).slice(0, 5),
      top_segments: topSegments,
      simulated_quotes: listFrom(simulatedQuotes).slice(0, 4),
    },
    charts_summary: {
      sentiment_timeline: timeline.map((item) => ({
        round: item.round_num || item.round || '',
        sentiment: round(item.sentiment ?? item.avg_sentiment ?? 0),
        actions: item.action_count || item.actions || 0,
      })),
      polarity_breakdown: polarityBreakdown.map((item) => ({
        label: item.key,
        share: round(item.share ?? 0),
        avg_sentiment: round(item.avgSentiment ?? 0),
        drivers: item.drivers || [],
      })),
    },
    assumptions: listFrom(assumptions).slice(0, 6),
    limitations: [...new Set(limitations)].slice(0, 6),
    safety_notices: safetyNotices,
    decision_options: decisionOptions,
    recommended_next_action: nextAction || recommendation || decision.next_best_action || validationItems[0]?.recommendation || channelItems[0]?.recommendation || 'Validate with a controlled audience or media test before scaling.',
    business_impact: businessImpact || {},
  }
}

export const __dashboardInsightInternals = { clamp, normalizeChannels }
