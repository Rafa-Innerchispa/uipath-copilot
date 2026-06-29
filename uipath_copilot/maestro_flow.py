"""Continuación automática del flujo Maestro en el servidor (mismo case_id)."""

from __future__ import annotations

from typing import Any

from uipath_copilot.activity_log import log_activity
from uipath_copilot.case_store import get_case
from uipath_copilot.processor import STAGES, has_blocking_gate, process_webhook


def continue_maestro_flow(case_id: str, *, base_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Ejecuta etapas pendientes sobre el mismo case_id (MongoDB + Ollama reales).
    Usado tras webhook Maestro Cloud y desde el panel (Continuar flujo).
    """
    prior = get_case(case_id) or {}
    snap = dict(base_payload or prior.get("payload_snapshot") or {})
    snap["case_id"] = case_id
    snap["integration_source"] = "maestro_cloud"
    snap.setdefault("panel_lang", prior.get("panel_lang") or "es")
    if prior.get("maestro_id_unsubstituted"):
        snap["maestro_id_unsubstituted"] = prior["maestro_id_unsubstituted"]
    if not snap.get("notes"):
        snap["notes"] = prior.get("notes") or "source=maestro_cloud"

    done = set(prior.get("stages_completed") or [])
    if len(done) >= len(STAGES):
        return {**prior, "flow": "already_complete", "flow_blocked": bool(prior.get("flow_blocked"))}

    log_activity("info", "MAESTRO", f"Continuando flujo · case {case_id[:8]}… · hecho={','.join(sorted(done)) or '—'}")

    last: dict[str, Any] = prior
    blocked = False
    for stage in STAGES:
        if stage in done:
            continue
        snap["stage"] = stage
        last = process_webhook(snap)
        done.add(stage)
        log_activity("ok", "MAESTRO", f"Etapa {stage} · case {case_id[:8]}…")

        blocker = has_blocking_gate(last.get("findings") or [])
        if blocker and stage != "Approval":
            blocked = True
            log_activity(
                "warn",
                "MAESTRO",
                f"Flujo detenido en {stage} · gate {blocker.get('gate')} · case {case_id[:8]}…",
            )
            break

    flow = "blocked_by_gate" if blocked else ("full_4_stages" if len(last.get("stages_completed") or []) >= len(STAGES) else "partial")
    return {**last, "flow": flow, "flow_blocked": blocked or bool(last.get("flow_blocked"))}


def should_auto_continue(result: dict[str, Any], *, from_maestro_cloud: bool) -> bool:
    if not from_maestro_cloud:
        return False
    done = set(result.get("stages_completed") or [])
    return len(done) < len(STAGES) and not result.get("flow_blocked")
