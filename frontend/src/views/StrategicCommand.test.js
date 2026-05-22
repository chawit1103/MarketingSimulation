import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { RouterView } from 'vue-router'

import router from '@/router'
import { flushPromises } from '@/test/helpers'
import StrategicCommand from './StrategicCommand.vue'

function mountView() {
  return mount(StrategicCommand, {
    global: {
      plugins: [router],
    },
  })
}

describe('StrategicCommand', () => {
  it('renders from the /strategic-command route', async () => {
    await router.push('/strategic-command')
    await router.isReady()

    const wrapper = mount({ components: { RouterView }, template: '<RouterView />' }, {
      global: { plugins: [router] },
    })
    await flushPromises()

    expect(wrapper.text()).toContain('CivicSense')
    expect(wrapper.text()).toContain('ระบบจำลองเสียงสะท้อนสาธารณะเพื่อการสื่อสารนโยบายอย่างรับผิดชอบ')
  })

  it('shows the requested Thai-first strategic command sections', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('ทดสอบความเสี่ยงก่อนประกาศนโยบาย')
    expect(text).toContain('วิเคราะห์กลุ่มประชาชนที่อาจเข้าใจผิดหรือได้รับผลกระทบ')
    expect(text).toContain('จำลอง public responsiveness บน Facebook, TikTok, X และ LINE')
    expect(text).toContain('เตรียมแผนรับมือวิกฤตข่าวสาร')
    expect(text).toContain('สรุปผลเป็น Strategy Pack สำหรับผู้บริหาร')
  })

  it('renders all four pillars', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('Public Responsiveness Intelligence')
    expect(text).toContain('Crisis-Information Watchouts')
    expect(text).toContain('Culturally Grounded Personas')
    expect(text).toContain('Executive-Ready Evidence')
    expect(text).toContain('ใช้ synthetic personas เพื่อฟังเสียงสะท้อนเชิงสมมุติ ไม่ใช่ข้อมูลประชาชนจริง')
    expect(text).toContain('ความพร้อมต่อเสียงสาธารณะ')
    expect(text).toContain('ประเด็นที่ต้องระวัง')
    expect(text).toContain('ขั้นตอนตรวจสอบ')
  })

  it('renders policy intake fields and output package items', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('ชื่อประเด็นหรือนโยบาย')
    expect(text).toContain('เป้าหมายของการสื่อสาร')
    expect(text).toContain('กลุ่มประชาชนที่ได้รับผลกระทบ')
    expect(text).toContain('ความอ่อนไหวของประเด็น')
    expect(text).toContain('ช่องทางสื่อสารหลัก')
    expect(text).toContain('ข้อความแถลงเบื้องต้น')
    expect(text).toContain('ความเสี่ยงที่กังวล')
    expect(text).toContain('คำถามที่ผู้บริหารต้องตัดสินใจ')
    expect(text).toContain('กลุ่มที่อาจเข้าใจผิดหรือได้รับผลกระทบ')
    expect(text).toContain('สิ่งที่ต้องการให้ระบบช่วยประเมิน')

    expect(text).toContain('Public Sentiment Risk Brief')
    expect(text).toContain('Crisis Watchout Brief')
    expect(text).toContain('Message Revision Memo')
    expect(text).toContain('Response Playbook')
    expect(text).toContain('Executive Strategy Pack')
    expect(text).toContain('Recommended Validation Step')
    expect(text).toContain('Demo Mode')
    expect(text).toContain('Synthetic public-response scenario')
    expect(text).toContain('Decision-support estimate only; not a real-world public outcome forecast')
  })

  it('shows safety boundaries without unsafe English claims', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('ใช้เพื่อประเมินความชัดเจน ความเสี่ยง และความพร้อมของการสื่อสารนโยบายหรือประเด็นสาธารณะ')
    expect(text).toContain('ไม่ใช้ข้อมูลประชาชนรายบุคคล รายชื่อประชาชน หรือ voter list')
    expect(text).toContain('แสดง source/provenance label เช่น Demo Mode, Local Estimate, Live Backend, Backend Verified หรือ Unknown Source ทุกครั้ง')
    expect(text).toContain('ไม่ใช่คำทำนายผลลัพธ์จริง คะแนนเสียง หรือกระแสสาธารณะที่รับประกันได้')
    expect(text).toContain('ต้องมี human review และ validation step ก่อนนำไปใช้สื่อสารสาธารณะจริง')
    expect(text).toContain('ห้ามใช้เพื่อ political microtargeting ปั่นกระแส โจมตีฝ่ายตรงข้าม สร้างข่าวปลอม หรือบิดเบือนข้อมูล')

    const unsafeClaims = [
      ['voter', 'targeting'].join(' '),
      ['micro', 'targeting'].join('-'),
      ['manipulate', 'voters'].join(' '),
      ['attack', 'opponent'].join(' '),
      ['fake', 'news', 'generation'].join(' '),
      ['guaranteed', 'public', 'sentiment', 'prediction'].join(' '),
      ['election', 'outcome', 'prediction'].join(' '),
      ['exact', 'vote', 'impact'].join(' '),
      ['production', 'ready'].join(' '),
    ]

    for (const unsafeClaim of unsafeClaims) {
      expect(text.toLowerCase()).not.toContain(unsafeClaim)
    }
  })
})
