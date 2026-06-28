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


def transition_case(case_id: str, action: str, *, comment: str = "") -> dict[str, Any]:
    """
    Avanza un caso Maestro. `action` debe coincidir con la transición definida en el proceso.
    Ejemplos típicos: ToInvestigation, ToRemediation, ToApproval, Complete.
    """
    if not uipath_configured():
        return {"ok": False, "skipped": True, "reason": "UIPATH_* no configurado"}

    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if UIPATH_ORG_UNIT_ID:
        headers["X-UIPATH-OrganizationUnitId"] = UIPATH_ORG_UNIT_ID

    url = (
        f"{UIPATH_BASE_URL}/odata/Cases({case_id})"
        "/UiPath.Server.Configuration.OData.TransitionState"
    )
    payload: dict[str, Any] = {"Action": action}
    if comment:
        payload["Comment"] = comment

    r = requests.post(url, headers=headers, json=payload, timeout=45)
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text[:500]}
    return {"ok": r.ok, "http_status": r.status_code, "data": data, "action": action}


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
