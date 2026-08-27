---
name: runway-dev-model-routers
description: "Integrate Runway Model Routers: inspect models via MCP, propose config, create router after approval, routed SDK generate call. Use with +runway-dev. Not for direct per-model endpoints or agent REST CLI."
user-invocable: true
---

# Runway Dev — Model Routers

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Create or wire a Model Router and make one routed SDK call (`client.generate.{video|image|audio}.create({ configId, input })`).

## New router (list surface)

1. `list_models` across relevant endpoints — do not guess eligible models or capabilities.
2. `get_credit_balance` — understand budget before proposing credit ceilings.
3. Propose: name, immutable `configId` slug, description, routing preference, model-list policy, capacity fallback, optional credit caps. **Wait for user approval** unless they supplied all fields.
4. `create_model_router`, then `update_model_router` for settings if needed. Note: MCP update is full replace, not deep merge.
5. Make one routed SDK call; poll `get_task`; use `get_task_routing` to explain which model ran.

## Existing router (detail surface)

1. `get_model_router` for current config and slug.
2. Clarify integration goal (wire into app vs test call).
3. Implement server-side routed generate endpoint per https://docs.dev.runwayml.com/model-routers
4. One end-to-end SDK call with pinned `configId`.

## Terminology

- Router record **id** (UUID) ≠ **configId** (immutable slug used in SDK `configId` field).

## Docs

- https://docs.dev.runwayml.com/llms.txt (model routers section)
- https://docs.dev.runwayml.com/model-routers
