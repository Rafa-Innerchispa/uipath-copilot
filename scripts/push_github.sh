#!/usr/bin/env bash
# Publica repo en GitHub (ejecutar una vez).
set -euo pipefail
cd "$(dirname "$0")/.."
git branch -M main 2>/dev/null || true
gh repo create uipath-copilot --public --source=. --remote=origin \
  --description "UiPath AgentHack 2026 Track 1 — Maestro Case copilot PC Doctor (real MongoDB, Ollama, WhatsApp)" \
  --push
echo "OK: https://github.com/Rafa-Innerchispa/uipath-copilot"
