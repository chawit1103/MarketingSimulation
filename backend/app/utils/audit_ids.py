"""Helpers for constraining audit metadata identifiers."""

from __future__ import annotations

import re

_SAFE_GENERATED_CAMPAIGN_ID = re.compile(r"^cmp_[0-9a-f]{12}$")


def safe_generated_campaign_id(value: object) -> str:
    """Keep only generated campaign IDs in audit metadata."""
    campaign_id = str(value or "").strip()
    if not campaign_id or len(campaign_id) > 64:
        return "unknown"
    if (
        any(char.isspace() for char in campaign_id)
        or "/" in campaign_id
        or "\\" in campaign_id
        or "@" in campaign_id
    ):
        return "unknown"
    if _SAFE_GENERATED_CAMPAIGN_ID.fullmatch(campaign_id):
        return campaign_id
    return "unknown"
