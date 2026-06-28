#!/usr/bin/env bash
# Smoke test hackathon — jurado / Rafael (sin secretos en salida).
set -euo pipefail
PROJECT="/home/rlopez/projects/uipath-copilot"
PORT="${UIPATH_COPILOT_PORT:-8097}"
BASE="http://127.0.0.1:${PORT}"
PASS=0
FAIL=0

check() {
  local name="$1" cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    echo "✅ $name"
    PASS=$((PASS + 1))
  else
    echo "❌ $name"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Hackathon smoke test uipath-copilot :${PORT} ==="
check "API status" "curl -sf $BASE/status"
check "MongoDB en status" "curl -sf $BASE/status | grep -q '\"clients\":'"
check "UiPath OAuth reachable" "curl -sf $BASE/status | grep -qE '\"reachable\"[[:space:]]*:[[:space:]]*true'"
check "Demo trigger real" "curl -sf --max-time 120 $BASE/api/v1/demo/trigger-sample | grep -q case_id"
check "Casos auditados" "curl -sf $BASE/api/v1/cases | grep -q '\"cases\"'"
check "Docs MongoDB" "curl -sf $BASE/api/v1/project-docs | grep -q proyecto-maestro-completo"
check "Escenarios demo" "curl -sf $BASE/api/v1/demo/scenarios | grep -q webhook_url"
check "Ngrok público" "curl -sf https://sworn-profusely-alongside.ngrok-free.dev/uipath/status | grep -q uipath-copilot"
check "OAuth CLI" "cd $PROJECT && source venv/bin/activate && python3 scripts/test_uipath_oauth.py"

echo ""
echo "PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]]
