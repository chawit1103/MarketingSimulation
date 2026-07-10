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

export const __dashboardInsightInternals = { clamp, normalizeChannels }
