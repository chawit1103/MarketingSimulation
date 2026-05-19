<template>
  <div class="strategic-command-page">
    <nav class="command-nav">
      <div class="nav-brand">3C SIMULATOR</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/strategic-command" class="nav-link">Strategic Command</router-link>
        <router-link to="/resources" class="nav-link">Resources</router-link>
        <router-link to="/proof-of-value" class="nav-link">Proof of Value</router-link>
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>
    </nav>

    <main>
      <section class="hero-section">
        <div class="hero-copy">
          <p class="section-label">Strategic Command / Decision Intelligence</p>
          <h1>3C Simulator Strategic Command</h1>
          <h2>ห้องจำลองสถานการณ์เพื่อทดสอบนโยบายและรับมือวิกฤตข่าวสาร</h2>
          <p class="hero-subtitle">
            จำลองเสียงสะท้อนจากประชาชน วิเคราะห์ความเสี่ยงของประเด็นอ่อนไหว
            และเตรียมแผนสื่อสารก่อนลงสนามจริง
          </p>
          <div class="hero-actions" aria-label="Strategic Command actions">
            <a class="command-button primary" href="#demo-flow">ขอ Demo 20 นาที</a>
            <a class="command-button secondary" href="#output-package">ดูตัวอย่าง Executive Strategy Pack</a>
            <router-link class="command-button ghost" to="/resources">เปิด Resource Hub</router-link>
          </div>
        </div>

        <aside class="command-panel" aria-label="Strategic Command dashboard preview">
          <div class="panel-header">
            <span>Crisis Intelligence Preview</span>
            <strong>Local Estimate</strong>
          </div>
          <div class="risk-gauge">
            <div class="gauge-score">72</div>
            <div>
              <span>ประเด็นอ่อนไหวสูง</span>
              <p>ต้องมี human review และ validation step ก่อนสื่อสารสาธารณะ</p>
            </div>
          </div>
          <div class="signal-grid">
            <div v-for="signal in dashboardSignals" :key="signal.label" class="signal-card">
              <span>{{ signal.label }}</span>
              <strong>{{ signal.value }}</strong>
              <p>{{ signal.note }}</p>
            </div>
          </div>
        </aside>
      </section>

      <section class="briefing-section" aria-labelledby="helps-heading">
        <div class="section-heading">
          <p class="section-label">What it helps with</p>
          <h2 id="helps-heading">ช่วยทีมยุทธศาสตร์เห็นความเสี่ยงก่อนตัดสินใจ</h2>
        </div>
        <div class="help-grid">
          <article v-for="item in helpCards" :key="item" class="help-card">
            <span aria-hidden="true"></span>
            <h3>{{ item }}</h3>
          </article>
        </div>
      </section>

      <section class="pillars-section" aria-labelledby="pillars-heading">
        <div class="section-heading">
          <p class="section-label">Four Pillars</p>
          <h2 id="pillars-heading">แกนการวิเคราะห์สำหรับนโยบาย ประเด็นสาธารณะ และวิกฤตข่าวสาร</h2>
        </div>
        <div class="pillar-grid">
          <article v-for="pillar in pillars" :key="pillar.title" class="pillar-card">
            <div class="pillar-index">{{ pillar.index }}</div>
            <div>
              <h3>{{ pillar.title }}</h3>
              <strong>{{ pillar.lead }}</strong>
              <p>{{ pillar.copy }}</p>
            </div>
          </article>
        </div>
      </section>

      <section id="policy-intake" class="intake-section" aria-labelledby="intake-heading">
        <div class="section-heading">
          <p class="section-label">Policy / Public Issue Intake</p>
          <h2 id="intake-heading">ชุดข้อมูลเริ่มต้นสำหรับจำลองประเด็นนโยบาย</h2>
          <p>
            ใช้เฉพาะข้อมูลที่ทีมอนุมัติแล้ว ไม่มีข้อมูลส่วนบุคคล รายชื่อประชาชน หรือข้อมูลดิบจากระบบภายใน
          </p>
        </div>
        <div class="intake-grid">
          <article v-for="field in intakeFields" :key="field" class="intake-field">
            <span>{{ field }}</span>
          </article>
        </div>
      </section>

      <section id="output-package" class="output-section" aria-labelledby="output-heading">
        <div class="section-heading">
          <p class="section-label">Output Package</p>
          <h2 id="output-heading">ผลลัพธ์ที่พร้อมใช้ในห้องประชุมผู้บริหาร</h2>
        </div>
        <div class="output-layout">
          <div class="output-list">
            <article v-for="output in outputPackage" :key="output.title" class="output-card">
              <span>{{ output.type }}</span>
              <h3>{{ output.title }}</h3>
              <p>{{ output.copy }}</p>
            </article>
          </div>
          <aside class="strategy-pack-preview" aria-label="Executive Strategy Pack preview">
            <div class="pack-header">
              <span>Executive Strategy Pack</span>
              <strong>Decision Support</strong>
            </div>
            <ol>
              <li>Risk summary</li>
              <li>Public sentiment hypotheses</li>
              <li>Crisis watchouts</li>
              <li>Message revision options</li>
              <li>Recommended validation step</li>
            </ol>
          </aside>
        </div>
      </section>

      <section class="safety-section" aria-labelledby="safety-heading">
        <div class="section-heading">
          <p class="section-label">Safety and Boundaries</p>
          <h2 id="safety-heading">ขอบเขตการใช้งานที่ต้องเห็นชัดในทุก Demo</h2>
        </div>
        <div class="boundary-grid">
          <article v-for="boundary in safetyBoundaries" :key="boundary" class="boundary-card">
            <span>{{ boundary }}</span>
          </article>
        </div>
      </section>

      <section id="demo-flow" class="demo-section" aria-labelledby="demo-heading">
        <div class="section-heading">
          <p class="section-label">15-Minute Demo Flow</p>
          <h2 id="demo-heading">ลำดับการสาธิตสำหรับทีมยุทธศาสตร์ภาครัฐหรือพรรคการเมือง</h2>
        </div>
        <div class="demo-flow">
          <article v-for="step in demoSteps" :key="step.title" class="demo-step">
            <span>{{ step.index }}</span>
            <div>
              <h3>{{ step.title }}</h3>
              <p>{{ step.copy }}</p>
            </div>
          </article>
        </div>
      </section>

      <section class="playbook-section" aria-label="Crisis response simulation playbook">
        <div>
          <p class="section-label">War Room แบบจำลองการรับมือวิกฤต</p>
          <h2>Response Playbook Blocks</h2>
          <p>
            ใช้เพื่อซ้อมการตอบสนองในสถานการณ์ข่าวสาร ไม่ใช่การโจมตีคู่แข่ง
            หรือการควบคุมความคิดเห็นของประชาชน
          </p>
        </div>
        <div class="playbook-grid">
          <article v-for="block in playbookBlocks" :key="block.title" class="playbook-block">
            <strong>{{ block.title }}</strong>
            <p>{{ block.copy }}</p>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const dashboardSignals = [
  { label: 'Readiness', value: 'Amber', note: 'ข้อความต้องปรับก่อนเผยแพร่' },
  { label: 'Watchouts', value: '5', note: 'ความเสี่ยงการตีความผิดและขยายประเด็น' },
  { label: 'Validation', value: 'Required', note: 'ต้องมีขั้นตอนตรวจสอบภาคสนาม' },
]

const helpCards = [
  'ทดสอบความเสี่ยงก่อนประกาศนโยบาย',
  'วิเคราะห์กลุ่มประชาชนที่อาจเข้าใจผิดหรือได้รับผลกระทบ',
  'จำลองกระแสบน Facebook, TikTok, X และ LINE',
  'เตรียมแผนรับมือวิกฤตข่าวสาร',
  'สรุปผลเป็น Strategy Pack สำหรับผู้บริหาร',
]

const pillars = [
  {
    index: '01',
    title: 'Crisis Intelligence',
    lead: 'ทดสอบความเสี่ยงก่อนเป็นข่าวลบ',
    copy: 'วิเคราะห์ว่าประเด็นใดอาจถูกตีความผิด ขยายความผิด หรือกลายเป็นวิกฤตข่าวสาร',
  },
  {
    index: '02',
    title: 'Social Media Simulation',
    lead: 'จำลองกระแสบนแพลตฟอร์มสังคมออนไลน์',
    copy: 'ประเมินการแพร่กระจายของประเด็นบน Facebook, TikTok, X และ LINE โดยใช้เป็น decision-support estimate เท่านั้น',
  },
  {
    index: '03',
    title: 'Culturally Grounded Personas',
    lead: 'วิเคราะห์ผ่านตัวแทนประชาชนจำลองที่มีบริบททางสังคมและวัฒนธรรม',
    copy: 'ใช้ synthetic personas เพื่อฟังเสียงสะท้อนเชิงสมมุติ ไม่ใช่ข้อมูลประชาชนจริง',
  },
  {
    index: '04',
    title: 'Executive-Ready Evidence',
    lead: 'เปลี่ยนผลวิเคราะห์เป็น dashboard, memo และ Executive Strategy Pack',
    copy: 'เพื่อให้ผู้บริหารเห็นความเสี่ยง ทางเลือก และ next action อย่างรวดเร็ว',
  },
]

const intakeFields = [
  'ชื่อประเด็นหรือนโยบาย',
  'เป้าหมายของการสื่อสาร',
  'กลุ่มประชาชนที่ได้รับผลกระทบ',
  'ความอ่อนไหวของประเด็น',
  'ช่องทางสื่อสารหลัก',
  'ข้อความแถลงเบื้องต้น',
  'ความเสี่ยงที่กังวล',
  'คำถามที่ผู้บริหารต้องตัดสินใจ',
  'กลุ่มที่อาจเข้าใจผิดหรือได้รับผลกระทบ',
  'สิ่งที่ต้องการให้ระบบช่วยประเมิน',
]

const outputPackage = [
  {
    type: 'Brief',
    title: 'Public Sentiment Risk Brief',
    copy: 'สรุปสมมุติฐานเสียงสะท้อน ความเสี่ยง และคำถามที่ต้องตรวจสอบเพิ่ม',
  },
  {
    type: 'Watchout',
    title: 'Crisis Watchout Brief',
    copy: 'ประเด็นที่อาจถูกตีความผิด ขยายความ หรือกลายเป็นกระแสลบ',
  },
  {
    type: 'Memo',
    title: 'Message Revision Memo',
    copy: 'แนวทางปรับข้อความให้ชัดขึ้น ลดความคลุมเครือ และเพิ่มหลักฐานสนับสนุน',
  },
  {
    type: 'Playbook',
    title: 'Response Playbook',
    copy: 'ลำดับการตอบสนอง บทบาทผู้รับผิดชอบ และข้อความสำหรับสถานการณ์จำลอง',
  },
  {
    type: 'Pack',
    title: 'Executive Strategy Pack',
    copy: 'สรุปสำหรับผู้บริหารพร้อมทางเลือก ข้อแลกเปลี่ยน และ next action',
  },
  {
    type: 'Validation',
    title: 'Recommended Validation Step',
    copy: 'ขั้นตอนตรวจสอบกับข้อมูลที่ได้รับอนุมัติ เช่น expert review, survey หรือ stakeholder review',
  },
]

const safetyBoundaries = [
  'เป็นระบบสนับสนุนการตัดสินใจ ไม่ใช่คำทำนายผลลัพธ์จริง',
  'ไม่ใช้ข้อมูลส่วนบุคคล',
  'ไม่ใช้รายชื่อประชาชน',
  'ไม่ใช้ voter list',
  'ไม่ใช้ raw CRM',
  'ไม่ทำการแบ่งเป้ารายบุคคลทางการเมือง',
  'ไม่ใช่เครื่องมือปั่นกระแส',
  'ไม่ใช่เครื่องมือโจมตีฝ่ายตรงข้าม',
  'ไม่สร้างข่าวปลอมหรือข้อมูลบิดเบือน',
  'ต้องใช้ข้อมูลที่ได้รับอนุมัติเท่านั้น',
  'ต้องมี human review ก่อนสื่อสารสาธารณะจริง',
]

const demoSteps = [
  {
    index: '1',
    title: 'เลือกประเด็นนโยบายหรือข้อความแถลง 1 เรื่อง',
    copy: 'เริ่มจากประเด็นที่ได้รับอนุมัติให้ใช้ใน demo และไม่มีข้อมูลส่วนบุคคล',
  },
  {
    index: '2',
    title: 'กำหนดกลุ่มประชาชนจำลองและช่องทางสื่อสาร',
    copy: 'ใช้ synthetic personas และช่องทาง Facebook, TikTok, X หรือ LINE เป็นกรอบประเมิน',
  },
  {
    index: '3',
    title: 'จำลองเสียงสะท้อนและความเสี่ยง',
    copy: 'ดูสมมุติฐานเสียงสะท้อน ความเข้าใจผิดที่อาจเกิดขึ้น และปัจจัยทางวัฒนธรรม',
  },
  {
    index: '4',
    title: 'ดู crisis watchouts',
    copy: 'ระบุข้อความที่อาจกลายเป็นประเด็นอ่อนไหวหรือสร้างความไม่ไว้วางใจ',
  },
  {
    index: '5',
    title: 'ปรับ message / response playbook',
    copy: 'เลือกแนวทางปรับข้อความและแผนตอบสนองที่ยังต้องผ่าน human review',
  },
  {
    index: '6',
    title: 'สรุปเป็น Executive Strategy Pack',
    copy: 'จัดผลลัพธ์ให้ผู้บริหารเห็นความเสี่ยง ทางเลือก และขั้นตอนตรวจสอบต่อไป',
  },
]

const playbookBlocks = [
  { title: 'Clarify', copy: 'ปรับข้อความให้ประชาชนเข้าใจตรงกัน ลดช่องว่างการตีความ' },
  { title: 'Evidence', copy: 'ระบุหลักฐานที่ทีมต้องเตรียมก่อนแถลงหรือชี้แจง' },
  { title: 'Escalation', copy: 'กำหนดจังหวะส่งต่อให้ผู้บริหาร ฝ่ายกฎหมาย หรือทีมสื่อสาร' },
]
</script>

<style scoped>
.strategic-command-page {
  min-height: 100vh;
  color: #d8e6f5;
  background: #f6f9fc;
}

.command-nav {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-8);
  background: rgba(4, 24, 50, 0.86);
  border-bottom: 1px solid rgba(207, 226, 244, 0.18);
  backdrop-filter: blur(18px);
}

.nav-brand {
  color: #ffffff;
  font-family: var(--font-mono);
  font-weight: 900;
  letter-spacing: 0;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--space-2);
}

.nav-link {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  color: #b9cee4;
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 800;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
}

main {
  overflow: hidden;
}

.hero-section,
.briefing-section,
.pillars-section,
.intake-section,
.output-section,
.safety-section,
.demo-section,
.playbook-section {
  width: min(1240px, calc(100% - 32px));
  margin: 0 auto;
}

.hero-section {
  position: relative;
  isolation: isolate;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 460px);
  gap: var(--space-8);
  align-items: center;
  min-height: min(820px, calc(100vh - 74px));
  padding: var(--space-16) 0 var(--space-12);
}

.hero-section::before {
  content: '';
  position: absolute;
  z-index: -1;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 100vw;
  transform: translateX(-50%);
  background: linear-gradient(180deg, rgba(6, 28, 58, 0.98), rgba(9, 32, 64, 0.96));
}

.section-label {
  margin: 0 0 var(--space-3);
  color: #73c9ff;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  letter-spacing: 0;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin-bottom: var(--space-3);
  color: #ffffff;
  font-size: clamp(2.5rem, 6vw, 5.8rem);
  line-height: 0.98;
}

.hero-copy h2 {
  max-width: 820px;
  margin: 0 0 var(--space-5);
  color: #d7ecff;
  font-family: var(--font-sans);
  font-size: clamp(1.55rem, 3vw, 2.45rem);
  font-weight: 800;
  line-height: 1.24;
}

.hero-subtitle {
  max-width: 760px;
  color: #b9cee4;
  font-size: var(--text-xl);
  line-height: 1.75;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-top: var(--space-8);
}

.command-button {
  display: inline-flex;
  align-items: center;
  min-height: 46px;
  padding: 0 var(--space-5);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 900;
}

.command-button.primary {
  color: #062144;
  background: #7ed3ff;
}

.command-button.secondary {
  color: #ffffff;
  border-color: rgba(126, 211, 255, 0.45);
  background: rgba(126, 211, 255, 0.12);
}

.command-button.ghost {
  color: #d7ecff;
  border-color: rgba(215, 236, 255, 0.26);
}

.command-panel,
.strategy-pack-preview {
  border: 1px solid rgba(207, 226, 244, 0.22);
  border-radius: var(--radius-lg);
  background: rgba(8, 34, 70, 0.86);
  box-shadow: 0 26px 70px rgba(0, 0, 0, 0.24);
}

.command-panel {
  padding: var(--space-6);
}

.panel-header,
.pack-header {
  display: flex;
  justify-content: space-between;
  gap: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid rgba(207, 226, 244, 0.16);
  color: #d7ecff;
  font-size: var(--text-sm);
  font-weight: 900;
}

.panel-header strong,
.pack-header strong {
  color: #76e0aa;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
}

.risk-gauge {
  display: grid;
  grid-template-columns: 124px 1fr;
  gap: var(--space-5);
  align-items: center;
  margin: var(--space-6) 0;
}

.gauge-score {
  display: grid;
  place-items: center;
  width: 124px;
  aspect-ratio: 1;
  border-radius: 50%;
  background:
    radial-gradient(circle at center, #082246 0 55%, transparent 56%),
    conic-gradient(#f3b53f 0 72%, rgba(255, 255, 255, 0.16) 72% 100%);
  color: #ffffff;
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 700;
}

.risk-gauge span {
  display: block;
  color: #ffffff;
  font-size: var(--text-lg);
  font-weight: 900;
}

.risk-gauge p,
.signal-card p,
.pillar-card p,
.output-card p,
.demo-step p,
.playbook-block p,
.section-heading p,
.strategy-pack-preview li {
  margin: var(--space-2) 0 0;
  color: inherit;
}

.signal-grid {
  display: grid;
  gap: var(--space-3);
}

.signal-card {
  padding: var(--space-4);
  border: 1px solid rgba(207, 226, 244, 0.15);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.055);
}

.signal-card span,
.output-card span {
  color: #9ab6d5;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.signal-card strong {
  display: block;
  margin-top: var(--space-1);
  color: #ffffff;
  font-size: var(--text-xl);
}

.briefing-section,
.pillars-section,
.intake-section,
.output-section,
.safety-section,
.demo-section,
.playbook-section {
  padding: var(--space-16) 0;
  color: #28415e;
}

.section-heading {
  max-width: 860px;
  margin-bottom: var(--space-8);
}

.section-heading h2,
.playbook-section h2 {
  color: #0b2a50;
  font-size: clamp(1.75rem, 3vw, 2.6rem);
}

.help-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--space-4);
}

.help-card,
.pillar-card,
.intake-field,
.output-card,
.boundary-card,
.demo-step,
.playbook-block {
  border: 1px solid #d6e2ee;
  border-radius: var(--radius-lg);
  background: #ffffff;
  box-shadow: 0 16px 38px rgba(23, 60, 95, 0.08);
}

.help-card {
  min-height: 164px;
  padding: var(--space-5);
}

.help-card span {
  display: block;
  width: 36px;
  height: 5px;
  margin-bottom: var(--space-5);
  border-radius: var(--radius-pill);
  background: #3d93d1;
}

.help-card h3,
.pillar-card h3,
.output-card h3,
.demo-step h3 {
  color: #0b2a50;
  font-family: var(--font-sans);
  font-size: var(--text-lg);
  line-height: 1.35;
}

.pillar-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.pillar-card {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: var(--space-5);
  padding: var(--space-6);
}

.pillar-index {
  color: #3d93d1;
  font-family: var(--font-mono);
  font-size: var(--text-xl);
  font-weight: 900;
}

.pillar-card strong {
  display: block;
  margin: var(--space-2) 0;
  color: #102f55;
  font-size: var(--text-base);
}

.intake-section,
.safety-section {
  width: 100%;
  max-width: none;
  padding-right: max(16px, calc((100% - 1240px) / 2));
  padding-left: max(16px, calc((100% - 1240px) / 2));
  background: #eaf2fa;
}

.intake-grid,
.boundary-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--space-3);
}

.intake-field,
.boundary-card {
  min-height: 96px;
  padding: var(--space-4);
  font-weight: 900;
}

.intake-field span,
.boundary-card span {
  color: #0b2a50;
}

.output-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: var(--space-5);
  align-items: start;
}

.output-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.output-card {
  min-height: 178px;
  padding: var(--space-5);
}

.output-card span {
  color: #3d6f9c;
}

.strategy-pack-preview {
  position: sticky;
  top: 96px;
  padding: var(--space-5);
  color: #c9ddf1;
}

.strategy-pack-preview ol {
  display: grid;
  gap: var(--space-3);
  padding-left: var(--space-5);
  margin: var(--space-5) 0 0;
}

.demo-flow {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.demo-step {
  display: grid;
  grid-template-columns: 52px 1fr;
  gap: var(--space-4);
  padding: var(--space-5);
}

.demo-step > span {
  display: grid;
  place-items: center;
  width: 44px;
  aspect-ratio: 1;
  border-radius: 50%;
  background: #0b2a50;
  color: #ffffff;
  font-family: var(--font-mono);
  font-weight: 900;
}

.playbook-section {
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: var(--space-8);
  align-items: start;
  padding-bottom: var(--space-20);
}

.playbook-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

.playbook-block {
  padding: var(--space-5);
}

.playbook-block strong {
  color: #0b2a50;
  font-size: var(--text-lg);
}

@media (max-width: 1080px) {
  .hero-section,
  .output-layout,
  .playbook-section {
    grid-template-columns: 1fr;
  }

  .command-panel,
  .strategy-pack-preview {
    position: static;
  }

  .help-grid,
  .intake-grid,
  .boundary-grid,
  .playbook-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .command-nav {
    align-items: flex-start;
    padding: var(--space-4);
  }

  .hero-section {
    min-height: auto;
    padding-top: var(--space-10);
  }

  .hero-actions,
  .command-button {
    width: 100%;
  }

  .command-button {
    justify-content: center;
  }

  .risk-gauge,
  .pillar-card,
  .demo-step,
  .output-list,
  .help-grid,
  .intake-grid,
  .boundary-grid,
  .demo-flow,
  .playbook-grid {
    grid-template-columns: 1fr;
  }

  .pillar-card,
  .demo-step {
    gap: var(--space-3);
  }
}
</style>
