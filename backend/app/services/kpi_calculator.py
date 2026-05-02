"""
KPI Calculator — Computes quantitative executive KPIs from simulation results.

Currently uses MOCK data while the simulation runner matures.
The `calculate()` method signature is designed so that when real simulation
data becomes available, only the internal computation logic needs updating.
"""
from typing import Dict, Any, List, Optional
import random

from ..models.report import (
    ExecutiveReport,
    SegmentSentiment,
    Influencer,
    TimelinePoint,
    ActionItem,
)
from ..utils.logger import get_logger

logger = get_logger("mirofish.services.kpi_calculator")


# ---------------------------------------------------------------------------
# Mock-data helpers — replace these when real simulation data is available
# ---------------------------------------------------------------------------

# Thai-centric segment names
_MOCK_SEGMENTS = [
    "กรุงเทพ Gen Z",
    "กรุงเทพ Millennials",
    "กรุงเทพ Gen X",
    "ภาคกลาง วัยทำงาน",
    "ภาคเหนือ นักศึกษา",
    "อีสาน แรงงาน",
    "ภาคใต้ ครอบครัว",
    "คนไทยในต่างประเทศ",
    "Expat ในกรุงเทพ",
    "ต่างจังหวัด ผู้สูงอายุ",
]

_MOCK_INFLUENCER_NAMES = [
    "Synthetic KOL A", "Synthetic Analyst B", "Synthetic Review Page C", "Synthetic Health Expert D",
    "Synthetic Food Creator E", "Synthetic Community Voice F", "Synthetic Merchant Page G", "Synthetic Elder Panel H",
]

_MOCK_INFLUENCER_TYPES = [
    "KOL", "academic", "blogger", "professional",
    "celebrity", "community_leader", "merchant", "elder",
]


def _clamp(value: float, low: float = -100.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _scale_to_hundred(raw: float, raw_min: float, raw_max: float) -> float:
    """Map a raw value from [raw_min, raw_max] to [0, 100]."""
    if raw_max == raw_min:
        return 50.0
    return _clamp(100.0 * (raw - raw_min) / (raw_max - raw_min), 0.0, 100.0)


# ---------------------------------------------------------------------------
# KPICalculator
# ---------------------------------------------------------------------------

class KPICalculator:
    """Compute executive KPIs from simulation results.

    Usage:
        calc = KPICalculator()
        report = calc.calculate(
            campaign_id="cmp_abc",
            simulation_data={...},       # dict from SimulationRunState
            graph_data={...},            # dict from graph tools summary
        )
    """

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def calculate(
        self,
        campaign_id: str,
        org_id: str = "default",
        simulation_data: Optional[Dict[str, Any]] = None,
        graph_data: Optional[Dict[str, Any]] = None,
        simulation_id: Optional[str] = None,
    ) -> ExecutiveReport:
        """Produce a full ExecutiveReport for the given campaign.

        When real simulation_data is provided, this method delegates to
        real-data computation paths.  Otherwise it falls back to plausible
        mock data suitable for demos and UI development.
        """
        report = ExecutiveReport.empty(campaign_id, org_id)
        report.simulation_id = simulation_id or (simulation_data or {}).get("simulation_id")
        report.run_id = (simulation_data or {}).get("run_id") or report.simulation_id or report.report_id

        # --- Determine whether we have real data ---
        use_real = self._has_real_kpi_data(simulation_data)

        if use_real:
            self._compute_from_real(report, simulation_data, graph_data)
            report.source_mode = "backend_verified"
            report.data_basis = "real_simulation"
            report.confidence = self._extract_confidence(simulation_data)
            report.limitations = list((simulation_data or {}).get("limitations") or [])
        else:
            self._compute_from_mock(report)
            report.source_mode = "local_estimate"
            report.data_basis = "local_estimate"
            report.confidence = None
            report.limitations = [
                "KPI values are local deterministic estimates because no persisted real simulation KPI output is available.",
                "Use this dashboard for planning direction only; validate with a real simulation or live audience test before spend decisions.",
            ]

        # --- Action plan (same pipeline for mock & real) ---
        self._generate_action_plan(report)

        return report

    # ------------------------------------------------------------------
    # Data-source detection
    # ------------------------------------------------------------------

    def _has_real_data(self, simulation_data: Optional[Dict[str, Any]]) -> bool:
        if not simulation_data:
            return False
        # Check for plausible simulation result structure
        rounds = simulation_data.get("rounds") or simulation_data.get("round_summaries")
        return bool(rounds and len(rounds) > 0)

    def _has_real_kpi_data(self, simulation_data: Optional[Dict[str, Any]]) -> bool:
        """Return True only when explicit KPI metrics are present.

        Raw runner rounds/actions prove that a backend run happened, but they do
        not yet contain sentiment/conversion KPI facts. Treating those as
        backend-verified would fabricate precision, so they remain local
        estimates until a real KPI schema is present.
        """
        if not simulation_data:
            return False
        metrics = simulation_data.get("kpis") or simulation_data.get("metrics") or simulation_data
        required = {"overall_sentiment", "conversion_probability", "crisis_risk"}
        return required.issubset(metrics.keys())

    def _extract_confidence(self, simulation_data: Optional[Dict[str, Any]]) -> Optional[float]:
        if not simulation_data:
            return None
        value = simulation_data.get("confidence") or simulation_data.get("confidence_score")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    # ------------------------------------------------------------------
    # Real-data computation (stub — complete when simulation runner matures)
    # ------------------------------------------------------------------

    def _compute_from_real(
        self,
        report: ExecutiveReport,
        simulation_data: Dict[str, Any],
        graph_data: Optional[Dict[str, Any]],
    ) -> None:
        """Compute KPIs from explicit persisted simulation KPI metrics."""
        metrics = simulation_data.get("kpis") or simulation_data.get("metrics") or simulation_data
        report.overall_sentiment = round(float(metrics.get("overall_sentiment", 0.0)), 1)
        report.conversion_probability = _clamp(float(metrics.get("conversion_probability", 0.0)), 0.0, 100.0)
        report.social_influence_index = _clamp(float(metrics.get("social_influence_index", metrics.get("social_influence", 0.0))), 0.0, 100.0)
        report.message_resonance = _clamp(float(metrics.get("message_resonance", 0.0)), 0.0, 100.0)
        report.crisis_risk = _clamp(float(metrics.get("crisis_risk", 0.0)), 0.0, 100.0)
        report.brand_perception_shift = _clamp(float(metrics.get("brand_perception_shift", 0.0)))
        report.opinion_polarization = _clamp(float(metrics.get("opinion_polarization", 0.0)), 0.0, 100.0)

        report.sentiment_by_segment = [
            SegmentSentiment(
                segment_name=str(row.get("segment_name") or row.get("name") or "Segment"),
                persona_count=int(row.get("persona_count") or row.get("size") or 0),
                avg_sentiment=float(row.get("avg_sentiment", row.get("sentiment", 0.0))),
                conversion_estimate=float(row.get("conversion_estimate", row.get("conversion", 0.0))),
            )
            for row in simulation_data.get("segments", [])
            if isinstance(row, dict)
        ]
        report.top_influencers = [
            Influencer(
                agent_name=str(row.get("agent_name") or row.get("name") or "Influencer"),
                agent_type=str(row.get("agent_type") or row.get("type") or "persona"),
                influence_score=float(row.get("influence_score", 0.0)),
                sentiment_impact=float(row.get("sentiment_impact", 0.0)),
            )
            for row in simulation_data.get("influencers", [])
            if isinstance(row, dict)
        ]
        report.sentiment_timeline = [
            TimelinePoint(
                round_num=int(row.get("round_num") or row.get("round") or idx + 1),
                simulated_hour=int(row.get("simulated_hour") or row.get("hour") or idx + 1),
                avg_sentiment=float(row.get("avg_sentiment", row.get("sentiment", report.overall_sentiment))),
                action_count=int(row.get("action_count") or row.get("total_actions") or 0),
            )
            for idx, row in enumerate(simulation_data.get("timeline", []))
            if isinstance(row, dict)
        ]

        if not report.sentiment_by_segment:
            report.sentiment_by_segment = [SegmentSentiment(segment_name="All personas", avg_sentiment=report.overall_sentiment)]
        if not report.sentiment_timeline:
            report.sentiment_timeline = [TimelinePoint(round_num=1, simulated_hour=1, avg_sentiment=report.overall_sentiment)]

    # ------------------------------------------------------------------
    # Mock-data computation
    # ------------------------------------------------------------------

    def _compute_from_mock(self, report: ExecutiveReport) -> None:
        """Populate report with plausible mock KPIs."""
        rng = random.Random(f"{report.org_id}:{report.campaign_id}:local_estimate")

        # Overall sentiment: mild positive
        overall = round(rng.uniform(15.0, 45.0), 1)
        report.overall_sentiment = overall

        # Conversion probability: correlated with positive sentiment
        report.conversion_probability = round(
            _scale_to_hundred(overall, -50.0, 80.0) * rng.uniform(0.8, 1.1), 1
        )
        report.conversion_probability = _clamp(report.conversion_probability, 0.0, 100.0)

        # Social influence index
        report.social_influence_index = round(rng.uniform(40.0, 75.0), 1)

        # Message resonance
        report.message_resonance = round(rng.uniform(30.0, 70.0), 1)

        # Crisis risk
        report.crisis_risk = round(rng.uniform(5.0, 35.0), 1)

        # Brand perception shift
        shift = round(rng.uniform(-10.0, 25.0), 1)
        report.brand_perception_shift = shift

        # Opinion polarization
        report.opinion_polarization = round(rng.uniform(15.0, 55.0), 1)

        # Segment breakdown
        report.sentiment_by_segment = self._mock_segments(overall, rng)

        # Modeled influence nodes
        report.top_influencers = self._mock_influencers(overall, rng)

        # Timeline (20 rounds, ~1 simulated hour each)
        report.sentiment_timeline = self._mock_timeline(rounds=20, rng=rng)

    # ------------------------------------------------------------------
    # Mock helpers
    # ------------------------------------------------------------------

    def _mock_segments(self, base_sentiment: float, rng: random.Random) -> List[SegmentSentiment]:
        segments: List[SegmentSentiment] = []
        for name in _MOCK_SEGMENTS:
            deviation = rng.uniform(-25.0, 25.0)
            avg = _clamp(base_sentiment + deviation)
            se = SegmentSentiment(
                segment_name=name,
                persona_count=rng.randint(40, 200),
                avg_sentiment=round(avg, 1),
                conversion_estimate=round(_scale_to_hundred(avg, -50.0, 80.0), 1),
            )
            segments.append(se)
        return segments

    def _mock_influencers(self, base_sentiment: float, rng: random.Random) -> List[Influencer]:
        infs: List[Influencer] = []
        # Pick 5 random names
        indices = rng.sample(range(len(_MOCK_INFLUENCER_NAMES)), min(5, len(_MOCK_INFLUENCER_NAMES)))
        for i in indices:
            inf_score = round(rng.uniform(50.0, 95.0), 1)
            impact = round(rng.uniform(-15.0, 30.0), 1)
            infs.append(Influencer(
                agent_name=_MOCK_INFLUENCER_NAMES[i],
                agent_type=_MOCK_INFLUENCER_TYPES[i],
                influence_score=inf_score,
                sentiment_impact=impact,
            ))
        # Sort by influence_score desc
        infs.sort(key=lambda x: x.influence_score, reverse=True)
        return infs

    def _mock_timeline(self, rounds: int = 20, rng: Optional[random.Random] = None) -> List[TimelinePoint]:
        rng = rng or random.Random()
        points: List[TimelinePoint] = []
        sentiment = 0.0
        for r in range(1, rounds + 1):
            # Sentiment evolves with small random walk
            delta = rng.uniform(-5.0, 6.5)  # slight upward bias
            sentiment = _clamp(sentiment + delta)
            points.append(TimelinePoint(
                round_num=r,
                simulated_hour=r,
                avg_sentiment=round(sentiment, 1),
                action_count=rng.randint(5, 40),
            ))
        return points

    # ------------------------------------------------------------------
    # Action plan generation (Think → Finish)
    # ------------------------------------------------------------------

    def _generate_action_plan(self, report: ExecutiveReport) -> None:
        """Generate executive action plan based on computed KPIs.

        In production this would use an LLM call; for now we use
        rule-based templates derived from the KPI values.
        """
        # Winning strategy
        if report.overall_sentiment > 30:
            report.winning_strategy = (
                "แคมเปญได้รับเสียงตอบรับเชิงบวกในวงกว้าง "
                "ควรรักษาทิศทางเนื้อหาและเพิ่มความถี่การเผยแพร่ "
                "โดยเฉพาะในกลุ่ม {top_segment}"
            ).format(
                top_segment=self._best_segment_name(report.sentiment_by_segment)
            )
        elif report.overall_sentiment > 0:
            report.winning_strategy = (
                "แคมเปญมีแนวโน้มบวกแต่ยังไม่แข็งแกร่งพอ "
                "ควรปรับข้อความให้โดนใจกลุ่มเป้าหมายมากขึ้น "
                "และใช้ Influencer ช่วยขยายผล"
            )
        else:
            report.winning_strategy = (
                "แคมเปญยังไม่บรรลุเป้าหมาย — "
                "แนะนำให้ปรับมุมสื่อสารใหม่และทดสอบ A/B ก่อนเปิดตัวจริง"
            )

        # Risk areas
        report.risk_areas = []
        if report.crisis_risk > 25:
            report.risk_areas.append("ความเสี่ยงวิกฤตสื่อสูง — ควรเตรียมแผนรับมือ Crisis Communication")
        if report.opinion_polarization > 40:
            report.risk_areas.append("ความคิดเห็นแบ่งขั้วสูง — อาจเกิดดราม่าในโลกโซเชียล")
        for seg in report.sentiment_by_segment:
            if seg.avg_sentiment < -10:
                report.risk_areas.append(
                    f"กลุ่ม {seg.segment_name} มี Sentiment ติดลบ ({seg.avg_sentiment:.0f}) — ควรทำความเข้าใจสาเหตุ"
                )
        if not report.risk_areas:
            report.risk_areas.append("ไม่พบจุดเสี่ยงสำคัญ — ดำเนินการตามแผนได้")

        # Action items
        report.action_items = [
            ActionItem(
                priority="high",
                action="ปรับข้อความแคมเปญสำหรับกลุ่มที่มี Sentiment ติดลบ",
                expected_impact="เพิ่ม Sentiment โดยรวม +10-15 จุด",
                timeline="1 สัปดาห์",
            ),
            ActionItem(
                priority="high" if report.crisis_risk > 25 else "medium",
                action="เตรียม Crisis Playbook สำหรับ Worst-Case Scenario",
                expected_impact="ลดความเสียหายได้ 50% หากเกิดวิกฤต",
                timeline="ทันที",
            ),
            ActionItem(
                priority="medium",
                action="ทำสัญญา Micro-Influencer ในกลุ่มเป้าหมายหลัก",
                expected_impact="เพิ่ม Social Influence Index +20 จุด",
                timeline="1 เดือน",
            ),
            ActionItem(
                priority="medium",
                action="รัน A/B Test กับข้อความ 3 เวอร์ชันกับกลุ่มตัวอย่าง 500 คน",
                expected_impact="ระบุข้อความที่มี Message Resonance สูงสุด",
                timeline="2 สัปดาห์",
            ),
            ActionItem(
                priority="low" if report.opinion_polarization < 40 else "high",
                action="จัดเวทีเสวนาออนไลน์เพื่อลดความเห็นต่าง",
                expected_impact="ลด Opinion Polarization ลง 15-20 จุด",
                timeline="1 เดือน",
            ),
        ]

        # Executive summary (Thai)
        sentiment_word = "เชิงบวก" if report.overall_sentiment > 15 else ("เป็นกลาง" if report.overall_sentiment > -10 else "เชิงลบ")
        report.executive_summary = (
            f"ภาพรวมแคมเปญมีแนวโน้ม{sentiment_word} "
            f"(Overall Sentiment {report.overall_sentiment:+.1f}) "
            f"โดยมี Conversion Probability ประมาณ {report.conversion_probability:.1f}% "
            f"Social Influence Index อยู่ที่ {report.social_influence_index:.1f}/100 "
            f"และ Crisis Risk {report.crisis_risk:.1f}% "
            f"กลุ่มที่ตอบรับดีที่สุดคือ {self._best_segment_name(report.sentiment_by_segment)} "
            f"ส่วนกลุ่มที่ควรเฝ้าระวังคือ {self._worst_segment_name(report.sentiment_by_segment)}"
        )

    # ------------------------------------------------------------------
    # Small helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _best_segment_name(segments: List[SegmentSentiment]) -> str:
        if not segments:
            return "N/A"
        return max(segments, key=lambda s: s.avg_sentiment).segment_name

    @staticmethod
    def _worst_segment_name(segments: List[SegmentSentiment]) -> str:
        if not segments:
            return "N/A"
        return min(segments, key=lambda s: s.avg_sentiment).segment_name
