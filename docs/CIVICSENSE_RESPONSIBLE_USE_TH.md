# CivicSense Responsible Use

เอกสารนี้กำหนด positioning และขอบเขตการใช้งานสำหรับ CivicSense ซึ่งเป็น vertical ด้าน public responsiveness intelligence ของ 3C Simulator สำหรับทีมสื่อสารนโยบาย ทีมยุทธศาสตร์ภาครัฐ และทีมที่ต้องประเมินความพร้อมของข้อความก่อนสื่อสารสาธารณะ

## Positioning

CivicSense ไม่ใช่เครื่องมือทำนายกระแสสาธารณะหรือผลลัพธ์ทางการเมือง แต่เป็นระบบช่วยเตรียม decision-support evidence เพื่อให้ทีมเห็น:

- ความชัดเจนของข้อความนโยบายหรือประเด็นสาธารณะ,
- public responsiveness hypotheses จาก synthetic personas,
- crisis-information watchouts,
- กลุ่มประชาชนที่อาจเข้าใจผิดหรือได้รับผลกระทบ,
- message revision options,
- validation step ที่ต้องทำก่อนสื่อสารจริง.

## Thai-First Public Responsiveness Labels

ใช้ label เหล่านี้ใน demo, docs, screenshots, exports และ executive pack เพื่อหลีกเลี่ยงการตีความว่าเป็นการคาดการณ์ผลลัพธ์จริง:

| English label | Thai-first meaning | Required boundary |
| --- | --- | --- |
| Public Responsiveness Preview | ภาพตัวอย่างความพร้อมต่อเสียงสาธารณะ | ต้องมี source label เช่น Local Estimate หรือ Demo Mode |
| ความพร้อมต่อเสียงสาธารณะ | สถานะความพร้อมของข้อความก่อนเผยแพร่ | ไม่ใช่คะแนนผลลัพธ์จริง |
| ประเด็นที่ต้องระวัง | จุดเสี่ยงที่อาจถูกตีความผิดหรือขยายประเด็น | ต้องมี human review |
| ขั้นตอนตรวจสอบ | survey, expert review, stakeholder review หรือ field validation | ต้องทำก่อนใช้สื่อสารจริง |
| Synthetic public-response scenario | สถานการณ์จำลองจากข้อมูลที่อนุมัติและ synthetic personas | ไม่ใช่ข้อมูลประชาชนจริง |

## Responsible Use Rules

- ใช้เพื่อประเมินความชัดเจน ความเสี่ยง และความพร้อมของการสื่อสารนโยบายหรือประเด็นสาธารณะ
- ใช้ synthetic personas และข้อมูลที่ได้รับอนุมัติเท่านั้น ไม่ใช้ข้อมูลประชาชนรายบุคคล รายชื่อประชาชน หรือ voter list
- แสดง source/provenance label เช่น Demo Mode, Local Estimate, Live Backend, Backend Verified หรือ Unknown Source ทุกครั้ง
- ผลลัพธ์เป็น decision-support estimate ไม่ใช่คำทำนายผลลัพธ์จริง คะแนนเสียง หรือกระแสสาธารณะที่รับประกันได้
- ต้องมี human review และ validation step ก่อนนำไปใช้สื่อสารสาธารณะจริง
- ห้ามใช้เพื่อ political microtargeting ปั่นกระแส โจมตีฝ่ายตรงข้าม สร้างข่าวปลอม หรือบิดเบือนข้อมูล

## Preserve Existing Simulation Behavior

CivicSense positioning เป็น copy/positioning layer สำหรับ public-policy vertical เท่านั้น ไม่เปลี่ยน route, API, live simulation, dashboard, War Room, comparator, or source-mode semantics ของ 3C Simulator เดิม
