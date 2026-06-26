#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [[ -f venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi
export UIPATH_COPILOT_PORT="${UIPATH_COPILOT_PORT:-8097}"
exec python3 main.py
