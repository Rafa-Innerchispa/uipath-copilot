"""Escenarios demo diversos — datos reales MongoDB PC Doctor (no siempre UArtes)."""

from __future__ import annotations

import uuid
from typing import Any

from tools.mongo import get_db


def _client_by_name_fragment(fragment: str) -> dict[str, Any] | None:
    db = get_db()
    return db.clients.find_one(
        {"name": {"$regex": fragment, "$options": "i"}},
        {"_id": 0, "client_id": 1, "name": 1, "ruc": 1},
    )


def _client_by_id(client_id: str) -> dict[str, Any] | None:
    return get_db().clients.find_one({"client_id": client_id}, {"_id": 0, "client_id": 1, "name": 1, "ruc": 1})


def _quote_for_client(client_id: str) -> dict[str, Any] | None:
    return get_db().quotes.find_one({"client_id": client_id}, {"_id": 0, "quote_id": 1, "total": 1, "client_id": 1})


def build_scenario_catalog() -> list[dict[str, Any]]:
    """Catálogo de consultas demo — cada una anclada a cliente/cotización real."""
    db = get_db()
    scenarios: list[dict[str, Any]] = []

    la_pradera = _client_by_name_fragment("La Pradera")
    q_pradera = _quote_for_client(la_pradera["client_id"]) if la_pradera else None
    if la_pradera and q_pradera:
        scenarios.append(
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

    torres = _client_by_name_fragment("Torres de la Merced")
    q_torres = _quote_for_client(torres["client_id"]) if torres else None
    if torres and q_torres:
        scenarios.append(
            {
                "id": "torres_merced_quote",
                "title_en": "Torres de la Merced — send quote exception",
                "title_es": "Edificio Torres de la Merced — excepción envío cotización",
                "incident_type": "quote_gate_blocked",
                "severity": "high",
                "client_name": torres["name"],
                "client_id": torres["client_id"],
                "quote_id": q_torres["quote_id"],
                "expected_gates": ["pdf_first"],
                "description_en": "Building client with RUC — quote ready-to-send gates.",
                "description_es": "Cliente edificio con RUC — gates listo-para-enviar.",
            }
        )

    probalsa = _client_by_name_fragment("PROBALSA")
    if probalsa:
        scenarios.append(
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
        scenarios.append(
            {
                "id": "innerchispa_field",
                "title_en": "InnerChispa Demo — post-inspection review",
                "title_es": "Cliente Demo InnerChispa — revisión post-inspección",
                "incident_type": "field_inspection_exception",
                "severity": "medium",
                "client_name": inner["name"],
                "client_id": inner["client_id"],
                "ruc": inner.get("ruc"),
                "expected_gates": ["hub_first", "mongodb_live"],
                "description_en": "Hackathon demo client — hub and MongoDB validation.",
                "description_es": "Cliente demo hackathon — validación hub y MongoDB.",
            }
        )

    dominguez = _client_by_name_fragment("DOMINGUEZ")
    if dominguez:
        scenarios.append(
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
        scenarios.append(
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

    if not scenarios:
        c = db.clients.find_one({}, {"_id": 0, "client_id": 1, "name": 1, "ruc": 1})
        if c:
            scenarios.append(
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
    return scenarios


def get_scenario(scenario_id: str) -> dict[str, Any] | None:
    for s in build_scenario_catalog():
        if s["id"] == scenario_id:
            return s
    return None


def build_webhook_payload(scenario_id: str, *, case_id: str | None = None, stage: str = "Intake") -> dict[str, Any]:
    sc = get_scenario(scenario_id)
    if not sc:
        raise ValueError(f"Escenario desconocido: {scenario_id}")

    cid = case_id or str(uuid.uuid4())
    logs = {
        "la_pradera_quote_pdf": f"Gate PDF-first en cotización {sc.get('quote_id')} — cliente {sc['client_name']}",
        "torres_merced_quote": f"Cotización {sc.get('quote_id')} Torres de la Merced — listo para enviar bloqueado",
        "probalsa_duplicate": f"Alta duplicada en campo — RUC {sc.get('ruc')} {sc['client_name']}",
        "innerchispa_field": f"Post-inspección InnerChispa demo — validar hub y cotizaciones",
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
        "raw_logs": logs.get(scenario_id, f"Demo scenario {scenario_id}"),
        "notes": f"scenario_id={scenario_id}",
        "scenario_id": scenario_id,
        "scenario_title_en": sc.get("title_en"),
        "scenario_title_es": sc.get("title_es"),
    }
