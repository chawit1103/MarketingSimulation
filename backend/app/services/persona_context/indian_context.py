"""Indian Context — India demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Indian
consumer insights, regional differences, and cultural values.
"""

# Indian metro region population (2024 estimates, millions)
REGION_POPULATION = {
    "mumbai": 21.7,
    "delhi": 33.8,
    "bangalore": 13.6,
    "kolkata": 15.3,
    "chennai": 12.4,
    "hyderabad": 11.2,
}

# Regional cultural profiles
REGION_PROFILES = {
    "mumbai": {
        "traits": ["fast-paced", "ambitious", "entrepreneurial", "cosmopolitan"],
        "values_emphasis": ["family", "achievement", "pragmatism"],
        "media": ["instagram", "youtube", "whatsapp", "jio"],
        "income_bias": "upper_middle",
        "occupations": ["finance professional", "bollywood worker", "business owner", "IT professional", "trader"],
        "lifestyle_note": "Maximum City — always on, always hustling. Local train commutes, vada pav culture. Bollywood dreams meet corporate grind. Status matters but practicality wins.",
    },
    "delhi": {
        "traits": ["status-conscious", "loud", "family-oriented", "political"],
        "values_emphasis": ["family", "tradition", "face"],
        "media": ["whatsapp", "instagram", "youtube", "facebook"],
        "income_bias": "upper_middle",
        "occupations": ["government officer", "business owner", "lawyer", "doctor", "trader"],
        "lifestyle_note": "Dilli-style: show-off culture, big weddings, bigger cars. Joint families still common. Winter weddings, CP hangouts, chole bhature cravings. 'Jugaad' is a way of life.",
    },
    "bangalore": {
        "traits": ["tech-savvy", "liberal", "cosmopolitan", "health-conscious"],
        "values_emphasis": ["innovation", "education", "individualism"],
        "media": ["instagram", "twitter_x", "youtube", "linkedin"],
        "income_bias": "upper_middle",
        "occupations": ["software engineer", "startup founder", "product manager", "data scientist", "designer"],
        "lifestyle_note": "Silicon Valley of India. Craft beer, startup meetups, Cubbon Park runs. Traffic frustration is real. Dating apps, flat-sharing, weekend getaways to Coorg.",
    },
    "kolkata": {
        "traits": ["intellectual", "cultural", "laid-back", "value-conscious"],
        "values_emphasis": ["culture", "education", "community"],
        "media": ["facebook", "whatsapp", "youtube", "tv"],
        "income_bias": "middle",
        "occupations": ["teacher", "government officer", "small business owner", "artist", "trader"],
        "lifestyle_note": "City of Joy — adda culture, Rosogolla, Durga Puja. Old-world charm with modern struggles. Price-sensitive market, strong local brand loyalty. Football over cricket.",
    },
    "chennai": {
        "traits": ["conservative", "disciplined", "education-focused", "traditional"],
        "values_emphasis": ["family", "tradition", "education"],
        "media": ["whatsapp", "youtube", "facebook", "tv"],
        "income_bias": "middle",
        "occupations": ["engineer", "doctor", "IT professional", "manufacturing worker", "teacher"],
        "lifestyle_note": "Deeply traditional yet rapidly modernising. Filter coffee, Carnatic music, Marina Beach. High engineering enrollment. Loyal to regional brands. Conservative spending habits.",
    },
    "hyderabad": {
        "traits": ["entrepreneurial", "food-loving", "blended-culture", "growing-fast"],
        "values_emphasis": ["family", "education", "hospitality"],
        "media": ["whatsapp", "instagram", "youtube", "jio"],
        "income_bias": "upper_middle",
        "occupations": ["IT professional", "pharma worker", "business owner", "engineer", "real estate"],
        "lifestyle_note": "Cyber city meets Nizami heritage. Biryani capital. IT corridor boom. Emerging startup scene. Pearl markets, old city charm, modern malls coexisting.",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "tech_professional": {
        "age_range": (24, 38),
        "income": "upper_middle",
        "regions": ["bangalore", "hyderabad", "mumbai"],
        "education": "bachelors",
        "values": ["achievement", "innovation", "family"],
        "decision": "researcher",
        "channels": ["youtube", "instagram", "twitter_x", "linkedin"],
        "spending": (15000, 60000),
        "narrative": "Software engineer at FAANG/startup earning in INR but thinking in global trends. Researches every purchase on YouTube and Reddit. Invests in gadgets, mutual funds, and international travel. Pays parents' bills.",
    },
    "small_town_aspirant": {
        "age_range": (20, 32),
        "income": "lower_middle",
        "regions": ["delhi", "kolkata", "chennai"],
        "education": "bachelors",
        "values": ["family", "face", "education"],
        "decision": "social_proof",
        "channels": ["youtube", "whatsapp", "instagram", "tiktok"],
        "spending": (3000, 15000),
        "narrative": "Tier-2/3 city youth. First-generation English speaker, college degree holder. Dreams of metro city life. Buys smartphone on EMI. Follows influencers for aspiration. WhatsApp forwards shape opinions.",
    },
    "rural_farmer": {
        "age_range": (35, 60),
        "income": "low",
        "regions": ["delhi", "kolkata", "chennai"],
        "education": "high_school",
        "values": ["family", "tradition", "community"],
        "decision": "traditional",
        "channels": ["tv", "radio", "whatsapp", "facebook"],
        "spending": (1000, 5000),
        "narrative": "Smallholder farmer in rural belt. Cash economy, seasonal income cycles. Buys from local kirana store on credit. Children are primary digital gateway. Trusts local retailer advice over ads.",
    },
    "urban_mom": {
        "age_range": (30, 48),
        "income": "middle",
        "regions": ["mumbai", "delhi", "chennai"],
        "education": "bachelors",
        "values": ["family", "tradition", "education"],
        "decision": "researcher",
        "channels": ["whatsapp", "youtube", "facebook", "instagram"],
        "spending": (5000, 25000),
        "narrative": "Metro mom juggling career and family. WhatsApp groups are her Google. Researches schools obsessively. Buys groceries from BigBasket/JioMart. Gold jewellery as investment. Kitchen gadget collector.",
    },
    "college_student": {
        "age_range": (18, 23),
        "income": "low",
        "regions": ["bangalore", "delhi", "mumbai", "hyderabad"],
        "education": "bachelors",
        "values": ["self_expression", "friendship", "freedom"],
        "decision": "impulsive",
        "channels": ["instagram", "youtube", "snapchat", "discord"],
        "spending": (1000, 5000),
        "narrative": "Engineering or commerce student. Gets monthly allowance from parents. Spends on chai-sutta, OTT subscriptions, and mobile data. Buys fast fashion from Myntra/AJIO. Influenced by college seniors and memes.",
    },
    "business_owner": {
        "age_range": (35, 55),
        "income": "high",
        "regions": ["mumbai", "delhi", "hyderabad"],
        "education": "bachelors",
        "values": ["family", "face", "achievement"],
        "decision": "researcher",
        "channels": ["whatsapp", "youtube", "linkedin", "newspaper"],
        "spending": (20000, 100000),
        "narrative": "SME owner — textiles, trading, or manufacturing. Family business legacy. Spends on real estate, gold, and children's foreign education. Uses WhatsApp for business. Drives Fortuner or Creta.",
    },
}

# Indian name pools (broad pan-Indian representation)
PERSONA_NAMES = {
    "male": ["Aarav", "Arjun", "Rohan", "Rahul", "Vikram", "Amit", "Raj", "Suresh",
             "Karthik", "Nikhil", "Manish", "Aditya", "Pranav", "Deepak", "Sanjay",
             "Varun", "Abhishek", "Harsh", "Gaurav", "Vivek"],
    "female": ["Priya", "Ananya", "Neha", "Shruti", "Pooja", "Divya", "Kavita", "Riya",
               "Deepika", "Aishwarya", "Lakshmi", "Meera", "Anjali", "Sneha", "Nandini",
               "Isha", "Tanya", "Swati", "Rashmi", "Bhavna"],
    "nickname_male": ["Raju", "Sonu", "Bunty", "Chintu", "Monty", "Golu", "Vicky",
                      "Pappu", "Rinku", "Karan", "Avi", "Manoj", "Ricky", "Sunny", "Tony"],
    "nickname_female": ["Guddi", "Chutki", "Babli", "Pinky", "Sweety", "Dimple",
                        "Simran", "Kajal", "Ritu", "Sonu", "Nikki", "Mona", "Tina", "Bindu", "Gauri"],
    "surnames": ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Reddy", "Nair",
                 "Verma", "Joshi", "Desai", "Mehta", "Chopra", "Das", "Mishra",
                 "Iyer", "Rao", "Pillai", "Choudhury", "Banerjee", "Yadav"],
}

# Common Indian consumer phrases
SHOPPING_PHRASES = [
    "Achha hai kya?", "Paisa vasool", "Best price dedo",
    "Discount kitna milega?", "Ek free chahiye", "COD available?",
    "Return policy kya hai?", "Ye original hai na?",
    "Dusre customer ne kya kaha?", "Rating kitni hai?",
    "Badiya hai", "Zabardast", "Kya offer chal raha hai?",
    "Flipkart se sasta milega", "Amazon Prime member hoon",
    "Festival sale mein lena", "Diwali pe khareedenge",
]

TRUST_FACTORS = [
    "परिवार/दोस्तों की सिफारिश", "ब्रांड का नाम जाना-पहचाना है",
    "ग्राहकों की समीक्षाएं और रेटिंग", "पहले इस्तेमाल किया है",
    "कीमत सही लगी (पैसा वसूल)", "सिलेब्रिटी एंडोर्समेंट",
    "वारंटी/गारंटी है", "स्थानीय दुकान पर उपलब्ध है",
    "त्योहार की सेल/OFFER", "COD उपलब्ध है", "रिटर्न पॉलिसी अच्छी है",
    "दूसरे बहुत खरीद रहे हैं", "अखबार/TV पर देखा है",
]

COUNTRY_NAME = "India / भारत"
CURRENCY = "INR"
