#!/usr/bin/env bash
# Un solo comando: bootstrap docs + API + systemd + URL ngrok
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 "$ROOT/scripts/bootstrap_hackathon_project.py" --max-pages 40
bash "$ROOT/scripts/install_uipath_stack.sh"
