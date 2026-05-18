# AI Research Prompt Pack For Proof-of-Value Intake

Updated: 2026-05-18

ชุด prompt นี้ช่วยให้ operator ใช้ ChatGPT, Claude, Gemini หรือ GenAI assistant อื่นเป็นผู้ช่วยเตรียม brief ก่อนนำข้อมูลที่ตรวจแล้วไปกรอก `/proof-of-value`.

หลักการสำคัญ:

- ใช้ภาษาไทยเป็นหลัก ใช้คำอังกฤษเฉพาะคำที่คุ้นเคย เช่น brief, campaign, segment, KPI, insight, strategy, validation.
- ใช้เฉพาะโจทย์หรือ brief ที่ลูกค้าอนุมัติให้ใช้สำหรับ Proof-of-Value.
- ห้ามใส่ PII, raw CRM, customer list, secrets, API keys, tokens, passwords หรือข้อมูลที่ต้องใช้ live integrations.
- ให้ GenAI ระบุ assumption ให้ชัด และห้ามสรุป claim ที่ไม่มีข้อมูลรองรับ.
- ผลลัพธ์เป็นข้อมูลเตรียม intake เท่านั้น ต้องให้ human operator ตรวจทานก่อนนำเข้า `/proof-of-value`.

## 1. Raw Customer Problem To Structured Campaign Brief

ใช้เมื่อมีเพียงโจทย์ธุรกิจหลวม ๆ จากลูกค้า

```text
คุณคือผู้ช่วย strategy สำหรับเตรียม Proof-of-Value brief ภาษาไทย

งานของคุณ:
แปลงโจทย์ดิบด้านล่างให้เป็น structured campaign brief ที่พร้อมให้ operator ตรวจทานก่อนกรอก /proof-of-value

โจทย์ดิบ:
<วางโจทย์ลูกค้าที่ได้รับอนุมัติไว้ตรงนี้>

ข้อกำหนดด้านความปลอดภัย:
- ห้ามเพิ่ม PII เช่น ชื่อบุคคล เบอร์โทร อีเมล LINE ID ที่เป็นส่วนตัว หรือเลขประจำตัว
- ห้ามใช้ raw CRM, customer list, customer records หรือข้อมูลรายบุคคล
- ห้ามขอ API keys, tokens, passwords, credentials หรือ live integrations
- หากข้อมูลไม่พอ ให้ระบุเป็น "Assumption" แทนการเดาแบบมั่นใจ
- ห้าม claim ว่าสามารถทำนายยอดขาย ROI หรือ ROAS ได้แน่นอน

กรุณาตอบเป็นภาษาไทย กระชับ และจัดหัวข้อ:
- campaign name or anonymized campaign code
- product/service
- objective
- target segment
- market context
- channel plan
- budget band
- competitor context
- creative direction A
- creative direction B
- creative direction C
- risk concerns
- success KPIs
- optional aggregate actuals
- assumptions to review
- questions to ask customer
- recommended validation notes for output package
- safety notes
```

## 2. Market And Competitor Research Prompt

ใช้เพื่อเตรียม market context และ competitor context โดยไม่อ้างว่าเป็นข้อมูลยืนยันถ้าไม่มี source ที่ได้รับอนุมัติ

```text
คุณคือผู้ช่วย research ภาษาไทยสำหรับ Proof-of-Value campaign brief

บริบทแคมเปญ:
<ใส่ข้อมูล campaign/product/target ที่ได้รับอนุมัติ>

ช่วยสรุป market context และ competitor context เพื่อใช้เป็น input สำหรับ /proof-of-value

ข้อกำหนด:
- ใช้ภาษาไทยเป็นหลัก
- แยก "ข้อมูลที่มาจาก brief" กับ "assumption ที่ควรตรวจสอบ"
- หลีกเลี่ยง unsupported claims
- อย่าใช้หรือขอ PII, raw CRM, customer list, secrets หรือ live integrations
- ถ้าไม่มี source ที่ได้รับอนุมัติ ให้เขียนว่าเป็น assumption หรือ hypothesis
- ห้ามสรุปว่า competitor หรือ market จะตอบสนองแบบแน่นอน

รูปแบบคำตอบ:
1. Market context สำหรับ brief
2. Competitor context สำหรับ brief
3. Consumer tension หรือ insight ที่เป็น hypothesis
4. Assumptions ที่ต้องให้ลูกค้าหรือ operator ตรวจ
5. Validation questions
```

## 3. Target Segment And Persona Prompt

ใช้เพื่อเตรียม target segment แบบปลอดภัย ไม่ลงข้อมูลรายบุคคล

```text
คุณคือผู้ช่วยกำหนด target segment สำหรับ Proof-of-Value

บริบทที่ได้รับอนุมัติ:
<วาง product/service, objective, market context>

ช่วยจัด target segment เป็นกลุ่มกว้าง ๆ ที่ปลอดภัยต่อการใช้ใน /proof-of-value

ข้อกำหนด:
- ห้ามสร้าง persona ที่มีชื่อจริง เบอร์โทร อีเมล ที่อยู่ หรือข้อมูลระบุตัวบุคคล
- ห้ามใช้ customer record หรือ raw CRM
- ใช้ segment ระดับกลุ่ม เช่น "คนทำงานเมืองใหญ่ที่ใส่ใจสุขภาพ"
- ระบุ motivation, barrier, trigger, channel fit และ risk sensitivity
- แยก assumption ให้ชัด

รูปแบบคำตอบ:
| Segment | Motivation | Barrier | Channel fit | Risk sensitivity | Assumptions |
```

## 4. A/B/C Creative Route Generation Prompt

ใช้เมื่อลูกค้ายังไม่มี creative direction A/B/C หรืออนุญาตให้ operator สร้าง working routes

```text
คุณคือผู้ช่วย creative strategy ภาษาไทย

สร้าง creative direction A/B/C สำหรับ Proof-of-Value intake จาก brief ที่ได้รับอนุมัติด้านล่าง

Brief:
<วาง brief ที่ปลอดภัยและได้รับอนุมัติ>

ข้อกำหนด:
- สร้าง 3 creative routes ที่ต่างกันจริง
- เขียนเป็น working routes ไม่ใช่ final ad copy
- ห้าม invent customer facts, performance promises หรือ claim ที่ไม่มีข้อมูลรองรับ
- ห้าม claim ว่าจะเพิ่มยอดขาย ROI หรือ ROAS แน่นอน
- ห้ามใช้ PII, raw CRM, customer list, secrets หรือ live integrations
- ใช้ภาษาไทยง่าย อ่านเร็ว

รูปแบบคำตอบ:
- Creative direction A: <ชื่อ route>
  - Core idea:
  - Message angle:
  - Best-fit segment:
  - Main risk:
- Creative direction B:
- Creative direction C:
- Assumptions to review:
```

## 5. Risk And Crisis Watchout Prompt

ใช้เพื่อเตรียม risk concerns และ crisis watchouts

```text
คุณคือผู้ช่วย risk review สำหรับ campaign Proof-of-Value

Campaign context:
<วาง brief ที่ได้รับอนุมัติ>

ช่วยหา risk drivers และ crisis watchouts ที่ควรใส่ใน /proof-of-value

ข้อกำหนด:
- ใช้ภาษาไทยเป็นหลัก
- ไม่กล่าวหาบุคคล แบรนด์ หรือ competitor โดยไม่มีหลักฐาน
- ไม่สร้างข่าวลือหรือข้อมูลเสียหายที่ไม่มี source
- ระบุว่าเป็น risk hypothesis ไม่ใช่ prediction
- ห้ามใช้ PII, raw CRM, customer list, secrets หรือ live integrations

รูปแบบคำตอบ:
1. Top risk drivers 3-5 ข้อ
2. Early warning signals
3. Mitigation ideas
4. Crisis response notes
5. Assumptions and validation needed
```

## 6. Success KPI And Validation Notes Prompt

ใช้เพื่อแปลง objective เป็น KPI และ recommended validation notes ที่ operator จะใช้ภายหลังใน output package. หมายเหตุ validation ไม่ใช่ field โดยตรงของ `/proof-of-value`.

```text
คุณคือผู้ช่วยวาง KPI และ validation plan สำหรับ Proof-of-Value

Brief:
<วาง brief ที่ได้รับอนุมัติ>

ช่วยเสนอ success KPIs และ recommended validation notes สำหรับ campaign นี้

ข้อกำหนด:
- KPI ต้องเป็น decision-support metric ไม่ใช่คำสัญญาผลลัพธ์
- ห้าม claim exact ROI/ROAS หรือ guaranteed prediction
- ถ้าใช้ historical actuals ต้องเป็น aggregate-only และได้รับอนุมัติ
- ห้ามใช้ PII, raw CRM, customer list, secrets หรือ live integrations
- Recommended validation notes เป็น operator notes สำหรับ downstream output package ไม่ใช่ direct /proof-of-value input field

รูปแบบคำตอบ:
- Primary KPI:
- Secondary KPIs:
- Questions to ask customer:
- Recommended validation notes for output package:
- Minimum evidence needed:
- Assumptions to review:
```

## 7. Final Proof-of-Value Intake Formatter Prompt

ใช้เป็นขั้นสุดท้ายก่อนนำข้อมูลที่ human-reviewed ไปกรอก `/proof-of-value`

```text
คุณคือผู้ช่วย format ข้อมูลสำหรับ /proof-of-value intake

ข้อมูลด้านล่างผ่านการเตรียมเบื้องต้นแล้ว แต่ต้องตรวจ safety และจัดให้อยู่ใน field ที่ถูกต้อง

Input:
<วางข้อมูล brief/research/creative/KPI ที่ได้รับอนุมัติ>

งานของคุณ:
1. จัดข้อมูลให้ตรงกับ field ของ /proof-of-value
2. ถ้าข้อมูลไม่พอ ให้ใส่ "ต้องให้ operator ตรวจ" แทนการเดา
3. ระบุ assumption ที่ต้องยืนยันกับลูกค้า
4. ตรวจว่ามี PII, raw CRM, customer list, secrets หรือ live integration requirement หรือไม่
5. ห้ามเพิ่ม claim เรื่อง guaranteed prediction, exact ROI/ROAS หรือ production deployment

Field ที่ต้องตอบ:
- campaign name or anonymized campaign code
- product/service
- objective
- target segment
- market context
- channel plan
- budget band
- competitor context
- creative direction A
- creative direction B
- creative direction C
- risk concerns
- success KPIs
- optional aggregate actuals
- assumptions to review
- questions to ask customer
- recommended validation notes for output package
- safety checklist
```

## 8. JSON/Markdown Output Formatter Prompt

ใช้เมื่อ operator ต้องการ copy output เป็น Markdown หรือ JSON ก่อนกรอกมือใน `/proof-of-value`

```text
กรุณาแปลงข้อมูลด้านล่างเป็น 2 รูปแบบ:
1. Markdown table
2. JSON object

Input:
<วาง structured brief ที่ operator ตรวจแล้ว>

ข้อกำหนด:
- ใช้ key ภาษาอังกฤษให้ตรงกับ /proof-of-value เท่าที่ทำได้
- ใช้เนื้อหาภาษาไทยเป็นหลัก
- อย่าใส่ PII, raw CRM, customer list, secrets, API keys, tokens, passwords หรือ live integrations
- ถ้ามี aggregate actuals ให้ระบุว่าเป็น aggregate-only และ approved หรือ "not provided"
- อย่า claim guaranteed prediction หรือ exact ROI/ROAS

JSON keys:
campaignNameOrCode, productService, objective, targetSegment, marketContext,
channelPlan, budgetBand, competitorContext, creativeA, creativeB, creativeC,
riskConcerns, successKpis, aggregateActuals, assumptionsToReview,
questionsToAskCustomer, recommendedValidationNotes
```

## Human Review Before Pasting

ก่อนนำผลลัพธ์ไปกรอก `/proof-of-value`, operator ต้องตรวจว่า:

- ไม่มี PII หรือข้อมูลที่ระบุตัวบุคคลได้
- ไม่มี raw CRM, customer list หรือ customer records
- ไม่มี secrets, credentials, API keys, tokens หรือ passwords
- ไม่มี requirement ให้เชื่อมต่อ live CRM, social listening, ad platform, analytics หรือ marketing automation
- มี creative direction A/B/C ครบ หรือมีการอนุมัติให้ operator สร้าง safe working routes
- assumption ถูกแยกชัดเจน
- recommended validation notes ถูกเก็บเป็น operator notes สำหรับ output package ไม่ใช่ field ที่กรอกใน `/proof-of-value`
- output ไม่อ้าง production readiness, guaranteed prediction, exact ROI/ROAS หรือการแทน market research
