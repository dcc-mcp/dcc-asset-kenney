from __future__ import annotations

from pathlib import Path
from typing import Any

from dcc_mcp_core.asset_import import AssetAttribution, AssetDescriptor, AssetFileVariant
from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _kenney import download


def asset_descriptor(asset: dict[str, Any]) -> dict[str, Any]:
    local_path = asset["file"]
    descriptor = AssetDescriptor(
        asset_id=f"kenney:{asset['url']}",
        variants=[
            AssetFileVariant(
                local_path=local_path,
                format=Path(local_path).suffix.lstrip(".").lower() or "unknown",
                preferred=True,
            )
        ],
        attribution=AssetAttribution(
            source_url=asset["url"],
            license_text=asset["usage_notice"],
            attribution_text=f"{asset['title']} — {asset['license_name']}.",
        ),
        extra={"download_url": asset["download_url"]},
    )
    descriptor.validate()
    return descriptor.to_dict()


@skill_entry
def main(asset_url_or_slug: str, output_dir: str, **_: Any) -> dict[str, Any]:
    try:
        asset = download(asset_url_or_slug, output_dir)
        return skill_success(
            "Kenney asset downloaded",
            asset=asset,
            asset_descriptor=asset_descriptor(asset),
        )
    except Exception as exc:
        return skill_exception(exc, message="Failed to download Kenney asset")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

