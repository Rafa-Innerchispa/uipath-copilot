"""Mensajes bilingües — panel, logs e informes Ollama."""

from __future__ import annotations

from typing import Any

# Cuatro consultas curadas para jurado — datos reales verificados
JURY_CONSULTATION_IDS = (
    "dominguez_residential",   # Flujo completo OK (sin bloqueos)
    "la_pradera_quote_pdf",    # Se detiene: PDF-first bloqueante
    "probalsa_duplicate",      # Se detiene: RUC duplicado
    "rommy_report_quality",    # Se detiene: placeholder @today en informe
)


def normalize_lang(lang: str | None) -> str:
    if not lang:
        return "es"
    lang = lang.lower().strip()[:2]
    return "en" if lang == "en" else "es"


def t(lang: str, key: str, **kwargs: Any) -> str:
    lang = normalize_lang(lang)
    table = _MESSAGES.get(key, {})
    msg = table.get(lang) or table.get("es") or key
    if kwargs:
        try:
            return msg.format(**kwargs)
        except KeyError:
            return msg
    return msg


_MESSAGES: dict[str, dict[str, str]] = {
    "ollama_system": {
        "es": "Eres copiloto operativo PC Doctor S.A. Responde en español, Markdown limpio, acciones concretas. Sin placeholders inventados.",
        "en": "You are the PC Doctor S.A. operational copilot. Respond in English, clean Markdown, concrete actions. Do not invent placeholders.",
    },
    "report_title": {"es": "# Caso Maestro — PC Doctor", "en": "# Maestro Case — PC Doctor"},
    "report_client": {"es": "**Cliente:**", "en": "**Client:**"},
    "report_stage": {"es": "## Etapa {stage}", "en": "## Stage {stage}"},
    "report_findings": {"es": "### Hallazgos (datos reales)", "en": "### Findings (live data)"},
    "report_analysis": {"es": "### Análisis copiloto — {stage}", "en": "### Copilot analysis — {stage}"},
    "gate_ok": {"es": "OK", "en": "OK"},
    "gate_block": {"es": "BLOQUEO", "en": "BLOCK"},
    "ollama_offline": {
        "es": "Ollama no disponible en :11434 — gates MongoDB ejecutados igualmente.",
        "en": "Ollama unavailable at :11434 — MongoDB gates still executed.",
    },
    "flow_start": {
        "es": "Inicio flujo · {client} · case {case_id}…",
        "en": "Flow start · {client} · case {case_id}…",
    },
    "flow_stage_ok": {
        "es": "Etapa {stage} OK · {client} · case {case_id}…",
        "en": "Stage {stage} OK · {client} · case {case_id}…",
    },
    "flow_blocked": {
        "es": "BLOQUEO en {stage}: {gate} — flujo detenido (regla operativa real). case {case_id}…",
        "en": "BLOCKED at {stage}: {gate} — flow stopped (real operational rule). case {case_id}…",
    },
    "flow_complete": {
        "es": "4 etapas completadas · aprobación pendiente · case {case_id}…",
        "en": "4 stages complete · approval pending · case {case_id}…",
    },
    "approval_done": {
        "es": "APROBADO · {client} · case {case_id}…",
        "en": "APPROVED · {client} · case {case_id}…",
    },
    "approval_reject": {
        "es": "RECHAZADO · {client} · case {case_id}…",
        "en": "REJECTED · {client} · case {case_id}…",
    },
    "prompt_intake": {
        "es": "Clasifica y resume el incidente operativo PC Doctor:",
        "en": "Classify and summarize the PC Doctor operational incident:",
    },
    "prompt_investigation": {
        "es": "Investiga a fondo con los datos MongoDB. Lista causas probables y evidencia:",
        "en": "Investigate using MongoDB data. List probable causes and evidence:",
    },
    "prompt_remediation": {
        "es": "Propón remediación concreta (cotización, informe, cliente, hub). Pasos numerados:",
        "en": "Propose concrete remediation (quote, report, client, hub). Numbered steps:",
    },
    "prompt_approval": {
        "es": "Resume para Rafael qué debe aprobar o rechazar (1 párrafo):",
        "en": "Summarize what Rafael should approve or reject (1 paragraph):",
    },
    "msg_flow_complete": {
        "es": "Flujo Intake→Investigation→Remediation→Approval completado. Aprueba en este panel.",
        "en": "Intake→Investigation→Remediation→Approval complete. Approve in this panel.",
    },
    "msg_flow_blocked": {
        "es": "Flujo detenido en {stage} por gate operativo. Revise hallazgos y apruebe excepción si aplica.",
        "en": "Flow stopped at {stage} by operational gate. Review findings and approve exception if needed.",
    },
    "approval_section": {
        "es": "## Decisión humana — {label}\n\n- **Estado:** `{status}`\n- **Fecha:** {stamp}\n- **Comentario:** {comment}\n\n**Caso cerrado operativamente.**",
        "en": "## Human decision — {label}\n\n- **Status:** `{status}`\n- **Date:** {stamp}\n- **Comment:** {comment}\n\n**Case closed operationally.**",
    },
    "approved_label": {"es": "APROBADO", "en": "APPROVED"},
    "rejected_label": {"es": "RECHAZADO", "en": "REJECTED"},
}
