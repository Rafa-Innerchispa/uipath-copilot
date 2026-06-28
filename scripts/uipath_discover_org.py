#!/usr/bin/env python3
"""Descubre tenant URL válida y Org Unit ID vía OAuth (lee solo .env)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

CLIENT_ID = os.getenv("UIPATH_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("UIPATH_CLIENT_SECRET", "").strip()
SCOPE = os.getenv("UIPATH_SCOPE", "OR.Administration OR.Execution OR.Monitoring")
CONFIGURED_BASE = os.getenv("UIPATH_BASE_URL", "").rstrip("/")

CANDIDATES = [
    CONFIGURED_BASE,
    "https://cloud.uipath.com/innerchispa/innerchispa",
    "https://cloud.uipath.com/innerchispa/InnerChispa",
    "https://cloud.uipath.com/innerchispa/DefaultTenant",
    "https://cloud.uipath.com/innerchispa/Default",
]
CANDIDATES = [c.rstrip("/") for c in CANDIDATES if c]


def get_token(base: str) -> str | None:
    org = base.replace("https://cloud.uipath.com/", "").split("/")[0]
    url = f"https://cloud.uipath.com/{org}/identity_/connect/token"
    r = requests.post(
        url,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": SCOPE,
        },
        timeout=30,
    )
    if r.status_code != 200:
        snippet = (r.text or "")[:180].replace("\n", " ")
        print(f"   HTTP {r.status_code}: {snippet}")
        return None
    try:
        return r.json().get("access_token")
    except Exception:
        return None


def list_folders(base: str, token: str) -> list[dict]:
    url = f"{base}/orchestrator_/odata/Folders?$select=Id,DisplayName,FullyQualifiedName&$top=20"
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    if r.status_code != 200:
        return [{"error": r.status_code, "body": r.text[:300]}]
    return r.json().get("value") or []


def main() -> int:
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Faltan UIPATH_CLIENT_ID / UIPATH_CLIENT_SECRET en .env", file=sys.stderr)
        return 1

    seen: set[str] = set()
    for base in CANDIDATES:
        if base in seen:
            continue
        seen.add(base)
        token = get_token(base)
        if not token:
            print(f"❌ OAuth falló: {base}")
            continue
        print(f"✅ OAuth OK: {base}")
        folders = list_folders(base, token)
        if folders and folders[0].get("error"):
            print(f"   Folders: HTTP {folders[0]['error']}")
            continue
        if not folders:
            print("   Sin carpetas (revisa permisos OR.Administration)")
            continue
        print("   Carpetas Orchestrator (copia Id → UIPATH_ORG_UNIT_ID en .env):")
        for f in folders:
            print(f"   - {f.get('DisplayName')}: {f.get('Id')}")
            print(f"     FQN: {f.get('FullyQualifiedName')}")
        print(f"\n→ UIPATH_BASE_URL={base}/")
        if folders[0].get("Id"):
            print(f"→ UIPATH_ORG_UNIT_ID={folders[0]['Id']}")
        return 0

    print("\nNingún tenant respondió. Abre Orchestrator y copia la URL del navegador.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
