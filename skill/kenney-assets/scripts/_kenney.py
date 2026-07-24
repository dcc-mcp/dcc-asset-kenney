from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE = "https://kenney.nl"
LICENSE = {
    "license_name": "CC0 1.0 Universal",
    "license_url": "https://kenney.nl/support",
    "usage_notice": "Kenney assets are CC0; the Kenney logo is reserved for official Kenney projects.",
}


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "dcc-mcp-kenney/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "ignore")


def asset_url(slug_or_url: str) -> str:
    if slug_or_url.startswith("http"):
        return slug_or_url
    return f"{BASE}/assets/{slug_or_url.strip('/')}"


def search(page: int = 1) -> list[dict[str, Any]]:
    url = f"{BASE}/assets" if page <= 1 else f"{BASE}/assets/page:{page}"
    text = get(url)
    items = []
    pattern = re.compile(
        r"<h2>\s*<a href=['\"](https://kenney\.nl/assets/[^'\"]+)['\"]>(.*?)</a>\s*</h2>",
        re.IGNORECASE | re.S,
    )
    for match in pattern.finditer(text):
        items.append({"title": html.unescape(match.group(2).strip()), "url": match.group(1), **LICENSE})
    return items


def inspect(slug_or_url: str) -> dict[str, Any]:
    url = asset_url(slug_or_url)
    text = get(url)
    title_match = re.search(r"<meta property='og:title' content='([^']+)'", text)
    zip_match = re.search(r"https://kenney.nl/media/pages/assets/[^']+?\.zip", text)
    license_ok = "Creative Commons CC0" in text or "CC0 licensed" in text
    return {
        "title": html.unescape((title_match.group(1) if title_match else url).replace("&middot;", "-")),
        "url": url,
        "download_url": zip_match.group(0) if zip_match else None,
        "license_detected": license_ok,
        **LICENSE,
    }


def download(slug_or_url: str, output_dir: str) -> dict[str, Any]:
    meta = inspect(slug_or_url)
    if not meta["download_url"]:
        raise RuntimeError("No Kenney zip URL found on asset page")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    target = Path(output_dir) / Path(urllib.parse.urlparse(meta["download_url"]).path).name
    req = urllib.request.Request(meta["download_url"], headers={"User-Agent": "dcc-mcp-kenney/0.1"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        target.write_bytes(resp.read())
    return {**meta, "file": str(target)}

