from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "kenney-assets"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    sys.path.insert(0, str(SCRIPTS))
    try:
        spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def validate_skill() -> None:
    from dcc_mcp_core import validate_skill

    report = validate_skill(str(SKILL))
    assert not report.has_errors, report


def descriptor_smoke() -> None:
    result = load("download_kenney_asset").asset_descriptor(
        {
            "title": "Factory Kit",
            "url": "https://kenney.nl/assets/factory-kit",
            "download_url": "https://kenney.nl/factory-kit.zip",
            "usage_notice": "Kenney assets are CC0.",
            "license_name": "CC0 1.0 Universal",
            "file": "C:/tmp/factory-kit.zip",
        }
    )
    assert result["variants"][0]["local_path"] == "C:/tmp/factory-kit.zip"
    assert result["attribution"]["source_url"] == "https://kenney.nl/assets/factory-kit"
    assert result["attribution"]["license_text"] == "Kenney assets are CC0."


def search_listing_smoke() -> None:
    kenney = load("_kenney")
    kenney.get = lambda _: """
        <a href='https://kenney.nl/assets/input-prompts'>
          <div class='cover'></div>
        </a>
        <h2><a href='https://kenney.nl/assets/input-prompts'>Input Prompts</a></h2>
    """
    assert [
        (asset["title"], asset["url"])
        for asset in kenney.search()
    ] == [("Input Prompts", "https://kenney.nl/assets/input-prompts")]


def entrypoint_smoke() -> None:
    from dcc_mcp_core._server import run_skill_script

    cases = {
        "search_kenney_assets": ({"page": "invalid"}, "Failed to search Kenney assets"),
        "inspect_kenney_asset": ({"asset_url_or_slug": 1}, "Failed to inspect Kenney asset"),
        "download_kenney_asset": (
            {"asset_url_or_slug": 1, "output_dir": "."},
            "Failed to download Kenney asset",
        ),
    }
    for name, (payload, message) in cases.items():
        script = SCRIPTS / f"{name}.py"
        assert run_skill_script(str(script), payload)["message"] == message

        completed = subprocess.run(
            [sys.executable, str(script)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 1, completed
        assert json.loads(completed.stdout)["message"] == message


def live_smoke() -> None:
    if os.environ.get("RUN_LIVE_API_SMOKE") != "true":
        print("skip live Kenney smoke")
        return
    search_result = load("search_kenney_assets").main(query="input prompts", limit=1)
    assert search_result["success"], search_result
    assert search_result["context"]["count"] == 1, search_result
    result = load("inspect_kenney_asset").main(asset_url_or_slug="factory-kit")
    assert result["success"], result
    assert result["context"]["asset"]["license_detected"], result
    assert result["context"]["asset"]["download_url"], result


def main() -> None:
    validate_skill()
    entrypoint_smoke()
    descriptor_smoke()
    search_listing_smoke()
    live_smoke()


if __name__ == "__main__":
    main()

