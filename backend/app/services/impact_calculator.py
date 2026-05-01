"""Business Impact Calculator — converts simulation KPIs to revenue projections.

Core formula:
  Effective Conversion = base_conversion × (1 + sentiment/200)
  Revenue = TAM × market_share × conversion × unit_price × message_resonance_factor
  Estimated Revenue Uplift = Revenue(optimized) - Revenue(baseline)
  ROI = (Revenue_uplift - campaign_cost) / campaign_cost × 100%
  Crisis Loss Potential = Revenue × (crisis_risk/100) × severity
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger("mirofish.impact_calculator")


# ── Models ────────────────────────────────────────────────

class BusinessParams(BaseModel):
    """Business inputs for revenue projection."""
    product_name: str = "Product"
    unit_price: float = 100.0              # THB per unit
    market_size: int = 100000               # Total Addressable Market (units)
    current_market_share: float = 10.0      # % — your current share
    base_conversion_rate: float = 5.0       # % — normal conversion without campaign
    campaign_cost: float = 500000.0         # THB — total campaign spend
    time_horizon_months: int = 6            # projection period


class ScenarioResult(BaseModel):
    """Single scenario projection."""
    scenario: str                           # "base" | "optimistic" | "pessimistic"
    sentiment: float
    conversion_rate: float
    estimated_units: int
    estimated_revenue: float
    revenue_uplift: float                   # vs baseline
    roi_pct: float


class ImpactResult(BaseModel):
    """Full business impact projection for one campaign."""
    campaign_id: str
    campaign_name: str
    product_name: str
    unit_price: float
    market_size: int
    scenarios: List[ScenarioResult]
    best_scenario: str                      # scenario name with best ROI
    projected_monthly_revenue: float
    projected_annual_revenue: float
    crisis_risk_potential_loss: float       # THB — worst case if crisis hits
    recommendation: str                     # ภาษาไทย — what to do


class ComparisonResult(BaseModel):
    """Side-by-side ROI comparison for multiple campaigns."""
    campaigns: List[ImpactResult]
    best_campaign_id: str
    best_campaign_name: str
    best_roi_pct: float
    total_potential_value: float            # Best campaign projected annual revenue


# ── Calculator ────────────────────────────────────────────

class ImpactCalculator:
    """Converts sentiment KPIs into business projections."""

    @staticmethod
    def calculate(campaign_id: str, campaign_name: str,
                  kpis: Dict[str, Any], params: BusinessParams) -> ImpactResult:
        """
        Given campaign KPIs and business parameters, produce a full impact projection.

        kpis dict expects:
            overall_sentiment, conversion_probability, crisis_risk,
            message_resonance, brand_perception_shift
        """
        sentiment = kpis.get("overall_sentiment", 0)
        crisis_risk = kpis.get("crisis_risk", 10)
        message_resonance = kpis.get("message_resonance", 50) / 100.0
        brand_shift = kpis.get("brand_perception_shift", 0)

        p = params  # shorthand

        # Scenarios
        scenarios = []
        for name, s_adj, mr_adj in [
            ("Base Case", 0, 1.0),
            ("Optimistic", +30, 1.15),
            ("Pessimistic", -30, 0.85),
        ]:
            effective_sentiment = sentiment + s_adj
            effective_conversion = p.base_conversion_rate * (1 + effective_sentiment / 200) * mr_adj
            effective_conversion = max(0.1, min(50, effective_conversion))

            share = p.current_market_share * (1 + brand_shift / 200)
            units = int(p.market_size * (share / 100) * (effective_conversion / 100))
            revenue = units * p.unit_price

            baseline_units = int(p.market_size * (p.current_market_share / 100) * (p.base_conversion_rate / 100))
            baseline_revenue = baseline_units * p.unit_price
            uplift = revenue - baseline_revenue
            roi = ((uplift - p.campaign_cost) / p.campaign_cost) * 100 if p.campaign_cost > 0 else 0

            scenarios.append(ScenarioResult(
                scenario=name,
                sentiment=round(effective_sentiment, 1),
                conversion_rate=round(effective_conversion, 2),
                estimated_units=units,
                estimated_revenue=round(revenue, 0),
                revenue_uplift=round(uplift, 0),
                roi_pct=round(roi, 1),
            ))

        # Best scenario
        best = max(scenarios, key=lambda s: s.roi_pct)

        # Crisis risk potential loss
        crisis_loss = scenarios[0].estimated_revenue * (crisis_risk / 100) * 0.5  # 50% severity

        # Projections
        monthly = best.estimated_units * p.unit_price / p.time_horizon_months
        annual = monthly * 12

        # Recommendation (Thai)
        if best.roi_pct > 50:
            rec = f"✅ ลงทุนต่อ — {best.scenario} ROI {best.roi_pct:.0f}% คาดการณ์รายได้ {best.estimated_revenue:,.0f} บาท ใน {p.time_horizon_months} เดือน"
        elif best.roi_pct > 0:
            rec = f"⚠️ กำไรบาง — {best.scenario} ROI {best.roi_pct:.0f}% คาดการณ์รายได้ {best.estimated_revenue:,.0f} บาท — ปรับ message เพื่อเพิ่ม conversion"
        else:
            rec = f"❌ ขาดทุน — ROI ติดลบ {best.roi_pct:.0f}% — เปลี่ยน strategy ก่อนลงทุนจริง"

        return ImpactResult(
            campaign_id=campaign_id,
            campaign_name=campaign_name,
            product_name=p.product_name,
            unit_price=p.unit_price,
            market_size=p.market_size,
            scenarios=[s.dict() for s in scenarios],
            best_scenario=best.scenario,
            projected_monthly_revenue=round(monthly, 0),
            projected_annual_revenue=round(annual, 0),
            crisis_risk_potential_loss=round(crisis_loss, 0),
            recommendation=rec,
        )

    @staticmethod
    def compare_impact(campaigns_data: List[Dict[str, Any]],
                       params: BusinessParams) -> ComparisonResult:
        """Compare business impact across multiple campaigns with same business params."""
        results = []
        for cdata in campaigns_data:
            result = ImpactCalculator.calculate(
                campaign_id=cdata["campaign_id"],
                campaign_name=cdata.get("campaign_name", cdata["campaign_id"][:12]),
                kpis=cdata.get("kpis", {}),
                params=params,
            )
            results.append(result)

        # Best by ROI
        best = max(results, key=lambda r: r.scenarios[1].roi_pct)  # optimistic scenario

        return ComparisonResult(
            campaigns=[r.dict() for r in results],
            best_campaign_id=best.campaign_id,
            best_campaign_name=best.campaign_name,
            best_roi_pct=best.scenarios[1].roi_pct,
            total_potential_value=best.projected_annual_revenue,
        )
