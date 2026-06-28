"""Action Center — tareas humanas vía Orchestrator API."""

from __future__ import annotations

from typing import Any

import requests

from uipath_copilot.maestro_client import get_access_token
from uipath_copilot.settings import (
    OPERATOR_WHATSAPP,
    PUBLIC_BASE_URL,
    UIPATH_BASE_URL,
    UIPATH_ORG_UNIT_ID,
)


def _orchestrator_headers(token: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if UIPATH_ORG_UNIT_ID:
        headers["X-UIPATH-OrganizationUnitId"] = str(UIPATH_ORG_UNIT_ID)
    return headers


def create_hitl_task(
    *,
    case_id: str,
    title: str,
    description: str,
    priority: str = "High",
) -> dict[str, Any]:
    """
    Crea tarea en Action Center (Orchestrator Tasks API).
    Requiere scope OR.Tasks u OR.Tasks.Create en External Application.
    """
    if not UIPATH_BASE_URL or not UIPATH_ORG_UNIT_ID:
        return {"ok": False, "skipped": True, "reason": "UIPATH_BASE_URL o ORG_UNIT_ID vacío"}

    token = get_access_token()
    url = (
        f"{UIPATH_BASE_URL}/orchestrator_/odata/Tasks/"
        "UiPath.Server.Configuration.OData.CreateTask"
    )
    body = {
        "taskData": {
            "Title": title[:128],
            "Description": (description + f"\n\nCaso: {case_id}\nPanel: {PUBLIC_BASE_URL}/api/v1/cases/{case_id}")[
                :2000
            ],
            "Priority": priority,
            "CatalogName": "PCDoctorMaestro",
        }
    }
    try:
        r = requests.post(url, headers=_orchestrator_headers(token), json=body, timeout=45)
        data = r.json() if r.text else {}
        return {"ok": r.ok, "http_status": r.status_code, "data": data}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def action_center_status() -> dict[str, Any]:
    return {
        "org_unit_id": UIPATH_ORG_UNIT_ID or None,
        "operator_whatsapp": bool(OPERATOR_WHATSAPP),
        "note": "Añade OR.Tasks en External Application para crear tareas HITL",
    }
