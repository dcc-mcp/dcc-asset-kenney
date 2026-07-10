from __future__ import annotations

import importlib.util
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "kenney-assets"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


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


def live_smoke() -> None:
    if os.environ.get("RUN_LIVE_API_SMOKE") != "true":
        print("skip live Kenney smoke")
        return
    result = load("inspect_kenney_asset").main(asset_url_or_slug="factory-kit")
    assert result["success"], result
    assert result["context"]["asset"]["license_detected"], result
    assert result["context"]["asset"]["download_url"], result


def main() -> None:
    validate_skill()
    descriptor_smoke()
    live_smoke()


if __name__ == "__main__":
    main()

