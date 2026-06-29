"""Scorecard plataforma UiPath — qué bonus está activo."""

from __future__ import annotations

from typing import Any

from tools.evolution_api import evolution_available
from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.action_center_client import action_center_status
from uipath_copilot.case_store import list_cases
from uipath_copilot.maestro_client import maestro_status
from uipath_copilot.platform_events import has_event, recent_events
from uipath_copilot.settings import PUBLIC_BASE_URL


def build_platform_scorecard() -> dict[str, Any]:
    ms = maestro_status()
    cases = list_cases(limit=5)
    try:
        clients = get_db().clients.count_documents({})
        quotes = get_db().quotes.count_documents({})
    except Exception:
        clients = quotes = 0

    last_tests = None
    try:
        from uipath_copilot.test_manager import load_last_results

        last_tests = load_last_results()
    except Exception:
        pass

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
            "points": "Panel operativo",
        },
        {
            "id": "agent_builder",
            "name": "Agent Builder (cloud)",
            "met": has_event("agent_builder"),
            "evidence": f"{PUBLIC_BASE_URL}/api/v1/agent-builder/intake",
            "points": "Bonus LLM UiPath",
            "setup": f"HTTP tool → {PUBLIC_BASE_URL}/api/v1/agent-builder/intake",
        },
        {
            "id": "apps_case_app",
            "name": "Apps / Case App",
            "met": has_event("apps_case_app") or any(c.get("approval_status") == "approved" for c in cases),
            "evidence": f"{PUBLIC_BASE_URL}/apps/case/{{case_id}}",
            "points": "UX jurado",
            "setup": f"Apps embed → {PUBLIC_BASE_URL}/apps/case/{{caseId}}",
        },
        {
            "id": "test_manager",
            "name": "Test Manager",
            "met": bool(last_tests and last_tests.get("failed", 1) == 0),
            "evidence": f"{PUBLIC_BASE_URL}/api/v1/test-manager/junit.xml",
            "points": "Calidad",
            "setup": "POST /api/v1/test-manager/run → adjuntar JUnit",
        },
        {
            "id": "document_understanding",
            "name": "Document Understanding",
            "met": has_event("document_understanding"),
            "evidence": f"{PUBLIC_BASE_URL}/api/v1/document-understanding/upload",
            "points": "Bonus profundo",
            "setup": f"DU → POST {PUBLIC_BASE_URL}/api/v1/document-understanding/ingest",
        },
    ]

    met_count = sum(1 for b in bonuses if b["met"])
    return {
        "public_base_url": PUBLIC_BASE_URL,
        "public_urls": {
            "dashboard": f"{PUBLIC_BASE_URL}/dashboard",
            "webhook": f"{PUBLIC_BASE_URL}/api/v1/uipath-webhook",
            "case_app": f"{PUBLIC_BASE_URL}/apps/case/{{case_id}}",
            "agent_builder": f"{PUBLIC_BASE_URL}/api/v1/agent-builder/intake",
            "test_manager_junit": f"{PUBLIC_BASE_URL}/api/v1/test-manager/junit.xml",
            "document_understanding": f"{PUBLIC_BASE_URL}/api/v1/document-understanding/upload",
        },
        "uipath_maestro": ms,
        "action_center": action_center_status(),
        "bonuses_met": met_count,
        "bonuses_total": len(bonuses),
        "score_pct": round(100 * met_count / len(bonuses)),
        "bonuses": bonuses,
        "recent_platform_events": recent_events(limit=8),
        "last_test_run": last_tests,
        "next_steps": [
            "Agent Builder: crear agente + HTTP tool (ver data/uipath_agent_builder/)",
            f"Apps: embed {PUBLIC_BASE_URL}/apps/case/{{caseId}}",
            f"Test Manager: curl -X POST {PUBLIC_BASE_URL}/api/v1/test-manager/run",
            f"DU: subir PDF a {PUBLIC_BASE_URL}/api/v1/document-understanding/upload",
        ],
    }
