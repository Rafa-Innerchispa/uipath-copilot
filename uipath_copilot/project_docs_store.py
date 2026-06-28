"""Snapshots de documentación del proyecto en MongoDB (consultables vía API)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, DESCENDING, MongoClient

from uipath_copilot.settings import MONGO_DB, MONGO_URI

DOCS_DB = "inneros_global"
DOCS_COLLECTION = "uipath_project_docs"

_client: MongoClient | None = None


def _col():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DOCS_DB][DOCS_COLLECTION]


def ensure_indexes() -> None:
    col = _col()
    col.create_index([("doc_id", ASCENDING)], unique=True)
    col.create_index([("updated_at", DESCENDING)])


def _now() -> datetime:
    return datetime.now(timezone.utc)


def upsert_doc(
    doc_id: str,
    *,
    title: str,
    path: str,
    content: str,
    tags: list[str] | None = None,
    source: str = "sync",
) -> dict[str, Any]:
    ensure_indexes()
    payload = {
        "doc_id": doc_id,
        "title": title,
        "path": path,
        "content": content,
        "tags": tags or [],
        "source": source,
        "updated_at": _now(),
        "char_count": len(content),
    }
    existing = _col().find_one({"doc_id": doc_id}, {"created_at": 1})
    if not existing:
        payload["created_at"] = _now()
    _col().update_one({"doc_id": doc_id}, {"$set": payload}, upsert=True)
    return _col().find_one({"doc_id": doc_id}, {"_id": 0}) or payload


def list_docs(limit: int = 50) -> list[dict[str, Any]]:
    ensure_indexes()
    cur = _col().find({}, {"_id": 0, "content": 0}).sort("updated_at", DESCENDING).limit(limit)
    return list(cur)


def get_doc(doc_id: str) -> dict[str, Any] | None:
    return _col().find_one({"doc_id": doc_id}, {"_id": 0})
