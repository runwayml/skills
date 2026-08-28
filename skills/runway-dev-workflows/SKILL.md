---
name: runway-dev-workflows
description: "Build, modify, debug, or verify integrations that expose Runway app workflows as API endpoints. Use get_workflows_setup_guide for current setup and API guidance. Use with +runway-dev. Not for model generation, routers, or Characters sessions."
user-invocable: true
---

# Runway Dev — Workflows

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Keep the connection between Runway app workflows and callable API endpoints correct.

## MCP tools

- `get_workflows_setup_guide` — get current setup, connections, help, and API reference links.

## Workflow

1. Call `get_workflows_setup_guide`.
2. Follow that guide; do not invent workflow publishing steps.
3. Inspect any existing integration, then implement, modify, debug, or verify its server-side call per returned API docs.

## Docs

- https://docs.dev.runwayml.com/llms.txt
