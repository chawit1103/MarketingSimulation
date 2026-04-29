"""Arabic/MENA Context — demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Arab consumer
insights, regional differences, and cultural values across the MENA region.
"""

COUNTRY_NAME = "Arab/MENA"
CURRENCY = "SAR (Saudi Riyal) / AED (UAE Dirham)"

# Arab/MENA population by region (2024 estimates, millions)
REGION_POPULATION = {
    "saudi_riyadh": 7.5,
    "uae_dubai": 3.6,
    "egypt_cairo": 22.0,
    "morocco_casablanca": 3.7,
    "jordan_amman": 4.0,
    "lebanon_beirut": 2.4,
}

# Regional cultural profiles
REGION_PROFILES = {
    "saudi_riyadh": {
        "traits": ["conservative", "status-conscious", "family-centered", "tech-savvy"],
        "values_emphasis": ["faith_ايمان", "family_عائلة", "honor_شرف"],
        "media": ["twitter_x", "snapchat", "youtube", "instagram", "tiktok"],
        "income_bias": "upper_middle",
        "occupations": ["government employee", "business executive", "engineer", "entrepreneur", "oil & gas professional"],
        "lifestyle_note": "الحياة في الرياض مزيج من التقاليد والحداثة، أسر متماسكة، تسوق في المولات الكبرى، اهتمام كبير بالعلامات التجارية الفاخرة",
    },
    "uae_dubai": {
        "traits": ["cosmopolitan", "status-driven", "diverse", "fast-paced"],
        "values_emphasis": ["hospitality_كرم", "honor_شرف", "community_مجتمع"],
        "media": ["instagram", "linkedin", "twitter_x", "youtube", "snapchat"],
        "income_bias": "high",
        "occupations": ["business executive", "finance professional", "tech entrepreneur", "real estate developer", "consultant"],
        "lifestyle_note": "دبي مدينة عالمية سريعة الخطى، تنوع ثقافي كبير، حياة الرفاهية والتسوق الفاخر، توازن بين الانفتاح والتقاليد",
    },
    "egypt_cairo": {
        "traits": ["resilient", "price-sensitive", "family-oriented", "humorous"],
        "values_emphasis": ["family_عائلة", "faith_ايمان", "community_مجتمع", "hospitality_كرم"],
        "media": ["facebook", "youtube", "instagram", "whatsapp", "tiktok"],
        "income_bias": "lower_middle",
        "occupations": ["government clerk", "teacher", "engineer", "small trader", "service worker"],
        "lifestyle_note": "القاهرة مدينة لا تنام، زحام وحياة شعبية، الأسر الكبيرة هي الأساس، الفكاهة المصرية جزء من الهوية، التسوق في الأسواق الشعبية والمولات",
    },
    "morocco_casablanca": {
        "traits": ["pragmatic", "bilingual", "family-centered", "entrepreneurial"],
        "values_emphasis": ["family_عائلة", "hospitality_كرم", "community_مجتمع"],
        "media": ["facebook", "instagram", "youtube", "whatsapp", "tiktok"],
        "income_bias": "middle",
        "occupations": ["business manager", "banker", "retail worker", "artisan", "call center agent"],
        "lifestyle_note": "الدار البيضاء عاصمة اقتصادية، مزيج من العربية والفرنسية والأمازيغية، حياة عصرية مع تمسك بالتقاليد، الأسواق التقليدية بجانب المولات الحديثة",
    },
    "jordan_amman": {
        "traits": ["educated", "pragmatic", "family-oriented", "tech-aware"],
        "values_emphasis": ["family_عائلة", "honor_شرف", "hospitality_كرم", "education"],
        "media": ["facebook", "instagram", "youtube", "twitter_x", "whatsapp"],
        "income_bias": "middle",
        "occupations": ["IT professional", "engineer", "doctor", "teacher", "government employee"],
        "lifestyle_note": "عمان مدينة هادئة نسبياً، مجتمع متعلم، ترابط عائلي قوي، ثقافة المقاهي والمطاعم، اهتمام بالتكنولوجيا وريادة الأعمال",
    },
    "lebanon_beirut": {
        "traits": ["resilient", "creative", "social", "adaptable"],
        "values_emphasis": ["family_عائلة", "community_مجتمع", "hospitality_كرم"],
        "media": ["instagram", "whatsapp", "facebook", "tiktok", "twitter_x"],
        "income_bias": "varied_low_to_high",
        "occupations": ["creative professional", "banker", "entrepreneur", "trader", "freelancer"],
        "lifestyle_note": "بيروت مدينة الصمود والإبداع، حياة ليلية نابضة، مطبخ عالمي، تنوع طائفي وثقافي، اقتصاد متقلب لكن روح المبادرة قوية",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "young_professional": {
        "age_range": (24, 35),
        "income": "upper_middle",
        "regions": ["saudi_riyadh", "uae_dubai", "jordan_amman"],
        "education": "bachelors",
        "values": ["faith_ايمان", "honor_شرف", "family_عائلة"],
        "decision": "brand_loyal",
        "channels": ["instagram", "twitter_x", "snapchat", "linkedin"],
        "spending": (8000, 25000),
        "narrative": "شاب/شابة جامعي يعمل في شركة كبرى، يهتم بالمظهر والماركات، يتابع المؤثرين على سناب وإنستغرام، يفضل الجودة على السعر، يتسوق من المولات والمتاجر الإلكترونية الفاخرة",
    },
    "family_matron": {
        "age_range": (35, 55),
        "income": "middle",
        "regions": ["saudi_riyadh", "egypt_cairo", "morocco_casablanca", "jordan_amman"],
        "education": "bachelors",
        "values": ["family_عائلة", "hospitality_كرم", "faith_ايمان"],
        "decision": "researcher",
        "channels": ["whatsapp", "facebook", "instagram", "youtube"],
        "spending": (5000, 15000),
        "narrative": "ربة منزل وأم مسؤولة عن الأسرة، تدير ميزانية المنزل، تبحث عن أفضل العروض، تتأثر بتوصيات الصديقات والقريبات عبر واتساب، تشتري لأطفالها وزوجها قبل نفسها",
    },
    "religious_scholar": {
        "age_range": (40, 65),
        "income": "middle",
        "regions": ["saudi_riyadh", "egypt_cairo", "jordan_amman"],
        "education": "masters",
        "values": ["faith_ايمان", "community_مجتمع", "honor_شرف"],
        "decision": "traditional",
        "channels": ["youtube", "twitter_x", "whatsapp", "telegram"],
        "spending": (4000, 12000),
        "narrative": "رجل دين أو داعية، محترم في مجتمعه، يهتم بالحلال والطيب، يتجنب المنتجات المشبوهة، يشارك المعرفة الدينية عبر يوتيوب وتويتر، يشتري من محلات موثوقة",
    },
    "entrepreneur": {
        "age_range": (28, 50),
        "income": "upper_middle",
        "regions": ["uae_dubai", "saudi_riyadh", "lebanon_beirut"],
        "education": "bachelors",
        "values": ["honor_شرف", "hospitality_كرم", "community_مجتمع"],
        "decision": "early_adopter",
        "channels": ["linkedin", "twitter_x", "instagram", "youtube"],
        "spending": (15000, 50000),
        "narrative": "رائد أعمال طموح، يتابع أحدث التقنيات، يستثمر في التكنولوجيا والعقارات، يهتم ببناء العلاقات، يسافر كثيراً، يتأثر بآراء رواد الأعمال الآخرين على لينكدإن وتويتر",
    },
    "university_student": {
        "age_range": (18, 24),
        "income": "low",
        "regions": ["egypt_cairo", "morocco_casablanca", "jordan_amman", "lebanon_beirut"],
        "education": "bachelors",
        "values": ["community_مجتمع", "family_عائلة", "faith_ايمان"],
        "decision": "social_proof",
        "channels": ["tiktok", "instagram", "youtube", "whatsapp"],
        "spending": (1000, 4000),
        "narrative": "طالب جامعي مهتم بالتقنية والموضة، يتابع المؤثرين على تيك توك وإنستغرام، ميزانيته محدودة لكنه يواكب الترندات، يتأثر بأصدقائه وزملائه في الجامعة",
    },
    "expat_worker": {
        "age_range": (25, 45),
        "income": "middle",
        "regions": ["uae_dubai", "saudi_riyadh", "lebanon_beirut"],
        "education": "bachelors",
        "values": ["hospitality_كرم", "family_عائلة", "community_مجتمع"],
        "decision": "price_sensitive",
        "channels": ["facebook", "whatsapp", "youtube", "instagram"],
        "spending": (4000, 15000),
        "narrative": "عامل مغترب من جنوب آسيا أو الوطن العربي، يرسل جزءاً كبيراً من راتبه لأسرته في بلده الأصلي، يبحث عن أفضل قيمة مقابل المال، يستخدم واتساب للتواصل مع العائلة، يشتري من المحلات الشعبية والسوبرماركت",
    },
}

# Arab name pools (for realistic name generation)
PERSONA_NAMES = {
    "male": [
        "محمد", "أحمد", "عمر", "علي", "خالد", "عبدالله", "يوسف", "حسن",
        "كريم", "طارق", "سامي", "فهد", "راشد", "إبراهيم", "ناصر",
        "محمود", "وليد", "صلاح", "هشام", "باسم",
    ],
    "female": [
        "فاطمة", "مريم", "نور", "سارة", "عائشة", "زينب", "ليلى", "هدى",
        "ريم", "منى", "أمل", "دينا", "رانيا", "نادين", "لطيفة",
        "خديجة", "جميلة", "سهى", "عبير", "حنان",
    ],
    "surnames": [
        "العتيبي", "القحطاني", "الرشيد", "الهاشمي", "العلي",
        "إبراهيم", "منصور", "جمعة", "سلمان", "الحسيني",
        "الغامدي", "المالكي", "الشريف", "النعيمي", "الظفيري",
        "الأسعد", "بدران", "صباغ", "الخوري", "فرحات",
    ],
}

# Common Arab consumer phrases (for LLM persona grounding)
ARABIC_SHOPPING_PHRASES = [
    "كم السعر؟", "آخر سعر", "غالي شوي",
    "عندكم توصيل؟", "هل عليه ضمان؟", "خذه والله يستاهل",
    "شفت الإعلان بالتلفزيون", "جربته قبل", "أختي جربته وعجبها",
    "شو رأيك بهذا المنتج؟", "أصلي ولا تقليد؟",
    "عندكم عروض؟", "اشتريته من المول", "اطلب أونلاين أوفر",
    "المحل الفلاني أرخص", "جودة أوروبية", "صناعة وطنية",
    "تخفيضات الموسم", "نفس يلي يستخدمه فلان",
]

TRUST_FACTORS = [
    "توصية الأهل والأصدقاء", "سمعة المتجر", "وجود ضمان",
    "تقييمات المستخدمين", "ماركة معروفة", "سعر معقول",
    "خدمة عملاء ممتازة", "منتج حلال", "سهولة الإرجاع",
    "توصية مؤثر موثوق", "إعلان احترافي", "صناعة بلد موثوق",
    "رأي خبير/طبيب", "تجربة سابقة إيجابية", "وجود فرع قريب",
]
