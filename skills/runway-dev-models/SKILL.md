---
name: runway-dev-models
description: "Build, modify, debug, or verify Runway model generation in an application: discover accessible models and constraints with MCP, implement SDK calls, and wire inputs and outputs into the product UI. Use with +runway-dev. Not for Model Routers, Characters, recipes, or agent-side generate scripts."
user-invocable: true
---

# Runway Dev — Models

> **Companion:** Use `+runway-dev` for shared setup when available. Otherwise connect Dev MCP, select a project with `list_projects`, read `llms.txt`, and keep `RUNWAYML_API_SECRET` server-side.

## Goal

Help the user choose and integrate a model endpoint (`/v1/text_to_video`, `/v1/text_to_image`, etc.) across their application, including its backend call and existing UI. Verify changes with one working SDK call when safe.

## MCP tools

- `list_models` — discover models the selected project can call and read each model's `inputConstraints`.
- `get_credit_balance` — check budget before billable verification.
- `get_task` — inspect or debug an existing task, not replace SDK wait helpers in application code.

## Workflow

1. Inspect the existing application. Confirm the user experience, target modality, and where generation inputs and outputs belong.
2. Call `list_models` with `{ projectId, endpoint }`. Pick a returned model; if context pins a model id, prefer it when accessible.
3. Follow the endpoint docs linked by `llms.txt`; do not infer request fields from another model.
4. Keep `RUNWAYML_API_SECRET` behind the application's server boundary.
5. Implement or update the SDK call by chaining `.waitForTaskOutput()` in Node or `.wait_for_task_output()` in Python directly from the create call.
6. If the application has a UI, wire its controls to the backend and render loading, error, and generated-output states.
7. When verification is appropriate, submit one test generation. Present the result and offer to persist output before its signed URL expires.

## Do not

- Guess model ids, ratios, or durations from memory or other models.
- Put API keys in frontend bundles.
- Add manual polling when the SDK wait helper fits, or resubmit on transient read errors.

## Docs

- Index: https://docs.dev.runwayml.com/llms.txt
- Setup: https://docs.dev.runwayml.com/guides/setup/
