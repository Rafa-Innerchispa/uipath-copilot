"""Eventos de integración plataforma UiPath (Agent Builder, DU, Apps, Test Manager)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, MongoClient

from uipath_copilot.settings import MONGO_DB, MONGO_URI

COLLECTION = "uipath_platform_events"
_client: MongoClient | None = None


def _col():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    col = _client[MONGO_DB][COLLECTION]
    col.create_index([("component", ASCENDING), ("at", ASCENDING)])
    return col


def record_event(component: str, action: str, **detail: Any) -> dict[str, Any]:
    doc = {
        "component": component,
        "action": action,
        "at": datetime.now(timezone.utc).isoformat(),
        **detail,
    }
    _col().insert_one(doc)
    return doc


def has_event(component: str, min_count: int = 1) -> bool:
    return _col().count_documents({"component": component}) >= min_count


def recent_events(component: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    q: dict[str, Any] = {}
    if component:
        q["component"] = component
    cur = _col().find(q, {"_id": 0}).sort("at", -1).limit(limit)
    return list(cur)
