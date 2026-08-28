---
name: runway-dev-recipes
description: "Build, modify, debug, or verify Runway recipe integrations: resolve recipe contracts, implement SDK client.recipes calls against POST /v1/recipes/{id}, and inspect tasks. Use with +runway-dev. Not for direct model endpoints or Model Routers."
user-invocable: true
---

# Runway Dev — Recipes

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Keep a recipe pipeline integration correct for the provided or configured recipe id. Verify changes with one working SDK call when safe.

## Workflow

1. Confirm the recipe id from provided context, existing code, or the user.
2. Fetch recipe contract from `llms.txt` — input schema and `client.recipes.{method}` mapping.
3. Check `RUNWAYML_API_SECRET` when implementing the SDK call.
4. Implement or update the server-side handler calling `POST /v1/recipes/{id}` via SDK.
5. When verification is appropriate, submit once and poll `get_task` until terminal status.

## Docs

- https://docs.dev.runwayml.com/llms.txt
