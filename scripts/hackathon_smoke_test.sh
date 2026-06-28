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
check "Consulta operativa" "curl -sf --max-time 120 $BASE/api/v1/consultations/probalsa_duplicate/run | grep -q case_id"
check "Catálogo consultas" "curl -sf $BASE/api/v1/consultations | grep -q consultations"
check "Casos auditados" "curl -sf $BASE/api/v1/cases | grep -q '\"cases\"'"
check "Panel jurado HTML" "curl -sf $BASE/dashboard | grep -q 'apiBase'"
check "Ngrok público status" "curl -sf -H 'ngrok-skip-browser-warning: true' https://sworn-profusely-alongside.ngrok-free.dev/uipath/status | grep -q uipath-copilot"
check "Ngrok público casos" "curl -sf -H 'ngrok-skip-browser-warning: true' https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/cases | grep -q '\"cases\"'"
check "Platform scorecard" "curl -sf $BASE/api/v1/platform-scorecard | grep -q bonuses_total"
check "Docs MongoDB" "curl -sf $BASE/api/v1/project-docs | grep -q proyecto-maestro-completo"
check "OAuth CLI" "cd $PROJECT && source venv/bin/activate && python3 scripts/test_uipath_oauth.py"

echo ""
echo "PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]]
