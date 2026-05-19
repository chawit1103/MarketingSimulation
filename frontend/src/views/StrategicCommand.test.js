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

    expect(wrapper.text()).toContain('3C Simulator Strategic Command')
    expect(wrapper.text()).toContain('ห้องจำลองสถานการณ์เพื่อทดสอบนโยบายและรับมือวิกฤตข่าวสาร')
  })

  it('shows the requested Thai-first strategic command sections', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('ทดสอบความเสี่ยงก่อนประกาศนโยบาย')
    expect(text).toContain('วิเคราะห์กลุ่มประชาชนที่อาจเข้าใจผิดหรือได้รับผลกระทบ')
    expect(text).toContain('จำลองกระแสบน Facebook, TikTok, X และ LINE')
    expect(text).toContain('เตรียมแผนรับมือวิกฤตข่าวสาร')
    expect(text).toContain('สรุปผลเป็น Strategy Pack สำหรับผู้บริหาร')
  })

  it('renders all four pillars', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('Crisis Intelligence')
    expect(text).toContain('Social Media Simulation')
    expect(text).toContain('Culturally Grounded Personas')
    expect(text).toContain('Executive-Ready Evidence')
    expect(text).toContain('ใช้ synthetic personas เพื่อฟังเสียงสะท้อนเชิงสมมุติ ไม่ใช่ข้อมูลประชาชนจริง')
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
    expect(text).toContain('Synthetic Scenario')
    expect(text).toContain('Decision-support estimate only; not a real-world outcome forecast')
  })

  it('shows safety boundaries without unsafe English claims', () => {
    const wrapper = mountView()
    const text = wrapper.text()

    expect(text).toContain('เป็นระบบสนับสนุนการตัดสินใจ ไม่ใช่คำทำนายผลลัพธ์จริง')
    expect(text).toContain('ไม่ใช้ข้อมูลส่วนบุคคล')
    expect(text).toContain('ไม่ใช้รายชื่อประชาชน')
    expect(text).toContain('ไม่ใช้ voter list')
    expect(text).toContain('ไม่ใช้ raw CRM')
    expect(text).toContain('ไม่ทำการแบ่งเป้ารายบุคคลทางการเมือง')
    expect(text).toContain('ไม่ใช่เครื่องมือปั่นกระแส')
    expect(text).toContain('ไม่ใช่เครื่องมือโจมตีฝ่ายตรงข้าม')
    expect(text).toContain('ไม่สร้างข่าวปลอมหรือข้อมูลบิดเบือน')
    expect(text).toContain('ไม่ทำนายผลการเลือกตั้ง')
    expect(text).toContain('ไม่ประเมินผลกระทบต่อคะแนนเสียง')
    expect(text).toContain('ไม่คำนวณ vote impact หรือ exact vote effect')
    expect(text).toContain('ต้องใช้ข้อมูลที่ได้รับอนุมัติเท่านั้น')
    expect(text).toContain('ต้องมี human review ก่อนสื่อสารสาธารณะจริง')

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
