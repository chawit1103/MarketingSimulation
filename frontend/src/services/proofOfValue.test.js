import { describe, expect, it } from 'vitest'

import {
  buildProofOfValuePackage,
  defaultProofOfValueIntake,
  validateProofOfValueIntake,
} from './proofOfValue'

function approvedIntake() {
  const intake = defaultProofOfValueIntake()
  Object.assign(intake, {
    campaignNameOrCode: 'POV-ENERGY-001',
    productService: 'Community energy plan',
    objective: 'Increase trust before launch',
    targetSegment: 'Urban homeowners',
    marketContext: 'Competitive retail energy market',
    channelPlan: 'Owned social, search, partner events',
    budgetBand: 'Medium planning band',
    competitorContext: 'Incumbent utility and challenger brands',
    creativeA: 'Trust proof points',
    creativeB: 'Savings education',
    creativeC: 'Community reliability',
    riskConcerns: 'Greenwashing sensitivity',
    successKpis: 'Awareness lift, qualified inquiries',
    aggregateActuals: 'Aggregate reach band only',
  })
  Object.keys(intake.confirmations).forEach((key) => {
    intake.confirmations[key] = true
  })
  return intake
}

function expectBlockedAndRedacted(fieldKey, payloadKey, unsafeValue, expectedReason) {
  const intake = approvedIntake()
  intake[fieldKey] = unsafeValue

  const validation = validateProofOfValueIntake(intake)
  const pack = buildProofOfValuePackage(intake)
  const payloadJson = JSON.stringify(pack.intake_summary)

  expect(validation.ready).toBe(false)
  expect(validation.unsafeSignals).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        key: fieldKey,
        reason: expect.stringContaining(expectedReason),
      }),
    ]),
  )
  expect(pack.intake_summary[payloadKey]).toBe('[blocked: unsafe intake signal]')
  expect(payloadJson).not.toContain(unsafeValue)
}

function expectReadyWith(fieldKey, safeValue) {
  const intake = approvedIntake()
  intake[fieldKey] = safeValue

  const validation = validateProofOfValueIntake(intake)
  const pack = buildProofOfValuePackage(intake)

  expect(validation.ready).toBe(true)
  expect(validation.unsafeSignals).toEqual([])
  expect(pack.status).toBe('ready_for_operator_review')
}

describe('proof-of-value intake workflow', () => {
  it('builds a ready package from approved business context', () => {
    const intake = approvedIntake()
    const validation = validateProofOfValueIntake(intake)
    const pack = buildProofOfValuePackage(intake)

    expect(validation.ready).toBe(true)
    expect(pack.status).toBe('ready_for_operator_review')
    expect(pack.source.source_mode).toBe('local_estimate')
    expect(pack.source.data_basis).toBe('customer_approved_brief')
    expect(pack.source.disclaimer).toBe('Decision-support estimate, not a guaranteed prediction.')
    expect(pack.deliverables).toContain('Strategy Pack PPTX')
  })

  it('blocks missing approvals and flags unsafe intake signals', () => {
    const intake = approvedIntake()
    intake.confirmations.noPii = false
    intake.marketContext = 'Includes contact person@example.test from a CRM export'
    intake.riskConcerns = 'Operator says an API key would be needed'

    const validation = validateProofOfValueIntake(intake)
    const pack = buildProofOfValuePackage(intake)

    expect(validation.ready).toBe(false)
    expect(validation.missingConfirmations).toContain('No PII')
    expect(validation.unsafeSignals.map((item) => item.field)).toContain('Market context')
    expect(validation.unsafeSignals.map((item) => item.field)).toContain('Risk concerns')
    expect(JSON.stringify(pack.intake_summary)).not.toContain('person@example.test')
    expect(JSON.stringify(pack.intake_summary)).not.toContain('API key')
    expect(pack.intake_summary.market_context).toBe('[blocked: unsafe intake signal]')
    expect(pack.intake_summary.risk_concerns).toBe('[blocked: unsafe intake signal]')
  })

  it('flags and redacts phone-like values', () => {
    const phoneExamples = [
      '+66 81 234 5678',
      '081-234-5678',
      '(02) 123 4567',
      'phone: 0812345678',
    ]

    for (const phone of phoneExamples) {
      expectBlockedAndRedacted(
        'targetSegment',
        'target_segment',
        `Pilot decision maker ${phone}`,
        'Phone-like',
      )
    }
  })

  it('does not flag ISO dates or normal date ranges as phone-like values', () => {
    expectReadyWith('marketContext', 'Launch runs 2026-06-01 to 2026-08-31')
  })

  it('flags and redacts SSN or national-ID-like values', () => {
    expectBlockedAndRedacted(
      'marketContext',
      'market_context',
      'Historical note includes SSN 000-00-0000',
      'National ID',
    )
  })

  it('flags and redacts long account or customer identifiers', () => {
    expectBlockedAndRedacted(
      'competitorContext',
      'competitor_context',
      'Compare against customer id CUST-PLACEHOLDER-1234567890',
      'Long account',
    )
  })

  it('does not flag safe marketing prose containing contact language', () => {
    expectReadyWith('marketContext', 'Audience prefers in-store contact during launch')
    expectReadyWith('channelPlan', 'Contact strategy uses LINE and retail staff training')
  })

  it('flags and redacts labeled contact identifiers', () => {
    const contactExamples = [
      ['targetSegment', 'target_segment', 'phone: 0812345678'],
      ['riskConcerns', 'risk_concerns', 'mobile: +66 81 234 5678'],
      ['channelPlan', 'channel_plan', 'line id: customer_abc123'],
      ['competitorContext', 'competitor_context', 'contact #: CUST123456789'],
    ]

    for (const [fieldKey, payloadKey, value] of contactExamples) {
      expectBlockedAndRedacted(fieldKey, payloadKey, value, 'Personal contact')
    }
  })

  it('flags and redacts sk-style placeholder tokens', () => {
    const fakeToken = ['sk', 'FAKEPLACEHOLDER'].join('-')
    expectBlockedAndRedacted(
      'riskConcerns',
      'risk_concerns',
      `Operator pasted ${fakeToken} by mistake`,
      'Key-shaped',
    )
  })

  it('flags and redacts ghp-style placeholder tokens', () => {
    const fakeToken = ['ghp', 'FAKEPLACEHOLDER'].join('_')
    expectBlockedAndRedacted(
      'creativeA',
      'creative_direction_a',
      `Do not use ${fakeToken}`,
      'GitHub token-like',
    )
  })

  it('flags and redacts Bearer-style placeholder tokens', () => {
    const fakeToken = ['Bearer', 'FAKEPLACEHOLDER'].join(' ')
    expectBlockedAndRedacted(
      'aggregateActuals',
      'aggregate_actuals',
      `Aggregate note accidentally included ${fakeToken}`,
      'Bearer token-like',
    )
  })
})
