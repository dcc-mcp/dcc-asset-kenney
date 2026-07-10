---
name: kenney-assets
description: Search, inspect, and download CC0 Kenney game asset packs as validated AssetDescriptors.
license: MIT
compatibility: "dcc-mcp-core 0.19+, Python 3.7+"
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    layer: domain
    tags:
      - asset
      - kenney
      - cc0
      - game-assets
      - 3d-models
      - download
    search-hint: "kenney, cc0 game assets, game asset pack, factory kit, low poly models, zip download"
    produces: [asset_descriptor]
    tools: tools.yaml
---

# Kenney Assets

Use this skill for Kenney CC0 game asset packs. The implementation parses
Kenney's public asset pages and keeps license metadata in every result. It does
not import files into a DCC scene; host-specific import belongs in host skills.

`download_kenney_asset` returns an `asset_descriptor` with the downloaded zip,
source URL, and CC0 attribution. Its zip variant may need extraction by the DCC
adapter before scene import.

