"""Consultas operativas — datos reales MongoDB PC Doctor (clientes y cotizaciones distintos)."""

from __future__ import annotations

import uuid
from typing import Any

from tools.mongo import get_db
from uipath_copilot.activity_log import log_activity
from uipath_copilot.i18n import JURY_CONSULTATION_IDS, normalize_lang, t as i18n_t
from uipath_copilot.processor import STAGES, has_blocking_gate, process_webhook


def _client_by_name_fragment(fragment: str) -> dict[str, Any] | None:
    db = get_db()
    return db.clients.find_one(
        {"name": {"$regex": fragment, "$options": "i"}},
        {"_id": 0, "client_id": 1, "name": 1, "ruc": 1},
    )


def _quote_for_client(client_id: str) -> dict[str, Any] | None:
    return get_db().quotes.find_one({"client_id": client_id}, {"_id": 0, "quote_id": 1, "total": 1, "client_id": 1})


def build_consultation_catalog() -> list[dict[str, Any]]:
    """Catálogo de consultas operativas — cada una anclada a cliente/cotización real."""
    db = get_db()
    catalog: list[dict[str, Any]] = []

    la_pradera = _client_by_name_fragment("La Pradera")
    q_pradera = _quote_for_client(la_pradera["client_id"]) if la_pradera else None
    if la_pradera and q_pradera:
        catalog.append(
            {
                "id": "la_pradera_quote_pdf",
                "title_en": "La Pradera — quote blocked (PDF-first gate)",
                "title_es": "Urbanización La Pradera — cotización bloqueada (gate PDF)",
                "incident_type": "quote_gate_blocked",
                "severity": "medium",
                "client_name": la_pradera["name"],
                "client_id": la_pradera["client_id"],
                "quote_id": q_pradera["quote_id"],
                "expected_gates": ["db38_matematica", "pdf_first"],
                "description_en": "Real quote ${} — DB38 OK but PDF-first document missing.".format(q_pradera.get("total")),
                "description_es": "Cotización real ${} — DB38 OK pero falta PDF-first.".format(q_pradera.get("total")),
            }
        )

    probalsa = _client_by_name_fragment("PROBALSA")
    if probalsa:
        catalog.append(
            {
                "id": "probalsa_duplicate",
                "title_en": "PROBALSA — duplicate client (RUC)",
                "title_es": "PROBALSA — cliente duplicado (RUC)",
                "incident_type": "client_duplicate",
                "severity": "high",
                "client_name": probalsa["name"],
                "client_id": probalsa["client_id"],
                "ruc": probalsa.get("ruc"),
                "expected_gates": ["anti_duplicacion_cliente"],
                "description_en": "Re-registration attempt with existing corporate RUC in MongoDB.",
                "description_es": "Intento de re-alta con RUC corporativo ya indexado.",
            }
        )

    inner = _client_by_name_fragment("InnerChispa")
    if inner:
        catalog.append(
            {
                "id": "innerchispa_field",
                "title_en": "InnerChispa — post-inspection review",
                "title_es": "InnerChispa — revisión post-inspección",
                "incident_type": "field_inspection_exception",
                "severity": "medium",
                "client_name": inner["name"],
                "client_id": inner["client_id"],
                "ruc": inner.get("ruc"),
                "expected_gates": ["hub_first", "mongodb_live"],
                "description_en": "Operational client — hub and MongoDB validation.",
                "description_es": "Cliente operativo — validación hub y MongoDB.",
            }
        )

    dominguez = _client_by_name_fragment("DOMINGUEZ")
    if dominguez:
        catalog.append(
            {
                "id": "dominguez_residential",
                "title_en": "Domínguez Gómez — residential inspection",
                "title_es": "Domínguez Gómez — inspección residencial",
                "incident_type": "field_inspection_exception",
                "severity": "medium",
                "client_name": dominguez["name"],
                "client_id": dominguez["client_id"],
                "ruc": dominguez.get("ruc"),
                "expected_gates": ["anti_duplicacion_cliente", "hub_first"],
                "description_en": "Individual client with RUC — field exception workflow.",
                "description_es": "Cliente residencial con RUC — flujo excepción campo.",
            }
        )

    rommy = _client_by_name_fragment("Rommy Moeller")
    if rommy:
        catalog.append(
            {
                "id": "rommy_report_quality",
                "title_en": "Rommy Moeller — report quality gate",
                "title_es": "Rommy Moeller — calidad de informe",
                "incident_type": "report_quality",
                "severity": "high",
                "client_name": rommy["name"],
                "client_id": rommy["client_id"],
                "ruc": rommy.get("ruc"),
                "expected_gates": ["anti_placeholders"],
                "description_en": "Technical report placeholder scan before delivery.",
                "description_es": "Escaneo placeholders en informe técnico.",
            }
        )

    if not catalog:
        c = db.clients.find_one({}, {"_id": 0, "client_id": 1, "name": 1, "ruc": 1})
        if c:
            catalog.append(
                {
                    "id": "fallback_field",
                    "title_en": "Field inspection (fallback)",
                    "title_es": "Inspección campo (fallback)",
                    "incident_type": "field_inspection_exception",
                    "severity": "medium",
                    "client_name": c.get("name"),
                    "client_id": c.get("client_id"),
                    "ruc": c.get("ruc"),
                }
            )

    hints = {
        "dominguez_residential": {
            "flow_hint_en": "Full 4-stage flow — all gates pass",
            "flow_hint_es": "Flujo completo 4 etapas — todos los gates OK",
        },
        "la_pradera_quote_pdf": {
            "flow_hint_en": "Stops at Intake — PDF-first gate (real block)",
            "flow_hint_es": "Se detiene en Intake — gate PDF-first real",
        },
        "probalsa_duplicate": {
            "flow_hint_en": "Stops at Intake — duplicate RUC detected",
            "flow_hint_es": "Se detiene en Intake — RUC duplicado detectado",
        },
        "rommy_report_quality": {
            "flow_hint_en": "Stops at Intake — @today placeholder in report",
            "flow_hint_es": "Se detiene en Intake — placeholder @today en informe",
        },
    }
    jury = [c for c in catalog if c["id"] in JURY_CONSULTATION_IDS]
    for item in jury:
        item.update(hints.get(item["id"], {}))
    return jury if jury else catalog


def get_consultation(consultation_id: str) -> dict[str, Any] | None:
    for item in build_consultation_catalog():
        if item["id"] == consultation_id:
            return item
    return None


def build_webhook_payload(
    consultation_id: str,
    *,
    case_id: str | None = None,
    stage: str = "Intake",
    panel_lang: str = "es",
) -> dict[str, Any]:
    sc = get_consultation(consultation_id)
    if not sc:
        raise ValueError(f"Consulta desconocida: {consultation_id}")

    cid = case_id or str(uuid.uuid4())
    logs = {
        "la_pradera_quote_pdf": f"Gate PDF-first en cotización {sc.get('quote_id')} — cliente {sc['client_name']}",
        "probalsa_duplicate": f"Alta duplicada en campo — RUC {sc.get('ruc')} {sc['client_name']}",
        "innerchispa_field": f"Post-inspección InnerChispa — validar hub y cotizaciones",
        "dominguez_residential": f"Visita residencial {sc['client_name']} — revisión post-SOP",
        "rommy_report_quality": f"Informe técnico pendiente: fecha @today — cliente {sc['client_name']}",
    }
    return {
        "case_id": cid,
        "stage": stage,
        "incident_type": sc["incident_type"],
        "severity": sc.get("severity", "medium"),
        "client_name": sc.get("client_name"),
        "client_id": sc.get("client_id"),
        "ruc": sc.get("ruc"),
        "quote_id": sc.get("quote_id"),
        "raw_logs": logs.get(consultation_id, f"Consulta operativa {consultation_id}"),
        "notes": f"consultation_id={consultation_id}",
        "scenario_id": consultation_id,
        "scenario_title_en": sc.get("title_en"),
        "scenario_title_es": sc.get("title_es"),
        "panel_lang": normalize_lang(panel_lang),
    }


def run_full_consultation(
    consultation_id: str, *, case_id: str | None = None, panel_lang: str = "es"
) -> dict[str, Any]:
    """Ejecuta etapas Maestro; se detiene si un gate bloqueante falla (regla operativa real)."""
    lang = normalize_lang(panel_lang)
    sc = get_consultation(consultation_id)
    if not sc:
        raise ValueError(f"Consulta desconocida: {consultation_id}")

    cid = case_id or str(uuid.uuid4())
    log_activity("info", "CONSULTA", i18n_t(lang, "flow_start", client=sc.get("client_name"), case_id=cid[:8]))

    last: dict[str, Any] = {}
    blocked = False
    for stage in STAGES:
        payload = build_webhook_payload(consultation_id, case_id=cid, stage=stage, panel_lang=lang)
        last = process_webhook(payload)
        log_activity("ok", "ETAPA", i18n_t(lang, "flow_stage_ok", stage=stage, client=sc.get("client_name"), case_id=cid[:8]))

        blocker = has_blocking_gate(last.get("findings") or [])
        if blocker and stage != "Approval":
            blocked = True
            log_activity(
                "warn",
                "BLOQUEO",
                i18n_t(
                    lang,
                    "flow_blocked",
                    stage=stage,
                    gate=blocker.get("gate", "?"),
                    case_id=cid[:8],
                ),
            )
            break

    if blocked:
        msg = i18n_t(lang, "msg_flow_blocked", stage=last.get("stage", "Intake"))
        flow = "blocked_by_gate"
    else:
        log_activity("ok", "CONSULTA", i18n_t(lang, "flow_complete", case_id=cid[:8]))
        msg = i18n_t(lang, "msg_flow_complete")
        flow = "full_4_stages"

    return {
        **last,
        "consultation_id": consultation_id,
        "flow": flow,
        "flow_blocked": blocked,
        "message": msg,
    }
