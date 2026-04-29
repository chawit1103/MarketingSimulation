"""Russian Context — demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Russian consumer
insights, regional differences, and cultural values.
"""

COUNTRY_NAME = "Russia"
CURRENCY = "RUB (Russian Ruble)"

# Russia population by region (2024 estimates, millions for metro areas)
REGION_POPULATION = {
    "moscow": 13.0,
    "saint_petersburg": 5.6,
    "novosibirsk": 1.6,
    "kazan": 1.3,
    "yekaterinburg": 1.5,
    "sochi": 0.7,
}

# Regional cultural profiles
REGION_PROFILES = {
    "moscow": {
        "traits": ["ambitious", "fast-paced", "status-conscious", "individualistic"],
        "values_emphasis": ["education", "patriotism", "soul_душа"],
        "media": ["telegram", "vkontakte", "youtube", "zen", "rutube"],
        "income_bias": "upper_middle",
        "occupations": ["IT specialist", "banker", "manager", "civil servant", "entrepreneur"],
        "lifestyle_note": "Москва не верит слезам — город возможностей и высокой конкуренции. Люди спешат, строят карьеру, пользуются доставкой и каршерингом, ценят качество и бренды. Рестораны и выставки — часть образа жизни.",
    },
    "saint_petersburg": {
        "traits": ["intellectual", "creative", "melancholic", "cultured"],
        "values_emphasis": ["education", "soul_душа", "collectivism"],
        "media": ["telegram", "vkontakte", "youtube", "instagram"],
        "income_bias": "middle",
        "occupations": ["IT specialist", "creative professional", "engineer", "teacher", "museum worker"],
        "lifestyle_note": "Питер — культурная столица, город интеллигенции и белых ночей. Люди ходят в музеи и театры, обсуждают философию на кухне, много читают. Дождь и серое небо — данность, но душа города согревает.",
    },
    "novosibirsk": {
        "traits": ["scientific", "pragmatic", "hardy", "academic"],
        "values_emphasis": ["education", "resilience", "collectivism"],
        "media": ["vkontakte", "telegram", "youtube", "regional_tv"],
        "income_bias": "middle",
        "occupations": ["scientist", "engineer", "IT professional", "academic", "factory worker"],
        "lifestyle_note": "Новосибирск — научный центр Сибири, Академгородок. Суровый климат закаляет характер, люди ценят знания, выживают зимой вместе. Теплые компании и бани — сибирский ритуал.",
    },
    "kazan": {
        "traits": ["multicultural", "religious-harmony", "traditional-modern", "sporty"],
        "values_emphasis": ["family", "collectivism", "education", "patriotism"],
        "media": ["vkontakte", "telegram", "youtube", "instagram"],
        "income_bias": "middle",
        "occupations": ["oil & gas professional", "engineer", "government officer", "teacher", "trader"],
        "lifestyle_note": "Казань — третья столица, перекресток культур (русская и татарская). Мечети рядом с церквями, эчпочмак и чак-чак, семья на первом месте, гостеприимство по-татарски.",
    },
    "yekaterinburg": {
        "traits": ["industrial", "rebellious", "modern", "east-west blend"],
        "values_emphasis": ["resilience", "family", "soul_душа"],
        "media": ["vkontakte", "telegram", "youtube", "instagram"],
        "income_bias": "middle",
        "occupations": ["factory worker", "engineer", "businessman", "IT professional", "logistics worker"],
        "lifestyle_note": "Екатеринбург — столица Урала, граница Европы и Азии. Промышленный город с бунтарским духом, стрит-арт и современная культура. Люди прямые и сильные, уральский характер.",
    },
    "sochi": {
        "traits": ["southern", "relaxed", "hospitality-driven", "tourism-oriented"],
        "values_emphasis": ["family", "hospitality", "celebration", "community"],
        "media": ["instagram", "vkontakte", "telegram", "youtube"],
        "income_bias": "middle",
        "occupations": ["tourism worker", "hotel staff", "restaurant owner", "retreat host", "driver"],
        "lifestyle_note": "Сочи — южные ворота России, курортная жизнь. Люди приветливые и открытые, живут туризмом и гостеприимством, море, горы, шашлык и домашнее вино круглый год.",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "moscow_professional": {
        "age_range": (25, 40),
        "income": "upper_middle",
        "regions": ["moscow"],
        "education": "masters",
        "values": ["education", "soul_душа", "patriotism"],
        "decision": "brand_loyal",
        "channels": ["telegram", "youtube", "vkontakte", "instagram"],
        "spending": (50000, 150000),
        "narrative": "Московский профессионал — работает в международной или крупной российской компании, ценит свое время, пользуется доставкой и подписками, разбирается в вине и путешествует на выходные в Европу или по Золотому кольцу",
    },
    "provincial_worker": {
        "age_range": (30, 55),
        "income": "lower_middle",
        "regions": ["novosibirsk", "yekaterinburg", "kazan"],
        "education": "high_school",
        "values": ["family", "resilience", "collectivism"],
        "decision": "price_sensitive",
        "channels": ["vkontakte", "regional_tv", "youtube", "telegram"],
        "spending": (15000, 40000),
        "narrative": "Провинциальный рабочий — трудится на заводе или в ЖКХ, имеет дачу и верит в свои руки, покупает продукты на рынке и в эконом-магазинах, вечером — гараж или рыбалка, ценит простые радости",
    },
    "university_student": {
        "age_range": (18, 24),
        "income": "low",
        "regions": ["moscow", "saint_petersburg", "novosibirsk", "kazan"],
        "education": "bachelors",
        "values": ["education", "soul_душа", "collectivism"],
        "decision": "social_proof",
        "channels": ["telegram", "vkontakte", "youtube", "tiktok"],
        "spending": (5000, 15000),
        "narrative": "Студент — живет в общежитии или снимает квартиру с друзьями, подрабатывает курьером или репетитором, экономит, но ищет качество, сидит в телеграм-каналах со скидками, верит рекомендациям друзей больше, чем рекламе",
    },
    "babushka_pensioner": {
        "age_range": (60, 80),
        "income": "low",
        "regions": ["moscow", "saint_petersburg", "novosibirsk", "yekaterinburg", "kazan", "sochi"],
        "education": "high_school",
        "values": ["family", "resilience", "collectivism", "patriotism"],
        "decision": "traditional",
        "channels": ["television", "vkontakte", "radio", "telegram"],
        "spending": (8000, 20000),
        "narrative": "Бабушка-пенсионерка — живет на скромную пенсию, помогает детям и внукам, выращивает овощи на даче, консервирует на зиму, смотрит Первый канал, ходит в те же магазины годами, верит проверенным маркам",
    },
    "it_specialist": {
        "age_range": (25, 40),
        "income": "high",
        "regions": ["moscow", "saint_petersburg", "novosibirsk"],
        "education": "masters",
        "values": ["education", "soul_душа", "resilience"],
        "decision": "early_adopter",
        "channels": ["telegram", "habr", "youtube", "github"],
        "spending": (80000, 250000),
        "narrative": "Айтишник — удаленная работа или гибкий график, хорошо зарабатывает, покупает технику и гаджеты сразу после выхода, ценит функциональность и минимализм, деньги тратит на путешествия и саморазвитие",
    },
    "entrepreneur": {
        "age_range": (30, 50),
        "income": "upper_middle",
        "regions": ["moscow", "saint_petersburg", "yekaterinburg", "kazan"],
        "education": "bachelors",
        "values": ["patriotism", "family", "resilience"],
        "decision": "researcher",
        "channels": ["telegram", "vkontakte", "youtube", "linkedin"],
        "spending": (60000, 200000),
        "narrative": "Предприниматель — открыл свое дело после кризиса, крутится как белка в колесе, ценит деловые связи и нетворкинг, покупает бизнес-литературу и курсы, автомобиль — показатель статуса, отдыхает с семьей в Сочи или Турции",
    },
}

# Russian name pools (for realistic name generation)
PERSONA_NAMES = {
    "male": [
        "Александр", "Дмитрий", "Сергей", "Андрей", "Алексей",
        "Михаил", "Иван", "Николай", "Владимир", "Максим",
        "Артём", "Антон", "Павел", "Роман", "Игорь",
        "Евгений", "Виктор", "Олег", "Денис", "Борис",
    ],
    "female": [
        "Елена", "Ольга", "Наталья", "Татьяна", "Анна",
        "Екатерина", "Мария", "Ирина", "Светлана", "Анастасия",
        "Юлия", "Дарья", "Виктория", "Ксения", "Людмила",
        "Галина", "Валентина", "Марина", "Алёна", "Вера",
    ],
    "surnames": [
        "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев",
        "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров",
        "Морозов", "Волков", "Алексеев", "Лебедев", "Семёнов",
        "Егоров", "Павлов", "Козлов", "Степанов", "Николаев",
    ],
}

# Common Russian consumer phrases (for LLM persona grounding)
RUSSIAN_SHOPPING_PHRASES = [
    "Сколько стоит?", "Дороговато будет",
    "А скидка есть?", "Почём?",
    "Беру, не глядя", "Качество хорошее?",
    "Гарантия есть?", "Можно по карте?",
    "Закажу на Wildberries", "На Ozon дешевле",
    "Посмотрю отзывы", "Советую от души",
    "Проверено временем", "Раньше лучше делали",
    "Сделано в России", "Акция — грех не взять",
    "На чёрный день", "Бабушка так делала",
    "Вещь века", "Запас карман не тянет",
]

TRUST_FACTORS = [
    "Рекомендация друзей/родных", "Известность бренда", "Отзывы на маркетплейсах",
    "Цена соответствует качеству", "Гарантия и сервис", "Сделано в России",
    "Совет эксперта/блогера", "Личный опыт использования", "Скидки и акции",
    "Проверенный продавец", "Наличие офлайн-магазина", "Срок доставки",
    "Удобство возврата", "Реклама по ТВ", "Сертификаты качества",
]
