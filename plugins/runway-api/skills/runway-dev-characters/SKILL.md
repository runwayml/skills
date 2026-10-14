---
name: runway-dev-characters
description: "Use when building or maintaining a Runway Characters integration, including avatar discovery or management, realtime Sessions, knowledge, and the call interface. Follow current Characters and SDK docs. Do not use for generating avatar videos from text or audio."
user-invocable: true
---

# Runway Characters

The Developer Portal calls these **Characters**; the API and SDK use **Avatars**. A realtime **Session** is one live conversation. Consult `runway-dev` for account setup and shared credential guidance when installed.

## Workflow

1. Inspect the app's call experience and server architecture. Ask whether it should use an existing Character, a documented preset, or a newly created custom Avatar only when that choice is not already clear.
2. When live account state or a user's Character matters, use Dev MCP to inspect the available Avatars and their state. Do not substitute a different Avatar or guess a preset ID. If a custom Avatar is requested, use its reference image and current API/MCP schema.
3. Follow the current [Characters integration guide](https://docs.dev.runwayml.com/characters/integration/) and [SDK documentation](https://docs.dev.runwayml.com/_llms-txt/characters.txt). Check the `@runwayml/avatars-react` README for current React components, hooks, and styles; use `@runwayml/avatars` for a non-React web client.
4. Create Sessions server-side with `@runwayml/sdk`. Keep `RUNWAYML_API_SECRET` on the server. Follow the current Session readiness and credential-consumption flow; expose only the one-time connection fields the browser SDK needs. Never send the API secret to the browser.
5. Handle permission, connecting, active, failed, and ended states in the app UI. End or cancel a Session during teardown according to the current SDK/API guidance. If single-use credentials have already been consumed and connection fails, create a new Session rather than reusing them.
6. Run local checks. A live Session may incur usage; only open one for verification when requested or approved.

## Live data and knowledge

Use the available MCP tools to inspect live Avatars with `list_avatars` and `get_avatar`, and knowledge documents with `list_avatar_knowledge_documents` and `get_avatar_knowledge_document`. `create_avatar`, `update_avatar`, and `delete_avatar` manage Avatars; the corresponding `*_avatar_knowledge_document` tools manage knowledge documents. After creating an Avatar, check it with `get_avatar` until its state is `READY` or `FAILED`. Read the existing record and current tool contract before changing it, and confirm destructive deletes with the user. If MCP is unavailable, continue app code that can be implemented from docs and existing IDs, and pause only the step that requires live account state.

## Current docs

- [Characters overview](https://docs.dev.runwayml.com/characters/)
- [Build an integration](https://docs.dev.runwayml.com/characters/integration/)
- [Session concepts and lifecycle](https://docs.dev.runwayml.com/characters/concepts/)
- [Characters documentation set](https://docs.dev.runwayml.com/_llms-txt/characters.txt)
- [React SDK](https://github.com/runwayml/avatar-sdk-react)
