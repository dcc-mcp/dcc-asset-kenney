from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _kenney import download


@skill_entry
def main(asset_url_or_slug: str, output_dir: str, **_: Any) -> dict[str, Any]:
    try:
        return skill_success("Kenney asset downloaded", asset=download(asset_url_or_slug, output_dir))
    except Exception as exc:
        return skill_exception(exc, message="Failed to download Kenney asset")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

