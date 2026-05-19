# PM2.5 Strategic Command Demo Script

Source: Demo Mode | Basis: User-provided policy scenario | Run ID: demo-strategic-pm25-dust-free-room-001 | Decision-Support Estimate

## Opening Talk Track

วันนี้เราจะใช้ Strategic Command จำลองการสื่อสารประเด็นนโยบาย PM2.5 ที่มีความสำคัญต่อสุขภาพประชาชน:

> อววน. สู้ฝุ่น PM2.5: นำร่องนวัตกรรมห้องปลอดฝุ่นต้นทุนต่ำเพื่อสุขภาพประชาชน

โจทย์นี้เหมาะกับ demo เพราะเป็นประเด็นที่ประชาชนเข้าใจง่าย มีตัวเลขชัดเจนจาก scenario ที่ได้รับมา คือ 3,600 บาทต่อห้อง, 83 ห้อง, 8 จังหวัดภาคเหนือ และมีทั้งโอกาสทางการสื่อสารและความเสี่ยงด้านความเชื่อมั่น

สิ่งที่เราจะดูไม่ใช่การคาดการณ์ผลจริง แต่เป็นการลด communication risk ก่อนสื่อสารสาธารณะ

## Why This Topic Was Selected

- เป็นประเด็นสุขภาพที่มีผลต่อชีวิตประจำวัน
- เชื่อมงานวิจัย มหาวิทยาลัย และ innovation กับปัญหา PM2.5 ได้ชัด
- มี risk ที่ทีมยุทธศาสตร์ต้องเตรียมตอบ เช่น proof, scale, hidden costs, and root-cause criticism
- เหมาะสำหรับสาธิต Executive Strategy Pack เพราะผู้บริหารต้องตัดสินใจเรื่อง framing, evidence, phase 2, และ validation step

## Safety Boundary Explanation

พูดให้ชัดก่อนเริ่ม:

> Demo นี้ไม่เกี่ยวกับการทำนายผลการเลือกตั้ง การคำนวณผลต่อคะแนนเสียง การแบ่งเป้ารายบุคคลทางการเมือง การโจมตีฝ่ายตรงข้าม หรือการควบคุมความคิดเห็นสาธารณะ จุดประสงค์คือช่วยทีมลดความเสี่ยงของการสื่อสารนโยบายก่อนลงสนามจริง

ใช้เฉพาะ user-provided policy scenario ไม่มีข้อมูลส่วนบุคคล ไม่มี voter lists ไม่มี raw CRM ไม่มี party membership data และไม่มี confidential government data

## 5-Minute Demo Script

| เวลา | Talk Track | What To Show |
| --- | --- | --- |
| 0:00-0:45 | เปิดด้วยโจทย์ PM2.5 และบอกว่าเป็น Demo Mode / Synthetic Scenario | `/strategic-command` hero และ Executive Strategy Pack preview |
| 0:45-1:45 | อธิบายว่าประเด็นมีทั้ง quick win และ risk เช่น proof, scale, hidden costs | What it helps with และ Four Pillars |
| 1:45-2:45 | แสดง intake fields: policy name, affected groups, channels, risk concerns | Policy / Public Issue Intake |
| 2:45-3:45 | อธิบาย output package ที่จะได้: risk brief, watchouts, message memo, playbook | Output Package section |
| 3:45-4:30 | ย้ำ safety boundaries และข้อห้าม | Safety and Boundaries section |
| 4:30-5:00 | ปิดด้วย next step: Controlled Private Pilot กับ 1 policy issue | PM2.5 Executive Strategy Pack docs |

## 15-Minute Demo Script

| เวลา | Talk Track | What To Show |
| --- | --- | --- |
| 0-2 นาที | เปิดบริบท PM2.5 ห้องปลอดฝุ่น 3,600 บาท, 83 ห้อง, 8 จังหวัดภาคเหนือ ในฐานะ user-provided scenario | `/strategic-command` hero |
| 2-4 นาที | อธิบายว่าทำไมต้อง Strategic Command: ก่อนสื่อสารจริงต้องเห็น risk, watchouts, and validation needs | What it helps with |
| 4-6 นาที | ใส่ policy issue, affected public groups, channels, and executive decision questions | Policy / Public Issue Intake |
| 6-8 นาที | อ่าน synthetic personas: parent, skeptic, implementer, expert, rural community/farmer | `PM25_DUST_FREE_ROOM_INPUT_TH.md` |
| 8-10 นาที | เปิด Crisis Watchout: AQI meter challenge, meme risk, root-cause criticism, 83-room criticism, hidden costs | PM2.5 Crisis Watchout Brief |
| 10-12 นาที | เปรียบเทียบ initial statement กับ revised message ที่ลด overclaim | Message Revision Memo |
| 12-14 นาที | แสดง Response Playbook สำหรับ 3 attacks หลัก | Response Playbook |
| 14-15 นาที | ย้ำ limitations and next step | Safety Boundaries และ Controlled Private Pilot CTA |

## What To Show On `/strategic-command`

- Hero: 3C Simulator Strategic Command
- Executive Strategy Pack preview: Demo Mode, Synthetic Scenario, Decision-support estimate wording
- What it helps with
- Four Pillars
- Policy / Public Issue Intake
- Output Package
- Safety and Boundaries
- Demo Flow

## How To Explain The Demo Package

พูดว่า:

> หลังจากเห็นหน้า Strategic Command เราสามารถเตรียม PM2.5 package ที่ทีมผู้บริหารใช้ประชุมได้ทันที ประกอบด้วย input, synthetic persona map, crisis watchouts, message revision, response playbook, and recommended validation step

เชื่อมไปที่:

- `docs/strategic-command/PM25_DUST_FREE_ROOM_INPUT_TH.md`
- `docs/strategic-command/PM25_EXECUTIVE_STRATEGY_PACK_TH.md`

## How To Close For Next Step

Close:

> ถ้าทีมเห็นว่ากรอบนี้ช่วยลดความเสี่ยงก่อนสื่อสารจริง ขั้นตอนถัดไปคือทดลองกับประเด็นนโยบาย 1 เรื่องแบบ Controlled Private Pilot โดยใช้ข้อมูลที่ทีมอนุมัติเท่านั้น และมี human review ก่อนใช้งานสาธารณะ

Ask:

- ประเด็น PM2.5 นี้ควรใช้ framing แบบ pilot model หรือ finished achievement?
- ใครเป็น owner ของ evidence และ maintenance answer?
- มี approved before/after measurement หรือไม่?
- ต้องการให้ทีมทดลอง revised message กี่ route?
- ใครต้อง review ก่อน public communication?
