---
name: runway-dev-models
description: "Build, modify, debug, or verify Runway model generation in a server-side app: discover accessible models and constraints with MCP, implement SDK calls, and inspect tasks. Use with +runway-dev. Not for Model Routers, Characters, recipes, or agent-side generate scripts."
user-invocable: true
---

# Runway Dev — Models

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Keep a model endpoint integration (`/v1/text_to_video`, `/v1/text_to_image`, etc.) correct for the user's server-side project. Verify changes with one working SDK call when safe.

## Workflow

1. Confirm the target endpoint from provided context or ask the user (video vs image vs audio). Inspect any existing integration before changing it.
2. `list_models` with `{ projectId, endpoint }`. Pick a returned model; read `inputConstraints` for ratio, duration, and required fields.
3. If context pins a model id, prefer it when listed and accessible.
4. Check `RUNWAYML_API_SECRET` only when writing the SDK call.
5. Implement or update the server-side route/handler per `llms.txt` for that endpoint.
6. When verification is appropriate, submit one test generation and poll with `get_task` until terminal status.
7. Present result; offer to persist output locally before signed URL expiry.

## Do not

- Guess model ids, ratios, or durations from memory or other models.
- Put API keys in frontend bundles.
- Skip polling or resubmit on transient read errors.
- Use `rw-generate-*` skills when the task is agent-direct generation, not app integration.

## Docs

- Index: https://docs.dev.runwayml.com/llms.txt
- Setup: https://docs.dev.runwayml.com/guides/setup/
