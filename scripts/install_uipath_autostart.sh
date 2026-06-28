#!/usr/bin/env bash
# Arranque automático uipath-copilot (:8097) + git sync seguro — sin perder secretos.
set -euo pipefail

PROJECT="/home/rlopez/projects/uipath-copilot"
MARKER="# uipath-copilot-autostart"

chmod +x "$PROJECT/run_uipath_copilot.sh"
chmod +x "$PROJECT/scripts/ensure_uipath_copilot.sh"
chmod +x "$PROJECT/scripts/git_sync_uipath_copilot.sh"
chmod +x "$PROJECT/scripts/sync_project_documentation.py"

REBOOT_LINE="@reboot sleep 90 && $PROJECT/scripts/ensure_uipath_copilot.sh"
WATCH_LINE="*/5 * * * * $PROJECT/scripts/ensure_uipath_copilot.sh >>$PROJECT/data/ensure_uipath.log 2>&1"
GIT_LINE="0 */6 * * * $PROJECT/scripts/git_sync_uipath_copilot.sh"

(crontab -l 2>/dev/null | grep -v "$MARKER" | grep -v "ensure_uipath_copilot.sh" | grep -v "git_sync_uipath_copilot.sh"; \
  echo "$MARKER"; echo "$REBOOT_LINE"; echo "$WATCH_LINE"; echo "$GIT_LINE") | crontab -

echo "Crontab uipath-copilot instalado:"
echo "  @reboot + cada 5 min → ensure :8097"
echo "  cada 6 h → git push seguro (sin .env)"
echo ""
echo "Systemd (recomendado, una vez con sudo):"
echo "  sudo bash $PROJECT/scripts/install_uipath_stack.sh"
echo ""
bash "$PROJECT/scripts/ensure_uipath_copilot.sh"
bash "$PROJECT/scripts/sync_project_documentation.py" 2>/dev/null || true
