"""Thai Persona model — a synthetic consumer grounded in Thai cultural context.

Key dimensions:
- Demographics: age, gender, region, income, education, occupation
- Psychographics: values, lifestyle, personality (MBTI), decision-making style
- Consumer Behavior: brand loyalty, price sensitivity, channel preference
- Social Context: family role, social class, community influence, face-saving
- Media: platform usage, content preferences, influencer susceptibility
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
import uuid


class Country(str, Enum):
    TH = "th"
    EN = "en"
    ZH = "zh"
    HI = "hi"
    ES = "es"
    FR = "fr"
    AR = "ar"
    BN = "bn"
    PT = "pt"
    RU = "ru"
    UR = "ur"


class ThaiRegion(str, Enum):
    BANGKOK = "bangkok"
    CENTRAL = "central"
    NORTH = "north"
    NORTHEAST = "northeast"   # Isan
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class IncomeLevel(str, Enum):
    LOW = "low"              # < 15,000 THB/mo
    LOWER_MIDDLE = "lower_middle"  # 15,000-30,000
    MIDDLE = "middle"        # 30,000-70,000
    UPPER_MIDDLE = "upper_middle"  # 70,000-150,000
    HIGH = "high"            # > 150,000


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    VOCATIONAL = "vocational"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"


class ThaiValueDimension(str, Enum):
    """Core Thai cultural values that influence decision-making."""
    FACE_SAVING = "face_saving"          # เกรงใจ, รักษาหน้า
    SOCIAL_HARMONY = "social_harmony"    # ความสามัคคี
    FAMILY_CENTRIC = "family_centric"    # ครอบครัวสำคัญ
    HIERARCHY_RESPECT = "hierarchy_respect"  # เคารพผู้อาวุโส
    SANUK = "sanuk"                      # ความสนุกสนาน
    BUNKHUN = "bunkhun"                  # บุญคุณ, reciprocity
    JAI_YEN = "jai_yen"                  # ใจเย็น, calm
    MAI_PEN_RAI = "mai_pen_rai"          # ไม่เป็นไร, easygoing
    GREENG_JAI = "greeng_jai"            # เกรงใจ, considerate
    NAM_JAI = "nam_jai"                  # น้ำใจ, generosity


class PurchaseDecisionStyle(str, Enum):
    IMPULSIVE = "impulsive"
    RESEARCHER = "researcher"            # ศึกษาก่อนซื้อ
    BRAND_LOYAL = "brand_loyal"
    PRICE_SENSITIVE = "price_sensitive"
    SOCIAL_PROOF = "social_proof"         # ซื้อตามรีวิว/อินฟลูฯ
    EARLY_ADOPTER = "early_adopter"
    TRADITIONAL = "traditional"           # ซื้อตามที่เคยใช้


class MediaChannel(str, Enum):
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    LINE = "line"
    TWITTER_X = "twitter_x"
    SHOPEE_LIVE = "shopee_live"
    TV = "tv"
    RADIO = "radio"
    NEWSPAPER = "newspaper"
    PANTIP = "pantip"


class PersonaAttribute(BaseModel):
    """Structured persona attributes for simulation."""
    country: Country = Country.TH
    age: int = 30
    gender: str = "female"
    region: ThaiRegion = ThaiRegion.BANGKOK
    province: str = "กรุงเทพมหานคร"
    income: IncomeLevel = IncomeLevel.MIDDLE
    education: EducationLevel = EducationLevel.BACHELORS
    occupation: str = "พนักงานบริษัท"
    
    # Psychographics
    values: List[ThaiValueDimension] = Field(default_factory=lambda: [
        ThaiValueDimension.FACE_SAVING,
        ThaiValueDimension.FAMILY_CENTRIC,
        ThaiValueDimension.SOCIAL_HARMONY,
    ])
    personality_mbti: str = "ISFJ"
    decision_style: PurchaseDecisionStyle = PurchaseDecisionStyle.SOCIAL_PROOF
    
    # Consumer behavior
    brand_loyalty_score: float = 0.5       # 0.0 = switches every time, 1.0 = never switches
    price_sensitivity_score: float = 0.6   # 0.0 =不在乎价格, 1.0 = extremely price sensitive
    social_influence_score: float = 0.7    # 0.0 = immune to social proof, 1.0 = highly influenced
    innovation_openness: float = 0.4       # 0.0 = traditionalist, 1.0 = early adopter
    
    # Media consumption
    primary_channels: List[MediaChannel] = Field(default_factory=lambda: [
        MediaChannel.FACEBOOK,
        MediaChannel.TIKTOK,
        MediaChannel.LINE,
    ])
    daily_screen_time_hours: float = 5.5
    influencer_susceptibility: float = 0.6  # 0.0 = ignores influencers, 1.0 = heavily influenced
    
    # Thai-specific
    family_size: int = 4
    sends_money_to_parents: bool = True    # ส่งเงินให้พ่อแม่
    owns_vehicle: str = "car"              # car, motorcycle, both, none
    housing: str = "own_house"             # own_house, condo, rent, with_parents
    
    # Financial
    monthly_spending_budget: float = 15000  # discretionary spending THB/mo
    saving_rate_percent: float = 15
    credit_card_usage: str = "occasional"  # none, occasional, heavy
    debt_attitude: str = "conservative"    # conservative, moderate, comfortable


class ThaiPersona(PersonaAttribute):
    """A fully grounded Thai synthetic consumer persona."""
    persona_id: str = Field(default_factory=lambda: f"per_{uuid.uuid4().hex[:12]}")
    org_id: str = ""
    campaign_id: str = ""
    
    # Identity
    name: str = ""
    nickname: str = ""                       # ชื่อเล่น
    bio: str = ""
    persona_narrative: str = ""              # Full backstory in Thai
    avatar_prompt: str = ""                  # Prompt for generating avatar image
    
    # Campaign stance (populated during simulation setup)
    initial_sentiment: str = "neutral"      # positive, negative, neutral, skeptical, curious
    opinion_on_topic: str = ""              # Pre-simulation opinion
    
    # Social graph
    influences: List[str] = Field(default_factory=list)     # persona_ids they influence
    influenced_by: List[str] = Field(default_factory=list)  # persona_ids influencing them
    influence_weight: float = 0.5           # 0.0 = no influence, 1.0 = opinion leader
    
    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    generation_model: str = ""
    generation_prompt_tokens: int = 0
    
    def to_oasis_profile(self, user_id: int, platform: str = "twitter") -> Dict[str, Any]:
        """Convert to OASIS agent profile for simulation."""
        base = {
            "user_id": user_id,
            "username": f"@{self.nickname}_{user_id}",
            "name": self.name,
            "bio": self.bio[:160],
            "persona": self._build_oasis_persona_text(),
        }
        
        if platform == "twitter":
            base.update({
                "follower_count": int(100 * self.influence_weight * self.social_influence_score),
                "friend_count": int(50 * self.social_influence_score),
                "statuses_count": int(200 * self.innovation_openness),
            })
        elif platform == "reddit":
            base.update({
                "karma": int(1000 * self.social_influence_score * self.influence_weight),
            })
        
        # Add Thai-specific metadata
        base["region"] = self.region.value
        base["income_level"] = self.income.value
        base["sentiment"] = self.initial_sentiment
        
        return base
    
    def _build_oasis_persona_text(self) -> str:
        """Build the persona text that the LLM agent uses to role-play."""
        parts = [
            f"คุณคือ{self.name} (ชื่อเล่น: {self.nickname})",
            f"อายุ {self.age} ปี อาศัยอยู่ที่{self.province}",
            f"อาชีพ: {self.occupation} รายได้ระดับ{self.income.value}",
            f"การศึกษา: {self.education.value}",
        ]
        
        if self.values:
            value_names = {
                ThaiValueDimension.FACE_SAVING: "รักษาหน้าและเกรงใจ",
                ThaiValueDimension.FAMILY_CENTRIC: "ให้ความสำคัญกับครอบครัว",
                ThaiValueDimension.SOCIAL_HARMONY: "ชอบความสามัคคี",
                ThaiValueDimension.BUNKHUN: "เชื่อเรื่องบุญคุณ",
                ThaiValueDimension.SANUK: "ชอบความสนุกสนาน",
                ThaiValueDimension.MAI_PEN_RAI: "สบายๆ ชิวๆ",
                ThaiValueDimension.GREENG_JAI: "เกรงใจผู้อื่น",
                ThaiValueDimension.NAM_JAI: "มีน้ำใจ",
            }
            value_texts = [value_names.get(v, v.value) for v in self.values[:4]]
            parts.append(f"ค่านิยม: {' '.join(value_texts)}")
        
        parts.append(f"สไตล์การซื้อ: {self.decision_style.value}")
        
        if self.persona_narrative:
            parts.append(f"\nเรื่องราว: {self.persona_narrative}")
        
        return "\n".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThaiPersona":
        return cls(**data)
