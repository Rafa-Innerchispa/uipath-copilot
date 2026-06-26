#!/usr/bin/env python3
"""
Mirror local de documentación de hackathons (Devpost + docs del sponsor).

Sin créditos Cursor. Opcional: resúmenes con Ollama local (--summarize).

Uso típico al crear proyecto:
  python3 scripts/bootstrap_hackathon_project.py

Solo re-scrape:
  python3 scripts/scrape_hackathon_resources.py --bootstrap
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "hackathon_resources"
RAW_DIR = OUT_DIR / "raw"
INDEX_PATH = OUT_DIR / "INDEX.json"
INDEX_MD = OUT_DIR / "INDEX.md"
DISCOVERED_PATH = OUT_DIR / "DISCOVERED_LINKS.json"
DISCOVERED_MD = OUT_DIR / "DISCOVERED_LINKS.md"

STATIC_DOC_SEEDS = [
    "https://docs.uipath.com/maestro",
    "https://docs.uipath.com/agents/automation-cloud/latest/user-guide/building-an-agent-in-studio-web",
    "https://docs.uipath.com/coded-automations",
    "https://docs.uipath.com/automation-cloud/automation-cloud/latest/user-guide/about-api-workflows",
    "https://docs.uipath.com/document-understanding",
]

GENERIC_ALLOWED = {
    "docs.uipath.com",
    "forum.uipath.com",
    "uipath.com",
    "academy.uipath.com",
    "devpost.com",
}

USER_AGENT = "inneros-hackathon-mirror/2.0 (local; Rafael PC Doctor)"
DELAY_SEC = 0.8


def configure(project_root: Path) -> None:
    global ROOT, OUT_DIR, RAW_DIR, INDEX_PATH, INDEX_MD, DISCOVERED_PATH, DISCOVERED_MD
    ROOT = project_root.resolve()
    OUT_DIR = ROOT / "docs" / "hackathon_resources"
    RAW_DIR = OUT_DIR / "raw"
    INDEX_PATH = OUT_DIR / "INDEX.json"
    INDEX_MD = OUT_DIR / "INDEX.md"
    DISCOVERED_PATH = OUT_DIR / "DISCOVERED_LINKS.json"
    DISCOVERED_MD = OUT_DIR / "DISCOVERED_LINKS.md"


def read_metadata(project_root: Path | None = None) -> dict:
    base = project_root or ROOT
    path = base / "docs" / "metadata.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def hackathon_hosts(base_url: str) -> set[str]:
    hosts = set(GENERIC_ALLOWED)
    parsed = urlparse(base_url)
    if parsed.netloc:
        hosts.add(parsed.netloc.lower())
    return hosts


def devpost_seeds(base_url: str) -> list[str]:
    base = base_url.rstrip("/")
    return [
        base + "/",
        base + "/resources",
        base + "/rules",
        base + "/details/tracks",
        base + "/details/dates",
        base + "/details/prizes",
        base + "/forum_topics",
    ]


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.links.append(v)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)


def fetch_url(url: str, timeout: int = 30) -> tuple[str, str | None]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        ctype = resp.headers.get("Content-Type", "")
        body = resp.read()
        charset = "utf-8"
        m = re.search(r"charset=([\w-]+)", ctype, re.I)
        if m:
            charset = m.group(1)
        return body.decode(charset, errors="replace"), ctype


def html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</p>", "\n\n", html)
    html = re.sub(r"(?is)</h[1-6]>", "\n\n", html)
    html = re.sub(r"(?is)<li[^>]*>", "\n- ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def slug_for(url: str) -> str:
    h = hashlib.sha1(url.encode()).hexdigest()[:10]
    path = urlparse(url).path.strip("/").replace("/", "_") or "root"
    path = re.sub(r"[^\w.-]", "_", path)[:80]
    return f"{path}_{h}"


def host_allowed(url: str, allowed_hosts: set[str]) -> bool:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    return any(host == h or host.endswith("." + h) for h in allowed_hosts)


def normalize(base: str, href: str, allowed_hosts: set[str]) -> str | None:
    if not href or href.startswith(("#", "mailto:", "javascript:")):
        return None
    full = urljoin(base, href)
    parsed = urlparse(full)
    if parsed.scheme not in ("http", "https"):
        return None
    clean = parsed._replace(fragment="", query="").geturl()
    return clean if host_allowed(clean, allowed_hosts) else None


def link_priority(url: str, hackathon_host: str) -> int:
    host = urlparse(url).netloc.lower()
    if "docs.uipath.com" in host:
        return 0
    if "forum.uipath.com" in host:
        return 1
    if "academy.uipath.com" in host:
        return 2
    if hackathon_host in host:
        return 3
    if "devpost.com" in host:
        return 5
    return 4


def extract_urls_from_text(text: str, base: str, allowed_hosts: set[str]) -> set[str]:
    found: set[str] = set()
    for match in re.findall(r"https?://[^\s<>\"'&]+", text):
        nxt = normalize(base, match.rstrip(".,;)&nbsp;"), allowed_hosts)
        if nxt:
            found.add(nxt)
    return found


def ollama_summarize(text: str, max_chars: int = 6000) -> str:
    try:
        import requests

        from config import OLLAMA_BASE_URL
    except Exception:
        return ""

    snippet = text[:max_chars]
    payload = {
        "model": "qwen2.5:7b",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Resume en español (máx 12 viñetas) requisitos técnicos "
                    "y acciones para cumplir el hackathon:\n\n" + snippet
                ),
            }
        ],
        "stream": False,
        "options": {"temperature": 0.1},
    }
    try:
        r = requests.post(
            f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat",
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        return r.json().get("message", {}).get("content", "")
    except Exception as exc:
        return f"(resumen Ollama no disponible: {exc})"


def scrape(
    seeds: list[str],
    max_pages: int,
    summarize: bool,
    *,
    allowed_hosts: set[str],
    hackathon_host: str = "",
    docs_only: bool = False,
    skip_devpost_noise: bool = True,
    seen: set[str] | None = None,
    fetched_ok: set[str] | None = None,
    all_discovered: set[str] | None = None,
    entries: list[dict] | None = None,
) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    def sort_queue(urls: list[str]) -> list[str]:
        return sorted(dict.fromkeys(urls), key=lambda u: link_priority(u, hackathon_host))

    if seen is None:
        seen = set()
    if fetched_ok is None:
        fetched_ok = set()
    if all_discovered is None:
        all_discovered = set()
    if entries is None:
        entries = []

    queue = sort_queue([u for u in seeds if u not in seen])

    while queue and len([e for e in entries if e.get("status") == "ok"]) < max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)

        if skip_devpost_noise and "devpost.com" in url:
            if any(x in url for x in ("/users/", "/software", "/hackathons", "info.devpost.com")):
                if hackathon_host not in url:
                    continue

        try:
            html, ctype = fetch_url(url)
        except Exception as exc:
            entries.append({"url": url, "status": "error", "error": str(exc)})
            continue

        parser = LinkExtractor()
        parser.feed(html)
        title = "".join(parser.title_parts).strip() or url
        text = html_to_text(html)

        slug = slug_for(url)
        md_path = RAW_DIR / f"{slug}.md"
        summary = ollama_summarize(text) if summarize and len(text) > 500 else ""

        md_body = "\n".join(
            [
                f"# {title}",
                "",
                f"- **URL:** {url}",
                f"- **Content-Type:** {ctype}",
                f"- **Scraped:** scripts/scrape_hackathon_resources.py",
                "",
            ]
        )
        if summary:
            md_body += "## Resumen Ollama (local)\n\n" + summary + "\n\n"
        md_body += "## Contenido extraído\n\n" + text[:50000]
        md_path.write_text(md_body, encoding="utf-8")

        entry = {
            "url": url,
            "title": title,
            "status": "ok",
            "file": str(md_path.relative_to(ROOT)),
            "chars": len(text),
            "priority": link_priority(url, hackathon_host),
        }
        if summary:
            entry["summary"] = summary[:500]
        entries.append(entry)
        fetched_ok.add(url)

        new_links: set[str] = set()
        new_links |= extract_urls_from_text(html, url, allowed_hosts)
        for href in parser.links:
            nxt = normalize(url, href, allowed_hosts)
            if nxt:
                new_links.add(nxt)
        all_discovered |= new_links

        for nxt in sort_queue(list(new_links)):
            if nxt in seen or nxt in queue:
                continue
            if docs_only and "docs.uipath.com" not in nxt and "forum.uipath.com" not in nxt:
                continue
            queue.append(nxt)

        time.sleep(DELAY_SEC)

    return _write_index(seeds, entries, fetched_ok, all_discovered, hackathon_host)


def _write_index(
    seeds: list[str],
    entries: list[dict],
    fetched_ok: set[str],
    all_discovered: set[str],
    hackathon_host: str,
) -> dict:
    pending = sorted(all_discovered - fetched_ok, key=lambda u: link_priority(u, hackathon_host))
    discovery = {
        "total_discovered": len(all_discovered),
        "fetched_ok": len(fetched_ok),
        "pending_count": len(pending),
        "pending_urls": pending[:200],
    }
    DISCOVERED_PATH.write_text(json.dumps(discovery, indent=2, ensure_ascii=False), encoding="utf-8")

    meta = read_metadata()
    hackathon_name = meta.get("hackathon_name", "Hackathon")
    lines = [
        f"# Links descubiertos — {hackathon_name}",
        "",
        f"- Descubiertos: **{discovery['total_discovered']}**",
        f"- Descargados: **{discovery['fetched_ok']}**",
        f"- Pendientes: **{discovery['pending_count']}** (ver JSON completo)",
        "",
        "Para bajar más: `python3 scripts/bootstrap_hackathon_project.py --max-pages 100`",
        "",
        "## Pendientes (prioridad alta primero)",
        "",
    ]
    for u in pending[:80]:
        lines.append(f"- [{link_priority(u, hackathon_host)}] {u}")
    DISCOVERED_MD.write_text("\n".join(lines), encoding="utf-8")

    index = {
        "generated_by": "scripts/scrape_hackathon_resources.py",
        "project": str(ROOT),
        "seed_urls": seeds,
        "pages_fetched": len([e for e in entries if e.get("status") == "ok"]),
        "discovery": discovery,
        "entries": entries,
    }
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        f"# Índice local — {hackathon_name}",
        "",
        "Generado automáticamente. Cursor: leer antes de implementar.",
        "",
        f"Páginas descargadas: **{index['pages_fetched']}** | Pendientes: **{discovery['pending_count']}**",
        "",
        "| Prioridad | Título | URL | Archivo |",
        "|-----------|--------|-----|---------|",
    ]
    for e in sorted(
        [x for x in entries if x.get("status") == "ok"],
        key=lambda x: x.get("priority", 9),
    ):
        title = e.get("title", "")[:50].replace("|", "/")
        md_lines.append(
            f"| {e.get('priority', '?')} | {title} | {e['url']} | `{e.get('file', '')}` |"
        )
    md_lines.extend(
        [
            "",
            "Ver también: `DISCOVERED_LINKS.md` para URLs aún no descargadas.",
            "",
            "Regenerar: `python3 scripts/bootstrap_hackathon_project.py`",
            "",
        ]
    )
    INDEX_MD.write_text("\n".join(md_lines), encoding="utf-8")
    return index


def run_bootstrap(project_root: Path, max_pages: int, summarize: bool) -> dict:
    configure(project_root)
    meta = read_metadata(project_root)
    base_url = meta.get("hackathon_url", "https://uipath-agenthack.devpost.com/")
    hackathon_host = urlparse(base_url).netloc.lower()
    allowed = hackathon_hosts(base_url)
    seeds = devpost_seeds(base_url) + STATIC_DOC_SEEDS

    seen: set[str] = set()
    fetched_ok: set[str] = set()
    all_discovered: set[str] = set()
    entries: list[dict] = []

    # Fase 1: Devpost core (rules, resources, tracks)
    scrape(
        seeds,
        max_pages=max(12, max_pages // 4),
        summarize=False,
        allowed_hosts=allowed,
        hackathon_host=hackathon_host,
        skip_devpost_noise=True,
        seen=seen,
        fetched_ok=fetched_ok,
        all_discovered=all_discovered,
        entries=entries,
    )

    # Fase 2: docs UiPath + forum (prioridad alta)
    scrape(
        list(all_discovered) + STATIC_DOC_SEEDS,
        max_pages=max_pages,
        summarize=summarize,
        allowed_hosts=allowed,
        hackathon_host=hackathon_host,
        docs_only=True,
        skip_devpost_noise=True,
        seen=seen,
        fetched_ok=fetched_ok,
        all_discovered=all_discovered,
        entries=entries,
    )

    index = _write_index(seeds, entries, fetched_ok, all_discovered, hackathon_host)
    return {
        "phases": ["devpost_core", "docs_uipath"],
        "total_pages": index["pages_fetched"],
        "pending": index["discovery"]["pending_count"],
        "output_dir": str(OUT_DIR),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Mirror local documentación hackathon")
    ap.add_argument("--project-root", type=Path, default=ROOT)
    ap.add_argument("--max-pages", type=int, default=60)
    ap.add_argument("--docs-only", action="store_true")
    ap.add_argument("--summarize", action="store_true")
    ap.add_argument(
        "--bootstrap",
        action="store_true",
        help="3 fases: Devpost core → docs UiPath → pendientes prioritarios",
    )
    args = ap.parse_args()
    configure(args.project_root)
    meta = read_metadata(args.project_root)
    base_url = meta.get("hackathon_url", "https://uipath-agenthack.devpost.com/")
    hackathon_host = urlparse(base_url).netloc.lower()
    allowed = hackathon_hosts(base_url)
    seeds = devpost_seeds(base_url) + STATIC_DOC_SEEDS

    if args.bootstrap:
        result = run_bootstrap(args.project_root, args.max_pages, args.summarize)
        print(json.dumps(result, indent=2))
        return

    result = scrape(
        seeds,
        max_pages=args.max_pages,
        summarize=args.summarize,
        allowed_hosts=allowed,
        hackathon_host=hackathon_host,
        docs_only=args.docs_only,
    )
    print(f"OK: {result['pages_fetched']} páginas → {OUT_DIR}")


if __name__ == "__main__":
    main()
