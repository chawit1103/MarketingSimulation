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
}


def _dashboard_for(demo_id: str) -> dict:
    campaign = next((item for item in DEMO_CAMPAIGNS if item["id"] == demo_id), DEMO_CAMPAIGNS[0])
    dashboard = DEMO_DASHBOARDS.get(demo_id, DEMO_DASHBOARDS["demo-premium-water"])
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
    return jsonify({"success": True, "data": DEMO_CAMPAIGNS})


@demo_bp.route("/campaigns/<demo_id>/dashboard", methods=["GET"])
def get_demo_dashboard(demo_id: str):
    return jsonify({"success": True, "data": _dashboard_for(demo_id)})
