#!/usr/bin/env python3
"""
Bootstrap de proyecto hackathon: docs locales + reglas Cursor.

Invocado al crear un proyecto nuevo (AG-12 provisioner o manualmente).
No consume créditos Cursor — solo HTTP local + disco.

  python3 scripts/bootstrap_hackathon_project.py
  python3 scripts/bootstrap_hackathon_project.py --project-root /path/to/proyecto
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "scripts" / "templates" / "hackathon"


def ensure_metadata(project_root: Path, hackathon_url: str | None) -> dict:
    meta_path = project_root / "docs" / "metadata.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        meta = {
            "project_name": project_root.name,
            "hackathon_name": "Hackathon",
            "hackathon_url": hackathon_url or "https://uipath-agenthack.devpost.com/",
            "assigned_port": None,
            "server_ip": "192.168.1.4",
            "visibility": "public",
        }
    if hackathon_url:
        meta["hackathon_url"] = hackathon_url.rstrip("/") + "/"
    meta_path.write_text(json.dumps(meta, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return meta


def install_cursor_rules(project_root: Path) -> list[str]:
    rules_dst = project_root / ".cursor" / "rules"
    rules_dst.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    src_dir = TEMPLATES / "cursor_rules"
    if src_dir.is_dir():
        for src in src_dir.glob("*.mdc"):
            dst = rules_dst / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
                installed.append(str(dst.relative_to(project_root)))
    return installed


def write_bootstrap_log(project_root: Path, report: dict) -> None:
    log_path = project_root / "docs" / "hackathon_resources" / "BOOTSTRAP_LOG.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Bootstrap log — {ts}",
        "",
        f"- Proyecto: `{project_root}`",
        f"- Fases scrape: {report.get('phases', [])}",
        f"- Páginas totales: {report.get('total_pages', '?')}",
        f"- Links pendientes: {report.get('pending', '?')}",
        "",
        "Agente recomendado: AG-21 `hackathon_docs_harvester` + AG-12 `project_provisioner`.",
        "",
        "Re-ejecutar: `python3 scripts/bootstrap_hackathon_project.py`",
        "",
    ]
    log_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=ROOT)
    ap.add_argument("--hackathon-url", type=str, default="")
    ap.add_argument("--max-pages", type=int, default=60)
    ap.add_argument("--summarize", action="store_true")
    ap.add_argument("--skip-scrape", action="store_true")
    args = ap.parse_args()

    project_root = args.project_root.resolve()
    meta = ensure_metadata(project_root, args.hackathon_url or None)
    rules = install_cursor_rules(project_root)

    report: dict = {"metadata": meta, "cursor_rules_installed": rules}

    if not args.skip_scrape:
        import subprocess
        import sys

        scrape_script = project_root / "scripts" / "scrape_hackathon_resources.py"
        cmd = [
            sys.executable,
            str(scrape_script),
            "--bootstrap",
            "--project-root",
            str(project_root),
            "--max-pages",
            str(args.max_pages),
        ]
        if args.summarize:
            cmd.append("--summarize")
        subprocess.run(cmd, check=True, cwd=str(project_root))
        discovered = project_root / "docs" / "hackathon_resources" / "DISCOVERED_LINKS.json"
        if discovered.is_file():
            pending = json.loads(discovered.read_text(encoding="utf-8")).get("pending_count", 0)
            index = project_root / "docs" / "hackathon_resources" / "INDEX.json"
            pages = 0
            if index.is_file():
                pages = json.loads(index.read_text(encoding="utf-8")).get("pages_fetched", 0)
            report["total_pages"] = pages
            report["pending"] = pending
            report["output_dir"] = str(project_root / "docs" / "hackathon_resources")

    write_bootstrap_log(project_root, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
