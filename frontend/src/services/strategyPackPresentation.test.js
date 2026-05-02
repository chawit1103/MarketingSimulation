import { describe, expect, it } from 'vitest'

import {
  normalizeStrategyPackSource,
  strategyPackSlideSourceLine,
  strategyPackValidationSummary,
} from './strategyPackPresentation'

describe('Strategy Pack source/provenance rendering', () => {
  const pack = {
    disclaimer: 'Scenario planning only; not guaranteed outcomes.',
    source: {
      source_mode: 'demo_mode',
      data_basis: 'demo_fixture',
      run_id: 'demo:premium-water',
      confidence_level: 'medium',
      recommended_next_validation_step: 'Validate with a controlled audience test.',
      limitations: ['Synthetic demo fixture.', 'No live social listening.'],
    },
  }

  it('normalizes strategy pack source metadata for display', () => {
    expect(normalizeStrategyPackSource(pack.source)).toEqual({
      source_mode: 'demo_mode',
      label: 'Demo Mode',
      data_basis: 'demo_fixture',
      run_id: 'demo:premium-water',
      confidence_level: 'medium',
      recommended_next_validation_step: 'Validate with a controlled audience test.',
      limitations: ['Synthetic demo fixture.', 'No live social listening.'],
    })
  })

  it('renders a compact provenance line for every slide footer', () => {
    expect(strategyPackSlideSourceLine(pack)).toBe(
      'Source: demo_mode | Basis: demo_fixture | Run ID: demo:premium-water | Confidence: medium'
    )
  })

  it('renders limitations and recommended validation without guarantee language', () => {
    const summary = strategyPackValidationSummary(pack)

    expect(summary.title).toBe('Limitations & Recommended Validation')
    expect(summary.source_line).toContain('Source: demo_mode')
    expect(summary.recommended_validation_step).toBe('Validate with a controlled audience test.')
    expect(summary.limitations).toHaveLength(2)
    expect(summary.disclaimer).toContain('not guaranteed outcomes')
  })
})
