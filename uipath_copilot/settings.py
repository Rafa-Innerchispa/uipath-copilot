"""Configuración aislada uipath-copilot (:8097)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

# Reutiliza Mongo/Ollama/Evolution del .env compartido
from config import (  # noqa: E402
    EVOLUTION_API_KEY,
    EVOLUTION_BASE_URL,
    EVOLUTION_INSTANCE,
    MONGO_DB,
    MONGO_URI,
    OLLAMA_BASE_URL,
)

UIPATH_COPILOT_PORT = int(os.getenv("UIPATH_COPILOT_PORT", "8097"))
UIPATH_COPILOT_HOST = os.getenv("UIPATH_COPILOT_HOST", "0.0.0.0")

# UiPath Automation Cloud (Maestro OData)
UIPATH_BASE_URL = os.getenv("UIPATH_BASE_URL", "").rstrip("/")
UIPATH_CLIENT_ID = os.getenv("UIPATH_CLIENT_ID", "")
_secret_file = os.getenv("UIPATH_CLIENT_SECRET_FILE", "").strip()
if _secret_file:
    _secret_path = Path(_secret_file)
    if not _secret_path.is_absolute():
        _secret_path = ROOT / _secret_path
    UIPATH_CLIENT_SECRET = _secret_path.read_text(encoding="utf-8").strip() if _secret_path.is_file() else ""
else:
    UIPATH_CLIENT_SECRET = os.getenv("UIPATH_CLIENT_SECRET", "")
UIPATH_SCOPE = os.getenv("UIPATH_SCOPE", "OR.Administration OR.Execution OR.Monitoring")
UIPATH_ORG_UNIT_ID = os.getenv("UIPATH_ORG_UNIT_ID", "")

# Token OAuth va a nivel organización, NO al tenant (evita HTML en lugar de JSON)
_org = os.getenv("UIPATH_ORGANIZATION", "").strip()
if not _org and UIPATH_BASE_URL:
    parts = UIPATH_BASE_URL.replace("https://", "").split("/")
    if len(parts) >= 2 and parts[0] == "cloud.uipath.com":
        _org = parts[1]
UIPATH_ORGANIZATION = _org
UIPATH_IDENTITY_TOKEN_URL = os.getenv(
    "UIPATH_IDENTITY_TOKEN_URL",
    f"https://cloud.uipath.com/{_org}/identity_/connect/token" if _org else "",
)

OLLAMA_MODEL_ANALYSIS = os.getenv("OLLAMA_MODEL_ANALYSIS", "qwen2.5:14b-instruct-q4_K_M")
OLLAMA_MODEL_CODER = os.getenv("OLLAMA_MODEL_CODER", "qwen2.5-coder:7b")

OPERATOR_WHATSAPP = os.getenv("UIPATH_OPERATOR_WHATSAPP", os.getenv("HACKATHON_WHATSAPP_TO", ""))
AGENTS_POOL_ROOT = Path(os.getenv("AGENTS_POOL_ROOT", "/home/rlopez/inneros_core/agents_pool"))

PUBLIC_BASE_URL = os.getenv("UIPATH_COPILOT_PUBLIC_URL", f"http://192.168.1.4:{UIPATH_COPILOT_PORT}")

CASES_COLLECTION = "uipath_maestro_cases"
