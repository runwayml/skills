---
name: runway-dev-workflows
description: "Link Runway app workflows to API endpoints via get_workflows_setup_guide MCP tool. Use with +runway-dev. Not for model generation, routers, or Characters sessions."
user-invocable: true
---

# Runway Dev — Workflows

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Help the user publish Runway app workflows as callable API endpoints.

## Workflow

1. Call MCP `get_workflows_setup_guide` — returns markdown with connections URL, help article, and API reference links.
2. Follow that guide; do not invent workflow publishing steps.
3. If integrating into an app, inspect workspace and wire server-side call per returned API docs.

## Docs

- https://docs.dev.runwayml.com/llms.txt
