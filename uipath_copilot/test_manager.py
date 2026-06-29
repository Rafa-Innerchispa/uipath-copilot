"""Test Manager — smoke tests reproducibles + JUnit XML."""

from __future__ import annotations

import json
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from uipath_copilot.platform_events import record_event
from uipath_copilot.settings import PUBLIC_BASE_URL, UIPATH_COPILOT_PORT

ROOT = Path(__file__).resolve().parents[1]

RESULTS_PATH = ROOT / "data" / "test_manager_results.json"
JUNIT_PATH = ROOT / "data" / "test_manager_junit.xml"


def _http_get(url: str, timeout: int = 30) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"ngrok-skip-browser-warning": "true", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def _run_checks() -> list[dict[str, Any]]:
    local = f"http://127.0.0.1:{UIPATH_COPILOT_PORT}"
    public = PUBLIC_BASE_URL.rstrip("/")
    checks: list[tuple[str, str, int]] = [
        ("status_local", f"{local}/status", 15),
        ("mongodb_clients", f"{local}/status", 15),
        ("consultations_catalog", f"{local}/api/v1/consultations", 15),
        ("cases_list", f"{local}/api/v1/cases", 15),
        ("dashboard_html", f"{local}/dashboard", 15),
        ("platform_scorecard", f"{local}/api/v1/platform-scorecard", 15),
        ("agent_builder_openapi", f"{local}/api/v1/agent-builder/openapi", 15),
        ("apps_config", f"{local}/api/v1/apps/config", 15),
        ("ngrok_status", f"{public}/status", 20),
        ("ngrok_cases", f"{public}/api/v1/cases", 20),
        ("ngrok_dashboard", f"{public}/dashboard", 20),
    ]
    results: list[dict[str, Any]] = []
    for name, url, timeout in checks:
        t0 = time.time()
        ok = False
        detail = ""
        try:
            code, body = _http_get(url, timeout=timeout)
            ok = code == 200
            if name == "mongodb_clients":
                ok = ok and '"clients"' in body and '"ok":true' in body.replace(" ", "")
            elif name == "dashboard_html":
                ok = ok and "apiBase" in body
            elif name == "cases_list":
                ok = ok and '"cases"' in body
            detail = f"HTTP {code}"
        except Exception as exc:
            detail = str(exc)[:120]
        results.append(
            {
                "name": name,
                "url": url,
                "passed": ok,
                "duration_ms": int((time.time() - t0) * 1000),
                "detail": detail,
            }
        )
    return results


def _oauth_check() -> dict[str, Any]:
    t0 = time.time()
    script = ROOT / "scripts" / "test_uipath_oauth.py"
    ok = False
    detail = "script missing"
    if script.is_file():
        try:
            proc = subprocess.run(
                ["python3", str(script)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=30,
            )
            ok = proc.returncode == 0
            detail = (proc.stdout or proc.stderr or "")[:200]
        except Exception as exc:
            detail = str(exc)
    return {
        "name": "uipath_oauth",
        "url": "scripts/test_uipath_oauth.py",
        "passed": ok,
        "duration_ms": int((time.time() - t0) * 1000),
        "detail": detail.strip(),
    }


def run_test_suite() -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat()
    tests = _run_checks()
    tests.append(_oauth_check())
    passed = sum(1 for t in tests if t["passed"])
    failed = len(tests) - passed
    suite = {
        "project": "PCDoctorMaestro",
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "failed": failed,
        "total": len(tests),
        "tests": tests,
        "public_base_url": PUBLIC_BASE_URL,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(suite, indent=2, ensure_ascii=False), encoding="utf-8")
    JUNIT_PATH.write_text(build_junit_xml(suite), encoding="utf-8")
    record_event("test_manager", "run", passed=passed, failed=failed, total=len(tests))
    return suite


def load_last_results() -> dict[str, Any] | None:
    if not RESULTS_PATH.is_file():
        return None
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def build_junit_xml(suite: dict[str, Any]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<testsuite name="PCDoctorMaestro" tests="{suite["total"]}" failures="{suite["failed"]}" time="0">',
    ]
    for t in suite.get("tests", []):
        name = escape(t["name"])
        if t["passed"]:
            lines.append(f'  <testcase name="{name}" time="{t.get("duration_ms", 0) / 1000:.3f}"/>')
        else:
            msg = escape(t.get("detail") or "failed")
            lines.append(f'  <testcase name="{name}" time="{t.get("duration_ms", 0) / 1000:.3f}">')
            lines.append(f'    <failure message="{msg}"/>')
            lines.append("  </testcase>")
    lines.append("</testsuite>")
    return "\n".join(lines)
