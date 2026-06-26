#!/usr/bin/env bash
# Instala servicio systemd uipath-copilot (:8097) + actualiza URL pública ngrok.
set -euo pipefail

PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
INNERSPARK="${INNERSPARK_PROJECT:-/home/rlopez/projects/innerspark-swarm-os-cursor-local}"
PORT="${UIPATH_COPILOT_PORT:-8097}"
USER_NAME="$(whoami)"

chmod +x "$PROJECT/run_uipath_copilot.sh" "$PROJECT/scripts/bootstrap_hackathon_project.py" 2>/dev/null || true

# Variables uipath en .env si faltan
append_env() {
  local key="$1" val="$2"
  if ! grep -q "^${key}=" "$PROJECT/.env" 2>/dev/null; then
    echo "${key}=${val}" >>"$PROJECT/.env"
  fi
}
[[ -f "$PROJECT/.env" ]] || cp "$PROJECT/.env.example" "$PROJECT/.env"
append_env UIPATH_COPILOT_PORT "$PORT"
append_env GATEWAY_UIPATH_COPILOT "http://127.0.0.1:${PORT}"
append_env UIPATH_COPILOT_PUBLIC_URL "https://sworn-profusely-alongside.ngrok-free.dev/uipath"

sudo tee /etc/systemd/system/swarm-uipath-copilot.service >/dev/null <<EOF
[Unit]
Description=UiPath Maestro Case Copilot PC Doctor :${PORT}
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${USER_NAME}
WorkingDirectory=${PROJECT}
EnvironmentFile=-${PROJECT}/.env
ExecStart=/usr/bin/bash ${PROJECT}/run_uipath_copilot.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

if sudo -n true 2>/dev/null; then
  sudo systemctl daemon-reload
  sudo systemctl enable swarm-uipath-copilot.service
  sudo systemctl restart swarm-uipath-copilot.service
  sudo systemctl restart swarm-public-gateway.service 2>/dev/null || true
else
  echo "Sin sudo: arrancando API con nohup (ejecuta este script con sudo una vez para systemd)."
  pkill -f "uipath_copilot.app:app" 2>/dev/null || true
  nohup bash "$PROJECT/run_uipath_copilot.sh" >>"$PROJECT/data/uipath_copilot.log" 2>&1 &
  if [[ -f "$INNERSPARK/run_public_gateway.sh" ]]; then
    pkill -f "scripts/public_gateway.py" 2>/dev/null || true
    sleep 2
    cd "$INNERSPARK" && nohup bash run_public_gateway.sh >>"$INNERSPARK/data/public_gateway.log" 2>&1 &
  fi
fi

mkdir -p "$PROJECT/data"
NGROK_URL="$(curl -sf http://127.0.0.1:4040/api/tunnels/public 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('public_url',''))" 2>/dev/null || true)"
if [[ -n "$NGROK_URL" ]]; then
  PUBLIC_WEBHOOK="${NGROK_URL}/uipath/api/v1/uipath-webhook"
  echo "public_uipath_webhook: ${PUBLIC_WEBHOOK}" >"$PROJECT/data/uipath_public_url.txt"
  echo "public_uipath_status: ${NGROK_URL}/uipath/status" >>"$PROJECT/data/uipath_public_url.txt"
  sed -i "s|^UIPATH_COPILOT_PUBLIC_URL=.*|UIPATH_COPILOT_PUBLIC_URL=${NGROK_URL}/uipath|" "$PROJECT/.env" 2>/dev/null || \
    append_env UIPATH_COPILOT_PUBLIC_URL "${NGROK_URL}/uipath"
fi

echo ""
echo "=== uipath-copilot instalado ==="
systemctl is-active swarm-uipath-copilot.service || true
curl -sf "http://127.0.0.1:${PORT}/status" | python3 -m json.tool 2>/dev/null | head -20 || echo "API aún arrancando..."
echo ""
echo "Webhook Maestro (pegar en UiPath):"
cat "$PROJECT/data/uipath_public_url.txt" 2>/dev/null || echo "(ngrok no activo — levantar swarm-ngrok)"
