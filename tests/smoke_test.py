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
    live_smoke()


if __name__ == "__main__":
    main()

