# Raw Brief To PoV Example

Updated: 2026-05-18

This is a synthetic example showing how a loose Thai business question can become structured Proof-of-Value intake data. It does not contain real customer data, PII, raw CRM, secrets, screenshots, or binary artifacts.

## Thai Raw Brief Example

```text
เราอยากทดสอบแคมเปญเครื่องดื่มน้ำแร่พรีเมียมสำหรับคนทำงานในเมือง
โจทย์คืออยากรู้ว่าควรสื่อสารเรื่องสุขภาพ ความคุ้มค่า หรือภาพลักษณ์แบบ lifestyle
ช่องทางหลักน่าจะเป็น TikTok, Instagram, retail display และ sampling ในออฟฟิศ
งบยังเป็นช่วงกว้าง ๆ ประมาณระดับกลาง ต้องระวังไม่ให้คนรู้สึกว่าแพงเกินไป
อยากได้คำแนะนำว่าควรเลือก creative route ไหน และควร validate อย่างไรต่อ
```

Safety note: this raw brief is synthetic demo data only.

## Prompt Used

```text
คุณคือผู้ช่วย strategy สำหรับเตรียม Proof-of-Value brief ภาษาไทย

แปลงโจทย์ดิบด้านล่างให้เป็น structured campaign brief ที่พร้อมให้ operator ตรวจทานก่อนกรอก /proof-of-value

ข้อกำหนด:
- ใช้ภาษาไทยเป็นหลัก
- หลีกเลี่ยง unsupported claims
- ระบุ assumption ให้ชัด
- ห้ามใช้ PII, raw CRM, customer list, secrets หรือ live integrations
- ห้าม claim ว่าสามารถทำนายยอดขาย ROI หรือ ROAS ได้แน่นอน

Field ที่ต้องตอบ:
campaign name or anonymized campaign code, product/service, objective, target segment,
market context, channel plan, budget band, competitor context, creative direction A,
creative direction B, creative direction C, risk concerns, success KPIs,
optional aggregate actuals, validation goal

โจทย์ดิบ:
<วางโจทย์ synthetic ด้านบน>
```

## Structured Output For Operator Review

| Field | Draft value |
| --- | --- |
| Campaign name or anonymized campaign code | DEMO-WATER-POV-001 |
| Product/service | น้ำแร่พรีเมียมสำหรับคนทำงานในเมือง |
| Objective | เลือกแนวทางสื่อสารหลักก่อนเริ่มใช้ media budget จริง และหาประเด็นที่ควร validate ต่อ |
| Target segment | คนทำงานเมืองใหญ่ที่ใส่ใจสุขภาพ ความสะดวก และภาพลักษณ์ของสินค้าที่ใช้ในชีวิตประจำวัน |
| Market context | หมวดเครื่องดื่มพรีเมียมแข่งขันด้วย benefit, lifestyle, price perception และช่องทางจำหน่ายที่เข้าถึงง่าย |
| Channel plan | TikTok, Instagram, retail display และ office sampling |
| Budget band | ระดับกลาง ใช้เป็น band กว้าง ไม่ระบุ exact spend |
| Competitor context | เครื่องดื่มสุขภาพ, น้ำแร่แบรนด์พรีเมียม, เครื่องดื่มฟังก์ชัน และกาแฟพร้อมดื่มที่แย่ง occasion เดียวกัน |
| Creative direction A | Health-first: เน้นความสดชื่นและการดูแลตัวเองในวันทำงาน |
| Creative direction B | Value clarity: อธิบายเหตุผลที่ราคาสูงกว่าเครื่องดื่มทั่วไปอย่างเข้าใจง่าย |
| Creative direction C | Lifestyle identity: สื่อสารภาพลักษณ์คนเมืองที่เลือกสิ่งที่ดีขึ้นในชีวิตประจำวัน |
| Risk concerns | ราคาดูแพงเกินไป, claim สุขภาพต้องไม่เกินหลักฐาน, lifestyle tone อาจดูไกลตัว |
| Success KPIs | Consideration, message clarity, perceived value, purchase intent proxy, risk sentiment |
| Optional aggregate actuals | Not provided |
| Validation goal | เลือก creative route ที่น่าใช้ต่อ และออกแบบ user test หรือ A/B real ad test แบบจำกัดวง |

## Assumptions To Review

- Segment "คนทำงานเมืองใหญ่" ต้องยืนยันกับลูกค้าว่าตรงกับ target จริงหรือไม่.
- Competitor set เป็น hypothesis จากโจทย์ ไม่ใช่ competitive research ที่ยืนยันแล้ว.
- KPI เป็น directional planning input ไม่ใช่ guaranteed outcome.
- Creative routes เป็น working routes และต้องให้ลูกค้าตรวจภาษาก่อนใช้จริง.

## Human Operator Review Before Pasting

ก่อนกรอก `/proof-of-value`, operator ควรตรวจ:

- Campaign code เป็น safe demo ID หรือ customer-approved code.
- ไม่มีชื่อบุคคล เบอร์โทร อีเมล LINE ID ส่วนตัว หรือข้อมูลระบุตัวบุคคล.
- ไม่มี raw CRM, customer list, customer records หรือข้อมูลรายคน.
- ไม่มี secrets, credentials, API keys, tokens หรือ passwords.
- ไม่มี requirement ให้เชื่อมต่อ live integrations.
- ถ้ามี aggregate actuals ภายหลัง ต้องเป็น aggregate-only และได้รับอนุมัติ.
- ทุก assumption ที่ GenAI ช่วยร่างต้องถูกตรวจโดยมนุษย์ก่อนใช้ใน customer-facing output.

## Research Output Warning

GenAI output is assumption-based unless backed by approved sources. Treat it as preparation material for operator review, not as market research replacement, guaranteed prediction, exact ROI/ROAS forecast, or production deployment evidence.
