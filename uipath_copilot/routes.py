"""Rutas FastAPI uipath-copilot."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from tools.evolution_api import evolution_available, send_whatsapp
from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.activity_log import list_activity, log_activity
from uipath_copilot.case_store import get_case, list_cases
from uipath_copilot.maestro_client import maestro_status
from uipath_copilot.platform_scorecard import build_platform_scorecard
from uipath_copilot.demo_scenarios import build_scenario_catalog, build_webhook_payload
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
        "demo_scenarios_url": f"{PUBLIC_BASE_URL}/api/v1/demo/scenarios",
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
async def uipath_webhook(body: WebhookPayload, background_tasks: BackgroundTasks):
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


@router.get("/demo/scenarios")
def demo_scenarios():
    """Catálogo de consultas demo — clientes/cotizaciones distintos en MongoDB."""
    catalog = build_scenario_catalog()
    return {
        "webhook_url": f"{PUBLIC_BASE_URL}/api/v1/uipath-webhook",
        "count": len(catalog),
        "scenarios": catalog,
        "trigger_url_pattern": f"{PUBLIC_BASE_URL}/api/v1/demo/trigger/{{scenario_id}}",
    }


@router.get("/demo/trigger/{scenario_id}")
@router.post("/demo/trigger/{scenario_id}")
def demo_trigger_scenario(scenario_id: str, stage: str = "Intake"):
    """Dispara una consulta demo concreta (cliente real distinto)."""
    try:
        payload = build_webhook_payload(scenario_id, stage=stage)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    log_activity("info", "DEMO", f"Trigger scenario {scenario_id} · {payload.get('client_name')}")
    return process_webhook(payload)


@router.get("/demo/trigger-sample")
def demo_trigger_sample(scenario_id: str | None = None):
    """
    Dispara demo — si ?scenario_id= la_pradera_quote_pdf usa catálogo;
    si no, rota entre escenarios para no repetir siempre el mismo cliente.
    """
    import uuid

    catalog = build_scenario_catalog()
    if not catalog:
        raise HTTPException(503, "MongoDB sin datos demo")

    if scenario_id:
        sid = scenario_id
    else:
        # Rotar: elige escenario cuyo id hash evita siempre el primero del listado
        idx = uuid.uuid4().int % len(catalog)
        sid = catalog[idx]["id"]

    try:
        payload = build_webhook_payload(sid)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    log_activity("info", "DEMO", f"trigger-sample → {sid}")
    return process_webhook(payload)
