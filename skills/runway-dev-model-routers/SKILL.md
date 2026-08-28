---
name: runway-dev-model-routers
description: "Build, modify, debug, or verify Runway Model Routers: inspect live config and eligible models via MCP, manage approved settings, integrate routed SDK calls, and inspect routing results. Use with +runway-dev. Not for direct per-model endpoints or agent REST CLI."
user-invocable: true
---

# Runway Dev — Model Routers

> **Companion:** Use `+runway-dev` for shared guidance when available. When this skill is installed alone, inspect the workspace, probe `RUNWAYML_API_SECRET` without printing it, and read current docs. Connect Dev MCP only when live account state or management is required.

## Goal

Keep a Model Router and its application integration correct. Verify changes with one routed SDK call (`client.generate.{video|image|audio}.create({ configId, input })`) when safe.

## Choose the path

- If the application has a known `configId` and the user supplied an implementation goal, proceed from the workspace and current docs. MCP is not required.
- If `configId` is missing, current live settings matter, or the user requests a router mutation, use Dev MCP. Do not imitate unavailable router-management tools with REST.
- A routed request does not choose a base model. The router selects one from its policy and the request's capabilities.

## Use MCP only when needed

- `list_model_routers` and `get_model_router`: resolve missing live config or inspect current settings. Resolve a `configId` to its record UUID before calling tools that require the UUID.
- `create_model_router`, `update_model_router`, and `delete_model_router`: apply approved router changes according to the live tool schema.
- `list_models`: call only for explicit allow-list, deny-list, or capability-policy work. Do not call it to choose a base model for a routed request.
- `get_credit_balance`: call only immediately before an approved billable verification.
- `get_task_routing`: call only after routed work exists or while diagnosing routing.

## Implement a routed call

1. Inspect the existing server boundary and the user-facing inputs and outputs.
2. Read https://docs.dev.runwayml.com/model-routers/generating.md for routed generation behavior.
3. Read https://docs.dev.runwayml.com/api.md for the exact endpoint contract. Do not duplicate full request schemas in skill prose or infer fields from direct-model endpoints.
4. Pass the router slug as `configId`. Put modality inputs under `input`.
5. Use routed `aspectRatio`, not the direct-model `ratio` field. Follow the current routed contract for every other field.
6. Chain the SDK wait helper directly from `create()`.

## Create or change a router

Use MCP to inspect or mutate live router state. Follow each tool's live schema. Ask for approval before a mutation unless the user already supplied the complete change, and confirm before deletion.

Call `list_models` only if the requested policy explicitly constrains models or capabilities. Router record **id** is the UUID used by management tools. **configId** is the immutable slug used by routed generation.

## Verify routing

1. Validate the intended HTTP payload with `dryRun: true`. The SDK does not currently support dry runs.
2. Keep the dry-run and live payloads identical except for `dryRun`.
3. Before a billable live call, get the credit balance and confirm the test.
4. Make one routed SDK call with the wait helper chained directly from `create()`.
5. After routed work completes, use `get_task_routing` only if routing confirmation or diagnosis is useful.

## Docs

- Model Router subset: https://docs.dev.runwayml.com/_llms-txt/model-routers.txt
- Routed generation: https://docs.dev.runwayml.com/model-routers/generating.md
- API contracts: https://docs.dev.runwayml.com/api.md
