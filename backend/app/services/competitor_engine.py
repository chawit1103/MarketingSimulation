"""Competitor Simulation Engine — multi-brand war gaming with event injection.

Simulates market share shifts when brands compete with different strategies.
Each brand has: base_sentiment, price_position, brand_strength
Events inject shocks: price_cut, scandal, product_launch, viral_campaign
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import random
import math
import logging

logger = logging.getLogger("mirofish.competitor_engine")


def _dump_model(model: BaseModel) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


# ── Models ────────────────────────────────────────────────

class BrandProfile(BaseModel):
    """One competitor brand in the simulation."""
    name: str                                          # Brand name (e.g., "Our Brand A")
    base_sentiment: float = 30                         # -100 to +100
    price_position: float = 50                         # 0-100 (0=cheapest, 100=premium)
    brand_strength: float = 60                         # 0-100 (brand equity/power)
    market_share: float = 25.0                         # % (initial)
    description: str = ""                              # Short description

class SimulationEvent(BaseModel):
    """A shock event injected into the simulation at a specific round."""
    name: str                                          # Event name
    round: int = 3                                     # When it happens (1-20)
    target_brand: str                                  # Which brand is affected
    type: str = "price_cut"                            # price_cut | scandal | product_launch | viral_campaign
    magnitude: float = 20                              # Impact magnitude (0-100)
    description: str = ""                              # What happened (Thai)
    duration_rounds: int = 3                           # How long effects last

class RoundResult(BaseModel):
    """Per-round market snapshot."""
    round_num: int
    brand_name: str
    sentiment: float                                   # -100 to +100
    market_share: float                                # %
    price_index: float                                 # 0-100
    social_volume: int                                  # number of posts/mentions

class SimulationResult(BaseModel):
    """Full competitor simulation result."""
    scenario_name: str
    rounds: int
    brands: List[str]
    timeline: List[RoundResult]                        # All rounds × all brands
    final_market_share: Dict[str, float]               # Brand → final share %
    share_shift: Dict[str, float]                      # Brand → change from initial
    winner: str                                        # Brand with most share gain
    key_events: List[Dict[str, Any]]                   # Event log
    source: Dict[str, Any] = Field(default_factory=dict)
    expected_sentiment_movement: Dict[str, float] = Field(default_factory=dict)
    affected_segments: List[str] = Field(default_factory=list)
    amplification_channels: List[str] = Field(default_factory=list)
    key_drivers: List[str] = Field(default_factory=list)
    recommended_response: str = ""
    response_playbook: List[Dict[str, Any]] = Field(default_factory=list)
    known_limitations: List[str] = Field(default_factory=list)


# ── Engine ────────────────────────────────────────────────

class CompetitorSimEngine:
    """Multi-brand market simulation with event injection."""

    @staticmethod
    def simulate(
        brands: List[BrandProfile],
        events: List[SimulationEvent] = None,
        rounds: int = 12,
        scenario_name: str = "Custom Scenario",
        scenario_metadata: Optional[Dict[str, Any]] = None,
    ) -> SimulationResult:
        """Run a multi-round simulation with brand competition and events."""

        if not brands or len(brands) < 2:
            raise ValueError("Need at least 2 brands to simulate competition")

        events = events or []
        scenario_metadata = scenario_metadata or {}
        random.seed(42)  # reproducible

        # Initialize state
        brand_state = {}
        for b in brands:
            brand_state[b.name] = {
                "sentiment": b.base_sentiment,
                "share": b.market_share,
                "price": b.price_position,
                "strength": b.brand_strength,
                "volume": 100,
            }

        # Event index by round
        events_by_round: Dict[int, List[SimulationEvent]] = {}
        for ev in events:
            events_by_round.setdefault(ev.round, []).append(ev)

        active_events: List[SimulationEvent] = []  # events currently in effect
        timeline: List[RoundResult] = []
        event_log: List[Dict[str, Any]] = []

        initial_shares = {b.name: b.market_share for b in brands}
        initial_sentiment = {b.name: b.base_sentiment for b in brands}

        for rnd in range(1, rounds + 1):
            # Process new events this round
            if rnd in events_by_round:
                for ev in events_by_round[rnd]:
                    active_events.append(ev)
                    event_log.append({
                        "round": rnd,
                        "name": ev.name,
                        "target": ev.target_brand,
                        "type": ev.type,
                        "impact": f"{'🟢' if ev.type in ('product_launch','viral_campaign') else '🔴' if ev.type == 'scandal' else '🟡'} {ev.description}",
                    })

            # Expire old events
            active_events = [ev for ev in active_events if rnd < ev.round + ev.duration_rounds]

            # Apply events to brand states
            for ev in active_events:
                if ev.target_brand in brand_state:
                    bs = brand_state[ev.target_brand]
                    if ev.type == "price_cut":
                        bs["price"] = max(0, bs["price"] - ev.magnitude * 0.5)
                        bs["sentiment"] = min(100, bs["sentiment"] + ev.magnitude * 0.3)  # consumers like lower prices
                        bs["volume"] += int(ev.magnitude * 3)
                    elif ev.type == "scandal":
                        bs["sentiment"] = max(-100, bs["sentiment"] - ev.magnitude)
                        bs["share"] = max(1, bs["share"] - ev.magnitude * 0.15)
                        bs["volume"] += int(ev.magnitude * 5)
                    elif ev.type == "product_launch":
                        bs["sentiment"] = min(100, bs["sentiment"] + ev.magnitude * 0.5)
                        bs["volume"] += int(ev.magnitude * 4)
                    elif ev.type == "viral_campaign":
                        bs["sentiment"] = min(100, bs["sentiment"] + ev.magnitude * 0.6)
                        bs["share"] = min(50, bs["share"] + ev.magnitude * 0.1)
                        bs["volume"] += int(ev.magnitude * 6)

            # Natural dynamics — brands interact
            for bname, bs in brand_state.items():
                # Random walk sentiment
                bs["sentiment"] += random.uniform(-5, 5)
                bs["sentiment"] = max(-100, min(100, bs["sentiment"]))

                # Competition: brands with lower price steal share from premium ones
                for other_name, other_bs in brand_state.items():
                    if other_name == bname:
                        continue
                    price_diff = other_bs["price"] - bs["price"]
                    if price_diff > 10:  # other is more expensive
                        steal = min(0.5, price_diff * 0.01) * (bs["strength"] / 100)
                        bs["share"] += steal
                        other_bs["share"] -= steal

                # Sentiment drives organic share
                sentiment_bonus = bs["sentiment"] * 0.02
                bs["share"] += sentiment_bonus * 0.5
                bs["share"] = max(1, min(60, bs["share"]))

                # Add noise
                bs["volume"] += random.randint(-20, 20)
                bs["volume"] = max(10, bs["volume"])

            # Normalize shares to sum to 100%
            total_share = sum(bs["share"] for bs in brand_state.values())
            if total_share > 0:
                for bs in brand_state.values():
                    bs["share"] = (bs["share"] / total_share) * 100

            # Record round results
            for bname, bs in brand_state.items():
                timeline.append(RoundResult(
                    round_num=rnd,
                    brand_name=bname,
                    sentiment=round(bs["sentiment"], 1),
                    market_share=round(bs["share"], 1),
                    price_index=round(bs["price"], 1),
                    social_volume=bs["volume"],
                ))

        # Final results
        final_shares = {bname: round(bs["share"], 1) for bname, bs in brand_state.items()}
        share_shift = {bname: round(final_shares[bname] - initial_shares.get(bname, 0), 1) for bname in final_shares}
        sentiment_shift = {
            bname: round(bs["sentiment"] - initial_sentiment.get(bname, bs["sentiment"]), 1)
            for bname, bs in brand_state.items()
        }
        winner = max(share_shift, key=share_shift.get)

        return SimulationResult(
            scenario_name=scenario_name,
            rounds=rounds,
            brands=[b.name for b in brands],
            timeline=[_dump_model(t) for t in timeline],
            final_market_share=final_shares,
            share_shift=share_shift,
            winner=winner,
            key_events=event_log,
            source={
                "type": "live_backend",
                "warning": "Backend deterministic competitor simulation. Not calibrated against live market outcomes.",
            },
            expected_sentiment_movement=sentiment_shift,
            affected_segments=scenario_metadata.get("affected_segments", []),
            amplification_channels=scenario_metadata.get("amplification_channels", []),
            key_drivers=scenario_metadata.get("key_drivers", []),
            recommended_response=scenario_metadata.get("recommended_response", ""),
            response_playbook=scenario_metadata.get("response_playbook", []),
            known_limitations=[
                "Deterministic backend model; no live social listening, OASIS run, or calibration loop was used.",
                "Outputs should be treated as scenario planning signals, not measured market facts.",
            ],
        )


# ── Pre-built Scenarios ──────────────────────────────────

PRICE_WAR_SCENARIO = {
    "name": "Price War — ราคาตัดราคา",
    "description": "คู่แข่งลดราคา 20% เราเลือกตอบโต้หรือไม่ตอบโต้",
    "metadata": {
        "affected_segments": ["Price-sensitive families", "Retail shoppers", "Value seekers", "Sales teams"],
        "amplification_channels": ["Facebook", "TikTok", "Retail media", "LINE"],
        "key_drivers": ["Discount depth", "Margin tolerance", "Retail visibility", "Competitor response timing"],
        "recommended_response": "Avoid a market-wide discount spiral; defend selected segments with guarded offers and proof of value.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Confirm price threat", "actions": ["Capture competitor offer details", "Map vulnerable SKUs/segments", "Set discount guardrails"]},
            {"stage": "first_24_hours", "title": "Defend high-value conversion", "actions": ["Launch selective offer tests", "Brief sales and retail partners", "Shift copy toward value proof"]},
            {"stage": "first_72_hours", "title": "Protect margin", "actions": ["Scale only profitable offers", "Monitor discount fatigue", "Prepare non-price differentiation assets"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 45, "price_position": 50, "brand_strength": 65, "market_share": 30, "description": "แบรนด์ของเรา — คุณภาพดี ราคากลาง"},
        {"name": "Competitor A", "base_sentiment": 35, "price_position": 55, "brand_strength": 70, "market_share": 35, "description": "คู่แข่งรายใหญ่ — แบรนด์แข็ง ราคาสูงกว่า"},
        {"name": "Competitor B", "base_sentiment": 25, "price_position": 25, "brand_strength": 40, "market_share": 20, "description": "คู่แข่งรายเล็ก — ตัดราคา ดัมพ์ตลาด"},
        {"name": "New Entrant", "base_sentiment": 50, "price_position": 30, "brand_strength": 35, "market_share": 15, "description": "แบรนด์ใหม่ — Viral หนัก ราคาถูก"},
    ],
    "events": [
        {"name": "Competitor B หั่นราคา 20%", "round": 3, "target_brand": "Competitor B", "type": "price_cut", "magnitude": 25, "description": "Competitor B ประกาศลดราคา 20% ทุกรายการ เริ่มสงครามราคา", "duration_rounds": 4},
    ],
}

INFLUENCER_BACKLASH_SCENARIO = {
    "name": "Influencer Backlash",
    "description": "A creator challenges a campaign claim and negative replies amplify across short-form feeds.",
    "metadata": {
        "affected_segments": ["Gen Z creators", "Trust-sensitive buyers", "High-intent social shoppers"],
        "amplification_channels": ["TikTok", "Instagram Reels", "X/Twitter", "Facebook groups"],
        "key_drivers": ["Claim credibility", "Creator authority", "Comment velocity", "Proof asset quality"],
        "recommended_response": "Move fast with proof-led creator repair, claim clarification, and social FAQ assets.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Freeze risky claims", "actions": ["Pause the disputed creative", "Approve a holding statement", "Identify the creator claim being challenged"]},
            {"stage": "first_24_hours", "title": "Publish proof and FAQ", "actions": ["Release substantiation assets", "Brief trusted creators", "Respond in the highest-velocity threads"]},
            {"stage": "first_72_hours", "title": "Rebuild trust loops", "actions": ["Shift spend to proof-led variants", "Retest claims with sensitive personas", "Track comment sentiment by channel"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 48, "price_position": 55, "brand_strength": 62, "market_share": 30, "description": "Campaign owner under claim scrutiny"},
        {"name": "Social Challenger", "base_sentiment": 34, "price_position": 45, "brand_strength": 56, "market_share": 28, "description": "Fast social rival"},
        {"name": "Legacy Brand", "base_sentiment": 38, "price_position": 58, "brand_strength": 72, "market_share": 27, "description": "Trusted incumbent"},
        {"name": "Creator Network", "base_sentiment": 28, "price_position": 35, "brand_strength": 42, "market_share": 15, "description": "Creator-led niche alternative"},
    ],
    "events": [
        {"name": "Influencer backlash", "round": 3, "target_brand": "Our Brand", "type": "scandal", "magnitude": 26, "description": "Creator challenges a campaign claim and negative comments accelerate.", "duration_rounds": 4},
        {"name": "Proof-led creator repair", "round": 7, "target_brand": "Our Brand", "type": "viral_campaign", "magnitude": 18, "description": "Trusted creators and FAQ assets reduce uncertainty.", "duration_rounds": 3},
    ],
}

PRODUCT_RECALL_SCENARIO = {
    "name": "Product Recall",
    "description": "A quality issue forces a recall decision while competitors target anxious customers.",
    "metadata": {
        "affected_segments": ["Existing customers", "Parents/families", "Retail partners", "Safety-sensitive buyers"],
        "amplification_channels": ["Facebook groups", "LINE communities", "News sites", "TikTok"],
        "key_drivers": ["Recall speed", "Refund clarity", "Safety proof", "Retail partner communication"],
        "recommended_response": "Lead with safety, clear replacement/refund rules, and partner scripts before paid defense.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Activate safety command", "actions": ["Confirm affected batches", "Publish holding statement", "Stop disputed inventory movement"]},
            {"stage": "first_24_hours", "title": "Make customers whole", "actions": ["Announce refund/replacement path", "Brief call center and retailers", "Create batch-check landing page"]},
            {"stage": "first_72_hours", "title": "Recover confidence", "actions": ["Publish independent QA evidence", "Retarget unaffected customers carefully", "Monitor repeat complaint clusters"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 42, "price_position": 52, "brand_strength": 66, "market_share": 34, "description": "Brand facing quality incident"},
        {"name": "Trusted Incumbent", "base_sentiment": 46, "price_position": 62, "brand_strength": 78, "market_share": 32, "description": "Safety-positioned competitor"},
        {"name": "Value Rival", "base_sentiment": 24, "price_position": 28, "brand_strength": 42, "market_share": 19, "description": "Price-led challenger"},
        {"name": "Retail Private Label", "base_sentiment": 30, "price_position": 35, "brand_strength": 38, "market_share": 15, "description": "Store-backed substitute"},
    ],
    "events": [
        {"name": "Recall report", "round": 2, "target_brand": "Our Brand", "type": "scandal", "magnitude": 34, "description": "Product quality issue triggers recall questions.", "duration_rounds": 5},
        {"name": "Safety recovery plan", "round": 7, "target_brand": "Our Brand", "type": "viral_campaign", "magnitude": 16, "description": "Refund, replacement, and QA proof begin rebuilding confidence.", "duration_rounds": 3},
    ],
}

REGULATORY_ISSUE_SCENARIO = {
    "name": "Regulatory Issue",
    "description": "A regulator questions campaign claims and the market waits for clarification.",
    "metadata": {
        "affected_segments": ["Compliance-sensitive buyers", "Enterprise customers", "Investors", "Trade media"],
        "amplification_channels": ["News sites", "LinkedIn", "X/Twitter", "Industry forums"],
        "key_drivers": ["Claim discipline", "Regulator response timing", "Legal review", "Executive credibility"],
        "recommended_response": "Narrow the claim, publish compliance posture, and separate factual clarification from promotion.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Legal hold and fact check", "actions": ["Pause claim-heavy ads", "Collect substantiation", "Align legal, PR, and sales scripts"]},
            {"stage": "first_24_hours", "title": "Clarify without overpromising", "actions": ["Publish factual clarification", "Brief enterprise accounts", "Prepare regulator response pack"]},
            {"stage": "first_72_hours", "title": "Restore operating rhythm", "actions": ["Relaunch compliant creative", "Track trade-media narrative", "Run claim-sensitivity retest"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 44, "price_position": 60, "brand_strength": 68, "market_share": 33, "description": "Premium brand under claim review"},
        {"name": "Compliant Incumbent", "base_sentiment": 42, "price_position": 58, "brand_strength": 74, "market_share": 34, "description": "Conservative category leader"},
        {"name": "Fast Challenger", "base_sentiment": 31, "price_position": 44, "brand_strength": 48, "market_share": 20, "description": "Aggressive marketer"},
        {"name": "Niche Expert", "base_sentiment": 36, "price_position": 66, "brand_strength": 40, "market_share": 13, "description": "Specialist brand"},
    ],
    "events": [
        {"name": "Regulator claim review", "round": 3, "target_brand": "Our Brand", "type": "scandal", "magnitude": 25, "description": "Regulatory attention creates uncertainty around campaign claims.", "duration_rounds": 4},
        {"name": "Compliant relaunch", "round": 8, "target_brand": "Our Brand", "type": "product_launch", "magnitude": 12, "description": "Claim-safe creative and proof pack stabilize the narrative.", "duration_rounds": 2},
    ],
}

ESG_CONTROVERSY_SCENARIO = {
    "name": "ESG Controversy",
    "description": "Sustainability or labor allegations threaten brand trust and investor/customer confidence.",
    "metadata": {
        "affected_segments": ["Purpose-led buyers", "Urban professionals", "Employees", "Investors"],
        "amplification_channels": ["X/Twitter", "LinkedIn", "News sites", "Facebook groups"],
        "key_drivers": ["Transparency", "Third-party evidence", "Executive response", "Employee advocacy"],
        "recommended_response": "Acknowledge concerns, publish verifiable actions, and avoid defensive greenwashing language.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Acknowledge and verify", "actions": ["Open internal fact-finding", "Prepare non-defensive holding statement", "Map stakeholder questions"]},
            {"stage": "first_24_hours", "title": "Show evidence path", "actions": ["Publish available data", "Invite third-party review", "Equip employee and partner spokespeople"]},
            {"stage": "first_72_hours", "title": "Commit to measurable fixes", "actions": ["Announce corrective milestones", "Track activist/community response", "Move spend away from image-only ESG claims"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 47, "price_position": 62, "brand_strength": 70, "market_share": 36, "description": "Brand with ESG positioning"},
        {"name": "Ethical Challenger", "base_sentiment": 43, "price_position": 65, "brand_strength": 52, "market_share": 22, "description": "Purpose-led rival"},
        {"name": "Mass Competitor", "base_sentiment": 32, "price_position": 42, "brand_strength": 68, "market_share": 30, "description": "Large mainstream competitor"},
        {"name": "Budget Substitute", "base_sentiment": 18, "price_position": 25, "brand_strength": 34, "market_share": 12, "description": "Low-price substitute"},
    ],
    "events": [
        {"name": "ESG allegation", "round": 3, "target_brand": "Our Brand", "type": "scandal", "magnitude": 30, "description": "Sustainability allegation spreads through activist and investor channels.", "duration_rounds": 5},
        {"name": "Third-party audit commitment", "round": 8, "target_brand": "Our Brand", "type": "viral_campaign", "magnitude": 14, "description": "Transparent action plan reduces some uncertainty.", "duration_rounds": 3},
    ],
}

FAKE_NEWS_SCENARIO = {
    "name": "Fake News / Rumor Amplification",
    "description": "A false rumor spreads faster than official clarification across social and community channels.",
    "metadata": {
        "affected_segments": ["Low-trust audiences", "Community group members", "Older buyers", "Price-sensitive families"],
        "amplification_channels": ["LINE", "Facebook groups", "TikTok", "X/Twitter"],
        "key_drivers": ["Correction speed", "Trusted messengers", "Community admin cooperation", "Search visibility"],
        "recommended_response": "Use rapid myth-busting, trusted local messengers, and search/social content that answers the rumor directly.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Classify rumor and source", "actions": ["Capture the false claim", "Identify top spreading channels", "Approve factual correction"]},
            {"stage": "first_24_hours", "title": "Push correction through trusted nodes", "actions": ["Brief community admins", "Publish searchable FAQ", "Equip frontline sales/support teams"]},
            {"stage": "first_72_hours", "title": "Suppress repeat spread", "actions": ["Run correction retargeting", "Monitor mutated rumor variants", "Document evidence for platform escalation"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 41, "price_position": 50, "brand_strength": 60, "market_share": 31, "description": "Brand targeted by rumor"},
        {"name": "Opportunist Rival", "base_sentiment": 30, "price_position": 42, "brand_strength": 48, "market_share": 25, "description": "Rival benefiting from uncertainty"},
        {"name": "Trusted Leader", "base_sentiment": 46, "price_position": 58, "brand_strength": 78, "market_share": 32, "description": "High-trust incumbent"},
        {"name": "Low-price Alternative", "base_sentiment": 22, "price_position": 24, "brand_strength": 32, "market_share": 12, "description": "Substitute for anxious buyers"},
    ],
    "events": [
        {"name": "Rumor spike", "round": 2, "target_brand": "Our Brand", "type": "scandal", "magnitude": 28, "description": "False claim spreads through community channels.", "duration_rounds": 4},
        {"name": "Trusted correction", "round": 6, "target_brand": "Our Brand", "type": "viral_campaign", "magnitude": 17, "description": "Trusted messengers and FAQ content reduce rumor persistence.", "duration_rounds": 3},
    ],
}

COMPETITOR_LAUNCH_SCENARIO = {
    "name": "Competitor Launch",
    "description": "A rival launches a new product with heavy media support and channel incentives.",
    "metadata": {
        "affected_segments": ["Switchable buyers", "Category explorers", "Retail shoppers", "Creators/affiliates"],
        "amplification_channels": ["TikTok", "YouTube", "Retail media", "Instagram"],
        "key_drivers": ["Novelty advantage", "Retail visibility", "Creator proof", "Offer competitiveness"],
        "recommended_response": "Defend the highest-value segment with differentiated proof, retention offers, and rapid message retest.",
        "response_playbook": [
            {"stage": "first_2_hours", "title": "Map the rival offer", "actions": ["Capture claims, price, and channels", "Identify vulnerable segments", "Brief sales and community teams"]},
            {"stage": "first_24_hours", "title": "Defend core customers", "actions": ["Launch retention proof assets", "Move spend to high-intent audiences", "Prepare selective offer guardrails"]},
            {"stage": "first_72_hours", "title": "Counter-position", "actions": ["Retest comparative message", "Scale winning channel pairs", "Monitor competitor fatigue and stock/channel issues"]},
        ],
    },
    "brands": [
        {"name": "Our Brand", "base_sentiment": 43, "price_position": 54, "brand_strength": 66, "market_share": 35, "description": "Incumbent defending share"},
        {"name": "Launch Rival", "base_sentiment": 40, "price_position": 48, "brand_strength": 64, "market_share": 24, "description": "Rival launching aggressively"},
        {"name": "Category Leader", "base_sentiment": 49, "price_position": 62, "brand_strength": 82, "market_share": 29, "description": "Large incumbent"},
        {"name": "Niche Challenger", "base_sentiment": 28, "price_position": 38, "brand_strength": 38, "market_share": 12, "description": "Small specialist"},
    ],
    "events": [
        {"name": "Rival product launch", "round": 2, "target_brand": "Launch Rival", "type": "product_launch", "magnitude": 26, "description": "Competitor launches with creator proof and channel incentives.", "duration_rounds": 4},
        {"name": "Our differentiated response", "round": 6, "target_brand": "Our Brand", "type": "viral_campaign", "magnitude": 16, "description": "Proof-led retention and comparative messaging defend core segments.", "duration_rounds": 3},
    ],
}

FIRST_MOVER_SCENARIO = {
    "name": "First Mover Advantage",
    "description": "เราเปิดตัวผลิตภัณฑ์ใหม่ก่อนคู่แข่ง — ดูว่าจะครองตลาดได้นานแค่ไหน",
    "brands": [
        {"name": "Our Brand", "base_sentiment": 40, "price_position": 55, "brand_strength": 60, "market_share": 25, "description": "แบรนด์เรา — First Mover เปิดตัวก่อน"},
        {"name": "Competitor X", "base_sentiment": 45, "price_position": 50, "brand_strength": 80, "market_share": 40, "description": "เจ้าตลาด — แข็งแกร่ง มีฐานลูกค้าใหญ่"},
        {"name": "Competitor Y", "base_sentiment": 30, "price_position": 40, "brand_strength": 50, "market_share": 20, "description": "ผู้ตาม — รอ copy เรา"},
        {"name": "Competitor Z", "base_sentiment": 20, "price_position": 30, "brand_strength": 30, "market_share": 15, "description": "Small player — ตลาดล่าง"},
    ],
    "events": [
        {"name": "เราออกผลิตภัณฑ์ใหม่", "round": 2, "target_brand": "Our Brand", "type": "product_launch", "magnitude": 25, "description": "เราเปิดตัวนวัตกรรมใหม่ ตลาดตื่นเต้น", "duration_rounds": 3},
        {"name": "Competitor Y ตอบโต้", "round": 6, "target_brand": "Competitor Y", "type": "product_launch", "magnitude": 20, "description": "Competitor Y ออกสินค้าลอกเรา — ตัดราคา 10%", "duration_rounds": 2},
    ],
}

SCANDAL_SCENARIO = {
    "name": "Crisis — Scandal คู่แข่ง",
    "description": "คู่แข่งรายใหญ่เกิด scandal — เราจะได้ส่วนแบ่งตลาดเท่าไหร่",
    "brands": [
        {"name": "Our Brand", "base_sentiment": 35, "price_position": 50, "brand_strength": 55, "market_share": 22, "description": "แบรนด์เรา — รอโอกาส"},
        {"name": "Big Competitor", "base_sentiment": 55, "price_position": 60, "brand_strength": 85, "market_share": 45, "description": "เจ้าตลาด — แต่กำลังเจอ scandal"},
        {"name": "Mid Competitor", "base_sentiment": 30, "price_position": 45, "brand_strength": 50, "market_share": 20, "description": "คู่แข่งกลาง — จะแย่ง share ด้วย"},
        {"name": "Budget Brand", "base_sentiment": 15, "price_position": 20, "brand_strength": 25, "market_share": 13, "description": "ตลาดล่าง — ได้ประโยชน์จาก scandal"},
    ],
    "events": [
        {"name": "Big Competitor scandal", "round": 3, "target_brand": "Big Competitor", "type": "scandal", "magnitude": 35, "description": "สื่อแฉ — Big Competitor ใช้แรงงานเด็กใน supply chain ข่าวไวรัลทั่วโลก #Boycott", "duration_rounds": 5},
    ],
}


def _with_metadata(scenario: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    merged = {**scenario}
    merged["metadata"] = {**metadata, **scenario.get("metadata", {})}
    return merged


_FIRST_MOVER_METADATA = {
    "affected_segments": ["Early adopters", "Category explorers", "Retail partners", "Creators"],
    "amplification_channels": ["TikTok", "YouTube", "Instagram", "Retail media"],
    "key_drivers": ["Launch speed", "Copycat timing", "Proof of novelty", "Channel availability"],
    "recommended_response": "Use the launch window to lock proof, creators, and retail visibility before copycats compress the advantage.",
    "response_playbook": [
        {"stage": "first_2_hours", "title": "Lock launch narrative", "actions": ["Confirm primary claim", "Brief creators", "Prepare competitor monitoring"]},
        {"stage": "first_24_hours", "title": "Scale proof fast", "actions": ["Move spend to high-intent channels", "Publish early testimonials", "Track copycat signals"]},
        {"stage": "first_72_hours", "title": "Defend novelty", "actions": ["Refresh comparative assets", "Protect retail placement", "Retest offer against switchable buyers"]},
    ],
}

_SCANDAL_METADATA = {
    "affected_segments": ["Trust-sensitive buyers", "Media followers", "Employees", "Retail partners"],
    "amplification_channels": ["News sites", "X/Twitter", "Facebook groups", "LinkedIn"],
    "key_drivers": ["Competitor response speed", "Evidence quality", "Boycott momentum", "Our opportunism risk"],
    "recommended_response": "Win share without appearing exploitative; emphasize reliability, customer proof, and category stability.",
    "response_playbook": [
        {"stage": "first_2_hours", "title": "Assess spillover risk", "actions": ["Monitor category sentiment", "Avoid gloating language", "Prepare customer reassurance"]},
        {"stage": "first_24_hours", "title": "Reassure and convert", "actions": ["Publish reliability proof", "Brief sales teams", "Target switchable segments carefully"]},
        {"stage": "first_72_hours", "title": "Hold trust advantage", "actions": ["Scale respectful comparison", "Track backlash against opportunism", "Prepare response if category trust falls"]},
    ],
}


SCENARIO_LIBRARY = {
    "price_war": PRICE_WAR_SCENARIO,
    "influencer_backlash": INFLUENCER_BACKLASH_SCENARIO,
    "creator_backlash": INFLUENCER_BACKLASH_SCENARIO,
    "product_recall": PRODUCT_RECALL_SCENARIO,
    "regulatory_issue": REGULATORY_ISSUE_SCENARIO,
    "esg_controversy": ESG_CONTROVERSY_SCENARIO,
    "fake_news": FAKE_NEWS_SCENARIO,
    "rumor_amplification": FAKE_NEWS_SCENARIO,
    "competitor_launch": COMPETITOR_LAUNCH_SCENARIO,
    "first_mover": _with_metadata(FIRST_MOVER_SCENARIO, _FIRST_MOVER_METADATA),
    "scandal": _with_metadata(SCANDAL_SCENARIO, _SCANDAL_METADATA),
}
