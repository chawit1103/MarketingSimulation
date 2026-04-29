"""Pakistani Context — demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Pakistani consumer
insights, regional differences, and cultural values.
"""

COUNTRY_NAME = "Pakistan"
CURRENCY = "PKR (Pakistani Rupee)"

# Pakistan population by region (2024 estimates, millions for metro areas)
REGION_POPULATION = {
    "karachi": 20.0,
    "lahore": 13.0,
    "islamabad": 2.3,
    "peshawar": 4.5,
    "quetta": 1.2,
    "faisalabad": 3.7,
}

# Regional cultural profiles
REGION_PROFILES = {
    "karachi": {
        "traits": ["cosmopolitan", "fast-paced", "entrepreneurial", "diverse"],
        "values_emphasis": ["faith_ایمان", "family", "hospitality"],
        "media": ["instagram", "youtube", "facebook", "tiktok", "twitter_x"],
        "income_bias": "middle",
        "occupations": ["businessman", "banker", "IT professional", "doctor", "textile worker"],
        "lifestyle_note": "کراچی — روشنیوں کا شہر، معاشی ریڑھ کی ہڈی۔ یہاں کی زندگی تیز، کاروباری اور متنوع ہے۔ بریانی اور چائے کے بغیر دن ادھورا، لوگ محنتی اور پُرجوش ہیں",
    },
    "lahore": {
        "traits": ["cultural", "food-loving", "warm", "historical"],
        "values_emphasis": ["family", "hospitality", "honor_عزت", "community"],
        "media": ["instagram", "facebook", "tiktok", "youtube", "whatsapp"],
        "income_bias": "middle",
        "occupations": ["businessman", "lawyer", "teacher", "government officer", "artist"],
        "lifestyle_note": "لاہور — دل والوں کا شہر، کھانے اور تہذیب کا مرکز۔ لوگ مہمان نواز، زندہ دل اور ثقافت سے جڑے ہیں۔ اینارکلی سے لے کر ایم ایم عالم روڈ تک خریداری کا شوق",
    },
    "islamabad": {
        "traits": ["educated", "organized", "peaceful", "bureaucratic"],
        "values_emphasis": ["education", "family", "faith_ایمان"],
        "media": ["instagram", "linkedin", "twitter_x", "youtube", "facebook"],
        "income_bias": "upper_middle",
        "occupations": ["government officer", "diplomat", "IT professional", "consultant", "academic"],
        "lifestyle_note": "اسلام آباد — پاکستان کا جدید اور منظم چہرہ۔ مارگلہ کی پہاڑیاں، صاف سڑکیں اور پُرسکون زندگی۔ یہاں کے لوگ تعلیم یافتہ اور معیار زندگی کے خواہاں ہیں",
    },
    "peshawar": {
        "traits": ["traditional", "honorable", "tribal", "resilient"],
        "values_emphasis": ["honor_عزت", "faith_ایمان", "hospitality", "family"],
        "media": ["facebook", "youtube", "whatsapp", "tiktok"],
        "income_bias": "lower_middle",
        "occupations": ["trader", "farmer", "craftsman", "government worker", "transport worker"],
        "lifestyle_note": "پشاور — بہادری اور روایت کا شہر۔ پٹھان ثقافت کا مرکز، قصہ خوانی بازار کی چائے، مہمان نوازی بے مثال، عزت اور غیرت زندگی کا محور",
    },
    "quetta": {
        "traits": ["tribal", "hardy", "traditional", "cross-border"],
        "values_emphasis": ["honor_عزت", "faith_ایمان", "family", "hospitality"],
        "media": ["facebook", "whatsapp", "television", "youtube"],
        "income_bias": "low",
        "occupations": ["trader", "farmer", "miner", "government worker", "transport worker"],
        "lifestyle_note": "کوئٹہ — بلوچستان کا دل، پہاڑوں میں بسی زندگی۔ سرد موسم، خشک میوہ جات، قبائلی روایات کا مضبوط اثر، سادہ مگر باعزت زندگی",
    },
    "faisalabad": {
        "traits": ["industrial", "hardworking", "pragmatic", "textile-hub"],
        "values_emphasis": ["family", "community", "faith_ایمان"],
        "media": ["facebook", "youtube", "tiktok", "whatsapp"],
        "income_bias": "lower_middle",
        "occupations": ["textile worker", "trader", "farmer", "factory owner", "mechanic"],
        "lifestyle_note": "فیصل آباد — صنعت کا شہر، ٹیکسٹائل کی دُنیا۔ محنتی اور مڈل کلاس عوام، سادہ زندگی، کارخانوں کی سیٹی اور منڈیوں کی چہل پہل",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "urban_professional": {
        "age_range": (25, 40),
        "income": "upper_middle",
        "regions": ["karachi", "lahore", "islamabad"],
        "education": "masters",
        "values": ["education", "family", "faith_ایمان"],
        "decision": "researcher",
        "channels": ["instagram", "linkedin", "youtube", "twitter_x"],
        "spending": (30000, 100000),
        "narrative": "شہری پیشہ ور — یونیورسٹی سے فارغ، بینک یا ملٹی نیشنل کمپنی میں ملازمت، آن لائن شاپنگ کا شوق، برانڈ پسند مگر قیمت سے بھی آگاہ، سنگل ہو تو فیملی کی ذمہ داری بھی",
    },
    "rural_farmer": {
        "age_range": (30, 60),
        "income": "lower_middle",
        "regions": ["faisalabad", "peshawar", "quetta"],
        "education": "primary",
        "values": ["faith_ایمان", "family", "honor_عزت", "community"],
        "decision": "traditional",
        "channels": ["television", "facebook", "radio"],
        "spending": (5000, 20000),
        "narrative": "دیہاتی کسان — زمین سے جُڑی زندگی، فصل کی آمدنی پر انحصار، سادہ اور روایتی خریداری، ہر چیز کا حساب کتاب، بچوں کی تعلیم اور شادی زندگی کا بڑا مقصد",
    },
    "university_student": {
        "age_range": (18, 25),
        "income": "low",
        "regions": ["karachi", "lahore", "islamabad", "peshawar"],
        "education": "bachelors",
        "values": ["education", "community", "faith_ایمان"],
        "decision": "social_proof",
        "channels": ["instagram", "tiktok", "youtube", "whatsapp"],
        "spending": (2000, 8000),
        "narrative": "یونیورسٹی کا طالب علم — والدین کی مالی مدد پر انحصار، دوستوں کے مشورے سے خریداری، موبائل اور فیشن کا جنون، کیمپس کی چائے اور رات گئے تک پڑھائی",
    },
    "housewife_mother": {
        "age_range": (28, 50),
        "income": "middle",
        "regions": ["karachi", "lahore", "islamabad", "faisalabad", "peshawar"],
        "education": "high_school",
        "values": ["family", "faith_ایمان", "hospitality", "community"],
        "decision": "researcher",
        "channels": ["whatsapp", "facebook", "youtube", "television"],
        "spending": (10000, 35000),
        "narrative": "گھریلو خاتون اور ماں — گھر کی مکمل ذمہ دار، بچوں کی پرورش اور تعلیم پر توجہ، کچن کا سامان اور بچوں کی چیزیں پہلی ترجیح، پڑوسن اور رشتہ داروں کی تجاویز اہم، واٹس ایپ گروپس سے نئی چیزیں سیکھتی ہیں",
    },
    "trader_businessman": {
        "age_range": (30, 55),
        "income": "upper_middle",
        "regions": ["karachi", "lahore", "peshawar", "faisalabad"],
        "education": "high_school",
        "values": ["honor_عزت", "family", "faith_ایمان", "hospitality"],
        "decision": "researcher",
        "channels": ["facebook", "youtube", "whatsapp", "instagram"],
        "spending": (20000, 80000),
        "narrative": "تاجر/بزنس مین — مارکیٹ کا بادشاہ، نقد لین دین پر یقین، بڑی خریداری سے پہلے پوری تحقیق، کاروباری دوستوں کے ساتھ چائے پر فیصلے، فیملی کی عزت اور نام سب سے اوپر",
    },
    "overseas_worker": {
        "age_range": (25, 45),
        "income": "upper_middle",
        "regions": ["karachi", "lahore", "peshawar", "faisalabad"],
        "education": "high_school",
        "values": ["family", "faith_ایمان", "hospitality", "honor_عزت"],
        "decision": "brand_loyal",
        "channels": ["whatsapp", "imo", "facebook", "youtube"],
        "spending": (50000, 200000),
        "narrative": "بیرون ملک مقیم — خلیج یا یورپ میں محنت مزدوری، زیادہ تر کمائی گھر بھیجتے ہیں، چھٹیوں پر واپس آ کر بڑی شاپنگ، فیملی کے مستقبل کے لیے زمین اور جائیداد میں سرمایہ کاری",
    },
}

# Pakistani/Urdu name pools (for realistic name generation)
PERSONA_NAMES = {
    "male": [
        "محمد", "علی", "احمد", "عمران", "بلاول",
        "فیصل", "حمزہ", "عثمان", "حسن", "کاشف",
        "اسامہ", "عرفان", "نوید", "شہزاد", "کامران",
        "طاہر", "زاہد", "سلمان", "عدنان", "سعید",
    ],
    "female": [
        "فاطمہ", "عائشہ", "مریم", "زینب", "حفصہ",
        "عالیہ", "نادیہ", "سائرہ", "شازیہ", "رابعہ",
        "سدرہ", "نمرہ", "بشریٰ", "رامین", "ثناء",
        "حنا", "بینا", "کائنات", "اریج", "اریبہ",
    ],
    "surnames": [
        "خان", "ملک", "قریشی", "شیخ", "چوہدری",
        "سید", "راجہ", "بٹ", "اعوان", "کھوکھر",
        "رحمان", "احمد", "علی", "عباسی", "مغل",
        "میمن", "پٹھان", "گجر", "ڈار", "لون",
    ],
}

# Common Pakistani consumer phrases (for LLM persona grounding)
PAKISTANI_SHOPPING_PHRASES = [
    "کیا قیمت ہے؟", "بھائی تھوڑا کم کر دیں",
    "فائنل ریٹ بتائیں", "کوالٹی اچھی ہے نہ؟",
    "گارنٹی ہے؟", "اصلی ہے؟",
    "درزی سے سلوایا ہے", "بازار سے لیا ہے",
    "آن لائن آرڈر کیا تھا", "کیش آن ڈیلیوری کریں",
    "اللہ کا نام لے کر شروع کریں", "ماشاءاللہ بہت اچھا ہے",
    "پیسے بعد میں دے دوں گا", "دکاندار اپنا ہے",
    "گھر بیٹھے منگوا لو", "فیس بک پر دیکھا تھا",
    "چھوٹی سی ڈیل ہے", "ٹرانسپورٹ کا خرچہ تو دیکھو",
]

TRUST_FACTORS = [
    "دوست/رشتہ دار کی سفارش", "دکاندار پر اعتماد", "برانڈ کی شہرت",
    "معیار/کوالٹی", "قیمت مناسب ہونا", "اصلی/اوریجنل ہونا",
    "اچھی سروس/بعد از فروخت", "حلال سرٹیفیکیشن", "پہلے سے استعمال کر رہے ہیں",
    "سیل/ڈسکاؤنٹ", "مقامی پیداوار", "واٹس ایپ پر اچھے ریویو",
    "معروف شخصیت کی سفارش", "آسان قسطوں کا آپشن", "گارنٹی/وارنٹی",
]
