---
name: runway-dev-model-routers
description: "Build, modify, debug, or verify Runway Model Routers: inspect live config and eligible models via MCP, manage approved settings, integrate routed SDK calls, and inspect routing results. Use with +runway-dev. Not for direct per-model endpoints or agent REST CLI."
user-invocable: true
---

# Runway Dev — Model Routers

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Keep a Model Router and its application integration correct. Verify changes with one routed SDK call (`client.generate.{video|image|audio}.create({ configId, input })`) when safe.

## MCP tools

- `list_model_routers` / `get_model_router` — inspect existing router configuration.
- `list_models` — inspect eligible models and capabilities.
- `create_model_router` / `update_model_router` / `delete_model_router` — manage routers after user approval; updates replace the full configuration.
- `get_credit_balance` — check budget before proposing credit ceilings or testing.
- `get_task_routing` — explain which model handled an existing routed task.

## New router

1. `list_models` across relevant endpoints — do not guess eligible models or capabilities.
2. `get_credit_balance` — understand budget before proposing credit ceilings.
3. Propose: name, immutable `configId` slug, description, routing preference, model-list policy, capacity fallback, optional credit caps. **Wait for user approval** unless they supplied all fields.
4. `create_model_router`, then `update_model_router` for settings if needed.
5. When verification is appropriate, make one routed SDK call with the SDK wait helper, then use `get_task_routing` to explain which model ran.

## Existing router

1. `get_model_router` for current config and slug.
2. Clarify integration goal (wire into app vs test call).
3. Implement the routed generate call behind the application's server boundary per https://docs.dev.runwayml.com/model-routers.md
4. Implement, modify, debug, or verify the routed call with that `configId`, based on the user's goal.

## Terminology

- Router record **id** (UUID) ≠ **configId** (immutable slug used in SDK `configId` field).

## Docs

- https://docs.dev.runwayml.com/llms.txt (model routers section)
- https://docs.dev.runwayml.com/model-routers.md
