"""Small in-memory rate limiter for public and high-risk API endpoints."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock
from typing import Deque, Dict, Optional, Tuple

from flask import current_app, jsonify, request


class RateLimitMiddleware:
    """Install a fixed-window-ish sliding log limiter.

    This is intentionally lightweight and dependency-free. It is suitable for a
    single-process app and local/demo protection. Production deployments with
    multiple workers should pair it with an edge/API gateway limiter.
    """

    GROUPS = (
        ("auth", ("/api/auth/login", "/api/auth/register"), "RATE_LIMIT_AUTH_PER_WINDOW"),
        ("demo", ("/api/demo",), "RATE_LIMIT_DEMO_PER_WINDOW"),
        ("status", ("/api/status",), "RATE_LIMIT_STATUS_PER_WINDOW"),
        ("decision", ("/api/decision",), "RATE_LIMIT_DECISION_PER_WINDOW"),
        ("brief", ("/api/brief",), "RATE_LIMIT_DECISION_PER_WINDOW"),
        ("competitor", ("/api/competitor",), "RATE_LIMIT_SIMULATION_PER_WINDOW"),
        ("settings", ("/api/settings/readiness", "/api/settings/providers"), "RATE_LIMIT_STATUS_PER_WINDOW"),
        ("simulation", ("/api/simulation",), "RATE_LIMIT_SIMULATION_PER_WINDOW"),
    )

    def __init__(self, app=None):
        self._hits: Dict[Tuple[str, str], Deque[float]] = defaultdict(deque)
        self._lock = Lock()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self._enforce)

    def _enforce(self):
        if request.method == "OPTIONS":
            return None
        if not current_app.config.get("RATE_LIMIT_ENABLED", True):
            return None

        group = self._group_for_path(request.path)
        if group is None:
            return None

        group_name, limit_key = group
        limit = int(current_app.config.get(limit_key, 60))
        if limit <= 0:
            return None

        window = int(current_app.config.get("RATE_LIMIT_WINDOW_SECONDS", 60))
        now = time.time()
        client_key = self._client_key()
        bucket_key = (group_name, client_key)

        with self._lock:
            bucket = self._hits[bucket_key]
            while bucket and bucket[0] <= now - window:
                bucket.popleft()

            if len(bucket) >= limit:
                retry_after = max(1, int(window - (now - bucket[0])))
                response = jsonify({
                    "success": False,
                    "error": "Rate limit exceeded",
                    "retry_after_seconds": retry_after,
                })
                response.status_code = 429
                response.headers["Retry-After"] = str(retry_after)
                response.headers["X-RateLimit-Limit"] = str(limit)
                response.headers["X-RateLimit-Remaining"] = "0"
                response.headers["X-RateLimit-Window"] = str(window)
                return response

            bucket.append(now)
        return None

    def _group_for_path(self, path: str) -> Optional[Tuple[str, str]]:
        for group_name, prefixes, limit_key in self.GROUPS:
            if any(path.startswith(prefix) for prefix in prefixes):
                return group_name, limit_key
        return None

    def _client_key(self) -> str:
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        if forwarded_for:
            return forwarded_for.split(",", 1)[0].strip()
        return request.remote_addr or "unknown"
