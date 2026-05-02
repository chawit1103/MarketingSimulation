import { expect, test } from '@playwright/test'

const demoCampaign = {
  id: 'demo-premium-water',
  name: 'Premium Water Launch TH',
  description: 'Synthetic demo campaign for premium water launch.',
  objective: 'product_launch',
  status: 'completed',
  target: {
    segment_name: 'Thai Urban Health Buyers',
    age_range: [22, 55],
    regions: ['Bangkok', 'Chiang Mai'],
    persona_count: 500,
    channels: ['facebook', 'instagram', 'tiktok', 'line', 'twitter_x'],
  },
  sim_config: {
    platform: 'both',
    platform_mode: 'creator_feed',
    max_rounds: 12,
    audience_channels: ['facebook', 'instagram', 'tiktok', 'line', 'twitter_x'],
  },
}

const demoDashboard = {
  campaign: demoCampaign,
  source: {
    type: 'demo_mode',
    warning: 'Synthetic demo data for product exploration; not a live simulation result.',
  },
  kpis: {
    overall_sentiment: 41,
    conversion_probability: 68,
    social_influence: 76,
    message_resonance: 73,
    crisis_risk: 'medium',
    brand_perception_shift: 18,
    opinion_polarization: 39,
    confidence_score: 82,
  },
  timeline: [
    { round_num: 1, sentiment: 8, posts_count: 42 },
    { round_num: 2, sentiment: 20, posts_count: 55 },
    { round_num: 3, sentiment: 41, posts_count: 72 },
  ],
  segments: [
    { name: 'Urban Health Buyers', sentiment: 63, conversion_estimate: 84, size: '24%' },
    { name: 'Price-Sensitive Mass', sentiment: -12, conversion_estimate: 28, size: '27%' },
  ],
  influencers: [
    { name: '@HealthBKK', platform: 'TikTok', impact_score: 91, sentiment: 64, reach: 310000 },
  ],
  evidence: {
    confidence_score: 82,
    assumptions: ['Synthetic persona mix for smoke testing.'],
    why_this_score: ['Health-focused buyers respond well to proof-led messaging.'],
    risk_drivers: ['Premium price needs clear proof points.'],
    quotes: ['If the proof is clear, I would try it.'],
    recommended_actions: [
      { priority: 'high', description: 'Add proof cards before launch.', timeline: 'Before launch' },
    ],
  },
  action_plan: actionPlan('demo_mode'),
}

function actionPlan(sourceType = 'backend_verified') {
  return {
    version: 'structured_action_plan_v1',
    source: {
      type: sourceType,
      warning: sourceType === 'demo_mode'
        ? 'Synthetic demo data for product exploration; not a live simulation result.'
        : 'Backend KPI and campaign records were loaded; confidence still depends on source completeness.',
    },
    headline: 'Pilot proof-led creative before scaling.',
    disclaimer: 'Recommendations are deterministic planning guidance, not guaranteed market predictions.',
    sections: {
      creative_adjustment: {
        title: 'Creative Adjustment',
        items: [{
          recommendation: 'Add proof cards and segment-specific variants.',
          reason: 'Message resonance is strongest among health buyers.',
          expected_impact: 'Improves clarity before spend increases.',
          risk: 'Weak proof can increase skepticism.',
        }],
      },
      channel_allocation: {
        title: 'Channel Allocation',
        items: [{
          recommendation: 'Shift test budget toward Facebook, TikTok, and Instagram.',
          reason: 'Conversion and social influence are strongest there.',
          expected_impact: 'Finds efficient channel mix before full launch.',
          risk: 'Short tests may miss delayed conversion.',
        }],
      },
      crisis_prevention: {
        title: 'Crisis Prevention',
        items: [{
          recommendation: 'Prepare FAQ for price and sustainability claims.',
          reason: 'Premium price is the primary risk driver.',
          expected_impact: 'Reduces escalation risk.',
          risk: 'Unclear claims can trigger backlash.',
        }],
      },
      validation_plan: {
        title: 'Validation Plan',
        items: [{
          recommendation: 'Run a small audience test before national spend.',
          reason: 'Demo data is directional.',
          expected_impact: 'Validates decision confidence.',
          risk: 'Skipping validation can overfit to assumptions.',
        }],
      },
    },
  }
}

const backendDecision = {
  recommended_strategy: {
    headline: 'Launch with guardrails',
    rationale: 'Strong conversion with manageable risk.',
  },
  business_impact: {
    revenue_impact: 1100000,
    crisis_loss: 250000,
    market_share_shift: 2,
    roi: 119,
  },
  business_mapping: [],
  primary_risk: {
    segment: 'Price-Sensitive Mass',
    driver: 'Premium price needs proof.',
  },
  actions: [{ priority: 'high', description: 'Add proof cards before launch.' }],
  action_plan: actionPlan('backend_verified'),
}

const liveWarRoomResult = {
  source: {
    type: 'live_backend',
    warning: 'Backend deterministic competitor simulation. Not calibrated against live market outcomes.',
  },
  brands: ['Premium Water Launch', 'Competitor A', 'Competitor B'],
  rounds: 12,
  winner: 'Premium Water Launch',
  final_market_share: {
    'Premium Water Launch': 41.2,
    'Competitor A': 33.4,
    'Competitor B': 25.4,
  },
  share_shift: {
    'Premium Water Launch': 6.2,
    'Competitor A': -2.1,
    'Competitor B': -4.1,
  },
  timeline: [
    { round_num: 1, brand_name: 'Premium Water Launch', market_share: 35 },
    { round_num: 1, brand_name: 'Competitor A', market_share: 35 },
    { round_num: 1, brand_name: 'Competitor B', market_share: 30 },
    { round_num: 12, brand_name: 'Premium Water Launch', market_share: 41.2 },
    { round_num: 12, brand_name: 'Competitor A', market_share: 33.4 },
    { round_num: 12, brand_name: 'Competitor B', market_share: 25.4 },
  ],
  key_events: [{ round: 3, name: 'Price Cut', impact: 'Competitor price cut triggered value pressure.' }],
  expected_sentiment_movement: {
    'Premium Water Launch': 8.1,
    'Competitor A': -2.5,
    'Competitor B': -3.4,
  },
  affected_segments: ['Price-sensitive families', 'Retail shoppers'],
  amplification_channels: ['Facebook', 'TikTok', 'LINE'],
  key_drivers: ['Discount depth', 'Proof quality'],
  recommended_response: 'Defend selected segments with proof of value.',
  response_playbook: [
    { stage: 'first_2_hours', title: 'Align response cell', reason: 'Confirm claims and owners.', actions: ['Publish proof points'] },
    { stage: 'first_24_hours', title: 'Launch proof content', reason: 'Reduce value concerns.', actions: ['Brief creators'] },
    { stage: 'first_72_hours', title: 'Scale validated message', reason: 'Hold conversion gains.', actions: ['Monitor competitor response'] },
  ],
}

const demoComparatorCampaigns = [
  { id: 'cmp_demo_emotional_story', campaign_id: 'cmp_demo_emotional_story', name: 'Variant A: Emotional Storytelling', direction: 'emotional_storytelling' },
  { id: 'cmp_demo_proof_trust', campaign_id: 'cmp_demo_proof_trust', name: 'Variant B: Proof-Led Trust', direction: 'proof_led_trust' },
  { id: 'cmp_demo_price_promo', campaign_id: 'cmp_demo_price_promo', name: 'Variant C: Price / Promotion', direction: 'price_promotion' },
]

const demoComparatorResult = {
  source: {
    type: 'demo_mode',
    source_mode: 'demo_mode',
    data_basis: 'demo_fixture',
    warning: 'Comparison uses deterministic demo fixtures only.',
  },
  source_mode: 'demo_mode',
  data_basis: 'demo_fixture',
  campaign_count: 3,
  metrics_comparison: [
    {
      key: 'conversion_probability',
      label: 'Conversion Probability',
      unit: '%',
      higher_is_better: true,
      values: [
        { campaign_id: 'cmp_demo_emotional_story', value: 57 },
        { campaign_id: 'cmp_demo_proof_trust', value: 69 },
        { campaign_id: 'cmp_demo_price_promo', value: 74 },
      ],
      winner_campaign_id: 'cmp_demo_price_promo',
      winner_value: 74,
      max_diff: 17,
    },
  ],
  campaign_summaries: demoComparatorCampaigns.map((campaign, index) => ({
    campaign_id: campaign.campaign_id,
    campaign_name: campaign.name,
    metric_wins: index === 2 ? 1 : 0,
    is_overall_winner: index === 2,
    recommended_use_case: index === 1 ? 'Use for trust-led launch review.' : 'Use for directional planning.',
    trade_offs: ['Demo fixture trade-off.'],
    source: { type: 'demo_mode', source_mode: 'demo_mode', data_basis: 'demo_fixture' },
  })),
  ranked_recommendation: [
    {
      rank: 1,
      campaign_id: 'cmp_demo_price_promo',
      campaign_name: 'Variant C: Price / Promotion',
      recommendation: 'Use for tactical promotion testing.',
      reason: '1 metric wins, conversion estimate 74%, risk medium.',
      source: { type: 'demo_mode', source_mode: 'demo_mode', data_basis: 'demo_fixture' },
    },
  ],
  risk_comparison: [],
  trade_offs: [],
  overall_winner: {
    campaign_id: 'cmp_demo_price_promo',
    campaign_name: 'Variant C: Price / Promotion',
    metric_wins: 1,
    total_metrics: 1,
    recommendation: 'Use this direction as the lead route, then validate assumptions.',
    source: { type: 'demo_mode', source_mode: 'demo_mode', data_basis: 'demo_fixture' },
  },
}

const revisedBriefResult = {
  version: 'revised_brief_v2',
  campaign_id: 'demo-premium-water',
  title: 'Premium Water Launch TH — Revised Brief v2',
  original_brief: {
    objective: 'product_launch',
    description: 'Synthetic demo campaign for premium water launch.',
    target_segments: ['Thai Urban Health Buyers'],
  },
  revised_brief: {
    objective: 'product_launch',
    target_segments: ['Thai Urban Health Buyers'],
    key_message: 'Lead with hydration proof and premium taste.',
    tone_and_voice: 'Clear, proof-led, calm, and specific.',
    proof_points: ['Add proof cards before launch.'],
    channel_recommendations: ['Facebook', 'TikTok', 'Instagram'],
    risk_guardrails: ['Prepare claim substantiation and price FAQ.'],
    validation_plan: ['Run a small audience test before national spend.'],
    creative_team_notes: ['Reason: Message resonance is strongest among health buyers.'],
  },
  provenance: {
    source_mode: 'demo_mode',
    type: 'demo_mode',
    data_basis: 'demo_fixture',
    campaign_id: 'demo-premium-water',
    assumptions: ['Synthetic demo evidence.'],
    limitations: ['Not a live market test.'],
    recommended_next_validation_step: 'Review the revised brief before running another simulation.',
  },
  disclaimer: 'This revised brief is deterministic planning guidance from the action plan, not a guaranteed performance improvement.',
}

const budgetScenarioResult = {
  version: 'budget_scenario_planner_v1',
  scenario_type: 'assumption_based_budget_planning',
  objective: 'conversion',
  total_budget: 2500000,
  duration_weeks: 8,
  risk_tolerance: 'medium',
  source: {
    type: 'demo_mode',
    source_mode: 'demo_mode',
    data_basis: 'demo_fixture',
    warning: 'Demo fixture for budget-planning walkthrough; not live campaign evidence.',
  },
  allocation_ranges: [
    {
      channel: 'facebook',
      recommended_pct_midpoint: 30,
      budget_range: { low: 615000, midpoint: 750000, high: 885000 },
      weekly_range: { low: 76875, high: 110625 },
      role: 'Core reach and audience response testing.',
      risk_note: 'Validate creative fatigue and audience overlap before scaling.',
    },
    {
      channel: 'tiktok',
      recommended_pct_midpoint: 25,
      budget_range: { low: 512500, midpoint: 625000, high: 737500 },
      weekly_range: { low: 64063, high: 92188 },
      role: 'Discovery and creative resonance testing.',
      risk_note: 'Fast amplification can expose weak claims quickly.',
    },
  ],
  segment_allocation_ranges: [
    { segment: 'Urban families', recommended_pct_midpoint: 46, budget_range: { low: 943000, midpoint: 1150000, high: 1357000 } },
    { segment: 'Creator-led discovery', recommended_pct_midpoint: 27, budget_range: { low: 553500, midpoint: 675000, high: 796500 } },
  ],
  trade_offs: [
    { choice: 'Reserve validation budget', upside: 'Keeps room for message testing before scale.', risk: 'Reduces short-term reach during the first wave.' },
  ],
  confidence_level: 'medium_directional',
  confidence_score: 82,
  assumptions: ['Allocation uses deterministic objective weights and any user-supplied channel mix.'],
  limitations: ['This is not exact ROI, ROAS, CAC, sales, or market-share prediction.'],
  recommended_validation_step: 'Reserve 10-20% of the budget for a controlled creative/channel test before scaling.',
  safe_wording: ['scenario estimate', 'assumption-based planning', 'channel mix what-if', 'directional budget guidance'],
  disclaimer: 'This budget scenario is directional planning guidance, not an exact ROI, ROAS, or media-performance prediction.',
}

async function installApiMocks(page, options = {}) {
  await page.addInitScript(() => {
    localStorage.removeItem('3c-auth-token')
    localStorage.removeItem('3c-api-key')
    sessionStorage.removeItem('3c-auth-token')
    sessionStorage.removeItem('3c-api-key')
    localStorage.setItem('3c-lang', 'en')
    localStorage.setItem('3c-theme', 'dark')
  })

  await page.route((url) => url.pathname.startsWith('/api/'), async (route) => {
    const url = new URL(route.request().url())
    const path = url.pathname

    if (path === '/api/demo/campaigns') {
      return json(route, { success: true, data: [demoCampaign] })
    }
    if (path === '/api/demo/campaigns/demo-premium-water/dashboard') {
      return json(route, { success: true, data: demoDashboard })
    }
    if (path === '/api/brief/quality') {
      return json(route, {
        success: true,
        data: {
          score: 100,
          level: 'strong',
          confidence_impact: 'low',
          missing_fields: [],
          recommendations: [],
          known_limitations: [],
        },
      })
    }
    if (path === '/api/brief/revise') {
      return json(route, { success: true, data: revisedBriefResult })
    }
    if (path === '/api/campaign') {
      return json(route, { success: true, data: [demoCampaign] })
    }
    if (path === '/api/campaign/cmp-live') {
      return json(route, { success: true, data: { ...demoCampaign, id: 'cmp-live', name: 'Backend Verified Campaign' } })
    }
    if (path === '/api/dashboard/campaign/cmp-live/kpi') {
      return json(route, { success: true, data: { ...demoDashboard.kpis, action_plan: actionPlan('backend_verified') } })
    }
    if (path === '/api/dashboard/campaign/cmp-live/timeline') {
      return json(route, { success: true, data: { timeline: demoDashboard.timeline } })
    }
    if (path === '/api/dashboard/campaign/cmp-live/segments') {
      return json(route, { success: true, data: { segments: demoDashboard.segments } })
    }
    if (path === '/api/decision/analyze') {
      return json(route, { success: true, data: backendDecision })
    }
    if (path === '/api/decision/what-if') {
      return json(route, { success: true, data: { kpi_deltas: {}, verdict: 'Controlled pilot' } })
    }
    if (path === '/api/decision/budget-scenario') {
      return json(route, { success: true, data: budgetScenarioResult })
    }
    if (path === '/api/comparator/demo/campaigns') {
      return json(route, {
        success: true,
        data: demoComparatorCampaigns,
        source: demoComparatorResult.source,
      })
    }
    if (path === '/api/comparator/demo/compare') {
      return json(route, { success: true, data: demoComparatorResult })
    }
    if (path === '/api/competitor/simulate') {
      if (options.failCompetitorSimulation) {
        return json(route, { success: false, error: 'Smoke-test backend unavailable' }, 503)
      }
      return json(route, { success: true, data: liveWarRoomResult })
    }
    if (path === '/api/status') {
      return json(route, {
        success: true,
        data: {
          status: 'ok',
          services: [{ key: 'api', label: 'Backend API', status: 'ok', detail: 'Mocked for e2e smoke test' }],
          estimate: { cost_per_100_personas_usd: 0, default_model: 'demo' },
        },
      })
    }
    if (path === '/api/settings/providers') {
      return json(route, {
        success: true,
        data: {
          llm_providers: [{ value: 'ollama', label: 'Ollama' }],
          embedding_providers: [{ value: 'ollama', label: 'Ollama' }],
          graph_db_modes: [{ value: 'local', label: 'Local Neo4j' }],
        },
      })
    }
    if (path === '/api/settings/readiness') {
      return json(route, {
        success: true,
        data: {
          mode: 'demo',
          ready: true,
          checks: {
            llm: { status: 'skipped', safe_detail: 'Demo mode does not require an LLM provider.', issues: [] },
            embedding: { status: 'skipped', safe_detail: 'Demo mode does not require an embedding provider.', issues: [] },
            neo4j: { status: 'skipped', safe_detail: 'Demo mode does not require Neo4j.', issues: [] },
          },
          sample_simulation: { status: 'available', label: 'Try Sample Campaign', detail: 'Use a deterministic demo campaign.' },
          cost_estimate: { per_100_personas: 0, label: 'Directional estimate only', disclaimer: 'Estimate only.' },
        },
      })
    }
    if (path === '/api/industry/templates') {
      return json(route, { success: true, data: [] })
    }

    return json(route, { success: false, error: `Unhandled e2e route: ${path}` }, 404)
  })
}

async function json(route, body, status = 200) {
  await route.fulfill({
    status,
    contentType: 'application/json',
    body: JSON.stringify(body),
  })
}

test.beforeEach(async ({ page }) => {
  await installApiMocks(page)
})

test('home page presents the product entry points', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByRole('heading', { name: /Simulate Public Opinion/i })).toBeVisible()
  await expect(page.getByRole('link', { name: /Campaigns/i })).toBeVisible()
  await expect(page.getByRole('link', { name: /Try Sample Campaign/i })).toBeVisible()
})

test('demo dashboard labels synthetic demo evidence', async ({ page }) => {
  await page.goto('/dashboard/demo-premium-water')

  await expect(page.getByRole('heading', { name: /Premium Water Launch TH/i }).first()).toBeVisible()
  await expect(page.getByText('Demo Mode').first()).toBeVisible()
  await expect(page.getByText('Confidence & Evidence')).toBeVisible()
  await expect(page.getByText('Synthetic demo data for product exploration')).toBeVisible()
})

test('backend dashboard route shows backend verified source', async ({ page }) => {
  await page.addInitScript(() => sessionStorage.setItem('3c-auth-token', 'smoke-test-token'))
  await page.goto('/dashboard/cmp-live')

  await expect(page.getByRole('heading', { name: /Backend Verified Campaign/i }).first()).toBeVisible()
  await expect(page.getByText('Backend Verified').first()).toBeVisible()
  await expect(page.getByText('Confidence & Evidence')).toBeVisible()
})

test('action plan section inherits source labeling', async ({ page }) => {
  await page.goto('/dashboard/demo-premium-water')
  await page.getByText('Action Plan', { exact: false }).first().scrollIntoViewIfNeeded()

  await expect(page.getByText('Action Plan', { exact: false }).first()).toBeVisible()
  await expect(page.getByText('Demo Mode').first()).toBeVisible()
  await expect(page.getByText('Creative Adjustment')).toBeVisible()
  await expect(page.getByText('Validation Plan')).toBeVisible()
})

test('dashboard can create a revised brief from the action plan', async ({ page }) => {
  await page.goto('/dashboard/demo-premium-water')
  await page.getByText('Action Plan', { exact: false }).first().scrollIntoViewIfNeeded()
  await page.getByRole('button', { name: 'Create Revised Brief' }).click()

  await expect(page.getByText('Brief v2').first()).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Revised Brief', exact: true })).toBeVisible()
  await expect(page.getByText('Lead with hydration proof and premium taste.')).toBeVisible()
  await expect(page.getByText('Review the revised brief before running another simulation.')).toBeVisible()
})

test('brief quality score can be checked without live providers', async ({ page }) => {
  await page.goto('/campaigns')
  await page.getByRole('button', { name: /New Campaign/i }).click()
  await page.getByText(/Skip/i).click()

  await page.getByPlaceholder('e.g. Product Launch Q2 2026').fill('Premium Water Launch TH')
  await page.getByPlaceholder('Brief description of the campaign objectives...').fill('Launch a premium hydration campaign.')
  await page.locator('select.form-input').selectOption('product_launch')
  await page.getByPlaceholder('e.g. Thai Urban Millennials').fill('Thai urban families')
  await page.getByPlaceholder('e.g. 8 weeks, Q3 launch window').fill('8 weeks')
  await page.getByPlaceholder('e.g. ฿2M-3M media spend').fill('THB 2M-3M')
  await page.getByPlaceholder('e.g. conversion, sentiment, brand lift').fill('Brand lift')
  await page.getByPlaceholder('Key rivals, pricing pressure, likely counter-moves...').fill('Premium water rivals')
  await page.getByPlaceholder('Tone rules, required proof, must-not-say claims...').fill('Avoid medical claims')
  await page.getByPlaceholder('Regulatory, PR, legal, safety, or claim risks...').fill('Claim review required')
  await page.getByRole('button', { name: 'Check Brief' }).click()

  await expect(page.getByText('Brief Quality Score')).toBeVisible()
  await expect(page.getByText('100%')).toBeVisible()
  await expect(page.getByText('Strong brief')).toBeVisible()
})

test('comparator uses backend demo fixtures and source labels', async ({ page }) => {
  await page.goto('/comparator')

  await expect(page.getByRole('heading', { name: /A\/B Message Comparator/i })).toBeVisible()
  await expect(page.getByText('Demo Mode').first()).toBeVisible()
  await page.getByText('Variant A: Emotional Storytelling').click()
  await page.getByText('Variant B: Proof-Led Trust').click()
  await page.getByText('Variant C: Price / Promotion').click()
  await page.getByRole('button', { name: /Compare Campaigns/i }).click()

  await expect(page.getByText('Variant C: Price / Promotion').first()).toBeVisible()
  await expect(page.getByText('Ranked Recommendation')).toBeVisible()
  await expect(page.getByText('Comparison uses deterministic demo fixtures only.')).toBeVisible()
})

test('war room displays live backend source for backend simulation', async ({ page }) => {
  await page.goto('/war-room')

  await expect(page.getByRole('heading', { name: /Competitor War Room/i })).toBeVisible()
  await expect(page.getByText('Live Backend').first()).toBeVisible()
  await expect(page.getByText('Decision Console')).toBeVisible()
  await expect(page.getByText('Expected Sentiment Movement')).toBeVisible()
})

test('budget planner returns directional scenario guidance with source label', async ({ page }) => {
  await page.goto('/budget-planner')

  await expect(page.getByRole('heading', { name: /Budget Scenario Planner/i })).toBeVisible()
  await expect(page.getByText('Scenario Estimate').first()).toBeVisible()
  await expect(page.getByText('Demo Mode').first()).toBeVisible()
  await expect(page.getByText('Suggested Allocation Range by Channel')).toBeVisible()
  await expect(page.getByText('Reserve 10-20% of the budget')).toBeVisible()
  await expect(page.getByText('not exact ROI').first()).toBeVisible()
  await expect(page.getByText(/not live campaign evidence/i).first()).toBeVisible()
})

test('war room requires explicit local estimate fallback when backend fails', async ({ page }) => {
  await page.unroute((url) => url.pathname.startsWith('/api/'))
  await installApiMocks(page, { failCompetitorSimulation: true })
  await page.goto('/war-room')

  await expect(page.getByText('Backend War Room simulation was unavailable')).toBeVisible()
  await page.getByRole('button', { name: 'Run Local Estimate' }).click()
  await expect(page.getByText('Local Estimate').first()).toBeVisible()
})

test('settings wizard shows demo readiness without secrets', async ({ page }) => {
  await page.goto('/settings')

  await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible()
  await expect(page.getByText('Setup Wizard')).toBeVisible()
  await expect(page.getByText('Demo only').first()).toBeVisible()
  await expect(page.getByText('Setup looks ready for this mode.')).toBeVisible()
  await expect(page.getByText('Cost Estimate').first()).toBeVisible()
})

test('feedback widget emits sanitized local analytics event', async ({ page }) => {
  await page.goto('/')
  await page.evaluate(() => {
    window.__analyticsEvents = []
    window.addEventListener('3c:analytics', (event) => {
      window.__analyticsEvents.push(event.detail)
    })
  })

  await page.getByRole('button', { name: 'Feedback' }).click()
  await page.getByRole('button', { name: '4' }).click()
  await page.locator('#feedback-confusion').selectOption('source_labels')
  await page.getByRole('button', { name: 'Send feedback' }).click()

  const feedbackEvent = await page.waitForFunction(() => (
    window.__analyticsEvents || []
  ).find((event) => event.event === 'feedback_submitted'))

  const event = await feedbackEvent.jsonValue()
  expect(event.properties).toEqual({
    rating: 4,
    confusion_area: 'source_labels',
    route_bucket: 'home',
  })
  expect(JSON.stringify(event)).not.toContain('api_key')
  expect(JSON.stringify(event)).not.toContain('campaign brief')
})
