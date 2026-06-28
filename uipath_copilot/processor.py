"""Procesamiento real de casos — MongoDB PC Doctor + gates + Ollama por etapa Maestro."""

from __future__ import annotations

import json
from typing import Any

from tools.gates import (
    check_duplicate_client,
    check_hub_first,
    check_placeholders,
    run_ready_to_send,
)
from tools.mongo import get_db
from tools.ollama_chat import ollama_available, ollama_chat
from uipath_copilot.action_center_client import create_hitl_task
from uipath_copilot.activity_log import log_activity
from uipath_copilot.case_store import append_event, get_case, save_case
from uipath_copilot.maestro_client import maestro_handoff_note
from uipath_copilot.settings import OLLAMA_MODEL_ANALYSIS, OLLAMA_MODEL_CODER

STAGES = ("Intake", "Investigation", "Remediation", "Approval")


def _load_recent_quote() -> dict[str, Any] | None:
    db = get_db()
    return db.quotes.find_one({}, {"_id": 0}, sort=[("created_at", -1)])


def _load_recent_report_export() -> str | None:
    from pathlib import Path

    from config import EXPORTS_DIR

    exports = sorted(Path(EXPORTS_DIR).glob("PCD-RPT-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if exports:
        return exports[0].read_text(encoding="utf-8")[:4000]
    return None


def _analyze_with_ollama(context: str, *, coder: bool = False) -> str:
    model = OLLAMA_MODEL_CODER if coder else OLLAMA_MODEL_ANALYSIS
    return ollama_chat(
        [
            {
                "role": "system",
                "content": (
                    "Eres copiloto operativo PC Doctor S.A. Responde en español, "
                    "Markdown limpio, acciones concretas. Sin placeholders inventados."
                ),
            },
            {"role": "user", "content": context},
        ],
        model=model,
        timeout=180,
    )


def _detect_incident(payload: dict[str, Any]) -> str:
    explicit = (payload.get("incident_type") or "").strip()
    if explicit:
        return explicit
    logs = (payload.get("raw_logs") or payload.get("notes") or "").lower()
    if "duplic" in logs or "ruc" in logs:
        return "client_duplicate"
    if "cotiz" in logs or "quote" in logs or "db38" in logs:
        return "quote_gate_blocked"
    if "hub" in logs:
        return "hub_missing"
    if "placeholder" in logs or "@today" in logs:
        return "report_quality"
    return "field_inspection_exception"


def _build_report_markdown(case_id: str, incident: str, findings: list[dict], analysis: str, stage: str) -> str:
    lines = [
        f"# Caso Maestro — PC Doctor ({stage})",
        "",
        f"- **case_id:** `{case_id}`",
        f"- **incident_type:** `{incident}`",
        f"- **etapa:** `{stage}`",
        "",
        "## Hallazgos (datos reales)",
        "",
    ]
    for f in findings:
        gate = f.get("gate", "check")
        status = "OK" if f.get("passed") else "BLOQUEO"
        lines.append(f"- [{status}] **{gate}**: {f.get('message', '')}")
    lines.extend(["", f"## Análisis copiloto — {stage}", "", analysis.strip(), ""])
    return "\n".join(lines)


def _run_real_checks(incident: str, payload: dict[str, Any]) -> list[dict]:
    findings: list[dict] = []
    db = get_db()

    ruc = payload.get("ruc") or payload.get("client_ruc")
    name = payload.get("client_name")
    client_id = payload.get("client_id")

    if incident == "client_duplicate" and (ruc or name):
        findings.append(check_duplicate_client(ruc=ruc, name=name))
    elif incident == "field_inspection_exception":
        if payload.get("client_id"):
            c = db.clients.find_one({"client_id": payload["client_id"]}, {"_id": 0, "name": 1, "ruc": 1})
            findings.append(
                {
                    "gate": "client_known",
                    "passed": True,
                    "severity": "info",
                    "message": f"Re-inspección cliente existente: {c.get('name') if c else payload.get('client_name')}",
                }
            )
        elif ruc or name:
            findings.append(check_duplicate_client(ruc=ruc, name=name))

    if client_id or ruc:
        cid = client_id
        if not cid and ruc:
            hit = db.clients.find_one({"ruc": ruc}, {"client_id": 1, "_id": 0})
            cid = hit.get("client_id") if hit else None
        if cid:
            findings.append(check_hub_first(cid))

    if incident == "quote_gate_blocked":
        quote_id = payload.get("quote_id")
        client_id = payload.get("client_id")
        if quote_id:
            ready = run_ready_to_send(quote_id, client_id)
            findings.extend(ready["gates"])
            findings.append(
                {
                    "gate": "quote_ready_to_send",
                    "passed": ready["ready"],
                    "severity": "bloqueante" if not ready["ready"] else "info",
                    "message": f"Cotización {quote_id} — {'LISTO' if ready['ready'] else f'{ready['blocking_count']} bloqueo(s)'}",
                    "quote_id": quote_id,
                }
            )
        else:
            quote = _load_recent_quote()
            if quote:
                findings.append(
                    {
                        "gate": "quote_snapshot",
                        "passed": True,
                        "severity": "info",
                        "message": f"Cotización reciente {quote.get('quote_id', '?')} total={quote.get('total', '?')}",
                        "quote_id": quote.get("quote_id"),
                    }
                )
            else:
                findings.append(
                    {
                        "gate": "quote_snapshot",
                        "passed": False,
                        "severity": "alta",
                        "message": "No hay cotizaciones en MongoDB — incluir quote_id en payload",
                    }
                )

    if incident == "report_quality":
        sample = _load_recent_report_export() or (payload.get("raw_logs") or "")
        findings.append(check_placeholders(sample, field="informe"))

    client_count = db.clients.count_documents({})
    quote_count = db.quotes.count_documents({})
    findings.append(
        {
            "gate": "mongodb_live",
            "passed": client_count > 0,
            "severity": "info",
            "message": f"MongoDB pcdoctor_swarm — {client_count} clientes, {quote_count} cotizaciones",
        }
    )
    return findings


def _needs_human(findings: list[dict], stage: str) -> bool:
    if stage == "Approval":
        return True
    return any(not f.get("passed") and f.get("severity") in ("bloqueante", "alta") for f in findings)


def _enrich_investigation(payload: dict[str, Any], findings: list[dict]) -> list[dict]:
    db = get_db()
    client_id = payload.get("client_id")
    if client_id:
        client = db.clients.find_one({"client_id": client_id}, {"_id": 0})
        if client:
            findings.append(
                {
                    "gate": "client_profile",
                    "passed": True,
                    "severity": "info",
                    "message": f"Cliente MongoDB: {client.get('name')} · RUC {client.get('ruc', '—')}",
                }
            )
            quotes = list(db.quotes.find({"client_id": client_id}, {"_id": 0, "quote_id": 1, "total": 1}).limit(3))
            if quotes:
                ids = ", ".join(q.get("quote_id", "?") for q in quotes)
                findings.append(
                    {
                        "gate": "client_quotes",
                        "passed": True,
                        "severity": "info",
                        "message": f"Cotizaciones del cliente: {ids}",
                    }
                )
    return findings


def _stage_analysis(stage: str, context: str, *, coder: bool = False) -> str:
    prompts = {
        "Intake": "Clasifica y resume el incidente operativo PC Doctor:",
        "Investigation": "Investiga a fondo con los datos MongoDB. Lista causas probables y evidencia:",
        "Remediation": "Propón remediación concreta (cotización, informe, cliente, hub). Pasos numerados:",
        "Approval": "Resume para Rafael qué debe aprobar o rechazar (1 párrafo):",
    }
    prefix = prompts.get(stage, prompts["Intake"])
    if not ollama_available():
        return "Ollama no disponible en :11434 — gates MongoDB ejecutados igualmente."
    return _analyze_with_ollama(f"{prefix}\n\n{context}", coder=coder or stage == "Remediation")


def process_webhook(payload: dict[str, Any]) -> dict[str, Any]:
    case_id = str(payload.get("case_id") or payload.get("CaseId") or "").strip()
    if not case_id:
        raise ValueError("case_id es obligatorio")

    stage = payload.get("stage") or payload.get("current_stage") or "Intake"
    if stage not in STAGES:
        stage = "Intake"

    severity = payload.get("severity") or "medium"
    incident = _detect_incident(payload)
    prior = get_case(case_id) or {}

    append_event(case_id, {"type": "webhook_received", "stage": stage, "incident": incident})
    log_activity("info", "MAESTRO", f"Webhook received · stage={stage} · {incident}")

    findings = _run_real_checks(incident, payload)
    if stage == "Investigation":
        findings = _enrich_investigation(payload, findings)

    needs_human = _needs_human(findings, stage)

    context = json.dumps(
        {
            "incident_type": incident,
            "severity": severity,
            "stage": stage,
            "prior_stages": [e.get("stage") for e in prior.get("events", []) if e.get("stage")],
            "payload": {k: payload.get(k) for k in ("client_name", "ruc", "client_id", "raw_logs", "notes")},
            "findings": findings,
        },
        ensure_ascii=False,
        indent=2,
    )
    analysis = _stage_analysis(stage, context)
    report_md = _build_report_markdown(case_id, incident, findings, analysis, stage)

    maestro_handoff = maestro_handoff_note(stage, needs_human)
    action_center_result = None
    if stage == "Approval" or (needs_human and stage == "Remediation"):
        action_center_result = create_hitl_task(
            case_id=case_id,
            title=f"[PC Doctor] Aprobación caso {case_id[:8]}…",
            description=f"Excepción `{incident}` etapa {stage} — revisar reporte en panel jurado.",
            priority="High" if severity in ("high", "critical", "alta") else "Medium",
        )

    stages_completed = list(dict.fromkeys((prior.get("stages_completed") or []) + [stage]))
    approval_status = prior.get("approval_status")
    if stage == "Approval" and not approval_status:
        approval_status = "pending"

    record = save_case(
        {
            "case_id": case_id,
            "stage": stage,
            "stages_completed": stages_completed,
            "incident_type": incident,
            "severity": severity,
            "needs_human": needs_human,
            "approval_status": approval_status,
            "client_name": payload.get("client_name") or prior.get("client_name"),
            "scenario_id": payload.get("scenario_id") or prior.get("scenario_id"),
            "scenario_title_en": payload.get("scenario_title_en") or prior.get("scenario_title_en"),
            "scenario_title_es": payload.get("scenario_title_es") or prior.get("scenario_title_es"),
            "quote_id": payload.get("quote_id") or prior.get("quote_id"),
            "findings": findings,
            "analysis": analysis,
            "report_markdown": report_md,
            "maestro_handoff": maestro_handoff,
            "action_center_task": action_center_result,
            "payload_snapshot": payload,
        }
    )
    append_event(case_id, {"type": "processed", "stage": stage, "needs_human": needs_human})

    return {
        "case_id": case_id,
        "stage": stage,
        "stages_completed": stages_completed,
        "incident_type": incident,
        "needs_human": needs_human,
        "approval_status": approval_status,
        "client_name": payload.get("client_name") or prior.get("client_name"),
        "scenario_id": payload.get("scenario_id"),
        "findings": findings,
        "report_markdown": report_md,
        "maestro_handoff": maestro_handoff,
        "action_center_task": action_center_result,
        "record": record,
        "message": (
            f"Etapa {stage} procesada. Maestro avanza en cloud cuando la tarea API Workflow termina OK."
            if stage != "Approval"
            else "Etapa Approval: completa la User task en Action Center o aprueba en panel /dashboard."
        ),
    }


def apply_human_decision(case_id: str, *, decision: str, comment: str = "") -> dict[str, Any]:
    doc = get_case(case_id)
    if not doc:
        raise ValueError("Caso no encontrado")

    decision = decision.lower().strip()
    if decision not in ("approve", "reject", "aprobar", "rechazar"):
        raise ValueError("decision debe ser approve o reject")

    approved = decision in ("approve", "aprobar")
    status = "approved" if approved else "rejected"

    append_event(
        case_id,
        {"type": "human_decision", "decision": status, "comment": comment[:500]},
    )
    record = save_case(
        {
            **doc,
            "approval_status": status,
            "needs_human": False,
            "human_comment": comment[:500],
            "stage": "Approval",
        }
    )
    return {"ok": True, "case_id": case_id, "approval_status": status, "record": record}
