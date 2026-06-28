"""Scorecard plataforma UiPath — qué bonus está activo."""

from __future__ import annotations

from typing import Any

from tools.evolution_api import evolution_available
from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.action_center_client import action_center_status
from uipath_copilot.case_store import list_cases
from uipath_copilot.maestro_client import maestro_status
from uipath_copilot.settings import PUBLIC_BASE_URL


def build_platform_scorecard() -> dict[str, Any]:
    ms = maestro_status()
    cases = list_cases(limit=5)
    try:
        clients = get_db().clients.count_documents({})
        quotes = get_db().quotes.count_documents({})
    except Exception:
        clients = quotes = 0

    bonuses = [
        {
            "id": "maestro_case",
            "name": "Maestro Case + webhook",
            "met": ms.get("reachable") and len(cases) > 0,
            "evidence": f"{len(cases)} casos en MongoDB" if cases else "Dispara Start Job",
            "points": "Track 1 obligatorio",
        },
        {
            "id": "api_workflows",
            "name": "API Workflows (Intake HTTP)",
            "met": len(cases) > 0,
            "evidence": "Caso UArtes / field_inspection procesado" if cases else "Configura Intake",
            "points": "Platform Usage",
        },
        {
            "id": "coded_agent_python",
            "name": "Coded Agent Python (:8097)",
            "met": True,
            "evidence": "FastAPI + gates + OData",
            "points": "Platform Usage",
        },
        {
            "id": "coding_agents_cursor",
            "name": "UiPath for Coding Agents (Cursor)",
            "met": True,
            "evidence": "Repo GitHub + AGENTS.md",
            "points": "Bonus jurado",
        },
        {
            "id": "ollama_sovereign",
            "name": "Ollama local (soberanía)",
            "met": ollama_available(),
            "evidence": "Análisis en /api/v1/cases",
            "points": "Diferenciador",
        },
        {
            "id": "mongodb_real",
            "name": "MongoDB PC Doctor real",
            "met": clients > 0,
            "evidence": f"{clients} clientes, {quotes} cotizaciones",
            "points": "Problema negocio real",
        },
        {
            "id": "whatsapp_hitl",
            "name": "WhatsApp HITL (Evolution)",
            "met": evolution_available(),
            "evidence": "Evolution :8082",
            "points": "HITL omnicanal",
        },
        {
            "id": "action_center_api",
            "name": "Action Center (User task Approval)",
            "met": any(
                c.get("approval_status") in ("approved", "rejected") for c in cases
            ),
            "evidence": "User task en Maestro Approval + /dashboard",
            "points": "HITL UiPath cloud",
        },
        {
            "id": "admin_maestro_ui",
            "name": "Admin Refine :5173/maestro",
            "met": True,
            "evidence": "Proxy /uipath-copilot",
            "points": "Demo visual",
        },
        {
            "id": "agent_builder",
            "name": "Agent Builder (cloud)",
            "met": False,
            "evidence": "Pendiente — ver ROADMAP_BONUS_COMMUNITY.md B2",
            "points": "Bonus LLM UiPath",
        },
        {
            "id": "apps_case_app",
            "name": "Apps / Case App",
            "met": False,
            "evidence": "Pendiente — ver roadmap B3",
            "points": "UX jurado",
        },
        {
            "id": "test_manager",
            "name": "Test Manager",
            "met": False,
            "evidence": "Ejecutar hackathon_smoke_test.sh → evidencia",
            "points": "Calidad",
        },
        {
            "id": "document_understanding",
            "name": "Document Understanding",
            "met": False,
            "evidence": "PDF ≤2 pág → webhook",
            "points": "Bonus profundo",
        },
    ]

    met_count = sum(1 for b in bonuses if b["met"])
    return {
        "public_base_url": PUBLIC_BASE_URL,
        "uipath_maestro": ms,
        "action_center": action_center_status(),
        "bonuses_met": met_count,
        "bonuses_total": len(bonuses),
        "score_pct": round(100 * met_count / len(bonuses)),
        "bonuses": bonuses,
        "next_steps": [
            "Maestro Approval → User task (Action Center)",
            "Agent Builder → HTTP tool al webhook",
            "Apps Case App → aprobación móvil",
            "Test Manager → adjuntar hackathon_smoke_test.sh",
        ],
    }
