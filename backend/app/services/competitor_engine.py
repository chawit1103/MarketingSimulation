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


# ── Engine ────────────────────────────────────────────────

class CompetitorSimEngine:
    """Multi-brand market simulation with event injection."""

    @staticmethod
    def simulate(
        brands: List[BrandProfile],
        events: List[SimulationEvent] = None,
        rounds: int = 12,
        scenario_name: str = "Custom Scenario",
    ) -> SimulationResult:
        """Run a multi-round simulation with brand competition and events."""

        if not brands or len(brands) < 2:
            raise ValueError("Need at least 2 brands to simulate competition")

        events = events or []
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
        winner = max(share_shift, key=share_shift.get)

        return SimulationResult(
            scenario_name=scenario_name,
            rounds=rounds,
            brands=[b.name for b in brands],
            timeline=[t.dict() for t in timeline],
            final_market_share=final_shares,
            share_shift=share_shift,
            winner=winner,
            key_events=event_log,
        )


# ── Pre-built Scenarios ──────────────────────────────────

PRICE_WAR_SCENARIO = {
    "name": "Price War — ราคาตัดราคา",
    "description": "คู่แข่งลดราคา 20% เราเลือกตอบโต้หรือไม่ตอบโต้",
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
