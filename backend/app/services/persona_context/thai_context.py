"""Thai Context — demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Thai
consumer insights, regional differences, and cultural values.
"""

# Thai population by region (2024 estimates, millions)
REGION_POPULATION = {
    "bangkok": 5.5,
    "central": 16.0,
    "north": 11.5,
    "northeast": 21.5,
    "east": 5.8,
    "south": 9.5,
    "west": 3.5,
}

# Regional cultural profiles
REGION_PROFILES = {
    "bangkok": {
        "traits": ["urban", "fast-paced", "status-conscious", "early-adopter"],
        "values_emphasis": ["face_saving", "hierarchy_respect"],
        "media": ["tiktok", "instagram", "twitter_x", "youtube"],
        "income_bias": "upper_middle",
        "occupations": ["office worker", "business owner", "freelancer", "government officer"],
        "lifestyle_note": "ชีวิตคนเมือง รถติด เวลาน้อย นิยมสั่งเดลิเวอรี่และช้อปปิ้งออนไลน์",
    },
    "north": {
        "traits": ["traditional", "artistic", "community-oriented", "slow-living"],
        "values_emphasis": ["family_centric", "nam_jai", "bunkhun"],
        "media": ["facebook", "youtube", "line", "radio"],
        "income_bias": "lower_middle",
        "occupations": ["farmer", "artisan", "small business owner", "tourism worker"],
        "lifestyle_note": "ชีวิตเรียบง่าย ผูกพันกับธรรมชาติ ประเพณีล้านนา มีน้ำใจต่อชุมชน",
    },
    "northeast": {
        "traits": ["hardworking", "family-oriented", "price-sensitive", "loyal"],
        "values_emphasis": ["family_centric", "bunkhun", "greeng_jai"],
        "media": ["facebook", "tiktok", "line", "shopee_live"],
        "income_bias": "low",
        "occupations": ["farmer", "laborer", "small vendor", "factory worker"],
        "lifestyle_note": "ชีวิตเกษตรกรรม ส่งเสียครอบครัว ลูกหลานไปทำงานต่างจังหวัด/กรุงเทพ",
    },
    "south": {
        "traits": ["direct", "religious", "community-strong", "entrepreneurial"],
        "values_emphasis": ["family_centric", "social_harmony"],
        "media": ["facebook", "youtube", "line", "tiktok"],
        "income_bias": "middle",
        "occupations": ["fisherman", "rubber farmer", "tourism worker", "trader"],
        "lifestyle_note": "ชีวิตติดทะเล ค้าขาย ศาสนาเข้มแข็ง ครอบครัวใหญ่",
    },
    "central": {
        "traits": ["balanced", "pragmatic", "mixed-traditional-modern"],
        "values_emphasis": ["social_harmony", "mai_pen_rai"],
        "media": ["facebook", "youtube", "line", "tiktok"],
        "income_bias": "middle",
        "occupations": ["factory worker", "government officer", "farmer", "merchant"],
        "lifestyle_note": "ชีวิตชานเมือง ผสมผสานเมือง-ชนบท เดินทางเข้ากรุงเทพ",
    },
    "east": {
        "traits": ["industrial", "migrant-worker", "pragmatic"],
        "values_emphasis": ["face_saving", "family_centric"],
        "media": ["facebook", "tiktok", "line", "youtube"],
        "income_bias": "middle",
        "occupations": ["factory worker", "logistics", "tourism worker", "farmer"],
        "lifestyle_note": "ชีวิตนิคมอุตสาหกรรม แรงงานข้ามถิ่น เศรษฐกิจภาคตะวันออก",
    },
    "west": {
        "traits": ["agricultural", "traditional", "nature-connected"],
        "values_emphasis": ["mai_pen_rai", "family_centric", "nam_jai"],
        "media": ["facebook", "youtube", "line", "tv"],
        "income_bias": "lower_middle",
        "occupations": ["farmer", "fisherman", "small vendor", "tourism worker"],
        "lifestyle_note": "ชีวิตเกษตร ประมง ติดธรรมชาติ การท่องเที่ยวเชิงอนุรักษ์",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "young_urban_professional": {
        "age_range": (25, 35),
        "income": "upper_middle",
        "regions": ["bangkok"],
        "education": "bachelors",
        "values": ["face_saving", "sanuk"],
        "decision": "social_proof",
        "channels": ["instagram", "tiktok", "twitter_x"],
        "spending": (20000, 50000),
        "narrative": "คนรุ่นใหม่ทำงานออฟฟิศในกรุงเทพ ใช้ชีวิตในคอนโด สั่ง Grab ทานข้าว ติดตามอินฟลูเอนเซอร์ การตัดสินใจซื้อขึ้นกับรีวิวและกระแสโซเชียล",
    },
    "family_mom": {
        "age_range": (30, 50),
        "income": "middle",
        "regions": ["bangkok", "central", "north"],
        "education": "bachelors",
        "values": ["family_centric", "greeng_jai", "hierarchy_respect"],
        "decision": "researcher",
        "channels": ["facebook", "line", "youtube"],
        "spending": (10000, 30000),
        "narrative": "คุณแม่ทำงาน เลี้ยงลูก 1-2 คน รับผิดชอบการตัดสินใจซื้อของครอบครัว ศึกษาข้อมูลก่อนซื้อ  ซื้อของผ่าน Shopee/Lazada ดูรีวิวจาก Pantip และกลุ่ม Facebook แม่ๆ",
    },
    "rural_elder": {
        "age_range": (50, 70),
        "income": "low",
        "regions": ["northeast", "north", "south"],
        "education": "high_school",
        "values": ["bunkhun", "hierarchy_respect", "traditional"],
        "decision": "traditional",
        "channels": ["facebook", "tv", "radio", "line"],
        "spending": (2000, 8000),
        "narrative": "ผู้สูงอายุในชนบท รับเงินจากลูกหลานที่ไปทำงานในเมือง ใช้จ่ายผ่านร้านค้าชุมชน ซื้อของใช้จำเป็น เชื่อถือคำแนะนำจากลูกหลานและเพื่อนบ้านมากกว่าโฆษณา",
    },
    "gen_z_student": {
        "age_range": (18, 24),
        "income": "low",
        "regions": ["bangkok", "central", "northeast"],
        "education": "bachelors",
        "values": ["sanuk", "mai_pen_rai", "face_saving"],
        "decision": "impulsive",
        "channels": ["tiktok", "instagram", "twitter_x", "shopee_live"],
        "spending": (3000, 10000),
        "narrative": "นักศึกษามหาวิทยาลัย รับเงินจากพ่อแม่ ใช้จ่ายกับความบันเทิง แฟชั่น และกินดื่ม ชอบซื้อตาม TikTok/IG เทรนด์ ตัดสินใจซื้อเร็ว แต่เปลี่ยนแบรนด์บ่อย",
    },
    "smb_owner": {
        "age_range": (35, 55),
        "income": "upper_middle",
        "regions": ["bangkok", "central", "east", "south"],
        "education": "bachelors",
        "values": ["face_saving", "family_centric", "hierarchy_respect"],
        "decision": "researcher",
        "channels": ["facebook", "line", "youtube"],
        "spending": (30000, 100000),
        "narrative": "เจ้าของธุรกิจขนาดกลาง-เล็ก มีลูกน้อง 5-50 คน ใช้ LINE OA สื่อสารกับลูกค้า ใช้ Facebook Ads โปรโมทธุรกิจ สนใจ ROI ชัดเจน ไม่เปลี่ยนแบรนด์ง่าย แต่เปลี่ยนถ้ามีคนแนะนำที่น่าเชื่อถือ",
    },
    "digital_nomad": {
        "age_range": (25, 40),
        "income": "upper_middle",
        "regions": ["bangkok", "north"],
        "education": "masters",
        "values": ["sanuk", "mai_pen_rai"],
        "decision": "early_adopter",
        "channels": ["twitter_x", "youtube", "instagram"],
        "spending": (20000, 60000),
        "narrative": "ฟรีแลนซ์/รีโมทเวิร์คเกอร์ ทำงานกับบริษัทต่างประเทศ ใช้ชีวิตใน coworking space และคาเฟ่ ใช้จ่ายกับประสบการณ์ เทคโนโลยี และท่องเที่ยว ไม่สนใจแบรนด์ใหญ่ ชอบลองของใหม่",
    },
    "factory_worker": {
        "age_range": (20, 45),
        "income": "lower_middle",
        "regions": ["east", "central", "northeast"],
        "education": "high_school",
        "values": ["family_centric", "greeng_jai", "bunkhun"],
        "decision": "price_sensitive",
        "channels": ["facebook", "tiktok", "line"],
        "spending": (3000, 10000),
        "narrative": "พนักงานโรงงานในนิคมอุตสาหกรรม ส่งเงินกลับบ้านต่างจังหวัด ซื้อของตามงบประมาณ ใช้จ่ายผ่าน 7-Eleven และตลาดนัด ชอบโปรโมชั่นและของแถม ดู TikTok เพื่อความบันเทิงหลังเลิกงาน",
    },
}

# Thai name pools (for realistic name generation)
THAI_NAMES = {
    "male": ["สมชาย", "ประสิทธิ์", "ธนวัฒน์", "ณัฐพงษ์", "กิตติศักดิ์", "วรพล", "ภาณุ", "ชยพล",
             "เอกชัย", "ศุภโชค", "ธีรพงษ์", "อนุชา", "วีรยุทธ", "ปิยะพงษ์", "นพดล"],
    "female": ["สมหญิง", "นภัสสร", "กัญญารัตน์", "สุภารัตน์", "พิมพ์ชนก", "ณัฐธิดา", "รุ่งนภา",
               "จันทิมา", "วรางคณา", "มัลลิกา", "เพ็ญนภา", "อรุณี", "สุนิสา", "รัตนา", "ภัทรธิดา"],
    "nickname_male": ["ต้น", "บอล", "โจ้", "นัท", "ก้อง", "อาร์ม", "บิ๊ก", "ปั๊บ", "เต้", "แม็ค",
                      "เจมส์", "ฟลุ๊ค", "แบงค์", "เบียร์", "เคน"],
    "nickname_female": ["เมย์", "ฝน", "นุช", "แป้ง", "กิ๊ฟ", "เบล", "มิ้น", "ปุ๊ก", "ติ๊ก", "แอน",
                        "นุ่น", "จอย", "มุก", "พิม", "เฟิร์น"],
    "surnames": ["วงศ์สุวรรณ", "รัตนโกสินทร์", "บุญนำพา", "แสงจันทร์", "ศรีสมบูรณ์",
                 "อินทรักษา", "ทองดี", "พานิชเจริญ", "แก้ววิเชียร", "ธรรมโชติ"],
}

# Common Thai consumer phrases (for LLM persona grounding)
THAI_SHOPPING_PHRASES = [
    "ของมันต้องมี", "ซื้อก่อนคิดทีหลัง", "รอโปร",
    "ซื้อตามรีวิว", "ของแท้ต้องดูจาก", "ลองก่อนซื้อ",
    "มีผ่อน 0% ไหม", "ส่งฟรีไหม", "เก็บเงินปลายทางได้ไหม",
    "ซื้อที่ห้างดีกว่า", "ซื้อออนไลน์ถูกกว่า", "ร้านนี้เชื่อถือได้ไหม",
    "เดี๋ยวถามเพื่อนก่อน", "เห็นใน TikTok", "แม่ค้าบอกว่าดี",
    "ลองใช้ sample ก่อน", "ของถูกและดีมีจริงไหม",
]

THAI_TRUST_FACTORS = [
    "รีวิวจากผู้ใช้จริง", "แนะนำโดยเพื่อน/ครอบครัว", "มีหน้าร้านอยู่จริง",
    "แบรนด์ดัง/รู้จัก", "มีใบรับรอง/อย.", "ใช้ดีอยู่แล้ว/ซื้อซ้ำ",
    "เห็นโฆษณาบ่อย", "โปรโมชั่นน่าสนใจ", "อินฟลูเอนเซอร์แนะนำ",
    "คนใช้เยอะ/เป็นกระแส", "บริการหลังการขายดี", "เป็นแบรนด์ไทย",
]

# For ContextRegistry compatibility
COUNTRY_NAME = "ประเทศไทย"
CURRENCY = "THB"
PERSONA_NAMES = THAI_NAMES
