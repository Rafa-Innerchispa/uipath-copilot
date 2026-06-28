"""Rutas FastAPI uipath-copilot."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from tools.evolution_api import evolution_available, send_whatsapp
from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.case_store import get_case, list_cases
from uipath_copilot.maestro_client import maestro_status
from uipath_copilot.processor import process_webhook
from uipath_copilot.project_docs_store import get_doc as get_project_doc
from uipath_copilot.project_docs_store import list_docs as list_project_docs
from uipath_copilot.settings import (
    OPERATOR_WHATSAPP,
    PUBLIC_BASE_URL,
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


def _notify_operator(report_md: str, case_id: str) -> dict[str, Any] | None:
    if not OPERATOR_WHATSAPP or not evolution_available():
        return None
    text = f"*PC Doctor Maestro Case*\nCaso: `{case_id}`\n\n{report_md[:3500]}"
    return send_whatsapp(OPERATOR_WHATSAPP, text)


@router.post("/uipath-webhook")
async def uipath_webhook(body: WebhookPayload, background_tasks: BackgroundTasks):
    try:
        result = process_webhook(body.model_dump())
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

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


@router.get("/demo/trigger-sample")
def demo_trigger_sample():
    """
    Dispara un caso REAL contra MongoDB PC Doctor (no mock).
    Usar en demo/video: lee clientes/cotizaciones existentes.
    """
    db = get_db()
    client = db.clients.find_one({}, {"_id": 0, "client_id": 1, "name": 1, "ruc": 1})
    if not client:
        raise HTTPException(503, "MongoDB sin clientes — ejecutar flujo PC Doctor primero")

    import uuid

    payload = WebhookPayload(
        case_id=str(uuid.uuid4()),
        incident_type="field_inspection_exception",
        severity="high",
        stage="Intake",
        raw_logs=f"Revisión post-visita cliente {client.get('name')} RUC {client.get('ruc')}",
        client_id=client.get("client_id"),
        client_name=client.get("name"),
        ruc=client.get("ruc"),
    )
    return process_webhook(payload.model_dump())
