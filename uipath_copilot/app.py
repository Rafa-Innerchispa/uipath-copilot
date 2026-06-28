"""FastAPI uipath-copilot — puerto 8097."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path

from tools.mongo import get_db
from tools.ollama_chat import ollama_available
from uipath_copilot.activity_log import log_activity, log_connection_check
from uipath_copilot.routes import router
from uipath_copilot.settings import PUBLIC_BASE_URL, UIPATH_COPILOT_PORT

app = FastAPI(
    title="UiPath Maestro Case Copilot — PC Doctor",
    description="Backend real Track 1: webhook Maestro + MongoDB + Ollama + WhatsApp",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def _startup_log():
    from tools.evolution_api import evolution_available

    from uipath_copilot.maestro_client import maestro_status

    log_activity("info", "SYS", "uipath-copilot starting on port %s" % UIPATH_COPILOT_PORT)
    ms = maestro_status()
    log_connection_check("UiPath OAuth", ms.get("reachable", False))
    try:
        n = get_db().clients.count_documents({})
        log_connection_check("MongoDB pcdoctor_swarm", True, f"{n} clients")
    except Exception as exc:
        log_connection_check("MongoDB", False, str(exc))
    log_connection_check("Ollama :11434", ollama_available())
    log_connection_check("WhatsApp Evolution", evolution_available())


@app.get("/status")
def status():
    from tools.evolution_api import evolution_available

    from uipath_copilot.maestro_client import maestro_status

    try:
        clients = get_db().clients.count_documents({})
        quotes = get_db().quotes.count_documents({})
        mongo_ok = True
    except Exception as exc:
        clients = quotes = 0
        mongo_ok = False
        mongo_err = str(exc)
    else:
        mongo_err = None

    return {
        "service": "uipath-copilot",
        "port": UIPATH_COPILOT_PORT,
        "public_base_url": PUBLIC_BASE_URL,
        "mongodb": {"ok": mongo_ok, "clients": clients, "quotes": quotes, "error": mongo_err},
        "ollama": {"ok": ollama_available()},
        "evolution_whatsapp": {"ok": evolution_available()},
        "uipath_maestro": maestro_status(),
        "endpoints": {
            "webhook": "POST /api/v1/uipath-webhook",
            "cases": "GET /api/v1/cases",
            "dashboard_jurado": "GET /dashboard",
            "project_docs": "GET /api/v1/project-docs",
            "demo_real": "GET /api/v1/demo/trigger-sample",
            "demo_scenarios": "GET /api/v1/demo/scenarios",
            "platform_scorecard": "GET /api/v1/platform-scorecard",
        },
    }


_DASHBOARD_HTML = Path(__file__).resolve().parent / "static" / "jurado_dashboard.html"


@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/jurado", response_class=HTMLResponse)
def jurado_dashboard():
    """Panel web público para jurado (ngrok /uipath/dashboard)."""
    if _DASHBOARD_HTML.is_file():
        return HTMLResponse(_DASHBOARD_HTML.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Dashboard no encontrado</h1>", status_code=404)


@app.get("/")
def root():
    return {
        "message": "UiPath Maestro Case Copilot — PC Doctor / InnerChispa",
        "dashboard": "/dashboard",
        "status": "/status",
        "company": "https://www.innerchispa.us",
    }
