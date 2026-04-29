"""Bengali/Bangladesh Context — demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Bangladeshi consumer
insights, regional differences, and cultural values.
"""

COUNTRY_NAME = "Bangladesh"
CURRENCY = "BDT (Bangladeshi Taka)"

# Bangladesh population by region (2024 estimates, millions)
REGION_POPULATION = {
    "dhaka": 22.0,
    "chittagong": 9.0,
    "sylhet": 5.2,
    "khulna": 7.0,
    "rajshahi": 6.2,
    "barisal": 4.5,
}

# Regional cultural profiles
REGION_PROFILES = {
    "dhaka": {
        "traits": ["urban", "fast-paced", "ambitious", "traffic-weary"],
        "values_emphasis": ["family", "education", "resilience"],
        "media": ["facebook", "youtube", "tiktok", "instagram"],
        "income_bias": "middle",
        "occupations": ["garment worker", "banker", "IT professional", "businessman", "government officer"],
        "lifestyle_note": "ঢাকা — রিকশার শহর, যানজট আর স্বপ্নের নগরী। মানুষ সকাল থেকে রাত অবধি সংগ্রাম করে, রিকশায় অফিস যায়, ফুটপাথের চা-সিঙ্গারা জীবনযাত্রার অংশ",
    },
    "chittagong": {
        "traits": ["commercial", "hardworking", "practical", "port-city"],
        "values_emphasis": ["family", "community", "hospitality"],
        "media": ["facebook", "youtube", "tiktok", "imo"],
        "income_bias": "middle",
        "occupations": ["trader", "ship crew", "factory worker", "businessman", "fisherman"],
        "lifestyle_note": "চট্টগ্রাম — বাণিজ্যের প্রাণকেন্দ্র, পাহাড় আর সমুদ্রের মিলন, ব্যবসায়ী মানসিকতার মানুষ, বন্দর ও জাহাজ শিল্পের প্রভাব জীবনে স্পষ্ট",
    },
    "sylhet": {
        "traits": ["expat-connected", "traditional", "religious", "tea-garden"],
        "values_emphasis": ["family", "faith", "community", "hospitality"],
        "media": ["facebook", "youtube", "imo", "whatsapp"],
        "income_bias": "upper_middle",
        "occupations": ["expatriate worker", "tea garden manager", "businessman", "farmer", "restaurant owner"],
        "lifestyle_note": "সিলেট — প্রবাসীদের এলাকা, চা বাগানের সবুজ, আধ্যাত্মিকতার মাটি। লন্ডন আর আমেরিকার টাকায় চলে অনেক পরিবার, ঈদে বাড়ে কেনাকাটা",
    },
    "khulna": {
        "traits": ["industrial", "resilient", "river-dependent", "pragmatic"],
        "values_emphasis": ["resilience", "family", "community"],
        "media": ["facebook", "youtube", "tiktok", "television"],
        "income_bias": "lower_middle",
        "occupations": ["shrimp farmer", "factory worker", "fisherman", "small trader", "day laborer"],
        "lifestyle_note": "খুলনা — শিল্প আর মৎস্যের শহর, নদীর পাড়ে জীবন, চিংড়ি ঘের আর কলকারখানা, সাধারণ মানুষ সংগ্রামী ও মিতব্যয়ী",
    },
    "rajshahi": {
        "traits": ["educational", "agricultural", "clean", "peaceful"],
        "values_emphasis": ["education", "family", "community"],
        "media": ["facebook", "youtube", "television", "newspaper"],
        "income_bias": "lower_middle",
        "occupations": ["teacher", "farmer", "small businessman", "student", "government officer"],
        "lifestyle_note": "রাজশাহী — শিক্ষার শহর, আম আর রেশমের জন্য বিখ্যাত, পরিষ্কার রাস্তাঘাট, শান্ত ছাত্রজীবন, গ্রামীণ-শহুরে মিশ্র সংস্কৃতি",
    },
    "barisal": {
        "traits": ["agrarian", "riverine", "slow-paced", "traditional"],
        "values_emphasis": ["family", "hospitality", "community"],
        "media": ["facebook", "television", "youtube", "radio"],
        "income_bias": "low",
        "occupations": ["farmer", "fisherman", "small trader", "boatman", "day laborer"],
        "lifestyle_note": "বরিশাল — নদীর দেশ, ধানক্ষেত আর গুড়ের পিঠা, শান্ত স্রোতের জীবন, নৌকা আর লঞ্চ ছাড়া চলাচল অসম্ভব, আতিথেয়তা প্রকৃতির অংশ",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "garment_worker": {
        "age_range": (20, 35),
        "income": "lower_middle",
        "regions": ["dhaka", "chittagong"],
        "education": "high_school",
        "values": ["family", "resilience", "community"],
        "decision": "price_sensitive",
        "channels": ["facebook", "tiktok", "youtube"],
        "spending": (3000, 8000),
        "narrative": "গার্মেন্টস কর্মী — ভোর থেকে রাত অবধি কারখানায় পরিশ্রম, বেতনের সিংহভাগ পাঠান গ্রামে পরিবারের কাছে, কেনাকাটায় দরদাম জানেন, ফেসবুক আর টিকটকই প্রধান বিনোদন",
    },
    "university_student": {
        "age_range": (18, 25),
        "income": "low",
        "regions": ["dhaka", "rajshahi", "chittagong", "sylhet"],
        "education": "bachelors",
        "values": ["education", "community", "family"],
        "decision": "social_proof",
        "channels": ["facebook", "youtube", "tiktok", "instagram"],
        "spending": (1500, 5000),
        "narrative": "বিশ্ববিদ্যালয়ের শিক্ষার্থী — ক্যাম্পাসের আড্ডা আর চায়ের কাপ, বন্ধুদের পরামর্শে কেনাকাটা, বাজেট সীমিত কিন্তু স্টাইল সচেতন, অনলাইন শপিংয়ে আগ্রহ বাড়ছে",
    },
    "rural_farmer": {
        "age_range": (30, 60),
        "income": "low",
        "regions": ["barisal", "khulna", "rajshahi"],
        "education": "primary",
        "values": ["family", "resilience", "community", "faith"],
        "decision": "traditional",
        "channels": ["television", "radio", "facebook"],
        "spending": (1000, 5000),
        "narrative": "গ্রামের কৃষক — ধান-পাট-মাছের চাষ, ফসলের মৌসুমে হাতে টাকা আসে, পরিবার বড়, কেনাকাটা হয় হাট-বাজারে, বিজ্ঞাপনের চেয়ে পড়শির পরামর্শে বিশ্বাসী",
    },
    "urban_professional": {
        "age_range": (25, 45),
        "income": "upper_middle",
        "regions": ["dhaka", "chittagong"],
        "education": "masters",
        "values": ["education", "family", "resilience"],
        "decision": "researcher",
        "channels": ["linkedin", "facebook", "youtube", "instagram"],
        "spending": (10000, 30000),
        "narrative": "শহুরে পেশাজীবী — প্রাইভেট কোম্পানি বা ব্যাংকে চাকরি, নিজের ফ্ল্যাট আর গাড়ির স্বপ্ন, অনলাইন রিভিউ পড়ে কেনাকাটা করেন, দামের চেয়ে মান গুরুত্বপূর্ণ",
    },
    "small_trader": {
        "age_range": (30, 55),
        "income": "middle",
        "regions": ["dhaka", "chittagong", "sylhet", "khulna"],
        "education": "high_school",
        "values": ["family", "community", "hospitality", "resilience"],
        "decision": "researcher",
        "channels": ["facebook", "youtube", "imo"],
        "spending": (5000, 15000),
        "narrative": "ছোট ব্যবসায়ী — দোকান বা ট্রেডিং করে সংসার চালান, নগদ টাকার লেনদেনে অভ্যস্ত, কিস্তিতে কেনাকাটা পছন্দ করেন, ব্যবসায়িক বন্ধুদের পরামর্শ গ্রহণ করেন",
    },
    "expat_worker": {
        "age_range": (28, 50),
        "income": "upper_middle",
        "regions": ["sylhet", "chittagong", "dhaka"],
        "education": "high_school",
        "values": ["family", "faith", "community", "hospitality"],
        "decision": "brand_loyal",
        "channels": ["imo", "whatsapp", "facebook", "youtube"],
        "spending": (20000, 80000),
        "narrative": "প্রবাসী কর্মী — মধ্যপ্রাচ্য বা ইউরোপ থেকে টাকা পাঠান, পরিবারের ভবিষ্যতের জন্য বিনিয়োগ করেন, দেশে ফিরলে বড় কেনাকাটা করেন, গ্রামে বাড়ি-জমিতে অর্থ ঢালেন",
    },
}

# Bengali name pools (for realistic name generation)
PERSONA_NAMES = {
    "male": [
        "মোহাম্মদ", "আব্দুল", "রফিকুল", "সোহেল", "করিম",
        "সজল", "আলমগীর", "তানভীর", "ফারহান", "শাহীন",
        "রাশেদুল", "মাসুদ", "রুবেল", "নয়ন", "জসিম",
        "কামরুল", "সাগর", "সুমন", "জাহাঙ্গীর", "মামুন",
    ],
    "female": [
        "ফাতেমা", "আয়শা", "নাসরিন", "শিরিন", "রোকেয়া",
        "সাবিনা", "নাজমা", "রোজিনা", "তাসলিমা", "রেহানা",
        "শারমিন", "ফারহানা", "নওশিন", "মালিহা", "তানিয়া",
        "সামিয়া", "নীলা", "জেসমিন", "সিমু", "আঞ্জুমান",
    ],
    "surnames": [
        "হাসান", "উদ্দিন", "ইসলাম", "হক", "রহমান",
        "আহমেদ", "খান", "মিয়া", "সরকার", "বিশ্বাস",
        "তালুকদার", "মোল্লা", "গাজী", "শেখ", "হোসেন",
    ],
}

# Common Bengali consumer phrases (for LLM persona grounding)
BENGALI_SHOPPING_PHRASES = [
    "দাম কতো?", "কম দামে দেবেন?", "স্যার একটু ছাড় দিন",
    "ক্যাশে কিনলে কতো?", "মান ভালো তো?", "আসল নাকি নকল?",
    "গ্যারান্টি আছে?", "দেখে কিনবো", "অনলাইনে অর্ডার করেছি",
    "বাজারে গিয়ে কিনবো", "শো-রুম থেকে কিনেছি", "বন্ধু বলেছে ভালো",
    "ফেসবুকে দেখেছি", "পার্শ্ববর্তী দোকানে সস্তা", "বড় দোকান থেকে কেনাই ভালো",
    "নগদে কিনলে ডিসকাউন্ট?", "হোম ডেলিভারি হয়?", "পুরোনোটা আর ভালো না",
]

TRUST_FACTORS = [
    "দোকানের সুনাম", "বন্ধু-পরিবারের সুপারিশ", "পণ্যটি আগে ব্যবহার করেছি",
    "দাম সাশ্রয়ী", "মান ভালো", "বড় ব্র্যান্ড",
    "ওয়ারেন্টি/গ্যারান্টি", "ফেসবুকে ভালো রেটিং", "পরিচিত বিক্রেতা",
    "মোড়কে উৎপাদনের তারিখ", "ভালো কাস্টমার সার্ভিস", "স্থানীয় পণ্য",
    "হালাল সার্টিফিকেট", "ফ্রি ডেলিভারি", "অভিজ্ঞতা থেকে বিশ্বাস",
]
