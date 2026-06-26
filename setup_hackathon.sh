#!/usr/bin/env bash
# Un solo comando: bootstrap docs + API + systemd + URL ngrok
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/bootstrap_hackathon_project.py --max-pages 40 2>/dev/null || python3 scripts/bootstrap_hackathon_project.py --max-pages 40
bash scripts/install_uipath_stack.sh
