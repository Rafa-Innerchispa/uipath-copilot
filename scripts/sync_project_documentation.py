#!/usr/bin/env python3
"""Sincroniza markdown canónico → MongoDB inneros_global.uipath_project_docs."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from uipath_copilot.project_docs_store import upsert_doc  # noqa: E402

CANONICAL_DOCS: list[tuple[str, str, list[str]]] = [
    ("proyecto-maestro-completo", "docs/PROYECTO_MAESTRO_COMPLETO.md", ["master", "uipath", "estado"]),
    ("walkthrough", "docs/walkthrough.md", ["changelog", "operativo"]),
    ("hackathon-requirements", "docs/HACKATHON_REQUIREMENTS.md", ["jurado", "checklist"]),
    ("submision-jurado", "docs/SUBMISION_JURADO.md", ["devpost", "video"]),
    ("tu-checklist", "docs/TU_CHECKLIST_3_CLICKS.md", ["manual", "oauth"]),
    ("guia-plataforma-jurado", "docs/GUIA_PLATAFORMA_UIPATH_PARA_JURADO.md", ["jurado", "uipath", "video"]),
    ("community-roadmap", "docs/COMMUNITY_LICENSE_ROADMAP.md", ["licencia", "roadmap"]),
    ("agents-md", "AGENTS.md", ["cursor", "agentes"]),
    ("readme", "README.md", ["repo", "arranque"]),
]


def main() -> int:
    synced = 0
    for doc_id, rel_path, tags in CANONICAL_DOCS:
        path = ROOT / rel_path
        if not path.is_file():
            print(f"⚠ omitido (no existe): {rel_path}")
            continue
        content = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").replace("-", " ").title()
        upsert_doc(doc_id, title=title, path=rel_path, content=content, tags=tags, source="sync_script")
        synced += 1
        digest = hashlib.sha256(content.encode()).hexdigest()[:12]
        print(f"✓ {doc_id} ({len(content)} chars, sha256:{digest})")

    print(f"\n{synced} documentos en MongoDB → inneros_global.uipath_project_docs")
    print("Consulta: GET http://127.0.0.1:8097/api/v1/project-docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
