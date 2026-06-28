"""Action Center — tareas humanas vía Orchestrator API o Maestro User task."""

from __future__ import annotations

import os
from typing import Any

import requests

from uipath_copilot.maestro_client import get_access_token
from uipath_copilot.settings import (
    OPERATOR_WHATSAPP,
    PUBLIC_BASE_URL,
    UIPATH_BASE_URL,
    UIPATH_ORG_UNIT_ID,
)

USE_ORCHESTRATOR_TASKS_API = os.getenv("UIPATH_ACTION_CENTER_API", "").lower() in ("1", "true", "yes")


def action_center_url() -> str | None:
    if not UIPATH_BASE_URL:
        return None
    return f"{UIPATH_BASE_URL.rstrip('/')}/actioncenter_"


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
    Por defecto usar User task en Maestro Approval (ver docs/ACTION_CENTER_B1.md).
    API: export UIPATH_ACTION_CENTER_API=true + scope OR.Tasks
    """
    ac_url = action_center_url()
    if not USE_ORCHESTRATOR_TASKS_API:
        return {
            "ok": False,
            "skipped": True,
            "mode": "maestro_user_task",
            "action_center_url": ac_url,
            "panel_fallback": f"{PUBLIC_BASE_URL}/dashboard",
            "hint": "Add User task in Maestro Approval stage + open Action Center UI. Optional: OR.Tasks scope + UIPATH_ACTION_CENTER_API=true",
        }

    if not UIPATH_BASE_URL or not UIPATH_ORG_UNIT_ID:
        return {"ok": False, "skipped": True, "reason": "UIPATH_BASE_URL o ORG_UNIT_ID vacío"}

    # Preferir User task en Maestro Approval (Action Center UI). API Orchestrator requiere OR.Tasks.
    token = get_access_token()
    urls = [
        f"{UIPATH_BASE_URL}/orchestrator_/odata/Tasks/UiPath.Server.Configuration.OData.CreateTask",
        f"{UIPATH_BASE_URL}/orchestrator_/odata/Tasks",
    ]
    body = {
        "Title": title[:128],
        "Description": (description + f"\n\nCaso: {case_id}\nPanel: {PUBLIC_BASE_URL}/api/v1/cases/{case_id}")[
            :2000
        ],
        "Priority": priority,
    }
    alt_body = {"taskData": {**body, "CatalogName": "PCDoctorMaestro"}}
    last: dict[str, Any] = {}
    for url in urls:
        for payload in (alt_body, body):
            try:
                r = requests.post(url, headers=_orchestrator_headers(token), json=payload, timeout=45)
                data = r.json() if r.text and "json" in r.headers.get("content-type", "") else {"raw": r.text[:300]}
                last = {"ok": r.ok, "http_status": r.status_code, "data": data, "url": url}
                if r.ok:
                    return last
            except Exception as exc:
                last = {"ok": False, "error": str(exc), "url": url}
    if last.get("http_status") == 405:
        last["hint"] = (
            "HTTP 405: usa User task en stage Approval de Maestro (Action Center UI). "
            "Opcional: añade scope OR.Tasks en External Application."
        )
    return last


def action_center_status() -> dict[str, Any]:
    return {
        "org_unit_id": UIPATH_ORG_UNIT_ID or None,
        "operator_whatsapp": bool(OPERATOR_WHATSAPP),
        "action_center_url": action_center_url(),
        "api_mode": USE_ORCHESTRATOR_TASKS_API,
        "note": "Primary: User task in Maestro Approval. Fallback: /dashboard HITL panel.",
    }
