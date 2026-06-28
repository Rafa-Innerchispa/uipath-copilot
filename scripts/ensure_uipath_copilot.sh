#!/usr/bin/env bash
# Mantiene uipath-copilot :8097 activo (cron + @reboot). Usuario rlopez, sin sudo.
set -euo pipefail

PROJECT="/home/rlopez/projects/uipath-copilot"
PORT="${UIPATH_COPILOT_PORT:-8097}"
LOG="$PROJECT/data/ensure_uipath.log"
mkdir -p "$PROJECT/data"

_log() { echo "[$(date -Iseconds)] $*" >>"$LOG"; }

if curl -sf "http://127.0.0.1:${PORT}/status" >/dev/null 2>&1; then
  exit 0
fi

_log "port ${PORT} down — starting uipath-copilot"
pkill -f "${PROJECT}/main.py" 2>/dev/null || true
pkill -f "${PROJECT}/run_uipath_copilot.sh" 2>/dev/null || true
sleep 1
nohup bash "$PROJECT/run_uipath_copilot.sh" >>"$PROJECT/data/uipath_copilot.log" 2>&1 &
sleep 4

if curl -sf "http://127.0.0.1:${PORT}/status" >/dev/null 2>&1; then
  _log "OK started"
else
  _log "FAIL still down — revisa data/uipath_copilot.log"
  exit 1
fi
