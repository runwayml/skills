---
name: runway-dev
description: "Foundation for building, modifying, debugging, or verifying Runway Dev Platform integrations in an application: connect Dev MCP, use llms.txt to find current resources, resolve project context, use SDK wait helpers, and handle errors. Load with relevant runway-dev-* surface skills. Not for direct media generation scripts or REST CLI shortcuts."
user-invocable: true
---

# Runway Dev Platform

Durable workflow for integrating Runway Dev products into an application. MCP supplies live account state, the SDK is the application integration path, and `llms.txt` points to current setup guides and API references.

> **When to use:** Building, modifying, debugging, or verifying a Runway integration, including work started from Dev Portal.
>
> **Do not use for:** one-off media generation from the agent (`rw-generate-*` skills), direct REST CLI actions (`+use-runway-api`), or writing framework-specific integration code without Dev MCP (`rw-integrate-*` skills).

## Before you start

1. **Connect Dev MCP** if tools are missing. Server: `https://dev.runwayml.com/mcp`. OAuth via Runway developer account — never put an API key in MCP config. Finish login in the user's browser; do not automate OAuth. Docs: https://docs.dev.runwayml.com/guides/mcp
2. **Fetch** https://docs.dev.runwayml.com/llms.txt and follow linked docs — do not invent endpoints or field names.
3. **Inspect the workspace.** Existing project → find its backend boundary and user-facing integration point; ask where to wire Runway if unclear. Empty project → ask what to build; offer a small web app with visible inputs and output.

## MCP context

1. `whoami` — verify identity.
2. `list_projects` — pick project; never guess a `projectId`.
3. For generation: `list_models` with the target endpoint. Honor each model's `inputConstraints`; do not reuse values from another model.
4. `get_credit_balance` before a billable test.

## API key (SDK only)

MCP uses OAuth. Generation SDK calls use `RUNWAYML_API_SECRET` in server-side env or dotenv — never client-side, never in chat, never hard-coded. Ask the user to add it when the SDK call is imminent.

## SDK requests

1. Build one valid SDK request from the API docs linked by `llms.txt` and MCP `list_models` constraints.
2. For task-based SDK calls, use `.waitForTaskOutput()` in Node or `.wait_for_task_output()` in Python. Submit once; do not add a manual polling loop when the SDK helper fits.
3. Use MCP `get_task` only to inspect or debug an existing task outside the application's SDK flow.
4. Wire successful output into the application's intended UI or consumer. Persist outputs if the app needs them after signed URLs expire (~24–48h).

## Terminology

| UI / quickstart | MCP / API |
|-----------------|-----------|
| Characters | avatars (`list_avatars`, `get_avatar`) |
| Character ID | avatar UUID |
| Model Router config ID | immutable slug (`configId`) |
| live Session | `POST /v1/realtime_sessions` |

## Errors

- Validation error → show message, fix field from MCP constraints or docs, retry once.
- Auth/permission → stop; ask user to authenticate or pick accessible project.
- Rate limit → honor retry interval.
- `FAILED` task → report failure details; do not auto-resubmit.
- Missing MCP tool → do not invent REST fallbacks for account management.

## Surface skills

| Skill | When |
|-------|------|
| `+runway-dev-models` | Model generation integration |
| `+runway-dev-model-routers` | Model Router setup and routed calls |
| `+runway-dev-characters` | Characters / realtime sessions |
| `+runway-dev-recipes` | Recipe pipelines |
| `+runway-dev-workflows` | Runway app workflows → API endpoints |

Load `+runway-dev` first, then the relevant surface skill or skills. Usually one surface skill matches the user's goal; load more when the task crosses surfaces.
