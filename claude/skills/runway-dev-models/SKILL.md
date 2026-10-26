---
name: runway-dev-models
description: "Use when adding or maintaining a direct Runway Dev model endpoint in an application, including image, video, audio, or task handling. Discover current model access and constraints when needed, follow the exact endpoint contract, and integrate through the official SDK. For configured model-agnostic routing, use runway-dev-model-routers instead."
user-invocable: true
---

# Runway Dev models

Integrate a direct model endpoint into the application's existing server and user flow. Consult `runway-dev` for account setup, credential boundaries, and shared SDK guidance when that skill is installed.

## Workflow

1. Inspect the app and determine where users provide inputs and consume outputs. Keep Runway requests behind the app's server boundary.
2. Honor a model the user or existing app explicitly selected. If a model must be selected or current project access and constraints matter, use Dev MCP's `list_models` for the relevant project and endpoint. Never guess a project ID or infer access from a model name.
   For catalog summaries, preserve each endpoint's returned price units and constraints, and verify model counts against the full response.
3. Read the exact current endpoint reference from `https://docs.dev.runwayml.com/llms.txt` and `https://docs.dev.runwayml.com/api.md`. A model's fields, allowed values, inputs, and outputs can differ from other models; copy no schema from a neighboring endpoint.
4. Use the official SDK for the app's language. For task-creating calls, chain `waitForTaskOutput()` or `wait_for_task_output()` from the unawaited `create()` response. Handle documented task errors and let the user inspect or recover the task rather than silently submitting it again.
5. Wire success, loading, and error states into the existing interface. Treat signed output URLs as temporary; persist media if the application needs it later.
6. Validate with local checks such as type checks, builds, and tests that mock the SDK. Do not run a live generation yourself. Tell the user how to run the integration from their application, and note that live generations consume project credits.

## Inputs and credentials

Follow the current input documentation for HTTPS URLs, data URIs, and upload URIs. For browser-selected files, send the file to the application's server and use the SDK's documented upload flow. Do not pass local filesystem paths to the API or accept arbitrary client-supplied remote URLs without validation.

Keep `RUNWAYML_API_SECRET` on the server in the project's existing secret mechanism. Never expose it to browser code or place it in MCP configuration; Dev MCP uses OAuth separately.

## Current docs

- [Runway Dev agent context](https://docs.dev.runwayml.com/ai-context.md)
- [Models](https://docs.dev.runwayml.com/guides/models/)
- [Inputs](https://docs.dev.runwayml.com/assets/inputs/)
- [Outputs](https://docs.dev.runwayml.com/assets/outputs/)
- [SDK task waiting and errors](https://docs.dev.runwayml.com/api-details/sdks/)
