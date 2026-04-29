"""Chinese Context — 中国 demographic, cultural, and behavioral reference data.

Used by PersonaFactory to ground synthetic personas in real Chinese
consumer insights, regional differences, and cultural values.
"""

# Chinese population by province/municipality (2024 estimates, millions)
REGION_POPULATION = {
    "beijing": 21.9,
    "shanghai": 24.9,
    "guangdong": 127.1,
    "sichuan": 83.7,
    "hubei": 58.4,
    "zhejiang": 66.2,
}

# Regional cultural profiles
REGION_PROFILES = {
    "beijing": {
        "traits": ["political", "direct", "relationship-savvy", "status-conscious"],
        "values_emphasis": ["面子", "关系", "层级尊重"],
        "media": ["微信", "抖音", "微博", "小红书"],
        "income_bias": "upper_middle",
        "occupations": ["公务员", "国企员工", "科技从业者", "教育工作者", "文化从业者"],
        "lifestyle_note": "皇城根下，讲面子重关系。生活节奏快但讲究生活品质。胡同文化与现代CBD并存。子女教育投入大，学区房焦虑普遍。",
    },
    "shanghai": {
        "traits": ["cosmopolitan", "sophisticated", "pragmatic", "trend-conscious"],
        "values_emphasis": ["面子", "小资情调", "公平交易"],
        "media": ["小红书", "抖音", "微信", "大众点评"],
        "income_bias": "upper_middle",
        "occupations": ["金融从业者", "外企白领", "设计师", "创业者", "咨询顾问"],
        "lifestyle_note": "精致小资生活。咖啡文化浓厚，Brunch打卡。对品牌敏感度全国最高。海派文化，崇洋但不媚外，追求品质与格调。",
    },
    "guangdong": {
        "traits": ["entrepreneurial", "pragmatic", "food-obsessed", "family-oriented"],
        "values_emphasis": ["实用主义", "家族观念", "财神信仰"],
        "media": ["微信", "抖音", "快手", "淘宝直播"],
        "income_bias": "middle",
        "occupations": ["工厂主", "外贸从业者", "电子制造业工人", "餐饮业主", "物流从业者"],
        "lifestyle_note": "敢为天下先的创业精神。早茶文化、煲汤养生。务实消费，不重品牌重性价比。家族生意多，过年发红包大方。",
    },
    "sichuan": {
        "traits": ["laid-back", "food-loving", "social", "humorous"],
        "values_emphasis": ["安逸", "社交", "享受生活"],
        "media": ["抖音", "微信", "快手", "淘宝"],
        "income_bias": "lower_middle",
        "occupations": ["服务业从业者", "农业从业者", "旅游业从业者", "餐饮业主", "小商户"],
        "lifestyle_note": "天府之国，安逸巴适。火锅麻将茶馆三件套。消费重体验轻品牌。网红城市（成都）带动年轻人消费升级。",
    },
    "hubei": {
        "traits": ["resilient", "pragmatic", "education-focused", "direct"],
        "values_emphasis": ["教育", "家庭", "实用主义"],
        "media": ["微信", "抖音", "微博", "淘宝"],
        "income_bias": "middle",
        "occupations": ["制造业工人", "大学生", "教育从业者", "科技从业者", "物流从业者"],
        "lifestyle_note": "九省通衢，交通枢纽。教育大省，高考竞争激烈。武汉大学生数量全国前列。消费偏理性，重视教育投入。",
    },
    "zhejiang": {
        "traits": ["entrepreneurial", "digital-savvy", "trend-setting", "merchant-spirit"],
        "values_emphasis": ["创新", "实用主义", "家族传承"],
        "media": ["淘宝直播", "抖音", "小红书", "微信"],
        "income_bias": "upper_middle",
        "occupations": ["电商从业者", "小企业主", "科技从业者", "外贸从业者", "制造业管理者"],
        "lifestyle_note": "浙商精神，全民创业。杭州数字经济发达，义乌小商品全球闻名。直播带货文化盛行，消费紧跟数字潮流。",
    },
}

# Consumer segment archetypes
CONSUMER_ARCHETYPES = {
    "一线白领": {
        "age_range": (25, 38),
        "income": "upper_middle",
        "regions": ["beijing", "shanghai", "zhejiang"],
        "education": "bachelors",
        "values": ["面子", "自我提升", "品质生活"],
        "decision": "social_proof",
        "channels": ["小红书", "抖音", "微信", "大众点评"],
        "spending": (3000, 15000),
        "narrative": "北上深杭大厂/外企白领。996工作制，KPI压力大。消费追求品质和格调，看重小红书种草和朋友圈评价。愿意为便利付费（外卖、打车），关注自我投资（健身、知识付费）。",
    },
    "小镇青年": {
        "age_range": (20, 32),
        "income": "lower_middle",
        "regions": ["sichuan", "hubei", "guangdong"],
        "education": "high_school",
        "values": ["面子", "社交", "自我表达"],
        "decision": "impulsive",
        "channels": ["快手", "抖音", "拼多多", "微信"],
        "spending": (1000, 5000),
        "narrative": "三四线城市及县城青年。生活节奏慢，可支配时间多。消费升级意愿强但预算有限。通过快手/抖音了解潮流，拼多多解决日常购物。愿意为社交娱乐和游戏花钱。",
    },
    "银发族": {
        "age_range": (55, 75),
        "income": "middle",
        "regions": ["beijing", "shanghai", "guangdong", "sichuan"],
        "education": "high_school",
        "values": ["孝道", "传统", "健康"],
        "decision": "traditional",
        "channels": ["微信", "电视", "抖音"],
        "spending": (1000, 5000),
        "narrative": "退休老人，有稳定退休金。主要消费在保健品、孙辈礼物和日常买菜。微信是主要社交工具，喜欢转发养生文章。对电商信任度低，偏好线下实体店和熟人推荐。",
    },
    "宝妈": {
        "age_range": (28, 42),
        "income": "middle",
        "regions": ["beijing", "shanghai", "guangdong", "zhejiang"],
        "education": "bachelors",
        "values": ["家庭", "教育", "安全"],
        "decision": "researcher",
        "channels": ["小红书", "微信", "抖音", "淘宝"],
        "spending": (2000, 8000),
        "narrative": "精致妈妈，掌管家庭消费决策。孩子教育投入无上限。深入研究产品成分和安全性（特别是母婴产品）。加入各种妈妈群，信任群内推荐。618/双十一大囤货。",
    },
    "大学生": {
        "age_range": (18, 24),
        "income": "low",
        "regions": ["hubei", "beijing", "shanghai", "zhejiang"],
        "education": "bachelors",
        "values": ["自我表达", "社交", "个性"],
        "decision": "impulsive",
        "channels": ["抖音", "B站", "小红书", "微信"],
        "spending": (500, 3000),
        "narrative": "在校大学生，生活费来自父母。消费集中于餐饮、娱乐、美妆护肤品和数码产品。追求性价比但愿意为爱好氪金。追星、二次元、游戏文化圈层消费明显。",
    },
    "企业家": {
        "age_range": (35, 55),
        "income": "high",
        "regions": ["guangdong", "zhejiang", "shanghai"],
        "education": "masters",
        "values": ["面子", "关系", "成就"],
        "decision": "researcher",
        "channels": ["微信", "抖音", "专业媒体"],
        "spending": (10000, 50000),
        "narrative": "中小企业主，年收入100万以上。商务宴请和送礼消费占比高。座驾和腕表体现身份。关注政商关系和经济政策。消费注重品牌和面子，但也讲究实际价值。",
    },
}

# Chinese name pools (in Chinese characters)
PERSONA_NAMES = {
    "male": ["伟", "强", "磊", "涛", "军", "勇", "杰", "建华",
             "建国", "志强", "文博", "浩然", "宇轩", "子涵", "泽宇",
             "明哲", "俊杰", "博文", "天宇", "鸿飞"],
    "female": ["芳", "敏", "静", "丽", "娟", "婷", "雪", "雅芬",
               "美玲", "秀英", "雨萱", "诗涵", "梓涵", "梦琪", "思雨",
               "欣怡", "雅琪", "若琳", "晓萌", "慧敏"],
    "nickname_male": ["阿伟", "大强", "小磊", "阿涛", "军哥", "勇哥", "杰哥",
                      "老王", "小陈", "阿明", "大鹏", "龙哥", "阿文", "小宇", "飞哥"],
    "nickname_female": ["小芳", "敏敏", "静静", "丽丽", "娟娟", "婷婷", "小雪",
                        "美美", "小红", "阿玲", "小雨", "欣欣", "萌萌", "小雅", "小琳"],
    "surnames": ["王", "李", "张", "刘", "陈", "杨", "赵", "黄",
                 "周", "吴", "徐", "孙", "胡", "朱", "高",
                 "林", "何", "郭", "马", "罗"],
}

# Common Chinese consumer phrases
SHOPPING_PHRASES = [
    "种草了", "剁手", "真香", "绝绝子", "yyds",
    "买它买它", "这款卖爆了", "限时秒杀", "拼单吗",
    "看看评价", "良心推荐", "避雷", "智商税",
    "贫民窟女孩必备", "性价比之王", "回购无数次",
    "先加购物车", "等双十一", "满减凑单",
    "有运费险吗", "支持七天无理由吗",
]

TRUST_FACTORS = [
    "真实用户评价/买家秀", "朋友/家人推荐", "知名品牌/老字号",
    "官方旗舰店", "有质检报告", "一直用这个牌子/回购",
    "明星/网红推荐", "上过李佳琦/薇娅直播间", "小红书万赞笔记",
    "央视报道过", "口碑好/很多人买", "售后服务好",
    "七天无理由退换", "支持验货", "有线下实体店",
]

COUNTRY_NAME = "中国"
CURRENCY = "CNY"
