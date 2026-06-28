"""Cliente OAuth + transiciones Maestro Case (HTTP real)."""

from __future__ import annotations

import time
from typing import Any

import requests

from uipath_copilot.settings import (
    UIPATH_BASE_URL,
    UIPATH_CLIENT_ID,
    UIPATH_CLIENT_SECRET,
    UIPATH_IDENTITY_TOKEN_URL,
    UIPATH_ORG_UNIT_ID,
    UIPATH_SCOPE,
)

_token_cache: dict[str, Any] = {"access_token": "", "expires_at": 0.0}


def uipath_configured() -> bool:
    return bool(UIPATH_BASE_URL and UIPATH_CLIENT_ID and UIPATH_CLIENT_SECRET)


def get_access_token() -> str:
    if not uipath_configured():
        raise RuntimeError("UiPath OAuth no configurado — revisa UIPATH_* en .env")

    now = time.time()
    if _token_cache["access_token"] and _token_cache["expires_at"] > now + 60:
        return _token_cache["access_token"]

    url = UIPATH_IDENTITY_TOKEN_URL
    if not url:
        raise RuntimeError("UIPATH_IDENTITY_TOKEN_URL vacío — revisa UIPATH_BASE_URL / UIPATH_ORGANIZATION")

    data = {
        "grant_type": "client_credentials",
        "client_id": UIPATH_CLIENT_ID,
        "client_secret": UIPATH_CLIENT_SECRET,
        "scope": UIPATH_SCOPE,
    }
    r = requests.post(url, data=data, timeout=30)
    if r.status_code != 200:
        snippet = (r.text or "")[:200]
        raise RuntimeError(f"OAuth UiPath HTTP {r.status_code}: {snippet}")
    try:
        body = r.json()
    except Exception as exc:
        raise RuntimeError("OAuth UiPath devolvió no-JSON (revisa URL identity org-level)") from exc
    _token_cache["access_token"] = body["access_token"]
    _token_cache["expires_at"] = now + int(body.get("expires_in", 3600))
    return _token_cache["access_token"]


def maestro_handoff_note(stage: str, needs_human: bool) -> dict[str, Any]:
    """
    Maestro Case Management avanza por tareas completadas en cloud (event-driven),
    no por TransitionState OData (BPMN clásico — devuelve HTTP 405 en Case).
    """
    next_stage = {
        "Intake": "Investigation",
        "Investigation": "Remediation",
        "Remediation": "Approval" if needs_human else "Complete",
        "Approval": "Complete",
    }.get(stage, "Investigation")
    return {
        "mode": "stage_task_complete",
        "stage_processed": stage,
        "expected_next_stage": next_stage,
        "needs_human": needs_human,
        "note": (
            "Configura API Workflow en Intake, Investigation y Remediation "
            "con el mismo webhook y campo stage. Approval = User task en Action Center."
        ),
    }


def transition_case(case_id: str, action: str, *, comment: str = "") -> dict[str, Any]:
    """Legacy BPMN — no usar con Maestro Case Management."""
    return {
        "ok": False,
        "skipped": True,
        "reason": "Maestro Case usa tareas por etapa; ver maestro_handoff",
        "action": action,
        "case_id": case_id,
    }


def maestro_status() -> dict[str, Any]:
    if not uipath_configured():
        return {"configured": False, "reachable": False}
    try:
        get_access_token()
        return {
            "configured": True,
            "reachable": True,
            "base_url": UIPATH_BASE_URL,
            "identity_url": UIPATH_IDENTITY_TOKEN_URL,
        }
    except Exception as exc:
        return {
            "configured": True,
            "reachable": False,
            "base_url": UIPATH_BASE_URL,
            "identity_url": UIPATH_IDENTITY_TOKEN_URL,
            "error": str(exc),
        }
