#!/usr/bin/env bash
# Git sync seguro: solo código/docs públicos. NUNCA .env ni .uipath_secret.
set -euo pipefail

PROJECT="/home/rlopez/projects/uipath-copilot"
LOG="$PROJECT/data/git_sync.log"
cd "$PROJECT"

_log() { echo "[$(date -Iseconds)] $*" >>"$LOG"; }

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  _log "skip: no git repo"
  exit 0
fi

# Sincronizar docs a MongoDB antes del commit
if [[ -f venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi
python3 scripts/sync_project_documentation.py >>"$LOG" 2>&1 || _log "warn: sync docs mongo failed"

git add \
  AGENTS.md README.md LICENSE .env.example .gitignore \
  docs/ maestro/ scripts/ uipath_copilot/ admin/src/ admin/vite.config.ts \
  run_uipath_copilot.sh setup_hackathon.sh main.py requirements.txt \
  2>/dev/null || true

# Archivos nuevos bajo esas rutas
git add -u docs/ scripts/ uipath_copilot/ admin/src/ 2>/dev/null || true
for f in docs/PROYECTO_MAESTRO_COMPLETO.md docs/COMMUNITY_LICENSE_ROADMAP.md docs/walkthrough.md \
  admin/src/pages/maestro/index.tsx scripts/ensure_uipath_copilot.sh \
  scripts/git_sync_uipath_copilot.sh scripts/install_uipath_autostart.sh \
  scripts/swarm-uipath-copilot.service scripts/test_uipath_oauth.py \
  uipath_copilot/project_docs_store.py; do
  [[ -f "$f" ]] && git add "$f" 2>/dev/null || true
done

if git diff --cached --quiet; then
  _log "nothing to commit"
  exit 0
fi

git commit -m "$(cat <<EOF
chore: sync automático docs y código uipath-copilot

$(date -Iseconds)
EOF
)" >>"$LOG" 2>&1 || { _log "commit failed"; exit 1; }

if git push origin HEAD >>"$LOG" 2>&1; then
  _log "pushed OK"
else
  _log "push failed (revisar gh auth)"
  exit 1
fi
