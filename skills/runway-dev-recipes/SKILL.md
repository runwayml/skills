---
name: runway-dev-recipes
description: "Integrate a Runway recipe pipeline via SDK client.recipes call against POST /v1/recipes/{id}. Use with +runway-dev. Not for direct model endpoints or Model Routers."
user-invocable: true
---

# Runway Dev — Recipes

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Make one working recipe SDK call for a pinned recipe id.

## Workflow

1. Confirm recipe id from quickstart context or ask the user.
2. Fetch recipe contract from `llms.txt` — input schema and `client.recipes.{method}` mapping.
3. Check `RUNWAYML_API_SECRET` when implementing the SDK call.
4. Server-side handler calling `POST /v1/recipes/{id}` via SDK.
5. Submit once; poll `get_task` until terminal status.

## Docs

- https://docs.dev.runwayml.com/llms.txt
