#!/usr/bin/env python3
"""Prueba OAuth UiPath sin imprimir secretos."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from uipath_copilot.maestro_client import maestro_status  # noqa: E402


def main() -> int:
    st = maestro_status()
    safe = {k: v for k, v in st.items() if k != "error"}
    print(json.dumps(safe, indent=2))
    if st.get("reachable"):
        print("OK: OAuth conectado")
        return 0
    print("FAIL:", st.get("error", "unknown")[:300])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
