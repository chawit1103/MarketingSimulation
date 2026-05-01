# สร้าง Industry Template ให้ MSaaS ด้วย AI

## 🎯 เอกสารนี้สำหรับใคร

- Marketing Manager ที่อยากสร้าง Industry Template เอง
- Agency ที่ต้องการสร้าง template ให้ลูกค้า
- Developer ที่อยากเร่งสร้าง template หลายอุตสาหกรรม

## 📖 วิธีใช้

1. Copy **Prompt** ด้านล่าง
2. เปิด ChatGPT / Claude / Gemini
3. วาง prompt → กด Enter
4. AI จะ generate JSON template ให้
5. Copy JSON → Import เข้า MSaaS (Settings → Industry Templates → Drop zone)

---

## ⚡ PROMPT (ภาษาไทย)

```
คุณคือผู้เชี่ยวชาญด้านการตลาดและพฤติกรรมผู้บริโภคในประเทศไทย

ขอให้คุณสร้าง Industry Template สำหรับ MSaaS (Marketing Simulation as a Service) ในรูปแบบ JSON สำหรับอุตสาหกรรม: [ใส่ชื่ออุตสาหกรรมภาษาไทย เช่น "ธนาคารและการเงิน / "อสังหาริมทรัพย์" / "FMCG อาหารและเครื่องดื่ม"]

### ข้อกำหนดสำคัญ

1. **ใช้ภาษาไทยเป็นหลัก** — ทุกชื่อ, คำอธิบาย, narrative ต้องเป็นภาษาไทย
2. **จำนวน Persona** — 5-6 segments รวม 20-30 archetypes
3. **จำนวน Crisis Scenarios** — 5-7 scenarios ที่เกิดขึ้นจริงในวงการนี้ในประเทศไทย
4. **จำนวน Document Seeds** — 3 templates (press release, แถลงการณ์ฉุกเฉิน, ประกาศทางการ)
5. **ทุก ID ต้องเป็น lowercase_english** — เช่น "debt_burdened", "rural_elder"

### Persona Design Rules

แบ่ง persona segments ตามนี้:
- **3-4 กลุ่มในระบบนิเวศของอุตสาหกรรม** — เช่น ผู้บริโภค/ผู้ใช้บริการ, ผู้ได้รับผลกระทบ, ภาคธุรกิจที่เกี่ยวข้อง
- **1-2 กลุ่มที่มีอิทธิพลต่อภาพลักษณ์** — NGO/นักวิชาการ, สื่อ/Influencer, นักการเมือง/ข้าราชการ
- **1 กลุ่มผู้บริหาร/ผู้มีส่วนได้เสียโดยตรง** — ซีอีโอ, ผู้ถือหุ้น, พนักงาน

แต่ละ archetype ต้องมี:
- narrative_th: เรื่องเล่า 2-3 ประโยค ที่สะท้อนชีวิตจริงของคนไทย
- interests: 3-5 หัวข้อที่ persona สนใจเป็นภาษาไทย
- purchase_style: หนึ่งใน [impulsive, price_sensitive, researcher, early_adopter, social_proof, brand_loyal, traditional]
- income: หนึ่งใน [low, lower_middle, middle, upper_middle]
- channels: หนึ่งในหรือผสมของ [facebook, twitter_x, tiktok, instagram, youtube, line, tv, radio, shopee_live]
- regions: หนึ่งในหรือผสมของ [bangkok, central, north, northeast, east, south, west]

### Crisis Scenario Rules

แต่ละ scenario ต้องเป็นสิ่งที่ **เกิดขึ้นจริงแล้วหรือมีโอกาสเกิดสูง** ในประเทศไทย:
- trigger: บรรยายเหตุการณ์เป็นภาษาไทย ประโยคเดียว จริงและเฉพาะเจาะจง
- impact: negative / positive / mixed
- intensity: 1-10 (10 = วิกฤตรุนแรงที่สุด)

### ⚠️ KEY CONSTRAINTS — ห้ามเปลี่ยนชื่อ key! ห้ามใช้ nested objects!

❗ **นี่คือสาเหตุที่ import ไม่ผ่านบ่อยที่สุด** — AI มัก "คิดเอง" เปลี่ยนชื่อ key หรือยัด fields ไว้ใน nested object — ห้ามเด็ดขาด!

**ต้องใช้ key ตรงตามนี้เท่านั้น — ระบบ validate ด้วย exact match:**
- persona_segments ใช้ `"id"` (ห้ามใช้ segment_id)
- persona_segments ใช้ `"name_th"`, `"name_en"` (ห้ามใช้ segment_name, name)
- archetypes ใช้ `"name_th"`, `"narrative_th"`, `"occupation_th"` (ห้ามใช้ name, description, job)
- archetypes fields ต้อง **flat** — `"purchase_style": "..."` ✅ / `"traits": { "purchase_style": "..." }` ❌
- crisis_scenarios ใช้ `"name_th"`, `"trigger"` (ห้ามใช้ name, title, description)
- document_seeds ใช้ `"name_th"`, `"description_th"`, `"content"` (ห้ามใช้ title, type, body)
- archetypes ใช้ `"purchase_style"`, `"income"`, `"age_range"` (ห้าม nested ใน traits object)

### Output Format

ตอบกลับเป็น JSON เท่านั้น — ไม่มีคำอธิบายนำ ไม่มีบทสรุป ใช้โครงสร้างดังนี้:

```json
{
  "id": "industry_id_english",
  "name_th": "ชื่ออุตสาหกรรมภาษาไทย",
  "name_en": "Industry Name in English",
  "description_th": "คำอธิบายสั้นๆ ว่าทำไมต้องใช้ simulation ในอุตสาหกรรมนี้ — 2-3 ประโยค",
  "description_en": "English short description",
  "icon": "emoji ที่แทนอุตสาหกรรมนี้",
  "color": "#HEX color",
  "objectives": ["crisis_simulation", "brand_perception", ...],
  "default_objective": "crisis_simulation",
  "default_platform": "both",
  "default_max_rounds": 20,
  "default_language": "th",
  "target_audience": {
    "age_range": [18, 65],
    "gender": "all",
    "regions": ["bangkok", "central", "east", "south", "northeast"],
    "persona_count": 100
  },
  "persona_segments": [
    {
      "id": "segment_id",
      "name_th": "ชื่อกลุ่ม Persona ภาษาไทย",
      "name_en": "Segment Name English",
      "count": 25,
      "interests": ["ความสนใจ1", "ความสนใจ2"],
      "archetypes": [
        {
          "id": "archetype_id",
          "name_th": "ชื่อบุคคลต้นแบบ",
          "name_en": "Archetype Name",
          "age_range": [25, 40],
          "income": "middle",
          "regions": ["bangkok"],
          "occupation_th": "อาชีพ",
          "channels": ["twitter_x", "facebook"],
          "narrative_th": "เรื่องเล่าภาษาไทย 2-3 ประโยค",
          "purchase_style": "researcher"
        }
      ]
    }
  ],
  "crisis_scenarios": [
    {
      "id": "crisis_id",
      "name_th": "ชื่อสถานการณ์วิกฤตภาษาไทย",
      "name_en": "Crisis Name English",
      "trigger": "เหตุการณ์ที่กระตุ้นวิกฤต — ภาษาไทย 1 ประโยค เฉพาะเจาะจง",
      "impact": "negative",
      "intensity": 8
    }
  ],
  "document_seeds": [
    {
      "id": "seed_id",
      "name_th": "ชื่อเอกสารภาษาไทย",
      "description_th": "คำอธิบายว่าเอกสารนี้คืออะไร ใช้เมื่อไหร่",
      "content": "เนื้อหาเอกสารภาษาไทย — เขียนให้เหมือนของจริง ใช้ [วงเล็บ] สำหรับส่วนที่ต้องกรอก"
    }
  ]
}
```

### ตัวอย่าง Energy Template (บางส่วน)

```json
{
  "id": "energy",
  "name_th": "พลังงาน / น้ำมัน / สาธารณูปโภค",
  "name_en": "Energy / Oil / Utilities",
  "icon": "⚡",
  "color": "#FF4500",
  "persona_segments": [
    {
      "id": "commuters",
      "name_th": "ผู้ใช้รถยนต์-มอเตอร์ไซค์",
      "name_en": "Vehicle Commuters & Motorists",
      "interests": ["ราคาน้ำมัน", "การเดินทาง", "รถ EV"],
      "archetypes": [
        {
          "id": "office_driver",
          "name_th": "มนุษย์เงินเดือนขับรถ",
          "age_range": [25, 40],
          "income": "middle",
          "regions": ["bangkok"],
          "occupation_th": "พนักงานออฟฟิศ",
          "channels": ["twitter_x", "facebook", "tiktok"],
          "narrative_th": "พนักงานออฟฟิศในกรุงเทพ ขับรถไปทำงานทุกวัน เส้นทางบางนา-สีลม ค่าน้ำมันเดือนละ 5,500-6,500 บาท น้ำมันขึ้นทีโกรธที บ่นในกลุ่ม LINE เพื่อนที่ทำงาน",
          "purchase_style": "price_sensitive"
        }
      ]
    }
  ],
  "crisis_scenarios": [
    {
      "id": "fuel_price_hike",
      "name_th": "ขึ้นราคาน้ำมัน 1-2 บาท/ลิตร",
      "trigger": "กบง. มีมติขึ้นราคาน้ำมันดีเซล 2 บาท/ลิตร มีผลพรุ่งนี้ 05:00 น.",
      "impact": "negative",
      "intensity": 8
    }
  ]
}
```

---

### 📌 ข้อควรระวัง

- ❌ อย่าใช้ทับศัพท์ที่ไม่จำเป็น — "consumer segment" → "กลุ่มผู้บริโภค"
- ❌ อย่าใช้ persona แบบ generic — "consumer", "user" → ใช้ "มนุษย์เงินเดือนเช่าคอนโด", "เจ้าของร้านชำต่างจังหวัด"
- ❌ ❌❌ **ห้ามใช้ค่า enum นอกเหนือจากที่กำหนด!** — ถ้า AI ใช้ `quality_driven`, `high`, `upcountry`, `market_analysis` = ระบบ reject ทันที
- ✅ narrative_th ต้องสะท้อนชีวิตจริง — ใส่ตัวเลข, สถานที่, พฤติกรรมเฉพาะ
- ✅ interests ภาษาไทย — "ดอกเบี้ยบ้าน", "ค่าผ่อนรถ", "โปรโมชั่น 0%"
- ✅ document_seeds — เขียนให้เหมือนประกาศ/แถลงการณ์จริง
- ✅ ถ้า import แล้ว error — ส่ง error message + JSON ให้ AI บอก "แก้ตาม error นี้" → 10 วิเสร็จ
```

---

## 🧪 ตัวอย่างทดสอบ

Copy prompt ด้านบน → เปลี่ยน `[ใส่ชื่ออุตสาหกรรมภาษาไทย]` → วางใน ChatGPT:

```
คุณคือผู้เชี่ยวชาญด้านการตลาดและพฤติกรรมผู้บริโภคในประเทศไทย

ขอให้คุณสร้าง Industry Template สำหรับ MSaaS ในรูปแบบ JSON สำหรับอุตสาหกรรม: ธนาคารและการเงิน
...
```

AI จะ output JSON → Copy → Import เข้า MSaaS → ใช้ได้ทันที!
