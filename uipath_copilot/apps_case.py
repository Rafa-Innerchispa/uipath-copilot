"""UiPath Apps — Case App (URLs públicas + metadatos para Apps Studio)."""

from __future__ import annotations

from typing import Any

from uipath_copilot.case_store import get_case, list_cases
from uipath_copilot.platform_events import record_event
from uipath_copilot.settings import PUBLIC_BASE_URL


def public_url(path: str) -> str:
    base = PUBLIC_BASE_URL.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    return f"{base}{path}"


def case_public_urls(case_id: str) -> dict[str, str]:
    return {
        "case_api": public_url(f"/api/v1/cases/{case_id}"),
        "case_app": public_url(f"/apps/case/{case_id}"),
        "dashboard_deep_link": public_url(f"/dashboard?case_id={case_id}"),
        "approve_api": public_url(f"/api/v1/cases/{case_id}/human-decision"),
        "action_center": "https://cloud.uipath.com/innerchispa/DefaultTenant/actioncenter_",
    }


def build_apps_config() -> dict[str, Any]:
    cases = list_cases(limit=10)
    pending = [
        c for c in cases
        if c.get("stage") == "Approval" and c.get("approval_status") not in ("approved", "rejected")
    ]
    return {
        "app_name": "PC Doctor Maestro Case App",
        "organization": "innerchispa",
        "public_base_url": PUBLIC_BASE_URL,
        "embed_dashboard": public_url("/dashboard"),
        "case_list_api": public_url("/api/v1/cases"),
        "webhook_url": public_url("/api/v1/uipath-webhook"),
        "pending_cases": [
            {
                "case_id": c["case_id"],
                "client_name": c.get("client_name"),
                "stage": c.get("stage"),
                "urls": case_public_urls(c["case_id"]),
            }
            for c in pending[:5]
        ],
        "setup_steps": [
            "Apps → New App → Connect to Maestro Case",
            f"Embed URL: {public_url('/apps/case/{{caseId}}')}",
            f"Approve POST: {public_url('/api/v1/cases/{{caseId}}/human-decision')}",
        ],
    }


def get_case_app_payload(case_id: str) -> dict[str, Any]:
    doc = get_case(case_id)
    if not doc:
        raise ValueError("Caso no encontrado")
    record_event("apps_case_app", "view", case_id=case_id)
    urls = case_public_urls(case_id)
    can_approve = doc.get("approval_status") not in ("approved", "rejected") and (
        doc.get("stage") == "Approval" or bool(doc.get("needs_human"))
    )
    return {
        "case": doc,
        "urls": urls,
        "can_approve": can_approve or bool(doc.get("needs_human")),
        "public_only": True,
    }
