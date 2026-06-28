"""Rutas FastAPI uipath-copilot."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ValidationError

from tools.evolution_api import evolution_available, send_whatsapp
from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.activity_log import list_activity, log_activity
from uipath_copilot.case_store import get_case, list_cases
from uipath_copilot.maestro_client import maestro_status
from uipath_copilot.platform_scorecard import build_platform_scorecard
from uipath_copilot.i18n import normalize_lang
from uipath_copilot.operational_consultations import (
    build_consultation_catalog,
    build_webhook_payload,
    run_full_consultation,
)
from uipath_copilot.processor import apply_human_decision, process_webhook
from uipath_copilot.project_docs_store import get_doc as get_project_doc
from uipath_copilot.project_docs_store import list_docs as list_project_docs
from uipath_copilot.settings import (
    OPERATOR_WHATSAPP,
    PUBLIC_BASE_URL,
    UIPATH_BASE_URL,
    UIPATH_COPILOT_PORT,
)

router = APIRouter(prefix="/api/v1", tags=["uipath-maestro"])


class WebhookPayload(BaseModel):
    case_id: str = Field(..., description="UUID del caso Maestro")
    incident_type: str | None = None
    severity: str = "medium"
    stage: str = "Intake"
    raw_logs: str = ""
    notes: str = ""
    client_id: str | None = None
    client_name: str | None = None
    ruc: str | None = None
    client_ruc: str | None = None
    quote_id: str | None = None
    scenario_id: str | None = None
    scenario_title_en: str | None = None
    scenario_title_es: str | None = None
    panel_lang: str | None = None


def _notify_operator(report_md: str, case_id: str) -> dict[str, Any] | None:
    if not OPERATOR_WHATSAPP or not evolution_available():
        return None
    text = f"*PC Doctor Maestro Case*\nCaso: `{case_id}`\n\n{report_md[:3500]}"
    return send_whatsapp(OPERATOR_WHATSAPP, text)


class HumanDecisionPayload(BaseModel):
    decision: str = Field(..., description="approve | reject (o aprobar | rechazar)")
    comment: str = ""


@router.get("/ui-config")
def api_ui_config():
    from uipath_copilot.action_center_client import action_center_status

    ac = action_center_status()
    return {
        "company_name": "InnerChispa",
        "company_url": "https://www.innerchispa.us",
        "product": "PC Doctor S.A. — Maestro Case Copilot",
        "public_base_url": PUBLIC_BASE_URL,
        "webhook_url": f"{PUBLIC_BASE_URL}/api/v1/uipath-webhook",
        "action_center": ac,
        "consultations_url": f"{PUBLIC_BASE_URL}/api/v1/consultations",
        "dashboard_urls": {
            "local": f"http://192.168.1.4:{UIPATH_COPILOT_PORT}/dashboard",
            "public": f"{PUBLIC_BASE_URL}/dashboard",
            "admin": "http://192.168.1.4:5173/maestro",
        },
    }


@router.get("/activity")
def api_activity(limit: int = 100):
    return {"lines": list_activity(limit=limit)}


@router.get("/activity-stream")
async def api_activity_stream():
    """SSE — terminal en vivo para el panel jurado."""

    async def generate():
        tick = 0
        while True:
            if tick % 5 == 0:
                ms = maestro_status()
                log_activity(
                    "info" if ms.get("reachable") else "warn",
                    "POLL",
                    f"UiPath OAuth {'reachable' if ms.get('reachable') else 'down'} · MongoDB clients={get_db().clients.count_documents({})}",
                )
            for line in list_activity(8):
                yield f"data: {json.dumps(line, ensure_ascii=False)}\n\n"
            tick += 1
            await asyncio.sleep(2)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )


@router.post("/cases/{case_id}/human-decision")
def api_human_decision(case_id: str, body: HumanDecisionPayload):
    """HITL desde panel web — complementa Action Center en Maestro."""
    try:
        result = apply_human_decision(case_id, decision=body.decision, comment=body.comment)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    log_activity("ok", "HITL", f"Human {result.get('approval_status')} case {case_id[:8]}…")
    return result


@router.post("/uipath-webhook")
async def uipath_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Entrada Maestro API Workflow.
    Acepta JSON en body O query ?case_id=&stage= (si Maestro manda body vacío).
    """
    qp = dict(request.query_params)
    raw = await request.body()
    payload: dict[str, Any] = {}

    if raw and raw.strip() not in (b"", b"{}", b"null"):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise HTTPException(
                422,
                f"JSON body invalid: {exc}. Paste JSON from data/maestro_webhook_body_*.json or use ?case_id=&stage= in URL.",
            ) from exc
        if isinstance(parsed, dict):
            payload = parsed

    for key, val in qp.items():
        if key not in payload or payload[key] in (None, ""):
            payload[key] = val

    if not payload.get("case_id") and payload.get("CaseId"):
        payload["case_id"] = payload["CaseId"]

    try:
        body = WebhookPayload.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(
            422,
            f"Missing fields: {exc.errors()}. Required: case_id (body or ?case_id=). stage defaults to Intake.",
        ) from exc

    try:
        result = process_webhook(body.model_dump())
    except ValueError as exc:
        log_activity("err", "WEBHOOK", str(exc))
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        log_activity("err", "WEBHOOK", str(exc))
        raise HTTPException(500, str(exc)) from exc

    log_activity(
        "ok",
        "WEBHOOK",
        f"Stage {result.get('stage')} · {result.get('incident_type')} · case {result.get('case_id', '')[:8]}…",
    )

    if result.get("needs_human") or result.get("report_markdown"):
        background_tasks.add_task(
            _notify_operator,
            result["report_markdown"],
            result["case_id"],
        )
    return result


@router.get("/project-docs")
def api_list_project_docs(limit: int = 30):
    """Índice de documentación sincronizada (MongoDB inneros_global)."""
    docs = list_project_docs(limit=limit)
    return {"docs": docs, "count": len(docs)}


@router.get("/project-docs/{doc_id}")
def api_get_project_doc(doc_id: str):
    doc = get_project_doc(doc_id)
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
    return doc


@router.get("/cases")
def api_list_cases(limit: int = 30):
    cases = list_cases(limit=limit)
    return {"cases": cases, "count": len(cases)}


@router.get("/cases/{case_id}")
def api_get_case(case_id: str):
    doc = get_case(case_id)
    if not doc:
        raise HTTPException(404, "Caso no encontrado")
    return doc


@router.get("/platform-scorecard")
def api_platform_scorecard():
    """Checklist bonus Community — qué falta para el jackpot."""
    return build_platform_scorecard()


@router.get("/consultations")
def list_consultations():
    """Catálogo de consultas operativas — clientes/cotizaciones reales en MongoDB."""
    catalog = build_consultation_catalog()
    return {
        "webhook_url": f"{PUBLIC_BASE_URL}/api/v1/uipath-webhook",
        "count": len(catalog),
        "consultations": catalog,
        "run_full_url_pattern": f"{PUBLIC_BASE_URL}/api/v1/consultations/{{consultation_id}}/run-full",
    }


@router.post("/consultations/{consultation_id}/run-full")
def run_consultation_full(consultation_id: str, lang: str = Query("es")):
    """Ejecuta etapas Maestro; se detiene si gate bloqueante falla."""
    try:
        return run_full_consultation(consultation_id, panel_lang=normalize_lang(lang))
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/consultations/{consultation_id}/run")
@router.post("/consultations/{consultation_id}/run")
def run_consultation_stage(consultation_id: str, stage: str = "Intake", lang: str = Query("es")):
    """Ejecuta una sola etapa de la consulta operativa."""
    try:
        payload = build_webhook_payload(consultation_id, stage=stage, panel_lang=normalize_lang(lang))
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    log_activity("info", "CONSULTA", f"{stage} · {payload.get('client_name')} · {consultation_id}")
    return process_webhook(payload)


# Alias legacy (scripts antiguos) — sin exponer en UI
@router.get("/demo/scenarios")
def _legacy_demo_scenarios():
    c = build_consultation_catalog()
    return {"scenarios": c, "consultations": c, "count": len(c)}


@router.post("/demo/trigger/{scenario_id}")
def _legacy_demo_trigger(scenario_id: str, stage: str = "Intake"):
    return run_consultation_stage(scenario_id, stage=stage)


@router.get("/demo/trigger-sample")
def _legacy_trigger_sample(consultation_id: str | None = None):
    import uuid

    catalog = build_consultation_catalog()
    if not catalog:
        raise HTTPException(503, "MongoDB sin datos operativos")
    cid = consultation_id or catalog[uuid.uuid4().int % len(catalog)]["id"]
    return run_consultation_stage(cid, stage="Intake")
