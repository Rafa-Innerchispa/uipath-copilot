#!/usr/bin/env bash
# Instala UiPath CLI + case-tool (requiere Node.js 20+).
set -euo pipefail

export NVM_DIR="$HOME/.nvm"
if [[ ! -s "$NVM_DIR/nvm.sh" ]]; then
  echo "Instalando nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi
# shellcheck disable=SC1090
source "$NVM_DIR/nvm.sh"

nvm install 20
nvm use 20

mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"

npm install -g @uipath/cli
uip --version

# case-tool se auto-instala al primer uso; pre-instalar acelera CI
uip tools install @uipath/case-tool @uipath/orchestrator-tool @uipath/solution-tool 2>/dev/null || true

echo ""
echo "OK. Añade a ~/.bashrc:"
echo '  export PATH="$HOME/.npm-global/bin:$PATH"'
echo '  [ -s "$HOME/.nvm/nvm.sh" ] && . "$HOME/.nvm/nvm.sh" && nvm use 20 >/dev/null 2>&1'
echo ""
echo "Login (usa credenciales UiPath Labs en .env):"
echo '  uip login --client-id "$UIPATH_CLIENT_ID" --client-secret "$UIPATH_CLIENT_SECRET"'
