"""Integración Agent Builder — clasificación intake + webhook Maestro."""

from __future__ import annotations

import json
import re
import uuid
from typing import Any

from tools.ollama_chat import ollama_available, ollama_chat
from uipath_copilot.activity_log import log_activity
from uipath_copilot.platform_events import record_event
from uipath_copilot.processor import process_webhook
from uipath_copilot.settings import OLLAMA_MODEL_ANALYSIS

SYSTEM_PROMPT = """Eres el agente de intake de PC Doctor S.A. (Ecuador).
Clasifica excepciones operativas de campo y responde SOLO JSON válido:
{"incident_type":"...", "severity":"high|medium|low", "summary":"...", "client_hint":"..."}
Tipos: client_duplicate, quote_gate_blocked, hub_missing, report_quality, field_inspection_exception.
Si mencionan RUC duplicado → client_duplicate severity high.
Si falta PDF/cotización → quote_gate_blocked.
Si @today o placeholder → report_quality.
Visita/inspección residencial → field_inspection_exception."""


def _rule_classify(message: str) -> dict[str, Any] | None:
    low = message.lower()
    if any(k in low for k in ("duplicad", "ruc repet", "ya existe", "re-alta")):
        return {
            "incident_type": "client_duplicate",
            "severity": "high",
            "summary": "Posible cliente duplicado detectado en intake.",
            "client_hint": "",
        }
    if any(k in low for k in ("pdf", "cotizacion", "cotización", "quote")):
        return {
            "incident_type": "quote_gate_blocked",
            "severity": "medium",
            "summary": "Gate PDF-first / cotización bloqueada.",
            "client_hint": "",
        }
    if "@today" in low or "placeholder" in low:
        return {
            "incident_type": "report_quality",
            "severity": "high",
            "summary": "Informe con placeholder pendiente de corrección.",
            "client_hint": "",
        }
    if any(k in low for k in ("inspeccion", "inspección", "campo", "visita", "dominguez", "residential")):
        return {
            "incident_type": "field_inspection_exception",
            "severity": "medium",
            "summary": "Excepción post-inspección de campo.",
            "client_hint": "",
        }
    return None


def _ollama_classify(message: str) -> dict[str, Any]:
    if not ollama_available():
        return {
            "incident_type": "field_inspection_exception",
            "severity": "medium",
            "summary": message[:200],
            "client_hint": "",
        }
    raw = ollama_chat(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        model=OLLAMA_MODEL_ANALYSIS,
    )
    try:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            return json.loads(m.group())
    except json.JSONDecodeError:
        pass
    return {
        "incident_type": "field_inspection_exception",
        "severity": "medium",
        "summary": raw[:300],
        "client_hint": "",
    }


def classify_intake(message: str) -> dict[str, Any]:
    message = (message or "").strip()
    if not message:
        raise ValueError("message vacío")
    classified = _rule_classify(message) or _ollama_classify(message)
    record_event("agent_builder", "classify", message=message[:500], result=classified)
    log_activity("ok", "AGENT-BUILDER", f"Classified → {classified.get('incident_type')} ({classified.get('severity')})")
    return classified


def agent_intake_to_webhook(
    message: str,
    *,
    case_id: str | None = None,
    client_name: str | None = None,
    client_id: str | None = None,
    ruc: str | None = None,
    quote_id: str | None = None,
    stage: str = "Intake",
    panel_lang: str = "en",
    trigger_webhook: bool = True,
) -> dict[str, Any]:
    classified = classify_intake(message)
    cid = case_id or str(uuid.uuid4())
    payload = {
        "case_id": cid,
        "stage": stage,
        "incident_type": classified["incident_type"],
        "severity": classified.get("severity", "medium"),
        "client_name": client_name or classified.get("client_hint") or None,
        "client_id": client_id,
        "ruc": ruc,
        "quote_id": quote_id,
        "raw_logs": message,
        "notes": "source=agent_builder",
        "panel_lang": panel_lang,
        "scenario_id": "agent_builder_intake",
        "scenario_title_en": "Agent Builder — Intake classification",
        "scenario_title_es": "Agent Builder — clasificación intake",
    }
    out: dict[str, Any] = {"classification": classified, "case_id": cid, "webhook_payload": payload}
    if trigger_webhook:
        result = process_webhook(payload)
        record_event("agent_builder", "webhook", case_id=cid, stage=stage)
        out["webhook_result"] = result
    return out
