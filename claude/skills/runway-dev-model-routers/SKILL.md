---
name: runway-dev-model-routers
description: "Use when an application should send image, video, or audio generation through a saved Runway Model Router configuration, or when the user asks to inspect or manage one. Resolve the live config and follow current router docs. For a fixed direct model endpoint, use runway-dev-models instead."
user-invocable: true
---

# Runway Dev Model Routers

Model Routers let an application refer to a saved routing preference instead of embedding a particular model choice. Consult `runway-dev` for account setup, credential handling, and SDK task guidance when that skill is installed.

## Existing integration

1. Inspect the application's existing `configId` and its server-side request path.
2. When the live configuration or access must be verified, use Dev MCP to locate the router by `configId`, then fetch details using the identifier returned by the tool. A router record UUID and its `configId` are distinct values; pass the configured `configId` in SDK requests.
3. Read the current overview and generation guide at `https://docs.dev.runwayml.com/model-routers/` and `https://docs.dev.runwayml.com/model-routers/generating/`. Router request fields and types differ from direct-model endpoints; use the schema for the modality being called.
4. Integrate the documented SDK method (`generate.video`, `generate.image`, or `generate.audio`) behind the application's server boundary. Chain the SDK task wait helper directly from `create()`.
5. Validate with local checks such as type checks, builds, and tests that mock the SDK. Do not issue a live generation yourself. Tell the user how to run the integration from their application, and note that live generations consume project credits. To check routing without generating media, the user's application can send the documented HTTP request with `dryRun: true`; SDK dry-run support is not documented. Keep the dry-run and live input equivalent, and use current docs for response fields.

## Creating or changing a router

Use live MCP tools to inspect or manage router state. Clarify missing targets or routing preferences; when the user has specified them, carry out the requested creation or update without requiring another confirmation or a JSON preview. Summarize the result in plain English unless the user asks for raw configuration.

Updating `settings` replaces the full settings object and clears omitted optional fields. Read the current configuration before updating it and preserve settings the user did not ask to change. Updating only `name` or `description` leaves settings unchanged. Confirm before deleting a router unless the user already explicitly requested deletion of that exact router.

Check current eligible models and constraints through Dev MCP when they affect the configuration. Do not hardcode a model catalog, pricing, or model eligibility in this skill.

Use the available MCP tools for the requested action: `list_model_routers` and `get_model_router` for inspection; `create_model_router`, `update_model_router`, or `delete_model_router` for changes; `list_models` for current eligible models; `get_credit_balance` when the user asks about project credits; and `get_task_routing` to inspect an existing task's routing.

## Explain a routed result

The response and task detail can expose routing information such as the selected model and estimated or actual cost. Use the live response or documented task inspection tool to describe what happened; do not assume the router chose a model based only on its preference settings. If the user asks why an existing task routed a certain way, inspect its routing details through the available MCP tool.

## Current docs

- [Model Routers overview](https://docs.dev.runwayml.com/model-routers/)
- [Generating through a Router](https://docs.dev.runwayml.com/model-routers/generating/)
- [Configure a Router](https://docs.dev.runwayml.com/model-routers/configuration/)
- [Runway Dev agent context](https://docs.dev.runwayml.com/ai-context.md)
