"""Spanish Context — Spain + Latin America demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Spanish-speaking
consumer insights, regional differences, and cultural values.
"""

# Spain + LATAM city population (2024 estimates, millions)
REGION_POPULATION = {
    "madrid": 6.8,
    "barcelona": 5.7,
    "mexico_city": 22.5,
    "buenos_aires": 15.4,
    "bogota": 11.5,
    "lima": 11.3,
}

# Regional cultural profiles
REGION_PROFILES = {
    "madrid": {
        "traits": ["cosmopolitan", "social", "nightlife-loving", "professional"],
        "values_emphasis": ["family", "social_life", "tradition"],
        "media": ["instagram", "tiktok", "whatsapp", "youtube"],
        "income_bias": "upper_middle",
        "occupations": ["funcionario", "empresario", "tecnólogo", "financiero", "hostelero"],
        "lifestyle_note": "Madrid nunca duerme. Cañas after work, terrazas until late. Directos y sociables. Funcionario culture is real. Weekend escapes to Sierra. Obsessed with football and tapas.",
    },
    "barcelona": {
        "traits": ["cosmopolitan", "creative", "progressive", "multilingual"],
        "values_emphasis": ["community", "self_expression", "innovation"],
        "media": ["instagram", "twitter_x", "tiktok", "whatsapp"],
        "income_bias": "upper_middle",
        "occupations": ["diseñador", "desarrollador tech", "emprendedor", "académico", "hostelero"],
        "lifestyle_note": "Mediterranean innovation hub. Design + tech ecosystem. Catalan pride. Beach-meets-city lifestyle. Vermut culture. Tourist economy tension. Startup scene growing fast.",
    },
    "mexico_city": {
        "traits": ["resilient", "warm", "family-oriented", "hardworking"],
        "values_emphasis": ["family", "community", "tradition"],
        "media": ["facebook", "whatsapp", "tiktok", "youtube"],
        "income_bias": "middle",
        "occupations": ["oficinista", "comerciante", "chofer", "ingeniero", "maestro"],
        "lifestyle_note": "Chilango life: tacos everywhere, endless traffic, family Sundays. Strong informal economy. Tianguis culture coexists with Walmart. La Virgen de Guadalupe devotion. Fiestas are everything.",
    },
    "buenos_aires": {
        "traits": ["passionate", "nostalgic", "cultured", "resilient"],
        "values_emphasis": ["family", "passion", "culture"],
        "media": ["instagram", "whatsapp", "youtube", "twitter_x"],
        "income_bias": "middle",
        "occupations": ["psicólogo", "profesor", "comerciante", "artista", "oficinista"],
        "lifestyle_note": "Porteño psychoanalysis culture. Mate rituals. Late dinners (10 PM+). Inflation shapes every purchase decision. Bookstores and cafés everywhere. Tango nostalgia meets crypto realism.",
    },
    "bogota": {
        "traits": ["formal", "entrepreneurial", "aspirational", "class-conscious"],
        "values_emphasis": ["family", "status", "education"],
        "media": ["whatsapp", "facebook", "instagram", "tiktok"],
        "income_bias": "upper_middle",
        "occupations": ["empresario", "ingeniero", "consultor", "comerciante", "funcionario"],
        "lifestyle_note": "Rolo formality: 'usted' culture. Estrato shapes everything. Ajiaco Sundays, ciclovía. Tech and startup growing. Safety concerns drive digital-first behaviors. Family is the anchor.",
    },
    "lima": {
        "traits": ["entrepreneurial", "food-obsessed", "informal", "optimistic"],
        "values_emphasis": ["family", "achievement", "gastronomy"],
        "media": ["facebook", "whatsapp", "tiktok", "youtube"],
        "income_bias": "lower_middle",
        "occupations": ["emprendedor", "comerciante", "chef", "ingeniero", "transportista"],
        "lifestyle_note": "Gastronomic capital of LATAM. Ceviche pride. Informal economy dominates. Emprendedor spirit everywhere — everyone has a side business. District loyalty (Miraflores vs Surco vs Cono Norte).",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "urban_professional": {
        "age_range": (28, 42),
        "income": "upper_middle",
        "regions": ["madrid", "barcelona", "mexico_city"],
        "education": "masters",
        "values": ["achievement", "family", "social_life"],
        "decision": "social_proof",
        "channels": ["instagram", "linkedin", "whatsapp", "youtube"],
        "spending": (500, 3000),
        "narrative": "Professional in banking, consulting, or tech. Works hard, plays harder. Friday after-work cañas are sacred. Invests in experiences — travel, dining, festivals. Brand-conscious but value-aware.",
    },
    "latino_mom": {
        "age_range": (32, 52),
        "income": "middle",
        "regions": ["mexico_city", "bogota", "lima"],
        "education": "bachelors",
        "values": ["family", "tradition", "security"],
        "decision": "researcher",
        "channels": ["facebook", "whatsapp", "youtube"],
        "spending": (200, 1000),
        "narrative": "El corazón de la familia latina. Manages household budget like a CFO. WhatsApp group queen — shares recipes, school info, promos. Loyal to brands that understand family needs. Buys in bulk at wholesale clubs.",
    },
    "university_student": {
        "age_range": (18, 25),
        "income": "low",
        "regions": ["barcelona", "buenos_aires", "madrid"],
        "education": "bachelors",
        "values": ["self_expression", "freedom", "community"],
        "decision": "impulsive",
        "channels": ["tiktok", "instagram", "whatsapp"],
        "spending": (50, 400),
        "narrative": "Universitario living on budget but highly social. Shares piso with friends. Spends on nightlife, cheap travel, and fashion. Fast fashion (Zara, Shein) dominates wardrobe. Influenced by TikTok trends and peer group.",
    },
    "small_business_owner": {
        "age_range": (35, 55),
        "income": "middle",
        "regions": ["mexico_city", "lima", "bogota"],
        "education": "high_school",
        "values": ["family", "achievement", "community"],
        "decision": "pragmatic",
        "channels": ["facebook", "whatsapp", "youtube"],
        "spending": (300, 1500),
        "narrative": "Dueño de tienda de abarrotes, restaurante familiar o taller. Cash-flow focused. Uses WhatsApp Business for customer orders. Learns from YouTube tutorials. Family helps run the business. Cautious spender, invests in inventory first.",
    },
    "digital_creator": {
        "age_range": (22, 35),
        "income": "upper_middle",
        "regions": ["barcelona", "madrid", "buenos_aires"],
        "education": "bachelors",
        "values": ["self_expression", "freedom", "innovation"],
        "decision": "early_adopter",
        "channels": ["tiktok", "instagram", "youtube", "twitter_x"],
        "spending": (300, 2000),
        "narrative": "Content creator, freelance designer, or indie developer. Works from cafés and co-working spaces. Earns in multiple currencies (USD/EUR). Spends on aesthetics, tech gear, and travel. Values authenticity over brand prestige.",
    },
    "retired_couple": {
        "age_range": (60, 80),
        "income": "lower_middle",
        "regions": ["madrid", "mexico_city", "buenos_aires"],
        "education": "high_school",
        "values": ["family", "tradition", "health"],
        "decision": "traditional",
        "channels": ["tv", "facebook", "radio"],
        "spending": (200, 800),
        "narrative": "Jubilados con pensión fija. Sobremesa tradition — long meals with extended family. Spends on grandchildren, health, and home. TV news shapes worldview. Trusts lifelong brands. Banco físico over digital banking.",
    },
}

# Spanish name pools (Spain + LATAM)
PERSONA_NAMES = {
    "male": ["Alejandro", "Carlos", "Javier", "Miguel", "Diego", "Santiago", "Andrés", "Fernando",
             "Juan", "Luis", "Pablo", "Ricardo", "Eduardo", "Antonio", "José", "Manuel",
             "Francisco", "Rafael", "Alberto", "Gabriel"],
    "female": ["María", "Carmen", "Ana", "Isabel", "Laura", "Sofía", "Valentina", "Camila",
               "Lucía", "Paula", "Daniela", "Elena", "Marta", "Patricia", "Gabriela",
               "Adriana", "Rosa", "Claudia", "Carolina", "Victoria"],
    "nickname_male": ["Álex", "Carlitos", "Javi", "Miguelito", "Dieguito", "Santi", "Andrés", "Fer",
                      "Juancho", "Lucho", "Pablito", "Rick", "Lalo", "Toño", "Pepe", "Manu",
                      "Paco", "Rafa", "Beto", "Gabo"],
    "nickname_female": ["Maru", "Carmencita", "Anita", "Isa", "Lau", "Sofi", "Vale", "Cami",
                        "Luci", "Pau", "Dani", "Elenita", "Martita", "Paty", "Gaby",
                        "Adri", "Rosita", "Clau", "Caro", "Vicky"],
    "surnames": ["García", "Rodríguez", "Martínez", "Hernández", "López", "González", "Pérez",
                 "Sánchez", "Ramírez", "Díaz", "Torres", "Flores", "Morales", "Ruiz",
                 "Fernández", "Jiménez", "Moreno", "Álvarez", "Romero", "Navarro"],
}

# Common Spanish consumer phrases
SHOPPING_PHRASES = [
    "¿Tiene descuento?", "Aprovecha la oferta", "Vale la pena",
    "Está carísimo", "Qué ganga", "Precio amigo",
    "Envío gratis", "Pago en cuotas", "Devolución sin costo",
    "Lo vi en TikTok", "Recomendado por una amiga", "Calidad-precio",
    "Producto estrella", "Oferta relámpago", "Black Friday",
    "El Buen Fin", "Hot Sale", "Compra antes que se agote",
    "Garantía de por vida", "Hecho a mano",
]

TRUST_FACTORS = [
    "Recomendado por familia/amigos", "Marca reconocida de toda la vida",
    "Reseñas de compradores verificados", "Producto local/hecho aquí",
    "Garantía de devolución", "Lo usé antes y funciona",
    "Influencer de confianza lo recomienda", "Atención al cliente excelente",
    "Ofrece pago en cuotas / MSI", "Tiene tienda física",
    "Premios y certificaciones", "Mucha gente lo compra",
    "Apareció en TV/noticias", "Política de devolución clara",
    "Prácticas éticas/sostenibles",
]

COUNTRY_NAME = "España / Latinoamérica"
CURRENCY = "EUR"
