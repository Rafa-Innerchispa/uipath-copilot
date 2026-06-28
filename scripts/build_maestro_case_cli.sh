#!/usr/bin/env bash
# Genera definición Maestro Case PC Doctor vía CLI (sin Studio Web).
# Requiere: scripts/install_uipath_cli.sh + uip login
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEF="$ROOT/maestro/pcdoctor_field_exceptions.json"
mkdir -p "$ROOT/maestro"

export NVM_DIR="$HOME/.nvm"
# shellcheck disable=SC1090
[[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh" && nvm use 20 >/dev/null 2>&1 || true
export PATH="$HOME/.npm-global/bin:$PATH"

if ! command -v uip >/dev/null 2>&1; then
  echo "Ejecuta primero: bash scripts/install_uipath_cli.sh" >&2
  exit 1
fi

# Crear case base
uip maestro case cases add \
  --name "PCDoctorFieldExceptions" \
  --file "$DEF" \
  --case-identifier "PCD" \
  --identifier-type constant \
  --case-app-enabled

# Stages (IDs los asigna el CLI en el JSON; usamos labels conocidos)
# Nota: tras add, leer IDs reales del JSON si stages add requiere file ya existente
for label in Intake Investigation Remediation Approval; do
  uip maestro case stages add "$DEF" --label "$label" --type stage || true
done

uip maestro case validate "$DEF"

echo ""
echo "Definición generada: $DEF"
echo "Validación OK. Siguiente: publicar en cloud (ver docs/UIPATH_CLI_MAESTRO.md)"
