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
})
