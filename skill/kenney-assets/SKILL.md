---
name: kenney-assets
description: Search, inspect, and download CC0 Kenney game asset packs.
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    display_name: Kenney Assets
    group: asset.download.cc0
    default_icon: package
    affinity: any
    marketplace: dcc-asset-kenney
    tools: tools.yaml
    execution: sync
    permissions:
      - network
      - filesystem
    examples:
      - "Search Kenney for 3D asset packs"
      - "Inspect a Kenney asset page and license"
      - "Download a Kenney asset zip"
    contact:
      name: dcc-mcp team
      url: https://github.com/dcc-mcp/dcc-asset-kenney
    install:
      add_source: "dcc-mcp-cli marketplace add dcc-mcp/dcc-asset-kenney"
      then_install: "dcc-mcp-cli marketplace install dcc-asset-kenney"
---

# Kenney Assets

Use this skill for Kenney CC0 game asset packs. The implementation parses
Kenney's public asset pages and keeps license metadata in every result.

