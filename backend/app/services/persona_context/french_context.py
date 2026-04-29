"""French Context — France demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real French
consumer insights, regional differences, and cultural values.
"""

# French city/metro population (2024 estimates, millions)
REGION_POPULATION = {
    "paris": 12.4,
    "lyon": 2.4,
    "marseille": 1.9,
    "bordeaux": 1.4,
    "lille": 1.2,
    "toulouse": 1.5,
}

# Regional cultural profiles
REGION_PROFILES = {
    "paris": {
        "traits": ["cosmopolitan", "fast-paced", "intellectual", "stylish"],
        "values_emphasis": ["culture", "laïcité", "égalité"],
        "media": ["instagram", "twitter_x", "youtube", "lemonde"],
        "income_bias": "upper_middle",
        "occupations": ["cadre", "consultant", "fonctionnaire", "artiste", "chercheur"],
        "lifestyle_note": "Métro-boulot-dodo. Paris intramuros life: tiny apartments, café terrasses, boulangerie daily ritual. Cultural capital — expos, cinéma, théâtre. Grumbling is a national sport. Networking drinks after work.",
    },
    "lyon": {
        "traits": ["balanced", "gastronomic", "entrepreneurial", "pragmatic"],
        "values_emphasis": ["gastronomie", "qualité_de_vie", "tradition"],
        "media": ["instagram", "facebook", "youtube", "lefigaro"],
        "income_bias": "upper_middle",
        "occupations": ["entrepreneur", "chercheur pharma", "ingénieur", "fonctionnaire", "commerçant"],
        "lifestyle_note": "Capitale de la gastronomie. Bouchons lyonnais. Équilibre travail-vie personnelle. Hub pharmaceutique et biotech. Proche des Alpes pour le ski. Bourgeois discret — qualité sans ostentation.",
    },
    "marseille": {
        "traits": ["passionate", "multicultural", "direct", "resilient"],
        "values_emphasis": ["community", "family", "passion"],
        "media": ["facebook", "instagram", "youtube", "tiktok"],
        "income_bias": "lower_middle",
        "occupations": ["commerçant", "artisan", "transporteur", "travailleur portuaire", "restaurateur"],
        "lifestyle_note": "Marseille la rebelle. Pastis et pétanque. Méditerranée cosmopolite. Forte identité locale. OM football passion. Forte solidarité de quartier. Économie informelle significative. Accent chantant.",
    },
    "bordeaux": {
        "traits": ["refined", "wine-loving", "balanced", "quality-conscious"],
        "values_emphasis": ["qualité_de_vie", "gastronomie", "culture"],
        "media": ["instagram", "facebook", "youtube", "sudouest"],
        "income_bias": "upper_middle",
        "occupations": ["vigneron", "cadre", "architecte", "commerçant", "chercheur"],
        "lifestyle_note": "Art de vivre à la bordelaise. Vin comme religion. Architecture du XVIIIe classée UNESCO. TGV à 2h de Paris attire les néo-Bordelais. Marchés bio, vélo, vie éco-responsable.",
    },
    "lille": {
        "traits": ["warm", "hardworking", "convivial", "pragmatic"],
        "values_emphasis": ["community", "family", "solidarité"],
        "media": ["facebook", "youtube", "instagram", "lavoixdunord"],
        "income_bias": "middle",
        "occupations": ["employé", "commerçant", "infirmier", "enseignant", "ouvrier qualifié"],
        "lifestyle_note": "Accueil chaleureux du Nord. Friture, bière, Braderie de Lille. Influence flamande. Vie moins chère que Paris. Proximité Bruxelles/Londres (Eurostar). Forte culture ouvrière et associative.",
    },
    "toulouse": {
        "traits": ["tech-oriented", "student-friendly", "sunny", "young"],
        "values_emphasis": ["innovation", "qualité_de_vie", "liberté"],
        "media": ["instagram", "youtube", "twitter_x", "ladepeche"],
        "income_bias": "upper_middle",
        "occupations": ["ingénieur aérospatial", "chercheur", "étudiant", "startuper", "fonctionnaire"],
        "lifestyle_note": "Ville rose — capitale aérospatiale (Airbus). Étudiante et dynamique. Brique rose, canal du Midi, rugby. Douceur du Sud-Ouest. Écosystème startup en pleine croissance.",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "parisian_professional": {
        "age_range": (28, 42),
        "income": "upper_middle",
        "regions": ["paris"],
        "education": "masters",
        "values": ["culture", "liberté", "qualité_de_vie"],
        "decision": "researcher",
        "channels": ["instagram", "linkedin", "youtube", "lemonde"],
        "spending": (400, 3000),
        "narrative": "Cadre supérieur à La Défense ou startup dans le Marais. 35-40h officiellement, plus en réalité. Apéro after work, expo le weekend. Dépense en vêtements de qualité, restaurants, et escapades. Consommation engagée (bio, local, éthique).",
    },
    "provencial_artisan": {
        "age_range": (32, 55),
        "income": "middle",
        "regions": ["lyon", "marseille", "bordeaux"],
        "education": "vocational",
        "values": ["tradition", "gastronomie", "qualité"],
        "decision": "traditional",
        "channels": ["facebook", "youtube", "regional_press"],
        "spending": (200, 1000),
        "narrative": "Artisan — boulanger, fromager, ébéniste, ou viticulteur. Fierté du métier et du savoir-faire transmis. Clientèle locale fidèle. Présent au marché le samedi. Utilise peu le digital pro, sauf Instagram pour montrer son travail. Achète local.",
    },
    "student_intellectual": {
        "age_range": (19, 26),
        "income": "low",
        "regions": ["paris", "toulouse", "lyon"],
        "education": "bachelors",
        "values": ["culture", "égalité", "liberté"],
        "decision": "impulsive",
        "channels": ["instagram", "tiktok", "twitter_x", "discord"],
        "spending": (50, 400),
        "narrative": "Étudiant en sciences po, philo ou lettres. Débats passionnés au café. Manifestations étudiantes. Budget serré mais dépense pour livres, ciné, et sorties. Cuisine collective en coloc. Friperie et seconde main par conviction autant que par budget.",
    },
    "suburban_family": {
        "age_range": (33, 50),
        "income": "middle",
        "regions": ["lille", "lyon", "bordeaux"],
        "education": "bachelors",
        "values": ["family", "sécurité", "éducation"],
        "decision": "researcher",
        "channels": ["facebook", "youtube", "leboncoin"],
        "spending": (300, 1500),
        "narrative": "Famille pavillonnaire en périphérie. Deux enfants, un chien. Courses au hypermarché le samedi. Compare les prix sur Leclerc Drive. Investit dans la maison, les enfants et les vacances d'été. Voiture indispensable. Cacolac et madeleines pour le goûter.",
    },
    "entrepreneur_startup": {
        "age_range": (25, 40),
        "income": "upper_middle",
        "regions": ["paris", "toulouse", "lyon"],
        "education": "masters",
        "values": ["innovation", "liberté", "égalité"],
        "decision": "early_adopter",
        "channels": ["twitter_x", "linkedin", "youtube", "medium"],
        "spending": (500, 3000),
        "narrative": "Startuper French Tech — levée de fonds, pitch, scale-up. Travail à Station F ou en coworking. Lit du contenu tech US et FR. Utilise Notion, Stripe, Qonto. Dépense en SaaS, design, et networking. Se voit comme le futur champion national.",
    },
    "retiree_culture": {
        "age_range": (62, 80),
        "income": "upper_middle",
        "regions": ["paris", "bordeaux", "lyon"],
        "education": "masters",
        "values": ["culture", "tradition", "laïcité"],
        "decision": "traditional",
        "channels": ["tv", "radio", "facebook", "lefigaro"],
        "spending": (300, 1500),
        "narrative": "Retraité aisé — ancien cadre ou profession libérale. Abonné au théâtre, à l'opéra, aux conférences. Voyage culturel organisé (Italie, Grèce). Lit Le Monde et écoute France Inter. Consommation sélective. Fidèle aux marques de qualité française. Aide financièrement ses enfants.",
    },
}

# French name pools
PERSONA_NAMES = {
    "male": ["Jean", "Pierre", "Michel", "Philippe", "Nicolas", "Antoine", "Thomas", "Alexandre",
             "François", "Laurent", "Olivier", "Julien", "Guillaume", "Benjamin", "Lucas",
             "Hugo", "Louis", "Clément", "Matthieu", "Romain"],
    "female": ["Marie", "Camille", "Sophie", "Julie", "Claire", "Isabelle", "Caroline", "Émilie",
               "Aurélie", "Céline", "Marine", "Pauline", "Virginie", "Chloé", "Léa",
               "Manon", "Emma", "Louise", "Sarah", "Inès"],
    "nickname_male": ["Jeannot", "Pierrot", "Mimi", "Phil", "Nico", "Toine", "Tom", "Alex",
                      "Franck", "Lolo", "Olive", "Juju", "Gui", "Ben", "Lulu",
                      "Hugues", "Loulou", "Clem", "Matt", "Roro"],
    "nickname_female": ["Mimi", "Mimi", "Soso", "Juju", "Clairette", "Isa", "Caro", "Milie",
                        "Auré", "Cécé", "Momo", "Popo", "Vivi", "Chlo", "Lélé",
                        "Manouche", "Emmie", "Lou", "Sasa", "Ninès"],
    "surnames": ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand",
                 "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "Garcia",
                 "David", "Bertrand", "Roux", "Vincent", "Fournier"],
}

# Common French consumer phrases
SHOPPING_PHRASES = [
    "C'est cher", "Bon rapport qualité-prix", "Ça vaut le coup",
    "Fait en France", "Produit du terroir", "Soldes d'hiver/été",
    "Livraison gratuite", "Remboursé si pas satisfait", "Avis clients",
    "C'est une bonne affaire", "Je l'ai vu sur Instagram",
    "Recommandé par 60 Millions de Consommateurs", "Label Bio",
    "Indice de réparabilité", "Acheter local", "Circuit court",
    "Promo en cours", "Carte de fidélité", "Zéro déchet",
    "Fabriqué en France", "Qui se cache derrière la marque",
]

TRUST_FACTORS = [
    "Avis clients vérifiés", "Recommandé par des proches", "Marque française historique",
    "Label / certification (AB, AOP, Origine France Garantie)", "Déjà client / rachat",
    "Transparence sur les ingrédients", "Service client réactif",
    "Recommandé par UFC-Que Choisir / 60 Millions", "Fabriqué en France",
    "Engagement éthique / RSE", "Boutique physique à proximité", "Indice de réparabilité élevé",
    "Influenceur spécialisé (pas influenceur généraliste)", "Repris dans la presse (Le Monde, Les Échos)",
    "Garantie longue durée",
]

COUNTRY_NAME = "France"
CURRENCY = "EUR"
