"""PersonaFactory — generate multi-country synthetic consumer personas using LLM.

Supports 11 countries via ContextRegistry: TH, EN, ZH, HI, ES, FR, AR, BN, PT, RU, UR
"""
import random
import logging
from typing import Dict, Any, List, Optional

from ..models.persona import (
    ThaiPersona, PersonaAttribute, ThaiRegion, IncomeLevel,
    EducationLevel, ThaiValueDimension, PurchaseDecisionStyle,
    MediaChannel, Country,
)
from ..models.campaign import CampaignTarget
from .persona_context import ContextRegistry
from ..llm.provider_factory import LLMProviderFactory

logger = logging.getLogger('mirofish.persona_factory')


class PersonaFactory:
    """Generate grounded consumer personas for any supported country."""

    MAX_RETRIES = 2

    def __init__(self, llm_client=None):
        self.llm = llm_client or LLMProviderFactory.get_provider('simulation')
        self._context = None
        self._current_lang = None

    def _load_context(self, language: str):
        """Lazy-load persona context for the given language."""
        if self._current_lang != language:
            self._context = ContextRegistry.get_context(language)
            self._current_lang = language
        return self._context

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_batch(
        self,
        org_id: str,
        campaign_id: str,
        target: CampaignTarget,
        count: int = 100,
        language: str = "th",
    ) -> List[ThaiPersona]:
        """Generate a batch of personas matching campaign target and country."""
        ctx = self._load_context(language)
        personas: List[ThaiPersona] = []

        # Step 1: Select matching archetypes from country context
        archetypes = self._select_archetypes(target, count, ctx)
        archetype_counts = self._distribute_count(count, archetypes, ctx)

        # Step 2 & 3: Generate per archetype group
        persona_id = 0
        for arch_name, arch_count in archetype_counts.items():
            arch = ctx.CONSUMER_ARCHETYPES[arch_name]

            for _ in range(arch_count):
                persona_id += 1
                attrs = self._generate_attributes(arch, target, language, ctx)
                persona = ThaiPersona(
                    org_id=org_id,
                    campaign_id=campaign_id,
                    persona_id=f"per_{org_id}_{campaign_id}_{persona_id:04d}",
                    **attrs.model_dump(),
                )
                personas.append(persona)

        # Step 3: Generate narratives in batches
        self._generate_narratives_batch(personas, language, ctx)

        # Step 4: Assign social relationships
        self._assign_social_graph(personas)

        logger.info(
            f"Generated {len(personas)} personas for campaign {campaign_id} "
            f"(org={org_id}, country={ctx.COUNTRY_NAME}, target={target.segment_name})"
        )
        return personas

    # ------------------------------------------------------------------
    # Archetype selection & distribution
    # ------------------------------------------------------------------

    def _select_archetypes(self, target: CampaignTarget, count: int, ctx) -> List[str]:
        """Select consumer archetypes matching the campaign target."""
        available = list(ctx.CONSUMER_ARCHETYPES.keys())
        matching = []
        for name, arch in ctx.CONSUMER_ARCHETYPES.items():
            arch_min, arch_max = arch["age_range"]
            target_min, target_max = target.age_range
            if arch_max >= target_min and arch_min <= target_max:
                matching.append(name)
        if len(matching) < 2:
            matching = available[:3]
        return matching

    def _distribute_count(self, count: int, archetypes: List[str], ctx) -> Dict[str, int]:
        """Distribute persona count across archetypes with regional weighting."""
        distribution = {}
        weights = []
        for arch in archetypes:
            arch_data = ctx.CONSUMER_ARCHETYPES[arch]
            region_weight = sum(
                ctx.REGION_POPULATION.get(r, 1.0)
                for r in arch_data["regions"]
            )
            weights.append(region_weight)
        total_weight = sum(weights)
        remaining = count
        for i, arch in enumerate(archetypes):
            if i == len(archetypes) - 1:
                distribution[arch] = remaining
            else:
                share = max(1, int(count * weights[i] / total_weight))
                distribution[arch] = share
                remaining -= share
        return distribution

    # ------------------------------------------------------------------
    # Attribute generation
    # ------------------------------------------------------------------

    def _generate_attributes(
        self, archetype: Dict[str, Any], target: CampaignTarget,
        language: str, ctx
    ) -> PersonaAttribute:
        """Generate grounded PersonaAttribute from archetype template."""
        arch = archetype
        country = Country(language) if language in [c.value for c in Country] else Country.EN

        regions = arch["regions"]
        region_weights = [ctx.REGION_POPULATION.get(r, 1.0) for r in regions]
        region = random.choices(regions, weights=region_weights, k=1)[0]

        age_min, age_max = arch["age_range"]
        target_min, target_max = target.age_range
        age = random.randint(max(age_min, target_min), min(age_max, target_max))

        gender = target.gender if target.gender != "all" else random.choice(["male", "female"])
        income = IncomeLevel(arch["income"])
        education = EducationLevel(random.choice([
            "high_school", "vocational", "bachelors", "bachelors", "masters"
        ]))

        values = [ThaiValueDimension(v) for v in arch.get("values", ["family_centric"])[:4]]

        decision = PurchaseDecisionStyle(random.choice([
            arch.get("decision", "researcher"), arch.get("decision", "researcher"),
            "brand_loyal", "impulsive", "social_proof",
        ]))

        brand_loyalty = round(random.uniform(0.2, 0.8), 2)
        price_sensitivity = round(random.uniform(0.3, 0.9), 2)
        social_influence = round(random.uniform(0.3, 0.9), 2)
        innovation_openness = round(random.uniform(0.1, 0.7), 2)

        channels = [MediaChannel(c) for c in random.sample(
            arch.get("channels", ["facebook", "tiktok", "youtube"]),
            k=min(3, len(arch.get("channels", [])))
        )]

        spend_min, spend_max = arch.get("spending", (5000, 30000))
        monthly_spending = random.randint(spend_min, spend_max)

        region_profile = ctx.REGION_PROFILES.get(region, list(ctx.REGION_PROFILES.values())[0])
        occupation = random.choice(region_profile.get("occupations", ["professional"]))

        # Names from country context
        names = ctx.PERSONA_NAMES
        name_pool = names["male"] if gender == "male" else names["female"]
        nick_pool = names.get("nicknames_male", names["male"]) if gender == "male" else names.get("nicknames_female", names["female"])
        surname = random.choice(names.get("surnames", [""]))

        return PersonaAttribute(
            country=country,
            age=age,
            gender=gender,
            region=ThaiRegion.BANGKOK,  # placeholder — region is dynamic per country
            province=region,
            income=income,
            education=education,
            occupation=occupation,
            values=values,
            decision_style=decision,
            brand_loyalty_score=brand_loyalty,
            price_sensitivity_score=price_sensitivity,
            social_influence_score=social_influence,
            innovation_openness=innovation_openness,
            primary_channels=channels,
            influencer_susceptibility=round(random.uniform(0.2, 0.8), 2),
            monthly_spending_budget=monthly_spending,
            name=f"{random.choice(name_pool)} {surname}".strip(),
            nickname=random.choice(nick_pool),
        )

    # ------------------------------------------------------------------
    # LLM narrative generation
    # ------------------------------------------------------------------

    def _generate_narratives_batch(self, personas: List[ThaiPersona], language: str, ctx):
        """Generate narrative backstories for personas using LLM, batches of 5."""
        batch_size = 5
        for i in range(0, len(personas), batch_size):
            batch = personas[i:i + batch_size]
            for p in batch:
                try:
                    prompt = self._build_narrative_prompt(p, language, ctx)
                    messages = [{"role": "user", "content": prompt}]
                    response = self.llm.chat(messages=messages, temperature=0.9, max_tokens=500)
                    p.persona_narrative = response.strip()
                    p.bio = response.strip()[:160]
                    p.generation_model = self.llm.model
                except Exception as e:
                    logger.warning(f"Narrative generation failed: {e}")
                    # Fallback to archetype narrative
                    for arch_name, arch in ctx.CONSUMER_ARCHETYPES.items():
                        if self._matches_archetype(p, arch):
                            p.persona_narrative = arch.get("narrative", "")
                            p.bio = arch.get("narrative", "")[:160]
                            break

    def _build_narrative_prompt(self, persona: ThaiPersona, language: str, ctx) -> str:
        """Build LLM prompt for persona narrative generation."""
        region_info = ctx.REGION_PROFILES.get(
            persona.province,
            list(ctx.REGION_PROFILES.values())[0]
        )

        return f"""Create a realistic 3-5 sentence backstory for this consumer persona:

Name: {persona.name} (Nickname: {persona.nickname})
Age: {persona.age}
Gender: {'Male' if persona.gender == 'male' else 'Female'}
Location: {persona.province}
Occupation: {persona.occupation}
Income Level: {persona.income.value}
Education: {persona.education.value}
Decision Style: {persona.decision_style.value}
Regional Context: {region_info.get('lifestyle_note', '')}
Country: {ctx.COUNTRY_NAME}

Write in {'English' if language == 'en' else 'the native language of ' + ctx.COUNTRY_NAME}.
Respond ONLY with the backstory — no introduction or closing."""

    def _matches_archetype(self, persona: ThaiPersona, arch: Dict[str, Any]) -> bool:
        a_min, a_max = arch.get("age_range", (0, 100))
        return (a_min <= persona.age <= a_max and
                persona.income.value == arch.get("income", ""))

    # ------------------------------------------------------------------
    # Social graph
    # ------------------------------------------------------------------

    def _assign_social_graph(self, personas: List[ThaiPersona]):
        """Assign influence relationships based on similarity."""
        for i, p1 in enumerate(personas):
            for j, p2 in enumerate(personas):
                if i == j:
                    continue
                score = 0.0
                if p1.province == p2.province:
                    score += 0.3
                if any(v in p2.values for v in p1.values[:2]):
                    score += 0.2
                if p1.income == p2.income:
                    score += 0.1
                if abs(p1.age - p2.age) < 10:
                    score += 0.15
                if score > 0.5 and p1.influence_weight > p2.influence_weight:
                    p1.influences.append(p2.persona_id)
                    p2.influenced_by.append(p1.persona_id)
