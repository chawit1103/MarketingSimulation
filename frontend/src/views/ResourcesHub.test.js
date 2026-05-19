import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { RouterView } from 'vue-router'

import router from '@/router'
import ResourcesHub from './ResourcesHub.vue'
import { flushPromises } from '@/test/helpers'

function mountView() {
  return mount(ResourcesHub)
}

describe('ResourcesHub', () => {
  it('renders from the /resources route', async () => {
    await router.push('/resources')
    await router.isReady()

    const wrapper = mount({ components: { RouterView }, template: '<RouterView />' }, {
      global: { plugins: [router] },
    })
    await flushPromises()

    expect(wrapper.text()).toContain('Proof-of-Value Resource Hub')
    expect(wrapper.text()).toContain('Start Here: First Customer')
    expect(wrapper.text()).toContain('Public Policy / Strategic Command')
    expect(wrapper.text()).toContain('Customer Proof-of-Value')
  })

  it('shows readiness boundaries and proof-of-value guardrails', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('Local demo')
    expect(text).toContain('ready')
    expect(text).toContain('Controlled private pilot')
    expect(text).toContain('conditional candidate')
    expect(text).toContain('Public pilot')
    expect(text).toContain('Public internet exposure')
    expect(text).toContain('Production customer deployment')
    expect(text).toContain('blocked')
    expect(text).toContain('No PII')
    expect(text).toContain('No raw CRM records')
    expect(text).toContain('No customer lists')
    expect(text).toContain('No secrets')
    expect(text).toContain('No live integrations')
    expect(text).toContain('Decision-support estimate only')
  })

  it('organizes curated documentation links without duplicating full docs', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('Start Here: First Customer')
    expect(text).toContain('Public Policy / Strategic Command')
    expect(text).toContain('Customer Proof-of-Value')
    expect(text).toContain('Prepare Brief with AI')
    expect(text).toContain('Sales Materials')
    expect(text).toContain('Operator Checklist')
    expect(text).toContain('Data Safety and Guardrails')
    expect(text).toContain('Sample Packages')

    const hrefs = wrapper.findAll('a').map((link) => link.attributes('href'))
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/PROOF_OF_VALUE_OUTREACH_PACK.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/FOUNDER_FIRST_CUSTOMER_CLOSE_PACK.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/PROOF_OF_VALUE_ONE_PAGE_COPY.md')
    expect(hrefs).toContain('/proof-of-value')
    expect(hrefs).toContain('/strategic-command')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/STRATEGIC_COMMAND_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/PUBLIC_POLICY_POV_INTAKE_TEMPLATE_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/STRATEGIC_COMMAND_DEMO_SCRIPT_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/STRATEGIC_COMMAND_SAFETY_BOUNDARIES_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/strategic-command/PM25_DUST_FREE_ROOM_INPUT_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/strategic-command/PM25_EXECUTIVE_STRATEGY_PACK_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/strategic-command/PM25_DEMO_SCRIPT_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/strategic-command/PM25_SCREENSHOT_GUIDE_TH.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/PROOF_OF_VALUE_CUSTOMER_OUTPUT_TEMPLATE.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/PROOF_OF_VALUE_SALES_OFFER.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/CUSTOMER_BRIEF_INTAKE_TEMPLATE.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/AI_RESEARCH_PROMPT_PACK.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/POV_INTAKE_IMPORT_TEMPLATE.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/RAW_BRIEF_TO_POV_EXAMPLE.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/PROOF_OF_VALUE_OPERATOR_CHECKLIST.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/CUSTOMER_DATA_HANDLING.md')
    expect(hrefs).toContain('https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/docs/SAMPLE_PROOF_OF_VALUE_PACKAGE.md')
  })

  it('does not introduce unsafe customer-facing claims', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).not.toMatch(/production[- ]ready/i)
    expect(text).not.toMatch(/ready for production/i)
    expect(text).not.toMatch(/guaranteed prediction/i)
    expect(text).not.toMatch(/exact roi|exact roas/i)
  })
})
