# CivicSense Strategic Command Safety Boundaries

เอกสารนี้กำหนดขอบเขตสำหรับ CivicSense / Strategic Command vertical ทุกครั้งที่ใช้ใน demo, workshop, docs, screenshots, exports หรือ executive pack

## Allowed Use

- ประเมินความเสี่ยงของประเด็นนโยบายหรือประเด็นสาธารณะ
- ประเมิน public responsiveness และความพร้อมของข้อความก่อนเผยแพร่
- จำลองเสียงสะท้อนเชิงสมมุติจาก synthetic personas
- เตรียม crisis watchouts สำหรับทีมสื่อสาร
- ปรับข้อความให้ชัดเจนขึ้นและลดความคลุมเครือ
- สรุปทางเลือก ข้อแลกเปลี่ยน และ next action สำหรับผู้บริหาร
- แนะนำ validation step ก่อนสื่อสารสาธารณะจริง

## Disallowed Use

- ไม่ใช้เพื่อควบคุมความเห็นสาธารณะ
- ไม่ใช้เพื่อการแบ่งเป้ารายบุคคลทางการเมืองหรือ political microtargeting
- ไม่ใช้เพื่อการชักจูงรายบุคคล
- ไม่ใช้เพื่อสร้างข้อความโจมตีฝ่ายตรงข้าม
- ไม่ใช้เพื่อสร้างข่าวปลอมหรือข้อมูลบิดเบือน
- ไม่ใช้เพื่อทำนายผลการเลือกตั้ง
- ไม่ใช้เพื่อประเมินผลต่อคะแนนเสียง
- ไม่ใช้เพื่อประกาศว่า campaign หรือ policy จะสำเร็จแน่นอน
- ไม่ใช้เป็นหลักฐานแทน research, survey, field validation หรือ expert review

## Data Boundary

อนุญาตเฉพาะ:

- policy brief ที่ได้รับอนุมัติ,
- anonymized scenario,
- synthetic/demo data,
- aggregate context ที่ได้รับอนุมัติ,
- public context ที่ตรวจสอบแล้วและมีสิทธิ์ใช้.

ห้ามใช้:

- PII,
- รายชื่อประชาชน,
- voter list,
- raw CRM,
- contact database,
- raw social posts ที่ยังไม่ได้รับอนุมัติ,
- secrets, API keys, provider tokens, passwords, auth headers,
- ข้อมูลภายในที่ยังไม่ได้รับอนุมัติให้ใช้ใน demo.

## Output Boundary

ทุก output ต้องมี source/provenance label เช่น Demo Mode, Local Estimate, Live Backend, Backend Verified หรือ Unknown Source

Thai-first public responsiveness label ที่แนะนำให้ใช้คือ “ความพร้อมต่อเสียงสาธารณะ”, “ประเด็นที่ต้องระวัง”, “ขั้นตอนตรวจสอบ” และ “Synthetic public-response scenario” โดยต้องระบุเสมอว่าเป็น estimate ไม่ใช่ผลลัพธ์จริง

Output ต้องระบุว่า:

- เป็น decision-support estimate,
- ไม่ใช่ผลลัพธ์จริง,
- ต้องผ่าน human review,
- ต้องมี validation step ก่อนใช้สื่อสารสาธารณะ,
- ห้ามลบ limitation หรือ source label เมื่อนำไปใส่ deck, memo หรือ screenshot.

## Public Deployment Claim Boundary

Strategic Command demo ไม่ใช่การอนุมัติ public access, public internet exposure, self-serve political workflow หรือ production customer deployment

Presenter ต้องหลีกเลี่ยงคำกล่าวอ้างว่า:

- ระบบพร้อมเปิดใช้งานสาธารณะ,
- ระบบยืนยันผลลัพธ์ทางสังคมหรือการเมืองได้,
- ระบบแทนที่การตัดสินใจของผู้บริหารได้,
- ระบบแทนที่การตรวจสอบโดยมนุษย์ได้.
