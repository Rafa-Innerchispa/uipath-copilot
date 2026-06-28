"""FastAPI uipath-copilot — puerto 8097."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tools.mongo import get_db
from tools.ollama_chat import ollama_available
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
            "project_docs": "GET /api/v1/project-docs",
            "demo_real": "GET /api/v1/demo/trigger-sample",
        },
    }


@app.get("/")
def root():
    return {"message": "UiPath Maestro Case Copilot PC Doctor", "status": "/status"}
