"""Brazilian Context — demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Brazilian consumer
insights, regional differences, and cultural values.
"""

COUNTRY_NAME = "Brazil"
CURRENCY = "BRL (Brazilian Real)"

# Brazil population by region (2024 estimates, millions for metro areas)
REGION_POPULATION = {
    "sao_paulo": 22.5,
    "rio_de_janeiro": 13.0,
    "salvador": 4.0,
    "brasilia": 4.8,
    "belo_horizonte": 6.0,
    "recife": 4.2,
}

# Regional cultural profiles
REGION_PROFILES = {
    "sao_paulo": {
        "traits": ["workaholic", "competitive", "cosmopolitan", "fast-paced"],
        "values_emphasis": ["family", "jeitinho", "celebration"],
        "media": ["instagram", "youtube", "whatsapp", "linkedin", "tiktok"],
        "income_bias": "upper_middle",
        "occupations": ["banker", "tech professional", "lawyer", "business owner", "marketing executive"],
        "lifestyle_note": "São Paulo não para — a cidade que nunca dorme. Trânsito infernal, happy hour na Vila Madalena, entrega por iFood, e o sonho do apartamento próprio. Paulista trabalha duro e consome com exigência.",
    },
    "rio_de_janeiro": {
        "traits": ["laid-back", "social", "appearance-conscious", "creative"],
        "values_emphasis": ["alegria", "celebration", "community", "jeitinho"],
        "media": ["instagram", "whatsapp", "tiktok", "youtube", "twitter_x"],
        "income_bias": "middle",
        "occupations": ["creative professional", "tourism worker", "public servant", "teacher", "vendor"],
        "lifestyle_note": "Rio — praia, samba e Copa. Carioca valoriza o corpo, vai à praia no fim de semana, pede açaí, e divide tudo no grupo de WhatsApp. A vida social é o centro de tudo.",
    },
    "salvador": {
        "traits": ["festive", "spiritual", "community-oriented", "warm"],
        "values_emphasis": ["family", "celebration", "community", "faith"],
        "media": ["instagram", "whatsapp", "facebook", "tiktok", "youtube"],
        "income_bias": "lower_middle",
        "occupations": ["tourism worker", "street vendor", "artist", "civil servant", "teacher"],
        "lifestyle_note": "Salvador — axé, acarajé e tradição. A cidade mais negra do Brasil, sincretismo religioso, carnaval o ano inteiro, compras no centro histórico e na feira de São Joaquim.",
    },
    "brasilia": {
        "traits": ["formal", "bureaucratic", "planned", "political"],
        "values_emphasis": ["family", "education", "celebration"],
        "media": ["whatsapp", "instagram", "linkedin", "youtube", "twitter_x"],
        "income_bias": "upper_middle",
        "occupations": ["public servant", "politician", "lawyer", "diplomat", "consultant"],
        "lifestyle_note": "Brasília — a cidade do poder. Funcionalismo público domina, shopping é o point, carro é indispensável, churrasco no fim de semana com a família é sagrado.",
    },
    "belo_horizonte": {
        "traits": ["hospitable", "traditional", "bar-culture", "family-oriented"],
        "values_emphasis": ["family", "hospitality", "community"],
        "media": ["whatsapp", "instagram", "facebook", "youtube"],
        "income_bias": "middle",
        "occupations": ["engineer", "mining professional", "small business owner", "teacher", "IT professional"],
        "lifestyle_note": "BH — a capital dos botecos. Mineiro come pão de queijo, vai ao Mercado Central, recebe visita em casa com café fresco e bolinho. A palavra é aconchego e prosa boa.",
    },
    "recife": {
        "traits": ["creative", "tech-savvy", "festive", "regional-identity"],
        "values_emphasis": ["family", "celebration", "community", "resilience"],
        "media": ["instagram", "whatsapp", "tiktok", "youtube", "twitter_x"],
        "income_bias": "middle",
        "occupations": ["tech professional", "creative", "teacher", "tourism worker", "health professional"],
        "lifestyle_note": "Recife — frevo, manguebeat e tecnologia. Porto Digital é orgulho local, praia de Boa Viagem no fim de semana, tapioca com queijo coalho, e o Galo da Madrugada arrasta multidões.",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "paulista_professional": {
        "age_range": (25, 40),
        "income": "upper_middle",
        "regions": ["sao_paulo"],
        "education": "masters",
        "values": ["jeitinho", "family", "celebration"],
        "decision": "researcher",
        "channels": ["linkedin", "instagram", "youtube", "whatsapp"],
        "spending": (3000, 10000),
        "narrative": "Profissional de São Paulo — formado em universidade de ponta, trabalha na Faria Lima, pede tudo por aplicativo, lê reviews antes de comprar, valoriza marcas premium mas pesquisa preço, cartão de crédito parcelado em 12x",
    },
    "carioca_creative": {
        "age_range": (22, 38),
        "income": "middle",
        "regions": ["rio_de_janeiro"],
        "education": "bachelors",
        "values": ["alegria", "community", "celebration"],
        "decision": "social_proof",
        "channels": ["instagram", "tiktok", "whatsapp", "twitter_x"],
        "spending": (2000, 6000),
        "narrative": "Criativo carioca — trabalha com design, fotografia ou redes sociais, vida compartilhada nos stories do Instagram, compra em brechó descolado e feira hippie, valoriza experiências mais que produtos, adora um evento cultural gratuito",
    },
    "nordestino_worker": {
        "age_range": (25, 50),
        "income": "lower_middle",
        "regions": ["salvador", "recife"],
        "education": "high_school",
        "values": ["family", "faith", "resilience", "community"],
        "decision": "price_sensitive",
        "channels": ["facebook", "whatsapp", "youtube", "television"],
        "spending": (1000, 3000),
        "narrative": "Trabalhador nordestino — acorda cedo, pega ônibus lotado, sustenta a família com orgulho, pesquisa preço no mercado, compra na feira e no atacarejo, fiel às marcas que cabem no bolso, fé em Deus e festa junina o ano inteiro",
    },
    "university_student": {
        "age_range": (18, 25),
        "income": "low",
        "regions": ["sao_paulo", "rio_de_janeiro", "brasilia", "belo_horizonte", "recife"],
        "education": "bachelors",
        "values": ["alegria", "community", "celebration"],
        "decision": "impulsive",
        "channels": ["tiktok", "instagram", "twitter_x", "whatsapp"],
        "spending": (500, 2000),
        "narrative": "Estudante universitário — depende da mesada dos pais ou faz bico, vive de festa e rolê universitário, compra no site chinês (Shopee/AliExpress), segue tendências do TikTok, divide assinatura de streaming com amigos",
    },
    "small_business_owner": {
        "age_range": (30, 55),
        "income": "middle",
        "regions": ["sao_paulo", "belo_horizonte", "recife", "salvador"],
        "education": "high_school",
        "values": ["family", "jeitinho", "community"],
        "decision": "researcher",
        "channels": ["whatsapp", "instagram", "facebook", "youtube"],
        "spending": (2000, 8000),
        "narrative": "Dono de pequeno negócio — tem lojinha na quebrada ou comércio no bairro, usa WhatsApp Business pra atender cliente, faz promoção no Instagram, compra em atacado, o jeitinho brasileiro resolve tudo que a burocracia complica",
    },
    "influencer_digital": {
        "age_range": (20, 35),
        "income": "upper_middle",
        "regions": ["sao_paulo", "rio_de_janeiro"],
        "education": "bachelors",
        "values": ["alegria", "celebration", "community"],
        "decision": "early_adopter",
        "channels": ["instagram", "tiktok", "youtube", "twitter_x"],
        "spending": (4000, 15000),
        "narrative": "Influenciador digital — produz conteúdo o dia inteiro, recebe produtos de marcas, testa tudo antes de recomendar, vive de parcerias e publiposts, a estética do feed é prioridade, viaja bastante e posta tudo",
    },
}

# Brazilian name pools (for realistic name generation)
PERSONA_NAMES = {
    "male": [
        "João", "Pedro", "Lucas", "Gabriel", "Matheus",
        "Rafael", "Felipe", "Bruno", "Thiago", "Marcos",
        "Anderson", "José", "Carlos", "Paulo", "Antônio",
        "Francisco", "Luiz", "Rodrigo", "Fernando", "Gustavo",
    ],
    "female": [
        "Maria", "Ana", "Júlia", "Beatriz", "Fernanda",
        "Amanda", "Larissa", "Juliana", "Camila", "Natália",
        "Gabriela", "Carolina", "Patrícia", "Letícia", "Mariana",
        "Isabela", "Rafaela", "Bruna", "Débora", "Tatiane",
    ],
    "surnames": [
        "Silva", "Santos", "Oliveira", "Souza", "Lima",
        "Pereira", "Costa", "Ferreira", "Almeida", "Ribeiro",
        "Nascimento", "Carvalho", "Gomes", "Martins", "Barbosa",
    ],
}

# Common Brazilian consumer phrases (for LLM persona grounding)
BRAZILIAN_SHOPPING_PHRASES = [
    "Tem desconto no pix?", "Parcela em quantas vezes?",
    "Vou levar, faz aquele precinho?", "Olha a promoção!",
    "Tá caro, hein!", "Vou pesquisar na internet primeiro",
    "Pode ser no cartão?", "Tem frete grátis?",
    "Comprei na Shopee", "Qual é a garantia?",
    "Indicações de grupo de WhatsApp", "Vi no Instagram",
    "Viralizou no TikTok", "Tem cashback?",
    "Aproveita que é Black Friday", "Meu amigo comprou e recomendou",
    "Paguei baratinho", "Original ou réplica?",
]

TRUST_FACTORS = [
    "Indicação de amigos/família", "Avaliações positivas online",
    "Preço justo", "Marca conhecida", "Atendimento humanizado",
    "Garantia estendida", "Selos de qualidade (Inmetro/Anvisa)",
    "Influenciador confiável", "Tempo de mercado da empresa",
    "Facilidade de troca/devolução", "Loja física existe",
    "Grupo de WhatsApp com boas referências", "Cashback e benefícios",
    "Comentários no Reclame Aqui", "Produto nacional",
]
