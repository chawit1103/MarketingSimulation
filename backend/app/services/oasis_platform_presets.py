"""OASIS platform preset layer for campaign-oriented simulations.

OASIS currently provides native Twitter-like and Reddit-like environments.
These presets map modern campaign channels into behavior models that can run
on those native engines while keeping the UI honest about native support.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class OasisPlatformPreset:
    mode: str
    label: str
    description: str
    native_engine: str
    modeled_behavior: str
    native_support: bool = False
    twitter_actions: List[str] = field(default_factory=list)
    reddit_actions: List[str] = field(default_factory=list)
    recommended_channels: List[str] = field(default_factory=list)
    recsys_type: str = "default"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "label": self.label,
            "description": self.description,
            "native_engine": self.native_engine,
            "modeled_behavior": self.modeled_behavior,
            "native_support": self.native_support,
            "twitter_actions": self.twitter_actions,
            "reddit_actions": self.reddit_actions,
            "recommended_channels": self.recommended_channels,
            "recsys_type": self.recsys_type,
        }


DEFAULT_TWITTER_ACTIONS = [
    "CREATE_POST",
    "LIKE_POST",
    "REPOST",
    "FOLLOW",
    "DO_NOTHING",
    "QUOTE_POST",
]

DEFAULT_REDDIT_ACTIONS = [
    "LIKE_POST",
    "DISLIKE_POST",
    "CREATE_POST",
    "CREATE_COMMENT",
    "LIKE_COMMENT",
    "DISLIKE_COMMENT",
    "SEARCH_POSTS",
    "SEARCH_USER",
    "TREND",
    "REFRESH",
    "DO_NOTHING",
    "FOLLOW",
    "MUTE",
]


PRESETS: Dict[str, OasisPlatformPreset] = {
    "auto": OasisPlatformPreset(
        mode="auto",
        label="Auto-fit",
        description="Infer the closest OASIS behavior model from selected audience channels.",
        native_engine="both",
        modeled_behavior="Adaptive social simulation",
        native_support=True,
        twitter_actions=DEFAULT_TWITTER_ACTIONS,
        reddit_actions=DEFAULT_REDDIT_ACTIONS,
        recommended_channels=["twitter_x", "reddit", "facebook", "instagram", "tiktok"],
    ),
    "microblog": OasisPlatformPreset(
        mode="microblog",
        label="Microblog",
        description="Fast public feed behavior for X, Threads, LinkedIn, and news-commentary audiences.",
        native_engine="twitter",
        modeled_behavior="Short-form public feed",
        native_support=True,
        twitter_actions=DEFAULT_TWITTER_ACTIONS,
        reddit_actions=[],
        recommended_channels=["twitter_x", "linkedin"],
        recsys_type="twhin",
    ),
    "community_forum": OasisPlatformPreset(
        mode="community_forum",
        label="Community Forum",
        description="Threaded community discussion for Reddit, Facebook Groups, Pantip-style forums, and support communities.",
        native_engine="reddit",
        modeled_behavior="Threaded discussion and voting",
        native_support=True,
        twitter_actions=[],
        reddit_actions=DEFAULT_REDDIT_ACTIONS,
        recommended_channels=["reddit", "facebook"],
    ),
    "group_chat": OasisPlatformPreset(
        mode="group_chat",
        label="Group Chat",
        description="Closed community behavior for LINE, Messenger, WhatsApp, and private advocacy groups.",
        native_engine="reddit",
        modeled_behavior="Small-group conversation modeled on threaded comments",
        twitter_actions=[],
        reddit_actions=[
            "CREATE_POST",
            "CREATE_COMMENT",
            "LIKE_COMMENT",
            "SEARCH_USER",
            "FOLLOW",
            "MUTE",
            "DO_NOTHING",
            "CREATE_GROUP",
            "SEND_TO_GROUP",
            "LISTEN_FROM_GROUP",
        ],
        recommended_channels=["line", "facebook", "whatsapp"],
    ),
    "creator_feed": OasisPlatformPreset(
        mode="creator_feed",
        label="Creator Feed",
        description="Creator-led feed dynamics for TikTok, Instagram Reels, YouTube Shorts, and influencer launches.",
        native_engine="twitter",
        modeled_behavior="Creator recommendation feed modeled on public posting, reposting, and following",
        twitter_actions=[
            "CREATE_POST",
            "LIKE_POST",
            "REPOST",
            "QUOTE_POST",
            "FOLLOW",
            "REPORT_POST",
            "DO_NOTHING",
        ],
        reddit_actions=[
            "CREATE_POST",
            "CREATE_COMMENT",
            "LIKE_POST",
            "LIKE_COMMENT",
            "TREND",
            "REFRESH",
            "DO_NOTHING",
        ],
        recommended_channels=["tiktok", "instagram", "youtube"],
        recsys_type="content_embedding",
    ),
    "commerce_intent": OasisPlatformPreset(
        mode="commerce_intent",
        label="Commerce Intent",
        description="Purchase-intent behavior for TikTok Shop, live commerce, product launches, and conversion campaigns.",
        native_engine="reddit",
        modeled_behavior="Product consideration and purchase-intent discussion",
        twitter_actions=[
            "CREATE_POST",
            "LIKE_POST",
            "REPOST",
            "FOLLOW",
            "DO_NOTHING",
            "PURCHASE_PRODUCT",
        ],
        reddit_actions=[
            "CREATE_POST",
            "CREATE_COMMENT",
            "LIKE_POST",
            "LIKE_COMMENT",
            "SEARCH_POSTS",
            "TREND",
            "DO_NOTHING",
            "PURCHASE_PRODUCT",
        ],
        recommended_channels=["tiktok", "instagram", "youtube", "facebook"],
    ),
}


def normalize_channels(channels: List[str] | None) -> List[str]:
    values = channels if isinstance(channels, list) else []
    normalized = []
    for channel in values:
        value = str(channel or "").strip()
        if not value:
            continue
        normalized.append("twitter_x" if value == "twitter" else value)
    return list(dict.fromkeys(normalized))


def infer_mode(channels: List[str] | None) -> str:
    selected = set(normalize_channels(channels))
    if selected & {"tiktok", "instagram", "youtube", "shopee_live"}:
        return "creator_feed"
    if selected & {"line", "whatsapp", "messenger"}:
        return "group_chat"
    if selected & {"facebook", "reddit"}:
        return "community_forum"
    if selected & {"twitter_x", "linkedin", "threads"}:
        return "microblog"
    return "microblog"


def resolve_preset(
    mode: str | None = None,
    channels: List[str] | None = None,
    engine_platform: str | None = None,
) -> Dict[str, Any]:
    selected_mode = mode or "auto"
    if selected_mode == "auto":
        selected_mode = infer_mode(channels)

    preset = PRESETS.get(selected_mode, PRESETS["microblog"]).to_dict()
    preset["requested_mode"] = mode or "auto"
    preset["resolved_mode"] = selected_mode
    preset["audience_channels"] = normalize_channels(channels)
    preset["engine_platform"] = engine_platform or preset["native_engine"]
    preset["native_note"] = (
        "Native OASIS support" if preset["native_support"]
        else "Modeled on the closest native OASIS engine"
    )
    return preset

