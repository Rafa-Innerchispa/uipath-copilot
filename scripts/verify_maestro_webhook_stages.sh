#!/usr/bin/env bash
# Verifica webhook + 3 stages (Intake, Investigation, Remediation) — backend PC Doctor.
# No sustituye Maestro cloud; confirma que :8097 y ngrok responden bien.
set -euo pipefail

PROJECT="/home/rlopez/projects/uipath-copilot"
PORT="${UIPATH_COPILOT_PORT:-8097}"
LOCAL="http://127.0.0.1:${PORT}"
NGROK="https://sworn-profusely-alongside.ngrok-free.dev/uipath"
WEBHOOK="${NGROK}/api/v1/uipath-webhook"
PASS=0
FAIL=0

ok() { echo "✅ $1"; PASS=$((PASS + 1)); }
bad() { echo "❌ $1"; FAIL=$((FAIL + 1)); }

echo "=== Verificación Maestro webhook (3 stages) ==="
echo "Webhook público: $WEBHOOK"
echo ""

if curl -sf -H "ngrok-skip-browser-warning: true" "${NGROK}/status" | grep -q uipath-copilot; then
  ok "Ngrok /uipath/status"
else
  bad "Ngrok /uipath/status"
fi

if curl -sf "${LOCAL}/status" | grep -q '"reachable"[[:space:]]*:[[:space:]]*true'; then
  ok "UiPath OAuth (local status)"
else
  bad "UiPath OAuth (local status)"
fi

test_stage() {
  local stage="$1"
  local cid
  cid=$(python3 -c "import uuid; print(uuid.uuid4())")
  local body
  body=$(cat <<EOF
{"case_id":"${cid}","stage":"${stage}","incident_type":"field_inspection_exception","severity":"high","raw_logs":"verify script ${stage}","notes":"verify_maestro_stages.sh"}
EOF
)
  local out
  if ! out=$(curl -sf --max-time 180 -X POST "${LOCAL}/api/v1/uipath-webhook" \
    -H "Content-Type: application/json" \
    -d "$body" 2>/dev/null); then
    bad "POST local stage=${stage}"
    return
  fi
  if echo "$out" | grep -q "\"stage\"[[:space:]]*:[[:space:]]*\"${stage}\""; then
    ok "POST local stage=${stage} (case ${cid:0:8}…)"
  else
    bad "POST local stage=${stage} — respuesta inesperada"
    echo "   $(echo "$out" | head -c 120)"
  fi

  if curl -sf --max-time 180 -X POST "$WEBHOOK" \
    -H "Content-Type: application/json" \
    -H "ngrok-skip-browser-warning: true" \
    -d "$body" >/dev/null 2>&1; then
    ok "POST ngrok stage=${stage}"
  else
    bad "POST ngrok stage=${stage}"
  fi
}

for s in Intake Investigation Remediation; do
  test_stage "$s"
done

echo ""
echo "--- Checklist Maestro (tú en cloud) ---"
echo "  Intake          → API Workflow POST → URL ngrok (sin /home/...)"
echo "  Investigation   → API Workflow POST → mismo URL, body stage=Investigation"
echo "  Remediation     → API Workflow POST → mismo URL, body stage=Remediation"
echo "  Approval        → Simple Approval (NO webhook) → Action Center"
echo ""
echo "  Start Job input → vacío OK (tu case no tiene variables obligatorias)"
echo "  Aprobar         → NO en Start Job → cuando llegue a Approval → Action Center"
echo ""
echo "PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]]
