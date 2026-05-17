"""Public demo API for no-key product trials.

These endpoints return deterministic sample campaign data so a first-time user
can experience the value loop without configuring an LLM or creating an org.
"""

from flask import Blueprint, jsonify

from ..services.action_plan import ActionPlanService


demo_bp = Blueprint("demo", __name__)


DEMO_CAMPAIGNS = [
    {
        "id": "demo-premium-water",
        "name": "Premium Water Launch TH",
        "description": "ทดสอบแคมเปญน้ำดื่มพรีเมียมสำหรับคนเมือง ครอบครัว และกลุ่มสุขภาพ ก่อนใช้งบ media จริง",
        "objective": "product_launch",
        "status": "completed",
        "target": {
            "segment_name": "Thai Urban Health & Family Buyers",
            "age_range": [22, 55],
            "regions": ["Bangkok", "Central", "Chiang Mai"],
            "persona_count": 500,
            "channels": ["facebook", "instagram", "tiktok", "line", "twitter_x"],
        },
        "sim_config": {
            "platform": "both",
            "platform_mode": "creator_feed",
            "max_rounds": 12,
            "audience_channels": ["facebook", "instagram", "tiktok", "line", "twitter_x"],
        },
    },
    {
        "id": "demo-insurtech-trust",
        "name": "InsurTech Trust Recovery",
        "description": "จำลองข้อความกู้ความเชื่อมั่นหลังเคลมล่าช้า สำหรับประกันสุขภาพและ EV insurance",
        "objective": "crisis_simulation",
        "status": "completed",
        "target": {
            "segment_name": "Policyholders, EV Owners, Family Decision Makers",
            "age_range": [28, 60],
            "regions": ["Bangkok", "Eastern", "Northeast"],
            "persona_count": 420,
            "channels": ["facebook", "line", "twitter_x", "youtube"],
        },
        "sim_config": {
            "platform": "twitter",
            "platform_mode": "microblog",
            "max_rounds": 10,
            "audience_channels": ["facebook", "line", "twitter_x", "youtube"],
        },
    },
    {
        "id": "demo-energy-community",
        "name": "Community Energy Brief",
        "description": "เปรียบเทียบ narrative โรงไฟฟ้าและพลังงานสะอาดกับชุมชนท้องถิ่น สื่อ และนักลงทุน",
        "objective": "brand_perception",
        "status": "completed",
        "target": {
            "segment_name": "Local Community, Policy Watchers, Investors",
            "age_range": [25, 68],
            "regions": ["Eastern", "Central", "Bangkok"],
            "persona_count": 360,
            "channels": ["facebook", "line", "youtube", "reddit"],
        },
        "sim_config": {
            "platform": "reddit",
            "platform_mode": "community_forum",
            "max_rounds": 14,
            "audience_channels": ["facebook", "line", "youtube", "reddit"],
        },
    },
]


DEMO_DASHBOARDS = {
    "demo-premium-water": {
        "kpis": {
            "overall_sentiment": 41,
            "conversion_probability": 68,
            "social_influence": 76,
            "message_resonance": 73,
            "crisis_risk": "medium",
            "brand_perception_shift": 18,
            "opinion_polarization": 39,
            "confidence_score": 82,
        },
        "timeline": [
            {"round_num": 1, "sentiment": 8, "posts_count": 42},
            {"round_num": 2, "sentiment": 19, "posts_count": 57},
            {"round_num": 3, "sentiment": 31, "posts_count": 64},
            {"round_num": 4, "sentiment": 22, "posts_count": 71},
            {"round_num": 5, "sentiment": 38, "posts_count": 83},
            {"round_num": 6, "sentiment": 41, "posts_count": 91},
        ],
        "segments": [
            {"name": "Urban Health Buyers", "sentiment": 63, "conversion_estimate": 84, "size": "24%"},
            {"name": "Family Value Seekers", "sentiment": 37, "conversion_estimate": 61, "size": "31%"},
            {"name": "Price-Sensitive Mass", "sentiment": -12, "conversion_estimate": 28, "size": "27%"},
            {"name": "Eco Skeptics", "sentiment": -31, "conversion_estimate": 18, "size": "11%"},
            {"name": "Creator-led Gen Z", "sentiment": 58, "conversion_estimate": 79, "size": "7%"},
        ],
        "influencers": [
            {"name": "Synthetic Health Creator A", "platform": "TikTok", "impact_score": 91, "sentiment": 64, "reach": 310000},
            {"name": "Synthetic Family Reviewer B", "platform": "Facebook", "impact_score": 84, "sentiment": 42, "reach": 225000},
            {"name": "Synthetic Price Watch C", "platform": "X", "impact_score": 79, "sentiment": -28, "reach": 188000},
            {"name": "Synthetic Green Living Club D", "platform": "LINE", "impact_score": 72, "sentiment": 51, "reach": 96000},
        ],
        "evidence": {
            "confidence_score": 82,
            "recommended_validation_step": "Run a small proof-led creative test with family and health-buyer segments before national media spend.",
            "limitations": [
                "Premium water dashboard is a synthetic demo fixture, not measured market evidence.",
                "Media costs, retailer availability, and competitor promotions are not included.",
            ],
            "assumptions": [
                "จำลองด้วย persona 500 คน กระจายตามเมืองใหญ่ ครอบครัว และกลุ่มสุขภาพ",
                "ใช้ channel mix แบบ FB/IG/TikTok/LINE/X ตามพฤติกรรม media ไทย",
                "ยังไม่รวม media cost จริงหรือ competitor promotion เฉพาะพื้นที่",
            ],
            "why_this_score": [
                "Conversion 68% มาจาก Urban Health Buyers และ Creator-led Gen Z ที่ตอบรับ strong purity + lifestyle framing",
                "Crisis risk ปานกลางเพราะ 27% ของ Price-Sensitive Mass โต้กลับเรื่องราคาพรีเมียม",
                "Message resonance สูงเมื่อข้อความเชื่อม mineral benefit กับ daily routine มากกว่าคำว่า premium อย่างเดียว",
            ],
            "risk_drivers": [
                "ราคาแพงกว่าน้ำดื่มทั่วไปโดยไม่มี proof point ที่จับต้องได้",
                "คำว่า eco-friendly ถูกถามกลับเรื่อง packaging และแหล่งน้ำ",
                "หาก influencer ใช้ภาษาหรูเกินไป กลุ่มครอบครัวจะรู้สึกไม่เกี่ยวกับตัวเอง",
            ],
            "quotes": [
                "ถ้าราคาเพิ่มแต่มีผลตรวจแร่ธาตุชัด ๆ ก็ยอมลองนะ โดยเฉพาะสำหรับลูก",
                "คำว่า premium เฉย ๆ ยังไม่พอ ต้องบอกว่าต่างจากน้ำขวดอื่นตรงไหน",
                "ชอบถ้าแบรนด์พูดเรื่อง refill หรือขวดรีไซเคิลจริง ไม่ใช่แค่ภาพสวย",
            ],
            "recommended_actions": [
                {"priority": "critical", "description": "เพิ่ม proof card เรื่องแร่ธาตุ แหล่งน้ำ และมาตรฐานตรวจสอบในทุก creative", "timeline": "ก่อน launch"},
                {"priority": "high", "description": "ทำ creator brief แยก 2 ชุด: lifestyle สำหรับ Gen Z และ family safety สำหรับครอบครัว", "timeline": "สัปดาห์นี้"},
                {"priority": "medium", "description": "เตรียม FAQ เรื่องราคาและ packaging sustainability", "timeline": "ภายใน 10 วัน"},
            ],
        },
    },
    "demo-insurtech-trust": {
        "kpis": {
            "overall_sentiment": 18,
            "conversion_probability": 42,
            "social_influence": 69,
            "message_resonance": 64,
            "crisis_risk": "high",
            "brand_perception_shift": 11,
            "opinion_polarization": 57,
            "confidence_score": 76,
        },
        "timeline": [
            {"round_num": 1, "sentiment": -34, "posts_count": 58},
            {"round_num": 2, "sentiment": -21, "posts_count": 74},
            {"round_num": 3, "sentiment": -8, "posts_count": 86},
            {"round_num": 4, "sentiment": 6, "posts_count": 91},
            {"round_num": 5, "sentiment": 15, "posts_count": 96},
            {"round_num": 6, "sentiment": 18, "posts_count": 88},
        ],
        "segments": [
            {"name": "Delayed-Claim Policyholders", "sentiment": -42, "conversion_estimate": 19, "size": "29%"},
            {"name": "EV Owners Comparing Coverage", "sentiment": 12, "conversion_estimate": 46, "size": "24%"},
            {"name": "Family Health Decision Makers", "sentiment": 28, "conversion_estimate": 55, "size": "27%"},
            {"name": "Agent/Broker Network", "sentiment": 35, "conversion_estimate": 62, "size": "12%"},
            {"name": "Regulatory Watchers", "sentiment": -18, "conversion_estimate": 22, "size": "8%"},
        ],
        "influencers": [
            {"name": "Synthetic Insurance Explainer A", "platform": "YouTube", "impact_score": 88, "sentiment": 31, "reach": 185000},
            {"name": "Synthetic EV Owners Forum B", "platform": "Facebook", "impact_score": 82, "sentiment": 8, "reach": 142000},
            {"name": "Synthetic Claims Complaint C", "platform": "X", "impact_score": 79, "sentiment": -51, "reach": 121000},
            {"name": "Synthetic Family Finance D", "platform": "LINE", "impact_score": 73, "sentiment": 24, "reach": 98000},
        ],
        "evidence": {
            "confidence_score": 76,
            "recommended_validation_step": "Validate the revised claims-service promise with a small policyholder panel and broker review before public relaunch.",
            "limitations": [
                "InsurTech trust dashboard is a synthetic demo fixture, not claim-system or regulator evidence.",
                "No real customer records, policy numbers, claim files, or complaint posts are ingested.",
            ],
            "assumptions": [
                "Simulated crisis begins after visible claim-delay complaints across X, Facebook, and LINE.",
                "Trust recovery depends on concrete service-level actions, not apology copy alone.",
                "EV insurance buyers compare coverage clarity, claim speed, and garage-network confidence.",
            ],
            "why_this_score": [
                "Sentiment improves from negative to mildly positive when the message names claim-speed guarantees and escalation owners.",
                "Crisis risk remains high because delayed-claim personas continue amplifying unresolved cases.",
                "Broker and family decision-maker segments respond better to process transparency than discount-led offers.",
            ],
            "risk_drivers": [
                "Apology without visible claim backlog action can be read as PR-only.",
                "EV owners ask for garage-network proof and battery-coverage clarity.",
                "Regulatory watchers may escalate if claims about service guarantees are too broad.",
            ],
            "quotes": [
                "ถ้าบอกได้ว่าเคลมค้างจะจบเมื่อไหร่ และมีคนรับผิดชอบจริง ฉันจะฟังมากขึ้น",
                "EV insurance ต้องชัดเรื่องอู่ แบตเตอรี่ และระยะเวลาซ่อม ไม่ใช่แค่ premium ถูก",
                "ขอโทษอย่างเดียวไม่พอ ต้องเห็นระบบ tracking เคลมที่ตรวจสอบได้",
            ],
            "recommended_actions": [
                {"priority": "critical", "description": "Publish claim backlog action, escalation owner, and service-level timeline before any brand image push", "timeline": "First 24 hours"},
                {"priority": "high", "description": "Create EV coverage explainer cards with garage network and battery-claim boundaries", "timeline": "This week"},
                {"priority": "medium", "description": "Brief brokers and call-center teams with identical claim-recovery language", "timeline": "Within 10 days"},
            ],
        },
    },
    "demo-energy-community": {
        "kpis": {
            "overall_sentiment": 26,
            "conversion_probability": 34,
            "social_influence": 72,
            "message_resonance": 59,
            "crisis_risk": "medium",
            "brand_perception_shift": 15,
            "opinion_polarization": 66,
            "confidence_score": 74,
        },
        "timeline": [
            {"round_num": 1, "sentiment": -12, "posts_count": 47},
            {"round_num": 2, "sentiment": -4, "posts_count": 63},
            {"round_num": 3, "sentiment": 9, "posts_count": 76},
            {"round_num": 4, "sentiment": 18, "posts_count": 82},
            {"round_num": 5, "sentiment": 21, "posts_count": 79},
            {"round_num": 6, "sentiment": 26, "posts_count": 73},
        ],
        "segments": [
            {"name": "Local Community Leaders", "sentiment": 22, "conversion_estimate": 39, "size": "26%"},
            {"name": "Households Near Project Site", "sentiment": -24, "conversion_estimate": 16, "size": "30%"},
            {"name": "Policy And Media Watchers", "sentiment": 8, "conversion_estimate": 25, "size": "17%"},
            {"name": "Clean Energy Supporters", "sentiment": 58, "conversion_estimate": 61, "size": "15%"},
            {"name": "Investor / Business Groups", "sentiment": 41, "conversion_estimate": 53, "size": "12%"},
        ],
        "influencers": [
            {"name": "Synthetic Local Community Page A", "platform": "Facebook", "impact_score": 90, "sentiment": -12, "reach": 168000},
            {"name": "Synthetic Energy Policy Thread B", "platform": "Reddit", "impact_score": 81, "sentiment": 18, "reach": 94000},
            {"name": "Synthetic Regional News C", "platform": "YouTube", "impact_score": 78, "sentiment": 6, "reach": 112000},
            {"name": "Synthetic Investor Brief D", "platform": "LINE", "impact_score": 69, "sentiment": 39, "reach": 74000},
        ],
        "evidence": {
            "confidence_score": 74,
            "recommended_validation_step": "Run a community listening session and third-party environmental proof review before announcing project milestones.",
            "limitations": [
                "Energy community dashboard is a synthetic demo fixture, not public-hearing evidence.",
                "No real residents, land records, regulatory filings, or local complaint posts are ingested.",
            ],
            "assumptions": [
                "Local households prioritize health, land value, water use, traffic, and long-term monitoring.",
                "Investors respond to transition-plan credibility, but community acceptance controls escalation risk.",
                "Community forum behavior is simulated through public concern archetypes, not live hearing transcripts.",
            ],
            "why_this_score": [
                "Sentiment becomes positive when the message leads with measurable safeguards and community benefits.",
                "Polarization remains high because households near the project site distrust broad clean-energy framing.",
                "Clean-energy supporters and investor groups amplify proof-led transition messaging.",
            ],
            "risk_drivers": [
                "Benefit claims without local monitoring details trigger suspicion.",
                "If project jobs are framed too broadly, local households ask who actually benefits.",
                "Environmental language must be backed by third-party measurement and clear grievance channels.",
            ],
            "quotes": [
                "ถ้ามีตัวเลขตรวจวัดอากาศและน้ำที่คนในพื้นที่ดูได้จริง ความกังวลจะลดลง",
                "พูดเรื่องพลังงานสะอาดได้ แต่ต้องตอบว่าบ้านใกล้โครงการจะได้รับผลกระทบอะไร",
                "อยากเห็นช่องทางร้องเรียนและคนรับผิดชอบ ไม่ใช่แค่เวทีประชาสัมพันธ์",
            ],
            "recommended_actions": [
                {"priority": "critical", "description": "Publish monitoring plan, third-party measurement cadence, and grievance owner before project milestone announcements", "timeline": "Before public update"},
                {"priority": "high", "description": "Create community-first FAQ on health, water, traffic, land value, and local jobs", "timeline": "This week"},
                {"priority": "medium", "description": "Separate investor transition narrative from local-community safeguard narrative", "timeline": "Within 2 weeks"},
            ],
        },
    },
}


def _dashboard_for(demo_id: str) -> dict | None:
    campaign = next((item for item in DEMO_CAMPAIGNS if item["id"] == demo_id), None)
    dashboard = DEMO_DASHBOARDS.get(demo_id)
    if not campaign or not dashboard:
        return None
    source = {
        "type": "demo_mode",
        "source_mode": "demo_mode",
        "campaign_id": campaign["id"],
        "simulation_id": None,
        "run_id": f"demo:{campaign['id']}",
        "data_basis": "demo_fixture",
        "confidence": None,
        "limitations": [
            "Demo fixture only; not generated from a live simulation run.",
        ],
        "label": "Demo Mode",
        "warning": "Synthetic demo data for product exploration; not a live simulation result.",
    }
    action_plan = ActionPlanService().generate(
        campaign=campaign,
        kpis=dashboard.get("kpis", {}),
        segments=dashboard.get("segments", []),
        evidence=dashboard.get("evidence", {}),
        source=source,
    )
    return {
        "campaign": campaign,
        "source": source,
        "action_plan": action_plan,
        **dashboard,
    }


@demo_bp.route("/campaigns", methods=["GET"])
def list_demo_campaigns():
    ready_campaigns = [campaign for campaign in DEMO_CAMPAIGNS if campaign["id"] in DEMO_DASHBOARDS]
    return jsonify({"success": True, "data": ready_campaigns})


@demo_bp.route("/campaigns/<demo_id>/dashboard", methods=["GET"])
def get_demo_dashboard(demo_id: str):
    dashboard = _dashboard_for(demo_id)
    if dashboard is None:
        return jsonify({
            "success": False,
            "error": "Demo dashboard not found",
            "code": "demo_dashboard_not_found",
        }), 404
    return jsonify({"success": True, "data": dashboard})
