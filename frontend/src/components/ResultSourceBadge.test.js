import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import ResultSourceBadge from './ResultSourceBadge.vue'
import { testI18n } from '@/test/helpers'

function render(source, warning = '') {
  return mount(ResultSourceBadge, {
    props: { source, warning },
    global: { plugins: [testI18n()] },
  })
}

describe('ResultSourceBadge', () => {
  it.each([
    ['demo_mode', 'Demo Mode', 'source-demo'],
    ['local_estimate', 'Local Estimate', 'source-warning'],
    ['live_backend', 'Live Backend', 'source-live'],
    ['backend_verified', 'Backend Verified', 'source-verified'],
    ['unknown', 'Unknown Source', 'source-unknown'],
  ])('renders %s as %s', (source, label, className) => {
    const wrapper = render(source)

    expect(wrapper.text()).toContain(label)
    expect(wrapper.classes()).toContain(className)
  })

  it('falls back to Unknown Source and shows warnings', () => {
    const wrapper = render('unexpected_source', 'Treat this cautiously.')

    expect(wrapper.text()).toContain('Unknown Source')
    expect(wrapper.text()).toContain('Treat this cautiously.')
    expect(wrapper.classes()).toContain('source-unknown')
  })
})
