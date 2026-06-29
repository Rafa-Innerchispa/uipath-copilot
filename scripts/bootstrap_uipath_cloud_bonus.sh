#!/usr/bin/env bash
# Bootstrap bonus UiPath Cloud vía CLI (Agent Builder + Test Manager + Maestro validate).
# Requiere: Node 20, uip login OK, scopes Studio/TM en External Application.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="${UIPATH_COPILOT_PUBLIC_URL:-https://sworn-profusely-alongside.ngrok-free.dev/uipath}"
AGENT_DIR="$ROOT/uipath_cloud/pc_doctor_intake_agent"
AGENT_JSON="$ROOT/data/uipath_agent_builder/pc_doctor_intake_agent.json"
TM_KEY="PCDOC"
TM_NAME="PCDoctorMaestro"

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1090
[[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh" && nvm use 20 >/dev/null 2>&1 || true
export PATH="$HOME/.npm-global/bin:$PATH"

log() { echo "[bootstrap-cloud] $*"; }
fail() { log "ERROR: $*"; exit 1; }

command -v uip >/dev/null 2>&1 || fail "Ejecuta: bash scripts/install_uipath_cli.sh"

log "Instalando CLI tools (agent, test-manager, solution)..."
uip tools install @uipath/agent-tool >/dev/null 2>&1 || true
uip tools install @uipath/test-manager-tool >/dev/null 2>&1 || true
uip tools install @uipath/solution-tool >/dev/null 2>&1 || true

STATUS=$(uip login status --output plain 2>/dev/null | head -1 || true)
if ! echo "$STATUS" | grep -qi "logged in"; then
  fail "No hay sesión CLI. Ejecuta: uip login --client-id \"\$UIPATH_CLIENT_ID\" --client-secret \"\$(cat .uipath_secret)\""
fi
log "CLI login: OK (innerchispa)"

PROMPT=$(python3 - <<'PY'
import json
from pathlib import Path
p = Path("data/uipath_agent_builder/pc_doctor_intake_agent.json")
print(json.loads(p.read_text())["system_prompt"])
PY
)

log "1/5 — Scaffold Agent Builder local..."
mkdir -p "$ROOT/uipath_cloud"
if [[ -d "$AGENT_DIR" ]]; then
  log "   (existe $AGENT_DIR — omitiendo init; borra carpeta para regenerar)"
else
  uip agent init "$AGENT_DIR" --system-prompt "$PROMPT" --force
fi
uip agent validate "$AGENT_DIR" || log "   validate: revisar warnings"

log "2/5 — Push agent a Studio Web..."
if uip agent push "$AGENT_DIR" --name "PCDoctorIntakeAgent" 2>&1 | tee "$ROOT/data/agent_push.log"; then
  log "   push OK — abre Agents en cloud y publica si falta"
else
  log "   push falló (401 = faltan scopes Studio en External Application)"
  log "   Alternativa: backend ya expone POST ${PUBLIC}/api/v1/agent-builder/intake"
fi

log "3/5 — Test Manager proyecto + casos..."
if uip tm project list 2>/dev/null | grep -q "$TM_KEY"; then
  log "   proyecto $TM_KEY ya existe"
else
  uip tm project create --name "$TM_NAME" --project-key "$TM_KEY" \
    --description "Hackathon PC Doctor — webhook + gates MongoDB" \
    || log "   tm project create falló (401 = scope Test Manager)"
fi

uip tm testcases create --project-key "$TM_KEY" \
  --name "Webhook status 200" \
  --description "GET ${PUBLIC}/status responde uipath-copilot" \
  2>/dev/null || true

uip tm testcases create --project-key "$TM_KEY" \
  --name "Agent Builder intake" \
  --description "POST ${PUBLIC}/api/v1/agent-builder/intake clasifica excepción" \
  2>/dev/null || true

log "4/5 — Test Manager local (JUnit)..."
curl -sf -X POST "http://127.0.0.1:8097/api/v1/test-manager/run" >/dev/null \
  || log "   servidor :8097 no responde — arranca ./run_uipath_copilot.sh"

log "5/5 — Maestro Case validate..."
uip maestro case validate "$ROOT/maestro/pcdoctor_field_exceptions.json" \
  || log "   case JSON necesita tasks/entry rules (configura en Studio Web o CLI tasks add)"

cat <<EOF

=== Resumen bootstrap cloud ===
Agent local:     $AGENT_DIR
Push log:        $ROOT/data/agent_push.log
Test Manager:    uip tm project list
JUnit evidencia: ${PUBLIC}/api/v1/test-manager/junit.xml
Case App URL:    ${PUBLIC}/apps/case/{case_id}
Agent HTTP URL:  ${PUBLIC}/api/v1/agent-builder/intake

Si push/tm devuelven 401:
  Admin → External Application → añadir scopes:
    Studio, Agents, Test Manager, OR.Tasks
  Luego: uip login (de nuevo)

Apps (UiPath Apps): NO hay CLI dedicado — usa iframe:
  ${PUBLIC}/apps/case/{{caseId}}

Document Understanding: sin CLI packager — usa upload API o DU cloud → ingest JSON.

EOF
