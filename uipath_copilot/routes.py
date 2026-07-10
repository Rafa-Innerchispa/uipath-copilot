"""Rutas FastAPI uipath-copilot."""

from __future__ import annotations

import asyncio
import json
import re
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ValidationError

from tools.evolution_api import evolution_available, send_whatsapp
from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.activity_log import clear_activity, list_activity, log_activity
from uipath_copilot.case_store import (
    delete_all_cases,
    find_case_awaiting_stage,
    get_case,
    is_placeholder_case_id,
    list_cases,
)
from uipath_copilot.maestro_client import maestro_status
from uipath_copilot.platform_scorecard import build_platform_scorecard, run_platform_verification
from uipath_copilot.i18n import normalize_lang
from uipath_copilot.operational_consultations import (
    build_consultation_catalog,
    build_webhook_payload,
    run_full_consultation,
)
from uipath_copilot.maestro_flow import continue_maestro_flow, should_auto_continue
from uipath_copilot.processor import apply_human_decision, process_webhook
from uipath_copilot.project_docs_store import get_doc as get_project_doc
from uipath_copilot.project_docs_store import list_docs as list_project_docs
from uipath_copilot.agent_builder import agent_intake_to_webhook, classify_intake
from uipath_copilot.apps_case import build_apps_config, case_public_urls, get_case_app_payload
from uipath_copilot.document_understanding import extract_pdf_fields, ingest_document
from uipath_copilot.test_manager import JUNIT_PATH, RESULTS_PATH, build_junit_xml, load_last_results, run_test_suite
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
    if not OPERATOR_WHATSAPP:
        return None
    if not evolution_available():
        log_activity("warn", "WA", f"Evolution offline — no WhatsApp para caso {case_id}")
        return {"status": "skipped", "message": "Evolution no disponible"}
    text = f"*PC Doctor Maestro Case*\nCaso: `{case_id}`\n\n{report_md[:3500]}"
    result = send_whatsapp(OPERATOR_WHATSAPP, text)
    if result.get("status") != "sent":
        log_activity("warn", "WA", f"WhatsApp falló: {result.get('message', result)}")
    return result


class HumanDecisionPayload(BaseModel):
    decision: str = Field(..., description="approve | reject (o aprobar | rechazar)")
    comment: str = ""


class AgentBuilderIntakePayload(BaseModel):
    message: str = Field(..., description="Texto del operador / agente UiPath")
    case_id: str | None = None
    client_name: str | None = None
    client_id: str | None = None
    ruc: str | None = None
    quote_id: str | None = None
    stage: str = "Intake"
    panel_lang: str = "en"
    trigger_webhook: bool = True


class DocumentUnderstandingPayload(BaseModel):
    case_id: str | None = None
    client_name: str | None = None
    client_id: str | None = None
    ruc: str | None = None
    quote_id: str | None = None
    incident_type: str | None = None
    severity: str | None = None
    observations: str | None = None
    text_preview: str | None = None
    stage: str = "Intake"
    panel_lang: str = "en"
    source: str = "document_understanding"


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
            "public": f"{PUBLIC_BASE_URL}/dashboard",
            "public_case_pattern": f"{PUBLIC_BASE_URL}/dashboard?case_id={{case_id}}",
            "case_app_pattern": f"{PUBLIC_BASE_URL}/apps/case/{{case_id}}",
        },
        "bonus_endpoints": {
            "agent_builder_intake": f"{PUBLIC_BASE_URL}/api/v1/agent-builder/intake",
            "agent_builder_openapi": f"{PUBLIC_BASE_URL}/api/v1/agent-builder/openapi",
            "document_understanding_ingest": f"{PUBLIC_BASE_URL}/api/v1/document-understanding/ingest",
            "test_manager_run": f"{PUBLIC_BASE_URL}/api/v1/test-manager/run",
            "test_manager_junit": f"{PUBLIC_BASE_URL}/api/v1/test-manager/junit.xml",
            "apps_config": f"{PUBLIC_BASE_URL}/api/v1/apps/config",
        },
    }


@router.get("/activity")
def api_activity(limit: int = 100):
    return {"lines": list_activity(limit=limit)}


@router.post("/activity/clear")
def api_clear_activity():
    clear_activity()
    log_activity("info", "SYS", "Log de actividad limpiado")
    return {"ok": True}


@router.post("/demo/reset")
def api_demo_reset(confirm: str = Query("", description="Escribe RESET para confirmar")):
    """Limpia log en vivo y borra todos los casos Maestro en MongoDB."""
    if confirm.strip().upper() != "RESET":
        raise HTTPException(400, "Confirma con ?confirm=RESET")
    clear_activity()
    n = delete_all_cases()
    log_activity("info", "SYS", f"Reset demo — {n} casos borrados")
    return {"ok": True, "cases_deleted": n}


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


_UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def _body_preview(raw: bytes, limit: int = 120) -> str:
    text = (raw or b"").decode("utf-8", errors="replace").strip()
    if len(text) > limit:
        return text[:limit] + "…"
    return text or "(vacío)"


def _extract_fields_from_loose_json(text: str) -> dict[str, Any]:
    """Rescata campos si Maestro manda JSON casi válido (variables sin comillas, etc.)."""
    out: dict[str, Any] = {}
    for key in (
        "case_id", "CaseId", "stage", "incident_type", "severity",
        "client_name", "notes", "raw_logs", "client_id", "ruc", "quote_id",
    ):
        m = re.search(rf'["\']?{key}["\']?\s*:\s*"([^"]*)"', text, re.I)
        if m and m.group(1).strip():
            out["case_id" if key.lower() == "caseid" else key] = m.group(1).strip()
    if not out.get("case_id"):
        mu = _UUID_RE.search(text)
        if mu:
            out["case_id"] = mu.group(0)
    return out


def _parse_webhook_payload(raw: bytes, qp: dict[str, str]) -> tuple[dict[str, Any], bool]:
    """
    Devuelve (payload, body_ignored).
    body_ignored=True si el body no era JSON válido pero se rescató vía query/regex.
    """
    payload: dict[str, Any] = {}
    body_ignored = False
    stripped = raw.strip() if raw else b""
    # Maestro modo Object envía literal "[object Object]" — ignorar y usar query params
    ignored_bodies = (b"", b"{}", b"null", b"[object Object]")

    if stripped not in ignored_bodies:
        text = stripped.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            rescued = _extract_fields_from_loose_json(text)
            if rescued.get("case_id") or qp.get("case_id") or qp.get("CaseId"):
                payload = rescued
                body_ignored = True
            else:
                raise HTTPException(
                    422,
                    {
                        "detail": (
                            "JSON body invalid. Usa Plan B: case_id y stage en la URL (query) "
                            "y Body vacío o {}. O Body Raw con JSON mínimo "
                            '{"case_id":"{{caseId}}","stage":"Intake"}.'
                        ),
                        "body_preview": _body_preview(raw),
                    },
                )
        else:
            if isinstance(parsed, dict):
                payload = parsed
            elif isinstance(parsed, str) and parsed.strip():
                try:
                    payload = json.loads(parsed)
                except json.JSONDecodeError:
                    if _UUID_RE.fullmatch(parsed.strip()):
                        payload = {"case_id": parsed.strip()}
    elif stripped == b"[object Object]":
        body_ignored = True

    for key, val in qp.items():
        if key not in payload or payload.get(key) in (None, ""):
            payload[key] = val

    if not payload.get("case_id") and payload.get("CaseId"):
        payload["case_id"] = payload["CaseId"]

    return payload, body_ignored


def _is_unsubstituted_case_id(cid: str) -> bool:
    return is_placeholder_case_id(cid)


def _case_id_from_headers(headers: Any) -> str | None:
    for key in (
        "x-case-id",
        "x-maestro-case-id",
        "case-id",
        "x-uipath-case-id",
        "x-uipath-globaltrackingid",
    ):
        val = headers.get(key) or headers.get(key.replace("-", "_"))
        if val and not is_placeholder_case_id(str(val).strip()):
            return str(val).strip()
    return None


def _resolve_maestro_case_id(raw_id: str, stage: str, headers: Any) -> tuple[str, str | None]:
    """
    Devuelve (case_id_resuelto, raw_recibido_si_fue_placeholder).
    Maestro a menudo manda {{caseId}} literal — encadenamos etapas por MongoDB.
    """
    from_header = _case_id_from_headers(headers)
    if from_header:
        return from_header, raw_id if from_header != raw_id else None

    if not is_placeholder_case_id(raw_id):
        return raw_id, None

    stage_norm = stage.strip() if stage else "Intake"
    if stage_norm == "Intake":
        return str(uuid.uuid4()), raw_id

    waiting = find_case_awaiting_stage(stage_norm)
    if waiting:
        return waiting["case_id"], raw_id

    return str(uuid.uuid4()), raw_id


@router.post("/uipath-webhook")
async def uipath_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Entrada Maestro API Workflow.
    Acepta JSON en body O query ?case_id=&stage= (si Maestro manda body vacío o inválido).
    """
    qp = dict(request.query_params)
    raw = await request.body()
    payload, body_ignored = _parse_webhook_payload(raw, qp)

    raw_cid = str(payload.get("case_id") or qp.get("case_id") or qp.get("CaseId") or "").strip()
    stage_hint = str(payload.get("stage") or qp.get("stage") or "Intake")
    resolved_cid, placeholder_raw = _resolve_maestro_case_id(
        raw_cid, stage_hint, request.headers
    )
    payload["case_id"] = resolved_cid
    payload["integration_source"] = "maestro_cloud"
    if placeholder_raw:
        payload["maestro_id_unsubstituted"] = placeholder_raw
        if not payload.get("notes"):
            payload["notes"] = "source=maestro_cloud"
    elif not payload.get("notes"):
        payload["notes"] = "source=maestro_cloud"

    cid = resolved_cid
    if placeholder_raw:
        log_activity(
            "warn",
            "WEBHOOK",
            f"Maestro case_id sustituido {placeholder_raw!r} → {cid[:8]}… · stage={stage_hint}",
        )

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

    if placeholder_raw:
        result["maestro_case_id_received"] = placeholder_raw
        result["maestro_case_id_resolved"] = cid

    if body_ignored:
        log_activity("warn", "WEBHOOK", f"Body JSON ignorado; usados query params · case {cid[:8]}…")

    log_activity(
        "ok",
        "WEBHOOK",
        f"Stage {result.get('stage')} · {result.get('incident_type')} · case {result.get('case_id', '')[:8]}…",
    )

    if result.get("report_markdown"):
        background_tasks.add_task(
            _notify_operator,
            result["report_markdown"],
            result["case_id"],
        )

    from_maestro = payload.get("integration_source") == "maestro_cloud"
    if should_auto_continue(result, from_maestro_cloud=from_maestro):
        background_tasks.add_task(_auto_continue_maestro, cid, body.model_dump())

    return result


def _auto_continue_maestro(case_id: str, base_payload: dict) -> None:
    try:
        final = continue_maestro_flow(case_id, base_payload=base_payload)
        log_activity(
            "ok",
            "MAESTRO",
            f"Auto-continuación · {final.get('stage')} · "
            f"{ ' → '.join(final.get('stages_completed') or []) } · case {case_id[:8]}…",
        )
        if final.get("report_markdown"):
            _notify_operator(final["report_markdown"], case_id)
    except Exception as exc:
        log_activity("err", "MAESTRO", f"Auto-continuación falló · case {case_id[:8]}… · {exc}")


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


@router.post("/cases/{case_id}/continue-flow")
def api_continue_maestro_flow(case_id: str):
    """Completa etapas pendientes del mismo case_id (síncrono — Ollama 1–3 min)."""
    doc = get_case(case_id)
    if not doc:
        raise HTTPException(404, "Caso no encontrado")
    done = set(doc.get("stages_completed") or [])
    if len(done) >= 4:
        return {**doc, "flow": "already_complete", "message": "El caso ya tiene las 4 etapas"}

    log_activity("info", "MAESTRO", f"Continuar flujo · case {case_id[:8]}…")
    try:
        final = continue_maestro_flow(case_id, base_payload=doc.get("payload_snapshot") or {})
    except Exception as exc:
        log_activity("err", "MAESTRO", f"Continuar flujo falló · {exc}")
        raise HTTPException(500, str(exc)) from exc

    log_activity(
        "ok",
        "MAESTRO",
        f"Flujo continuado · {final.get('stage')} · "
        f"{' → '.join(final.get('stages_completed') or [])} · case {case_id[:8]}…",
    )
    return {
        **final,
        "status": "done",
        "message": "Etapas completadas" if not final.get("flow_blocked") else "Detenido por gate operativo",
    }


@router.get("/cases/{case_id}/public-urls")
def api_case_public_urls(case_id: str):
    doc = get_case(case_id)
    if not doc:
        raise HTTPException(404, "Caso no encontrado")
    return {"case_id": case_id, "urls": case_public_urls(case_id)}


@router.get("/agent-builder/openapi")
def api_agent_builder_openapi():
    """OpenAPI fragment para HTTP tool en Agent Builder."""
    return {
        "openapi": "3.0.0",
        "info": {"title": "PC Doctor Agent Builder Tools", "version": "1.0.0"},
        "servers": [{"url": PUBLIC_BASE_URL.rstrip("/")}],
        "paths": {
            "/api/v1/agent-builder/intake": {
                "post": {
                    "summary": "Classify intake and open Maestro case",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["message"],
                                    "properties": {
                                        "message": {"type": "string"},
                                        "trigger_webhook": {"type": "boolean", "default": True},
                                        "panel_lang": {"type": "string", "default": "en"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Classification + webhook result"}},
                }
            },
            "/api/v1/uipath-webhook": {
                "post": {
                    "summary": "Maestro webhook direct",
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    },
                }
            },
        },
    }


@router.post("/agent-builder/intake")
def api_agent_builder_intake(body: AgentBuilderIntakePayload):
    """Entrada Agent Builder — clasifica + opcionalmente dispara webhook Maestro."""
    try:
        return agent_intake_to_webhook(
            body.message,
            case_id=body.case_id,
            client_name=body.client_name,
            client_id=body.client_id,
            ruc=body.ruc,
            quote_id=body.quote_id,
            stage=body.stage,
            panel_lang=normalize_lang(body.panel_lang),
            trigger_webhook=body.trigger_webhook,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/agent-builder/classify")
def api_agent_builder_classify(body: AgentBuilderIntakePayload):
    """Solo clasificación (sin webhook) — pruebas Agent Builder."""
    try:
        return classify_intake(body.message)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/document-understanding/schema")
def api_du_schema():
    return {
        "fields": ["client_name", "ruc", "quote_id", "observations", "incident_type", "severity"],
        "max_pages": 2,
        "ingest_url": f"{PUBLIC_BASE_URL}/api/v1/document-understanding/ingest",
        "upload_url": f"{PUBLIC_BASE_URL}/api/v1/document-understanding/upload",
    }


@router.post("/document-understanding/ingest")
def api_du_ingest_json(body: DocumentUnderstandingPayload):
    """Ingest campos extraídos por UiPath Document Understanding."""
    try:
        return ingest_document(extracted=body.model_dump(), case_id=body.case_id, stage=body.stage, panel_lang=normalize_lang(body.panel_lang), source=body.source)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/document-understanding/upload")
async def api_du_upload(
    file: UploadFile = File(...),
    case_id: str | None = None,
    panel_lang: str = Query("en"),
):
    """Upload PDF ≤2 páginas — extracción local + webhook (demo DU bridge)."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Solo PDF")
    raw = await file.read()
    if len(raw) > 5_000_000:
        raise HTTPException(400, "PDF demasiado grande (max 5MB)")
    try:
        fields = extract_pdf_fields(raw)
        return ingest_document(pdf_bytes=raw, extracted=fields, case_id=case_id, panel_lang=normalize_lang(panel_lang))
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/apps/config")
def api_apps_config():
    return build_apps_config()


@router.get("/apps/case/{case_id}")
def api_apps_case(case_id: str):
    try:
        return get_case_app_payload(case_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/test-manager/results")
def api_test_manager_results():
    data = load_last_results()
    if not data:
        data = run_test_suite()
    return data


@router.post("/test-manager/run")
def api_test_manager_run():
    return run_test_suite()


@router.get("/test-manager/junit.xml")
def api_test_manager_junit():
    data = load_last_results()
    if not data:
        data = run_test_suite()
    xml = build_junit_xml(data)
    return PlainTextResponse(xml, media_type="application/xml")


@router.get("/test-manager/junit-file")
def api_test_manager_junit_file():
    if not JUNIT_PATH.is_file():
        run_test_suite()
    if not JUNIT_PATH.is_file():
        raise HTTPException(404, "JUnit no generado")
    return FileResponse(JUNIT_PATH, media_type="application/xml", filename="PCDoctorMaestro.xml")


@router.get("/platform-events")
def api_platform_events(limit: int = 30):
    from uipath_copilot.platform_events import recent_events

    return {"events": recent_events(limit=limit)}


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


@router.post("/platform-scorecard/verify-all")
def api_platform_verify_all(lang: str = Query("es")):
    """Ejecuta verificaciones mínimas (Test Manager, Agent Builder, DU, Case App) y devuelve scorecard."""
    from uipath_copilot.activity_log import log_activity

    log_activity("info", "SCORECARD", "Verificación 12/12 solicitada desde panel")
    return run_platform_verification(panel_lang=normalize_lang(lang))


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
