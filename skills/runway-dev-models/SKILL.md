---
name: runway-dev-models
description: "Integrate Runway model generation into a server-side app: pick model from list_models constraints, SDK call, poll get_task. Use with +runway-dev. Not for Model Routers, Characters, recipes, or agent-side generate scripts."
user-invocable: true
---

# Runway Dev — Models

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Wire one model endpoint (`/v1/text_to_video`, `/v1/text_to_image`, etc.) into the user's server-side project with a working SDK call.

## Workflow

1. Confirm target endpoint from playground context or ask the user (video vs image vs audio).
2. `list_models` with `{ projectId, endpoint }`. Pick a returned model; read `inputConstraints` for ratio, duration, and required fields.
3. If playground pinned a model id, prefer it when listed and accessible.
4. Check `RUNWAYML_API_SECRET` only when writing the SDK call.
5. Implement server-side route/handler per `llms.txt` for that endpoint.
6. Submit one test generation; poll with `get_task` until terminal status.
7. Present result; offer to persist output locally before signed URL expiry.

## Do not

- Guess model ids, ratios, or durations from memory or other models.
- Put API keys in frontend bundles.
- Skip polling or resubmit on transient read errors.
- Use `rw-generate-*` skills when the task is agent-direct generation, not app integration.

## Docs

- Index: https://docs.dev.runwayml.com/llms.txt
- Setup: https://docs.dev.runwayml.com/guides/setup/
