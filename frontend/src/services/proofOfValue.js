export const proofOfValueTextFields = [
  { key: 'campaignNameOrCode', payloadKey: 'campaign_name_or_code', label: 'Campaign name or anonymized code', required: true },
  { key: 'productService', payloadKey: 'product_service', label: 'Product/service', required: true },
  { key: 'objective', payloadKey: 'objective', label: 'Objective', required: true },
  { key: 'targetSegment', payloadKey: 'target_segment', label: 'Target segment', required: true },
  { key: 'marketContext', payloadKey: 'market_context', label: 'Market context', required: true },
  { key: 'channelPlan', payloadKey: 'channel_plan', label: 'Channel plan', required: true },
  { key: 'budgetBand', payloadKey: 'budget_band', label: 'Budget band', required: true },
  { key: 'competitorContext', payloadKey: 'competitor_context', label: 'Competitor context', required: true },
  { key: 'creativeA', payloadKey: 'creative_direction_a', label: 'Creative direction A', required: true },
  { key: 'creativeB', payloadKey: 'creative_direction_b', label: 'Creative direction B', required: true },
  { key: 'creativeC', payloadKey: 'creative_direction_c', label: 'Creative direction C', required: true },
  { key: 'riskConcerns', payloadKey: 'risk_concerns', label: 'Risk concerns', required: true },
  { key: 'successKpis', payloadKey: 'success_kpis', label: 'Success KPIs', required: true },
  { key: 'aggregateActuals', payloadKey: 'aggregate_actuals', label: 'Optional aggregate actuals', required: false },
]

export const proofOfValueConfirmations = [
  { key: 'approvedForPilotUse', label: 'Customer approved for pilot use', required: true },
  { key: 'noPii', label: 'No PII', required: true },
  { key: 'noRawCrmRecords', label: 'No raw CRM records', required: true },
  { key: 'noCustomerLists', label: 'No customer lists', required: true },
  { key: 'noSecrets', label: 'No secrets', required: true },
  { key: 'noLiveIntegrations', label: 'No live integrations', required: true },
]

const unsafePatterns = [
  {
    reason: 'Email-like text is not allowed in proof-of-value intake.',
    pattern: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i,
  },
  {
    reason: 'Raw CRM, contact, or customer-list language must be removed.',
    pattern: /\b(raw crm|crm export|customer list|email list|phone list|contact list|subscriber list|row-level|individual-level|household-level|account-level)\b/i,
  },
  {
    reason: 'Secrets or credential language must be removed.',
    pattern: /\b(api key|oauth|token|password|private key|client secret|graph credential|neo4j password|provider secret)\b/i,
  },
  {
    reason: 'Live integration language must be removed for proof-of-value sessions.',
    pattern: /\b(live crm|salesforce sync|hubspot sync|social listening integration|ad platform integration|marketing automation integration|live integration)\b/i,
  },
]

export function defaultProofOfValueIntake() {
  return {
    campaignNameOrCode: '',
    productService: '',
    objective: '',
    targetSegment: '',
    marketContext: '',
    channelPlan: '',
    budgetBand: '',
    competitorContext: '',
    creativeA: '',
    creativeB: '',
    creativeC: '',
    riskConcerns: '',
    successKpis: '',
    aggregateActuals: '',
    confirmations: {
      approvedForPilotUse: false,
      noPii: false,
      noRawCrmRecords: false,
      noCustomerLists: false,
      noSecrets: false,
      noLiveIntegrations: false,
      aggregateActualsApproved: false,
    },
  }
}

function fieldValue(intake, key) {
  return String(intake?.[key] || '').trim()
}

export function validateProofOfValueIntake(intake) {
  const missingFields = proofOfValueTextFields
    .filter((field) => field.required && !fieldValue(intake, field.key))
    .map((field) => field.label)

  const confirmations = intake?.confirmations || {}
  const missingConfirmations = proofOfValueConfirmations
    .filter((item) => item.required && confirmations[item.key] !== true)
    .map((item) => item.label)

  if (fieldValue(intake, 'aggregateActuals') && confirmations.aggregateActualsApproved !== true) {
    missingConfirmations.push('Aggregate actuals are approved and aggregate-only')
  }

  const unsafeSignals = []
  for (const field of proofOfValueTextFields) {
    const value = fieldValue(intake, field.key)
    if (!value) continue

    for (const unsafe of unsafePatterns) {
      if (unsafe.pattern.test(value)) {
        unsafeSignals.push({
          field: field.label,
          key: field.key,
          reason: unsafe.reason,
        })
      }
    }
  }

  return {
    ready: missingFields.length === 0 && missingConfirmations.length === 0 && unsafeSignals.length === 0,
    missingFields,
    missingConfirmations,
    unsafeSignals,
  }
}

function safeValue(intake, field, unsafeKeys) {
  if (unsafeKeys.has(field.key)) return '[blocked: unsafe intake signal]'
  return fieldValue(intake, field.key) || null
}

export function buildProofOfValuePackage(intake) {
  const validation = validateProofOfValueIntake(intake)
  const unsafeKeys = new Set(validation.unsafeSignals.map((item) => item.key))
  const intakeSummary = {}

  for (const field of proofOfValueTextFields) {
    intakeSummary[field.payloadKey] = safeValue(intake, field, unsafeKeys)
  }

  return {
    version: 'proof_of_value_intake_v1',
    status: validation.ready ? 'ready_for_operator_review' : 'blocked_until_safe_and_approved',
    source: {
      source_mode: 'local_estimate',
      data_basis: 'customer_approved_brief',
      confidence_level: 'operator_review_required',
      disclaimer: 'Decision-support estimate, not a guaranteed prediction.',
    },
    guardrails: [
      'No PII',
      'No raw CRM records',
      'No customer lists',
      'No secrets',
      'No live integrations',
      'Visible source/provenance labels required',
      'No production-readiness claims',
      'No guaranteed prediction',
      'No exact ROI/ROAS prediction',
    ],
    validation,
    intake_summary: intakeSummary,
    deliverables: [
      'Brief Quality Score',
      'Campaign Simulation Summary',
      'A/B/C Creative Comparator result',
      'Risk and Crisis Watchouts',
      'Revised Brief v2',
      'Strategy Pack PPTX',
      'Optional Actual vs Estimate comparison for approved aggregate actuals',
    ],
    workflow_steps: [
      'Confirm approved intake and guardrails',
      'Score brief quality',
      'Run campaign simulation summary',
      'Compare A/B/C creative directions',
      'Review risk and crisis watchouts',
      'Create Revised Brief v2',
      'Prepare Strategy Pack PPTX',
      'Review limitations and recommended validation',
    ],
  }
}
