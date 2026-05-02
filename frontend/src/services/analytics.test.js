import assert from 'node:assert/strict'
import test from 'node:test'

import { isAllowedAnalyticsEvent, sanitizeAnalyticsPayload } from './analytics.js'

test('analytics allowlist includes pilot journey events', () => {
  [
    'demo_dashboard_opened',
    'brief_quality_scored',
    'simulation_started',
    'simulation_completed',
    'dashboard_viewed',
    'action_plan_viewed',
    'revised_brief_created',
    'comparator_used',
    'budget_scenario_run',
    'export_clicked',
    'war_room_scenario_run',
    'settings_provider_test_failed',
    'feedback_submitted',
  ].forEach((eventName) => {
    assert.equal(isAllowedAnalyticsEvent(eventName), true)
  })

  assert.equal(isAllowedAnalyticsEvent('raw_campaign_brief_uploaded'), false)
})

test('analytics payload sanitizer drops sensitive fields and redacts token-like values', () => {
  const sanitized = sanitizeAnalyticsPayload({
    route_bucket: 'dashboard',
    source_mode: 'demo_mode',
    rating: 4,
    campaign_name: 'Private campaign name',
    brief_text: 'Raw brief content',
    api_key: 'sk-test-secret-1234567890',
    provider_detail: 'failed with sk-ant-secret-1234567890 in payload',
    nested: { raw: 'should not be serialized' },
    list: ['safe', 'sk-or-secret-1234567890'],
  })

  assert.deepEqual(sanitized, {
    route_bucket: 'dashboard',
    source_mode: 'demo_mode',
    rating: 4,
    provider_detail: 'failed with [redacted] in payload',
    list: ['safe', '[redacted]'],
  })
})
