"""English Context — US/UK/Global demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Western
consumer insights, regional differences, and cultural values.
"""

# US + UK population by region (2024 estimates, millions)
REGION_POPULATION = {
    "northeast": 57.2,
    "south": 131.4,
    "midwest": 69.2,
    "west": 78.8,
    "uk_london": 8.9,
    "uk_north": 15.5,
}

# Regional cultural profiles
REGION_PROFILES = {
    "northeast": {
        "traits": ["educated", "direct", "fast-paced", "liberal"],
        "values_emphasis": ["individualism", "achievement"],
        "media": ["instagram", "twitter_x", "youtube", "linkedin"],
        "income_bias": "upper_middle",
        "occupations": ["finance professional", "academic", "healthcare worker", "tech worker", "lawyer"],
        "lifestyle_note": "Fast-paced urban corridor, Boston-to-DC. Highly educated, career-focused. Commuter culture, premium coffee, brunch on weekends.",
    },
    "south": {
        "traits": ["hospitable", "religious", "traditional", "community-oriented"],
        "values_emphasis": ["freedom", "family", "faith"],
        "media": ["facebook", "youtube", "tiktok", "tv"],
        "income_bias": "middle",
        "occupations": ["healthcare worker", "teacher", "truck driver", "retail worker", "manufacturing"],
        "lifestyle_note": "Church on Sunday, college football on Saturday. Strong family ties, barbecue culture, lower cost of living, car-dependent.",
    },
    "midwest": {
        "traits": ["hardworking", "pragmatic", "friendly", "modest"],
        "values_emphasis": ["family", "community", "fairness"],
        "media": ["facebook", "youtube", "tv", "radio"],
        "income_bias": "middle",
        "occupations": ["manufacturing worker", "farmer", "nurse", "teacher", "truck driver"],
        "lifestyle_note": "Blue-collar work ethic, DIY culture. State fairs, high school sports, potluck dinners. Skeptical of coastal elites.",
    },
    "west": {
        "traits": ["innovative", "outdoorsy", "individualistic", "health-conscious"],
        "values_emphasis": ["freedom", "self_expression", "innovation"],
        "media": ["instagram", "tiktok", "youtube", "twitter_x"],
        "income_bias": "upper_middle",
        "occupations": ["software engineer", "creative professional", "entrepreneur", "service worker", "healthcare worker"],
        "lifestyle_note": "Tech-driven, wellness-obsessed. Hiking, yoga, cold brew, electric vehicles. Startup culture meets outdoors lifestyle.",
    },
    "uk_london": {
        "traits": ["cosmopolitan", "reserved", "multicultural", "fast-paced"],
        "values_emphasis": ["equality", "individualism", "fairness"],
        "media": ["instagram", "twitter_x", "whatsapp", "youtube"],
        "income_bias": "upper_middle",
        "occupations": ["finance professional", "creative", "tech worker", "civil servant", "hospitality worker"],
        "lifestyle_note": "Pub after work, Pret for lunch, Tube commute. Diverse, expensive, status-aware but understated. Rental crisis shapes spending.",
    },
    "uk_north": {
        "traits": ["down-to-earth", "community-oriented", "pragmatic", "humorous"],
        "values_emphasis": ["community", "family", "fairness"],
        "media": ["facebook", "youtube", "tv", "whatsapp"],
        "income_bias": "lower_middle",
        "occupations": ["manufacturing worker", "NHS worker", "retail worker", "teacher", "tradesperson"],
        "lifestyle_note": "Pub culture, football-mad, Greggs for breakfast. Strong local identity, lower cost of living, skeptical of London-centric everything.",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "suburban_mom": {
        "age_range": (30, 50),
        "income": "upper_middle",
        "regions": ["south", "midwest", "west"],
        "education": "bachelors",
        "values": ["family", "achievement", "safety"],
        "decision": "researcher",
        "channels": ["facebook", "instagram", "youtube"],
        "spending": (500, 2000),
        "narrative": "Suburban mom managing household of 3-5. Researches everything on Amazon reviews and mom Facebook groups. Drives an SUV, shops at Target and Costco. Values convenience and safety above price.",
    },
    "silicon_valley_techie": {
        "age_range": (25, 40),
        "income": "high",
        "regions": ["west"],
        "education": "masters",
        "values": ["innovation", "efficiency", "self_improvement"],
        "decision": "early_adopter",
        "channels": ["twitter_x", "youtube", "reddit", "discord"],
        "spending": (2000, 8000),
        "narrative": "FAANG engineer or startup dev in SF Bay Area. Buys latest gadgets on launch day. Subscribes to everything. Optimizes life with apps. Reads Hacker News, listens to tech podcasts. RSUs fund the lifestyle.",
    },
    "midwest_worker": {
        "age_range": (25, 55),
        "income": "lower_middle",
        "regions": ["midwest"],
        "education": "high_school",
        "values": ["family", "fairness", "freedom"],
        "decision": "price_sensitive",
        "channels": ["facebook", "tv", "youtube"],
        "spending": (200, 800),
        "narrative": "Factory or trades worker in Ohio/Michigan/Indiana. Loyal to American brands. Shops at Walmart. Watches football and listens to country radio. Budget-conscious, skeptical of trends, values durability.",
    },
    "gen_z_creator": {
        "age_range": (18, 26),
        "income": "low",
        "regions": ["west", "northeast", "uk_london"],
        "education": "bachelors",
        "values": ["self_expression", "freedom", "individualism"],
        "decision": "impulsive",
        "channels": ["tiktok", "instagram", "discord", "twitch"],
        "spending": (100, 1000),
        "narrative": "College student or recent grad, aspiring content creator. Lives on TikTok trends and Spotify playlists. Buys from DTC brands, thrifts for vintage. Values authenticity, hates traditional advertising.",
    },
    "wall_street_professional": {
        "age_range": (28, 45),
        "income": "high",
        "regions": ["northeast"],
        "education": "masters",
        "values": ["achievement", "status", "freedom"],
        "decision": "researcher",
        "channels": ["linkedin", "twitter_x", "bloomberg"],
        "spending": (3000, 10000),
        "narrative": "Finance professional in NYC. Status-driven spending: luxury watches, premium gym, Michelin restaurants. Time-poor, money-rich. Reads financial news constantly. Network is everything.",
    },
    "retiree_florida": {
        "age_range": (60, 80),
        "income": "middle",
        "regions": ["south"],
        "education": "bachelors",
        "values": ["freedom", "family", "tradition"],
        "decision": "traditional",
        "channels": ["tv", "facebook", "email"],
        "spending": (500, 3000),
        "narrative": "Retired couple in Florida or Arizona. Fixed income but comfortable. Loyal to brands they've used for decades. Watches cable news, uses Facebook to see grandkids. Values reliability and customer service.",
    },
}

# English name pools (US + UK)
PERSONA_NAMES = {
    "male": ["James", "Michael", "David", "Robert", "William", "Christopher", "Daniel", "Matthew",
             "Andrew", "Thomas", "Oliver", "Harry", "George", "Jack", "Benjamin", "Alexander",
             "Ethan", "Noah", "Liam", "Mason"],
    "female": ["Emma", "Olivia", "Sophia", "Isabella", "Charlotte", "Amelia", "Emily", "Sarah",
               "Jessica", "Ashley", "Elizabeth", "Margaret", "Grace", "Hannah", "Chloe",
               "Mia", "Abigail", "Ella", "Ava", "Lily"],
    "nickname_male": ["Jim", "Mike", "Dave", "Rob", "Will", "Chris", "Dan", "Matt", "Andy",
                      "Tom", "Ben", "Alex", "Jake", "Nick", "Josh", "Ed", "Sam", "Pete", "Pat", "Joe"],
    "nickname_female": ["Emma", "Liv", "Soph", "Bella", "Lottie", "Amy", "Em", "Sarah", "Jess",
                        "Ash", "Liz", "Maggie", "Gracie", "Hannah", "Katie", "Jen", "Mia", "Abby", "Ellie", "Megan"],
    "surnames": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
                 "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin",
                 "Thompson", "White", "Harris", "Clark", "Lewis", "Walker", "Young", "King", "Wright", "Hill"],
}

# Common English consumer phrases
SHOPPING_PHRASES = [
    "Limited time offer", "Best price guaranteed", "Free shipping",
    "Read the reviews first", "Is this worth it?", "Add to cart",
    "Subscribe and save", "Try before you buy", "Money-back guarantee",
    "Black Friday deal", "Prime delivery", "Buy now, pay later",
    "Customer favourite", "I saw it on TikTok", "Going viral right now",
    "Honest review", "Worth the hype?", "Dupe alert",
]

TRUST_FACTORS = [
    "Verified purchase reviews", "Recommended by friends/family", "Recognised brand name",
    "Money-back guarantee", "Independent lab tested", "Already use this brand / repeat buyer",
    "Featured in reputable media", "Influencer / expert endorsement", "Award-winning",
    "Transparent about ingredients / sourcing", "Excellent customer support", "Social proof (high sales volume)",
    "Amazon's Choice / Best Seller badge", "Free returns policy", "Ethical / sustainable practices",
]

COUNTRY_NAME = "United States / United Kingdom / Global English"
CURRENCY = "USD"
