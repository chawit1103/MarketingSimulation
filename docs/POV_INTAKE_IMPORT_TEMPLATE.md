# PoV Intake Import Template

Updated: 2026-05-18

ใช้ template นี้เพื่อเตรียมข้อมูลจาก approved brief หรือ GenAI-assisted research ก่อนนำไปกรอก `/proof-of-value`. ปัจจุบันเป็น copy/paste workflow เท่านั้น แอปไม่ส่งข้อมูลออกไปยัง external AI provider.

## Copy/Paste Instructions

1. เริ่มจาก brief หรือโจทย์ที่ลูกค้าอนุมัติให้ใช้สำหรับ Proof-of-Value.
2. ใช้ [AI Research Prompt Pack](AI_RESEARCH_PROMPT_PACK.md) เพื่อช่วยจัดโครงสร้าง หากข้อมูลยังเป็นโจทย์ดิบ.
3. ให้ operator ตรวจทุก field ก่อนกรอก `/proof-of-value`.
4. กรอกข้อมูลด้วยมือหรือ copy เฉพาะ field ที่ผ่าน safety review แล้ว.
5. Tick confirmation ใน `/proof-of-value` เฉพาะเมื่อมั่นใจว่าไม่มีข้อมูลต้องห้าม.

## Safety Checklist

- [ ] ใช้เฉพาะข้อมูลที่ลูกค้าอนุมัติสำหรับ PoV นี้
- [ ] ไม่มี PII เช่น ชื่อบุคคล เบอร์โทร อีเมล LINE ID ส่วนตัว ที่อยู่ หรือเลขประจำตัว
- [ ] ไม่มี raw CRM, customer list, customer records หรือข้อมูลรายบุคคล
- [ ] ไม่มี API keys, provider tokens, passwords, OAuth credentials, graph credentials หรือ secrets
- [ ] ไม่มี requirement ให้ใช้ live CRM, social listening, ad platform, analytics หรือ marketing automation integration
- [ ] หากมี historical actuals ต้องเป็น aggregate-only และได้รับอนุมัติ
- [ ] Creative direction A/B/C ครบ หรือมีการอนุมัติให้ operator สร้าง safe working routes
- [ ] Assumptions ถูกแยกออกจากข้อมูลที่ได้รับอนุมัติ
- [ ] ไม่มี claim เรื่อง production readiness, guaranteed prediction หรือ exact ROI/ROAS

## Markdown Template

```markdown
## Proof-of-Value Intake

| Field | Value |
| --- | --- |
| Campaign name or anonymized campaign code |  |
| Product/service |  |
| Objective |  |
| Target segment |  |
| Market context |  |
| Channel plan |  |
| Budget band |  |
| Competitor context |  |
| Creative direction A |  |
| Creative direction B |  |
| Creative direction C |  |
| Risk concerns |  |
| Success KPIs |  |
| Optional aggregate actuals | Not provided / aggregate-only approved values |
| Validation goal |  |

## Assumptions To Review

- <assumption to verify>

## Safety Notes

- Approved for PoV use: Yes / No
- No PII: Yes / No
- No raw CRM/customer lists: Yes / No
- No secrets/credentials: Yes / No
- No live integrations required: Yes / No
- Aggregate actuals approved if provided: Yes / No / Not provided
```

## JSON Template

```json
{
  "campaignNameOrCode": "",
  "productService": "",
  "objective": "",
  "targetSegment": "",
  "marketContext": "",
  "channelPlan": "",
  "budgetBand": "",
  "competitorContext": "",
  "creativeA": "",
  "creativeB": "",
  "creativeC": "",
  "riskConcerns": "",
  "successKpis": "",
  "aggregateActuals": "",
  "validationGoal": "",
  "assumptionsToReview": [],
  "safetyNotes": {
    "approvedForPovUse": false,
    "noPii": false,
    "noRawCrmOrCustomerLists": false,
    "noSecretsOrCredentials": false,
    "noLiveIntegrations": false,
    "aggregateActualsApprovedIfProvided": false
  }
}
```

## Field Mapping To `/proof-of-value`

| Template field | `/proof-of-value` field |
| --- | --- |
| campaignNameOrCode | Campaign name or anonymized code |
| productService | Product/service |
| objective | Objective |
| targetSegment | Target segment |
| marketContext | Market context |
| channelPlan | Channel plan |
| budgetBand | Budget band |
| competitorContext | Competitor context |
| creativeA | Creative direction A |
| creativeB | Creative direction B |
| creativeC | Creative direction C |
| riskConcerns | Risk concerns |
| successKpis | Success KPIs |
| aggregateActuals | Optional aggregate actuals |

## Operator Warning

Do not paste disallowed data into `/proof-of-value`, screenshots, issues, docs, chat, or decks. If the source material contains PII, raw CRM, customer lists, secrets, credentials, or live integration requirements, remove or replace them with approved aggregate or anonymized context before continuing.
