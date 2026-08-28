---
name: runway-dev-workflows
description: "Build, modify, debug, or verify integrations that expose Runway app workflows as API endpoints. Use get_workflows_setup_guide for current setup and API guidance. Use with +runway-dev. Not for model generation, routers, or Characters sessions."
user-invocable: true
---

# Runway Dev — Workflows

> **Companion:** Use `+runway-dev` for shared setup when available. Otherwise connect Dev MCP, select a project with `list_projects`, follow the returned setup guide, and keep `RUNWAYML_API_SECRET` server-side.

## Goal

Keep the connection between Runway app workflows and callable API endpoints correct.

## MCP tools

- `get_workflows_setup_guide` — get current setup, connections, help, and API reference links.

## Workflow

1. Call `get_workflows_setup_guide` with the selected `projectId`.
2. Follow that guide; do not invent workflow publishing steps.
3. Inspect the existing workflow contract and application integration before changing either.
4. Implement, modify, debug, or verify the server-side call per the returned API docs. Wire inputs, invocation state, errors, and outputs into the existing UI or consumer.
5. When verification is appropriate, run one invocation with representative inputs and present the result.

## Docs

- https://docs.dev.runwayml.com/llms.txt
