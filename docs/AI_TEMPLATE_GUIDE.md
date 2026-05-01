# 🚀 สร้าง Industry Template ด้วย AI — 3 ขั้นตอน

เอกสารนี้สำหรับ **Marketing Manager** ที่อยากสร้าง Industry Template เองโดยไม่ต้องเขียนโค้ด

ใช้เวลา: **5 นาที**

---

## 📖 วิธีใช้

### Step 1: Copy Prompt

Copy ข้อความด้านล่างทั้งหมด:

```
คุณคือผู้เชี่ยวชาญด้านการตลาดและพฤติกรรมผู้บริโภคในประเทศไทย

ขอให้คุณสร้าง Industry Template สำหรับ MSaaS (Marketing Simulation as a Service) ในรูปแบบ JSON สำหรับอุตสาหกรรม: [ใส่ชื่ออุตสาหกรรมภาษาไทย]

### ข้อกำหนด

1. ใช้ภาษาไทยเป็นหลัก — ทุกชื่อ, คำอธิบาย, narrative ต้องเป็นภาษาไทย
2. 5-6 persona segments รวม 20-30 archetypes — สะท้อนชีวิตจริงของคนไทย
3. 5-7 crisis scenarios — เหตุการณ์ที่เกิดจริงหรือมีโอกาสเกิดสูงในไทย
4. 3 document seed templates (press release, แถลงการณ์, ประกาศทางการ)
5. ทุก ID เป็น lowercase_english

### ⚠️ ENUM CONSTRAINTS (ห้ามใช้ค่าอื่นเด็ดขาด!)

ค่าต่อไปนี้ต้องใช้ **ตรงตามที่กำหนดเท่านั้น** — สะกดผิดแม้แต่ตัวเดียว = ระบบ reject:

**purchase_style (ห้ามใช้คำอื่น!):**
เลือกจาก 7 ค่านี้เท่านั้น: impulsive | price_sensitive | researcher | early_adopter | social_proof | brand_loyal | traditional
❌ ห้ามใช้: quality_driven, roi_focused, luxury_driven, none, value_conscious, rational, emotional, หรือคำอื่นใด

**income:**
เลือกจาก 5 ค่านี้เท่านั้น: low | lower_middle | middle | upper_middle
❌ ห้ามใช้: high, medium, upper, premium, elite, poor, rich

**channels:**
เลือกจาก 9 ค่านี้เท่านั้น: facebook | twitter_x | tiktok | instagram | youtube | line | tv | radio | shopee_live
❌ ห้ามใช้: twitter (ต้อง twitter_x), linkedin, pantip, wechat, discord, podcasts, phone, email, news_portals

**regions (ประเทศไทย):**
เลือกจาก 7 ค่านี้เท่านั้น: bangkok | central | north | northeast | east | south | west
❌ ห้ามใช้: upcountry, urban, rural, eastern_seaboard, metropolitan, ทับศัพท์ภาษาไทย

**objectives:**
เลือกจาก 5 ค่านี้เท่านั้น: crisis_simulation | brand_perception | product_launch | competitor_response | message_testing
❌ ห้ามใช้: market_analysis, policy_impact_assessment, stakeholder_management, campaign_optimization

**impact (crisis scenarios):**
เลือกจาก 3 ค่านี้เท่านั้น: negative | positive | mixed

### 🔑 KEY CONSTRAINTS — ห้ามเปลี่ยนชื่อ key! ห้ามใช้ nested objects!

❗❗❗ **นี่คือสาเหตุอันดับ 1 ที่ import ไม่ผ่าน** — AI มัก "คิดเอง" เปลี่ยนชื่อ key หรือยัดทุกอย่างไว้ใน `"traits": {...}` — ห้ามทำเด็ดขาด!

ต้องใช้ key ตรงตามนี้เท่านั้น — สะกดผิด = พัง:

**persona_segments[x]:**
| ✅ ใช้ key นี้ | ❌ ห้ามใช้ |
|---------------|----------|
| `"id"` | `segment_id`, `seg_id`, `group_id` |
| `"name_th"` | `segment_name`, `name`, `title` |
| `"name_en"` | `segment_name_en`, `label` |
| `"count"` | `size`, `persona_count` |
| `"interests"` | `topics`, `tags`, `keywords` |

**archetypes[x]:**
| ✅ ใช้ key นี้ | ❌ ห้ามใช้ |
|---------------|----------|
| `"id"` | `arch_id`, `archetype_id`, `persona_id` |
| `"name_th"` | `name`, `title`, `label` |
| `"name_en"` | `label`, `display_name` |
| `"age_range"` | `age`, `age_min + age_max` |
| `"income"` | `income_level`, `salary` |
| `"regions"` | `region`, `location`, `city` |
| `"occupation_th"` | `job`, `role`, `occupation` |
| `"channels"` | `media`, `platform`, `social` |
| `"narrative_th"` | `description`, `story`, `bio`, `backstory` |
| `"purchase_style"` | `decision`, `buying`, `behavior` |

**crisis_scenarios[x]:**
| ✅ ใช้ key นี้ | ❌ ห้ามใช้ |
|---------------|----------|
| `"id"` | `crisis_id`, `event_id` |
| `"name_th"` | `title`, `name`, `event` |
| `"name_en"` | `title_en`, `label` |
| `"trigger"` | `description`, `scenario`, `detail`, `event` |
| `"impact"` | `impact_type`, `type` |
| `"intensity"` | `level`, `severity`, `score` |

**document_seeds[x]:**
| ✅ ใช้ key นี้ | ❌ ห้ามใช้ |
|---------------|----------|
| `"id"` | `doc_id`, `seed_id` |
| `"name_th"` | `title`, `name`, `label` |
| `"description_th"` | `desc`, `summary`, `type` |
| `"content"` | `body`, `text`, `document` |

**❌❌❌ ห้ามใช้ nested objects เช่น:**
```json
❌ "traits": { "purchase_style": "...", "income": "..." }  // ห้าม!
✅ "purchase_style": "researcher", "income": "middle"       // ถูกต้อง — flat fields!
```

### Persona Segments ที่ต้องมี
- 3-4 กลุ่มผู้บริโภค/ผู้ใช้บริการในระบบนิเวศ
- 1-2 กลุ่มผู้มีอิทธิพล (NGO, สื่อ, Influencer, นักการเมือง)
- 1 กลุ่มผู้บริหาร/ผู้มีส่วนได้เสีย

### Crisis Scenarios
เขียน trigger เป็นภาษาไทย 1 ประโยคที่เฉพาะเจาะจง ระบุ impact (negative/positive/mixed) และ intensity (1-10)

### Document Seeds
เขียนเนื้อหาให้เหมือนเอกสารจริง ใช้ [วงเล็บ] สำหรับส่วนที่ต้องกรอก

### Output: JSON เท่านั้น ห้ามมีคำอธิบายนำหรือสรุป

โครงสร้าง JSON:
{
  "id": "industry_id",
  "name_th": "ชื่ออุตสาหกรรม",
  "name_en": "Industry Name",
  "description_th": "คำอธิบาย",
  "description_en": "Description",
  "icon": "🎯",
  "color": "#HEX",
  "objectives": ["crisis_simulation", "brand_perception"],
  "default_objective": "crisis_simulation",
  "default_platform": "both",
  "default_max_rounds": 20,
  "default_language": "th",
  "target_audience": {"age_range": [18, 65], "gender": "all", "regions": ["bangkok", "central", "east", "south", "northeast"], "persona_count": 100},
  "persona_segments": [{
    "id": "seg_id",
    "name_th": "ชื่อกลุ่ม",
    "name_en": "Segment Name",
    "count": 30,
    "interests": ["ความสนใจไทย1", "ความสนใจไทย2"],
    "archetypes": [{
      "id": "arch_id",
      "name_th": "ชื่อบุคคล",
      "name_en": "Name",
      "age_range": [25, 40],
      "income": "middle",
      "regions": ["bangkok"],
      "occupation_th": "อาชีพ",
      "channels": ["facebook", "tiktok"],
      "narrative_th": "เรื่องเล่า 2-3 ประโยค สะท้อนชีวิตจริง",
      "purchase_style": "researcher"
    }]
  }],
  "crisis_scenarios": [{
    "id": "crisis_id",
    "name_th": "ชื่อวิกฤต",
    "name_en": "Crisis Name",
    "trigger": "เหตุการณ์ภาษาไทย 1 ประโยค",
    "impact": "negative",
    "intensity": 8
  }],
  "document_seeds": [{
    "id": "seed_id",
    "name_th": "ชื่อเอกสาร",
    "description_th": "คำอธิบาย",
    "content": "เนื้อหาเอกสาร — ใช้ [วงเล็บ] สำหรับส่วนที่ต้องกรอก"
  }]
}
```

### Step 2: เปลี่ยนชื่ออุตสาหกรรม

เปลี่ยน `[ใส่ชื่ออุตสาหกรรมภาษาไทย]` เป็นอุตสาหกรรมที่ต้องการ เช่น:

- `ธนาคารและการเงินในยุคหนี้ครัวเรือนสูง`
- `อสังหาริมทรัพย์ วิกฤตกำลังซื้อหด`
- `FMCG อาหารและเครื่องดื่ม สงครามราคา`
- `ประกันภัยและ InsurTech`
- `ค้าปลีกและ E-Commerce`
- `ยานยนต์ EV Transformation`
- `โทรคมนาคม หลังควบรวม TRUE-DTAC`
- `โรงแรมและท่องเที่ยว ฟื้นตัวหลังโควิด`

### Step 3: วาง Prompt + Import

1. เปิด **ChatGPT** / **Claude** / **Gemini**
2. วาง prompt → กด Enter
3. AI จะ generate JSON
4. Copy JSON ทั้งหมด
5. เข้า **MSaaS → Settings → Industry Templates → Drop Zone**
6. ลากไฟล์ .json หรือวาง → Import
7. Template พร้อมใช้ที่หน้า **New Campaign** ทันที!

---

## ✅ ผลลัพธ์ที่คุณจะได้

- ✅ Persona 20-30 แบบที่สะท้อนคนไทยจริง
- ✅ Crisis scenarios 5-7 แบบที่เกิดจริงในวงการ
- ✅ Document seeds 3 แบบพร้อมใช้
- ✅ ใช้ได้ทันที — สร้าง campaign จาก template ใน 1 คลิก
- ✅ แชร์ให้ agency/client import ใช้ต่อได้

---

## 💡 Tips

- **ยิ่ง prompt เฉพาะเจาะจงยิ่งดี** — "อสังหาฯ" vs "อสังหาริมทรัพย์แนวราบ วิกฤตดอกเบี้ยสูง คนกู้ไม่ผ่าน"
- **AI แต่ละตัวเก่งต่างกัน** — Claude เก่งภาษาไทยและละเอียด, ChatGPT เก่ง structure, Gemini เร็วและฟรี
- **Enum values เป๊ะๆ** — 🔴 purchase_style/income/channels ต้องตรงตาม list — prompt มี constraints แล้ว
- **Key names ห้ามเปลี่ยน!** — 🔴🔴 Gemini/Claude มัก "คิดเอง" เปลี่ยน schema (segment_id, description, traits nested) — **ห้าม!** ต้องใช้ key ตามตารางเท่านั้น
- **Flat fields เท่านั้น!** — `"purchase_style": "researcher"` ✅ / `"traits": {"purchase_style": "..."}` ❌
- **ตรวจสอบก่อน import** — ระบบจะ validate JSON ให้ ถ้า format ผิดจะมี error message บอกว่าพลาดที่ field ไหน
- **Import ไม่ผ่าน? ไม่ต้อง panic** — ส่ง JSON + error message ให้ AI บอกว่า "แก้ให้หน่อย" มันจะแก้ให้ใน 10 วิ
- **แก้ไขทีหลังได้** — import → ใช้ → export → แก้ → import ใหม่
- **4 templates พร้อมแล้ว** — Energy, Finance, Real Estate, FMCG ใช้เป็นตัวอย่าง/ต้นแบบได้

---

## 📦 ตัวอย่าง Prompt สำเร็จรูป

Copy อันนี้ไปใช้เลย — เปลี่ยนแค่ชื่ออุตสาหกรรม:

> **ธนาคาร/การเงิน:** `ธนาคารและการเงินในไทย ยุคหนี้ครัวเรือน 90% GDP ดอกเบี้ยสูง NPL พุ่ง`
>
> **อสังหาฯ:** `อสังหาริมทรัพย์ไทย ตลาดซบเซา กู้ไม่ผ่าน ดอกเบี้ยสูง คนรอซื้อ โครงการล้น`
>
> **FMCG:** `FMCG อาหารและเครื่องดื่มในไทย สงครามราคา Modern Trade กดดัน คนไทยจนลง ซื้อของถูก`
>
> **ประกันภัย:** `ประกันภัยไทย หลังวิกฤต COVID เจ๊ง ความเชื่อมั่นต่ำ ประกันสุขภาพโต ประกัน EV มา`
>
> **Retail:** `ค้าปลีกและ E-Commerce ไทย ตลาดหด กำลังซื้อต่ำ Lazada/Shopee/TikTok Shop แข่งตัดราคา`
