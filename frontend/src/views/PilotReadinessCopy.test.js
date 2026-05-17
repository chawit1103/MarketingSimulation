import { describe, expect, it } from 'vitest'

import en from '@/locales/en.json'

describe('Customer pilot readiness wording', () => {
  it('frames controlled pilots without production-readiness claims', () => {
    const pilotCopy = [
      en.dashboard.decisionHeadlinePilot,
      en.dashboard.decisionNextPilot,
      en.dashboard.verdictPilot,
      en.warRoom.decisionPilot,
      en.warRoom.decisionPilotReason,
      en.warRoom.recommendPilot,
      en.warRoom.recommendPilotSummary,
    ].join(' ')

    expect(pilotCopy).toContain('controlled pilot')
    expect(pilotCopy).toContain('limited pilot')
    expect(pilotCopy).toContain('monitoring')
    expect(pilotCopy).not.toMatch(/production[- ]ready/i)
    expect(pilotCopy).not.toMatch(/ready for production/i)
    expect(pilotCopy).not.toMatch(/public pilot/i)
    expect(pilotCopy).not.toMatch(/guaranteed prediction/i)
    expect(pilotCopy).not.toMatch(/exact roi|exact roas/i)
  })
})
