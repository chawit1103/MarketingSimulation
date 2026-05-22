export const civicSenseProduct = {
  name: 'CivicSense',
  taglineTh: 'ระบบจำลองเสียงสะท้อนสาธารณะเพื่อการสื่อสารนโยบายอย่างรับผิดชอบ',
  descriptorEn: 'Public Responsiveness Intelligence',
}

export const publicResponsivenessLabels = {
  previewTitle: 'Public Responsiveness Preview',
  sourceMode: 'Local Estimate',
  readiness: 'ความพร้อมต่อเสียงสาธารณะ',
  watchouts: 'ประเด็นที่ต้องระวัง',
  validation: 'ขั้นตอนตรวจสอบ',
  syntheticScenario: 'Synthetic public-response scenario',
  decisionSupportOnly: 'Decision-support estimate only; not a real-world public outcome forecast',
}

export const civicSenseResponsibleUseRules = [
  'ใช้เพื่อประเมินความชัดเจน ความเสี่ยง และความพร้อมของการสื่อสารนโยบายหรือประเด็นสาธารณะ',
  'ใช้ synthetic personas และข้อมูลที่ได้รับอนุมัติเท่านั้น ไม่ใช้ข้อมูลประชาชนรายบุคคล รายชื่อประชาชน หรือ voter list',
  'แสดง source/provenance label เช่น Demo Mode, Local Estimate, Live Backend, Backend Verified หรือ Unknown Source ทุกครั้ง',
  'ผลลัพธ์เป็น decision-support estimate ไม่ใช่คำทำนายผลลัพธ์จริง คะแนนเสียง หรือกระแสสาธารณะที่รับประกันได้',
  'ต้องมี human review และ validation step ก่อนนำไปใช้สื่อสารสาธารณะจริง',
  'ห้ามใช้เพื่อ political microtargeting ปั่นกระแส โจมตีฝ่ายตรงข้าม สร้างข่าวปลอม หรือบิดเบือนข้อมูล',
]
