"""Document Understanding — ingest PDF / campos DU → webhook Maestro."""

from __future__ import annotations

import io
import re
import uuid
from typing import Any

from pypdf import PdfReader

from uipath_copilot.activity_log import log_activity
from uipath_copilot.platform_events import record_event
from uipath_copilot.processor import process_webhook

RUC_RE = re.compile(r"\b\d{13}\b")
CLIENT_HINTS = re.compile(
    r"(?:cliente|client|raz[oó]n social|nombre)[:\s]+([^\n\r]{3,80})",
    re.IGNORECASE,
)


def extract_pdf_fields(pdf_bytes: bytes, max_pages: int = 2) -> dict[str, Any]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = min(len(reader.pages), max_pages)
    text_parts: list[str] = []
    for i in range(pages):
        text_parts.append(reader.pages[i].extract_text() or "")
    text = "\n".join(text_parts).strip()
    ruc_match = RUC_RE.search(text)
    client_match = CLIENT_HINTS.search(text)
    placeholders = []
    for pat in (r"@today", r"\bTBD\b", r"\bN/A\b", r"\bpendiente\b"):
        if re.search(pat, text, re.IGNORECASE):
            placeholders.append(pat.replace("\\b", "").replace("\\", ""))
    return {
        "page_count": pages,
        "text_preview": text[:1200],
        "ruc": ruc_match.group(0) if ruc_match else None,
        "client_name": client_match.group(1).strip() if client_match else None,
        "placeholders_found": placeholders,
        "has_placeholders": bool(placeholders),
    }


def _incident_from_extraction(fields: dict[str, Any]) -> tuple[str, str]:
    if fields.get("has_placeholders"):
        return "report_quality", "high"
    if fields.get("ruc"):
        return "field_inspection_exception", "medium"
    return "quote_gate_blocked", "medium"


def ingest_document(
    *,
    pdf_bytes: bytes | None = None,
    extracted: dict[str, Any] | None = None,
    case_id: str | None = None,
    stage: str = "Intake",
    panel_lang: str = "en",
    source: str = "document_understanding",
) -> dict[str, Any]:
    fields = dict(extracted or {})
    if pdf_bytes:
        local = extract_pdf_fields(pdf_bytes)
        fields = {**local, **{k: v for k, v in fields.items() if v not in (None, "")}}

    incident_type = fields.get("incident_type")
    severity = fields.get("severity")
    if not incident_type:
        incident_type, severity = _incident_from_extraction(fields)

    cid = case_id or str(uuid.uuid4())
    raw_logs = fields.get("text_preview") or fields.get("observations") or "Document Understanding ingest"
    payload = {
        "case_id": cid,
        "stage": stage,
        "incident_type": incident_type,
        "severity": severity or "medium",
        "client_name": fields.get("client_name"),
        "client_id": fields.get("client_id"),
        "ruc": fields.get("ruc"),
        "quote_id": fields.get("quote_id"),
        "raw_logs": raw_logs,
        "notes": f"source={source}",
        "panel_lang": panel_lang,
        "scenario_id": "document_understanding",
        "scenario_title_en": "Document Understanding — PDF ingest",
        "scenario_title_es": "Document Understanding — ingest PDF",
    }
    result = process_webhook(payload)
    record_event("document_understanding", "ingest", case_id=cid, fields=fields)
    log_activity("ok", "DU", f"Ingest case {cid[:8]}… · {incident_type}")
    return {
        "ok": True,
        "case_id": cid,
        "extracted_fields": fields,
        "webhook_result": result,
    }
