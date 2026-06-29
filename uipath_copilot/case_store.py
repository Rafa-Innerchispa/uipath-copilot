"""Persistencia de casos Maestro en MongoDB (auditoría real)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, MongoClient

from uipath_copilot.settings import CASES_COLLECTION, MONGO_DB, MONGO_URI

_client: MongoClient | None = None


def _db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[MONGO_DB]


def ensure_case_indexes() -> None:
    col = _db()[CASES_COLLECTION]
    col.create_index([("case_id", ASCENDING)], unique=True)
    col.create_index([("created_at", ASCENDING)])
    col.create_index([("stage", ASCENDING)])


def _now() -> datetime:
    return datetime.now(timezone.utc)


def save_case(doc: dict[str, Any]) -> dict[str, Any]:
    ensure_case_indexes()
    col = _db()[CASES_COLLECTION]
    case_id = doc["case_id"]
    existing = col.find_one({"case_id": case_id}, {"_id": 0})
    if existing:
        doc["created_at"] = existing.get("created_at", _now())
    else:
        doc["created_at"] = _now()
    # Nunca pisar eventos con copia stale del documento anterior
    doc.pop("events", None)
    if existing and existing.get("events"):
        doc["events"] = existing.get("events", [])
    else:
        doc.setdefault("events", [])
    doc["updated_at"] = _now()
    if not doc.get("client_name") and doc.get("payload_snapshot"):
        doc["client_name"] = doc["payload_snapshot"].get("client_name")
    col.update_one({"case_id": case_id}, {"$set": doc}, upsert=True)
    saved = col.find_one({"case_id": case_id}, {"_id": 0}) or doc
    return _serialize_case(saved)


def append_event(case_id: str, event: dict[str, Any]) -> None:
    ensure_case_indexes()
    _db()[CASES_COLLECTION].update_one(
        {"case_id": case_id},
        {
            "$push": {"events": {**event, "at": _now().isoformat()}},
            "$set": {"updated_at": _now()},
        },
    )


def get_case(case_id: str) -> dict[str, Any] | None:
    doc = _db()[CASES_COLLECTION].find_one({"case_id": case_id}, {"_id": 0})
    return _serialize_case(doc) if doc else None


def _serialize_case(doc: dict[str, Any]) -> dict[str, Any]:
    out = dict(doc)
    for key in ("created_at", "updated_at"):
        val = out.get(key)
        if hasattr(val, "isoformat"):
            out[key] = val.isoformat()
    # Legacy: "pending" bloqueaba el botón Aprobar en el panel
    if out.get("approval_status") == "pending":
        out["approval_status"] = None
    return out


def list_cases(limit: int = 50) -> list[dict[str, Any]]:
    ensure_case_indexes()
    cur = _db()[CASES_COLLECTION].find({}, {"_id": 0}).sort("updated_at", -1).limit(limit)
    return [_serialize_case(c) for c in cur]


def delete_all_cases() -> int:
    """Borra todos los casos Maestro (reset demo)."""
    ensure_case_indexes()
    res = _db()[CASES_COLLECTION].delete_many({})
    return int(res.deleted_count)


def case_audit_signals() -> dict[str, int]:
    """Señales agregadas — no limitar a los N casos recientes del panel."""
    ensure_case_indexes()
    col = _db()[CASES_COLLECTION]
    stages4 = ["Intake", "Investigation", "Remediation", "Approval"]
    return {
        "total": col.count_documents({}),
        "approved": col.count_documents({"approval_status": "approved"}),
        "rejected": col.count_documents({"approval_status": "rejected"}),
        "at_approval": col.count_documents({"stage": "Approval"}),
        "hitl_decided": col.count_documents(
            {"approval_status": {"$in": ["approved", "rejected"]}}
        ),
        "full_flow": col.count_documents({"stages_completed": {"$all": stages4}}),
        "maestro_cloud": col.count_documents({"integration_source": "maestro_cloud"}),
    }


def is_placeholder_case_id(case_id: str) -> bool:
    c = (case_id or "").strip()
    if not c:
        return True
    if "{{" in c or "}}" in c:
        return True
    placeholders = {
        "VARIABLE_CASE_ID",
        "PON_AQUI_CASE_ID",
        "{{caseId}}",
        "{{ caseId }}",
        "caseId",
    }
    return c.upper() in placeholders or c in placeholders


_STAGE_PRIOR = {
    "Investigation": "Intake",
    "Remediation": "Investigation",
    "Approval": "Remediation",
}


def find_case_awaiting_stage(stage: str) -> dict[str, Any] | None:
    """Caso reciente que completó la etapa anterior pero no esta (Maestro sin case_id real)."""
    prior = _STAGE_PRIOR.get(stage)
    if not prior:
        return None
    cur = (
        _db()[CASES_COLLECTION]
        .find({}, {"_id": 0})
        .sort("updated_at", -1)
        .limit(30)
    )
    for doc in cur:
        cid = str(doc.get("case_id") or "")
        if is_placeholder_case_id(cid):
            continue
        done = doc.get("stages_completed") or []
        if prior in done and stage not in done:
            return _serialize_case(doc)
    return None
