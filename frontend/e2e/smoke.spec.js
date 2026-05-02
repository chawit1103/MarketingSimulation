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

test('war room displays live backend source for backend simulation', async ({ page }) => {
  await page.goto('/war-room')

  await expect(page.getByRole('heading', { name: /Competitor War Room/i })).toBeVisible()
  await expect(page.getByText('Live Backend').first()).toBeVisible()
  await expect(page.getByText('Decision Console')).toBeVisible()
  await expect(page.getByText('Expected Sentiment Movement')).toBeVisible()
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
