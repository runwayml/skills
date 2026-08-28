---
name: runway-dev
description: "Foundation for building, modifying, debugging, or verifying Runway Dev Platform integrations in an application: connect Dev MCP, use llms.txt to find current resources, resolve project context, use SDK wait helpers, and handle errors. Load with relevant runway-dev-* surface skills. Not for direct media generation scripts or REST CLI shortcuts."
user-invocable: true
---

# Runway Dev Platform

Workflow for integrating Runway Dev products into an application. Use MCP for live account state and management, the SDK for application code, and current docs for API contracts.

> **When to use:** Building, modifying, debugging, or verifying a Runway integration, including work started from Dev Portal.
>
> **Do not use for:** one-off media generation from the agent or direct REST CLI actions.

## Start with the work

Make useful progress before explaining setup. Inspect the workspace and existing configuration without narrating each check. Ask a question only when missing information blocks the next change.

- Existing project: find its server boundary and user-facing integration point. Add a server route or function before integrating a frontend-only project.
- Empty workspace: ask what the user wants to build. You may recommend a small web app with visible inputs and output as a Runway starting point, but do not claim the user requested one.
- Before giving credential setup instructions, test whether `RUNWAYML_API_SECRET` is present without printing its value, for example with `test -n "${RUNWAYML_API_SECRET:-}"`. If it is present, skip dotenv instructions.
- Use the official SDK. Install `@runwayml/sdk` for Node or `runwayml` for Python only if the project needs it and does not already have it.
- Keep updates short. Do not narrate a long setup sequence or checklist.

## Current contracts

Installed skill prose is workflow guidance, not the canonical API schema. Resolve current contracts in this order:

1. Fetch https://docs.dev.runwayml.com/llms.txt.
2. Fetch only the exact linked documentation subset relevant to the task.
3. If that subset does not define the contract, read https://docs.dev.runwayml.com/api.md.
4. If machine-readable detail is still needed, use https://docs.dev.runwayml.com/openapi.json.

Do not invent endpoints, field names, or model constraints.

## MCP policy

Encourage connecting Dev MCP as the happy path for live account context and management. Connect `https://dev.runwayml.com/mcp` with Runway OAuth. Never put an API key in MCP config or automate browser OAuth.

If the user declines or the connection fails, never block account-independent work. Continue with live docs, existing application config, or environment configuration. SDK and API integration code remain allowed. Stop only when the next requested step requires live account discovery, account or resource mutations, or billable verification.

Never imitate an unavailable MCP account-management or resource-management tool with a REST call. Explain the MCP dependency only when it blocks the requested action.

Call MCP tools only when the result affects the next step:

- `whoami` when identity or access is uncertain.
- `list_projects` when a live `projectId` must be selected or verified. Never guess one.
- `list_models` when model access, selection, or current constraints matter.
- `get_credit_balance` immediately before an approved billable verification.

## API key (SDK only)

MCP uses OAuth. SDK calls use an organization-scoped API key from Developer Portal settings. Probe `RUNWAYML_API_SECRET` without printing it. If missing when a live SDK call is imminent, ask the user to store the key in a server-side environment file or secret manager. Never expose it client-side, in chat, or in source control; ensure local environment files are ignored.

## SDK requests

1. Build one valid SDK request from the current API docs and, when needed, MCP `list_models` constraints.
2. Chain the wait helper directly from the create call: `await client.<operation>.create({...}).waitForTaskOutput()` in Node or `client.<operation>.create(...).wait_for_task_output()` in Python. Do not await `create()` before calling the helper.
3. Catch the SDK's `TaskFailedError` and surface its task details. Submit once; do not add a manual polling loop or auto-resubmit.
4. Use MCP `get_task` only to inspect or debug an existing task outside the application's SDK flow.
5. Wire successful output into the application's intended UI or consumer. Persist outputs if the app needs them after signed URLs expire (~24–48h).

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
- Missing MCP tool → continue account-independent implementation; stop only when live account state or management is required.

## Surface skills

| Skill | When |
|-------|------|
| `+runway-dev-models` | Model generation integration |
| `+runway-dev-model-routers` | Model Router setup and routed calls |
| `+runway-dev-characters` | Characters / realtime sessions |
| `+runway-dev-recipes` | Recipe pipelines |
| `+runway-dev-workflows` | Runway app workflows → API endpoints |

Use `+runway-dev` with the relevant surface skill or skills when both are installed. Surface skills repeat their minimum setup so they remain useful when installed alone. Usually one surface matches the user's goal; load more when the task crosses surfaces.
