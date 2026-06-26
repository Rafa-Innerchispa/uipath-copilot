"""Procesamiento real de casos — MongoDB PC Doctor + gates + Ollama."""

from __future__ import annotations

import json
import re
from typing import Any

from tools.gates import check_duplicate_client, check_hub_first, check_placeholders
from tools.mongo import get_db
from tools.ollama_chat import ollama_available, ollama_chat
from uipath_copilot.case_store import append_event, save_case
from uipath_copilot.maestro_client import transition_case
from uipath_copilot.settings import OLLAMA_MODEL_ANALYSIS, OLLAMA_MODEL_CODER


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


def _build_report_markdown(case_id: str, incident: str, findings: list[dict], analysis: str) -> str:
    lines = [
        f"# Caso Maestro — PC Doctor",
        "",
        f"- **case_id:** `{case_id}`",
        f"- **incident_type:** `{incident}`",
        "",
        "## Hallazgos (datos reales)",
        "",
    ]
    for f in findings:
        gate = f.get("gate", "check")
        status = "OK" if f.get("passed") else "BLOQUEO"
        lines.append(f"- [{status}] **{gate}**: {f.get('message', '')}")
    lines.extend(["", "## Análisis copiloto (Ollama local)", "", analysis.strip(), ""])
    return "\n".join(lines)


def _run_real_checks(incident: str, payload: dict[str, Any]) -> list[dict]:
    findings: list[dict] = []
    db = get_db()

    ruc = payload.get("ruc") or payload.get("client_ruc")
    name = payload.get("client_name")
    client_id = payload.get("client_id")

    if incident in ("client_duplicate", "field_inspection_exception") and (ruc or name):
        findings.append(check_duplicate_client(ruc=ruc, name=name))

    if client_id or ruc:
        cid = client_id
        if not cid and ruc:
            hit = db.clients.find_one({"ruc": ruc}, {"client_id": 1, "_id": 0})
            cid = hit.get("client_id") if hit else None
        if cid:
            findings.append(check_hub_first(cid))

    if incident == "quote_gate_blocked":
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
                    "message": "No hay cotizaciones en MongoDB — crear una inspección real primero",
                }
            )

    if incident == "report_quality":
        sample = _load_recent_report_export() or (payload.get("raw_logs") or "")
        findings.append(check_placeholders(sample, field="informe"))

    client_count = db.clients.count_documents({})
    findings.append(
        {
            "gate": "mongodb_live",
            "passed": client_count > 0,
            "severity": "info",
            "message": f"MongoDB pcdoctor_swarm — {client_count} clientes indexados",
        }
    )
    return findings


def _next_maestro_action(stage: str, needs_human: bool) -> str | None:
    if needs_human:
        return "ToApproval"
    mapping = {
        "Intake": "ToInvestigation",
        "Investigation": "ToRemediation",
        "Remediation": "Complete",
    }
    return mapping.get(stage)


def process_webhook(payload: dict[str, Any]) -> dict[str, Any]:
    case_id = str(payload.get("case_id") or payload.get("CaseId") or "").strip()
    if not case_id:
        raise ValueError("case_id es obligatorio")

    stage = payload.get("stage") or payload.get("current_stage") or "Intake"
    severity = payload.get("severity") or "medium"
    incident = _detect_incident(payload)

    append_event(case_id, {"type": "webhook_received", "stage": stage, "incident": incident})

    findings = _run_real_checks(incident, payload)
    needs_human = any(not f.get("passed") and f.get("severity") in ("bloqueante", "alta") for f in findings)

    context = json.dumps(
        {
            "incident_type": incident,
            "severity": severity,
            "stage": stage,
            "payload": {k: payload.get(k) for k in ("client_name", "ruc", "client_id", "raw_logs", "notes")},
            "findings": findings,
        },
        ensure_ascii=False,
        indent=2,
    )
    analysis = ""
    if ollama_available():
        analysis = _analyze_with_ollama(
            f"Analiza este caso operativo PC Doctor y propone remediación:\n\n{context}"
        )
    else:
        analysis = "Ollama no disponible en :11434 — gates MongoDB ejecutados igualmente."

    report_md = _build_report_markdown(case_id, incident, findings, analysis)

    maestro_action = _next_maestro_action(stage, needs_human)
    transition_result = None
    if maestro_action:
        transition_result = transition_case(case_id, maestro_action, comment=incident)

    record = save_case(
        {
            "case_id": case_id,
            "stage": stage,
            "incident_type": incident,
            "severity": severity,
            "needs_human": needs_human,
            "findings": findings,
            "analysis": analysis,
            "report_markdown": report_md,
            "maestro_transition": transition_result,
            "payload_snapshot": payload,
            "events": [{"type": "processed", "stage": stage}],
        }
    )

    return {
        "case_id": case_id,
        "incident_type": incident,
        "needs_human": needs_human,
        "findings": findings,
        "report_markdown": report_md,
        "maestro_transition": transition_result,
        "record": record,
    }
