const SOURCE_LABELS = {
  demo_mode: 'Demo Mode',
  local_estimate: 'Local Estimate',
  live_backend: 'Live Backend',
  backend_verified: 'Backend Verified',
  unknown: 'Unknown Source',
}

export function normalizeStrategyPackSource(source = {}) {
  const sourceMode = source.source_mode || source.type || 'unknown'
  const normalizedMode = Object.hasOwn(SOURCE_LABELS, sourceMode) ? sourceMode : 'unknown'
  return {
    source_mode: normalizedMode,
    label: SOURCE_LABELS[normalizedMode],
    data_basis: source.data_basis || 'unknown',
    run_id: source.run_id || 'not available',
    confidence_level: source.confidence_level || 'unknown',
    recommended_next_validation_step:
      source.recommended_next_validation_step || 'Validate with real audience evidence before approval.',
    limitations: Array.isArray(source.limitations) ? source.limitations : [],
  }
}

export function strategyPackSlideSourceLine(pack = {}) {
  const source = normalizeStrategyPackSource(pack.source)
  return `Source: ${source.source_mode} | Basis: ${source.data_basis} | Run ID: ${source.run_id} | Confidence: ${source.confidence_level}`
}

export function strategyPackValidationSummary(pack = {}) {
  const source = normalizeStrategyPackSource(pack.source)
  return {
    title: 'Limitations & Recommended Validation',
    source_line: strategyPackSlideSourceLine(pack),
    recommended_validation_step: source.recommended_next_validation_step,
    limitations: source.limitations,
    disclaimer:
      pack.disclaimer || 'Decision-support scenario planning, not a guaranteed market prediction.',
  }
}
