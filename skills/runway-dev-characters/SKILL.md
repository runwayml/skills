---
name: runway-dev-characters
description: "Build, modify, debug, or verify Runway Characters integrations: inspect preset or custom avatars with MCP and manage live Sessions via SDK. Use with +runway-dev. UI says Characters; MCP/API use avatars. Not for avatar video generation endpoints or embed-only UI without server sessions."
user-invocable: true
---

# Runway Dev — Characters

> **Companion:** Use `+runway-dev` for shared setup when available. Otherwise connect Dev MCP, select a project with `list_projects`, read the Characters docs from `llms.txt`, and keep `RUNWAYML_API_SECRET` server-side.

## Goal

Keep a Characters integration and its live Session lifecycle correct across the application's backend and UI. Verify changes end-to-end when safe.

## Terminology

- Dev Portal **Characters** = API **avatars** (`list_avatars`, `get_avatar`).
- **Character ID** = avatar UUID.
- **live Session** = realtime conversation via `POST /v1/realtime_sessions`.
- Fallback preset when the user wants a default: `influencer` (`{ type: 'runway-preset', presetId: 'influencer' }`).

## No character specified

1. Ask whether the user wants an existing character, a preset, or a custom character from an image. Do not branch into avatar-video generation unless requested.
2. For a custom character, ask the user to supply the image and use `create_avatar` according to its live MCP tool schema. If the user wants a default instead, use preset `influencer`.
3. Implement the Session lifecycle behind the server boundary: create once, poll `NOT_READY` until `READY`, consume connection credentials once, and return only the connection fields the client needs.
4. Connect the application's call UI with the current Avatar SDK, then end or cancel the Session during teardown so it does not keep running.
5. For end-to-end verification, connect one Session successfully and cleanly end it.

## Character specified

1. `get_avatar` for status and attached knowledge document ids.
2. Use that character id; do not substitute another avatar.
3. If status is `PROCESSING`, poll until `READY` or stop on `FAILED`.

## MCP tools

- `list_avatars` / `get_avatar` — inspect custom avatars in project.
- `create_avatar` / `update_avatar` / `delete_avatar` — manage custom characters; confirm destructive changes before applying them.
- `list_avatar_knowledge_documents` / `get_avatar_knowledge_document` — inspect attached knowledge.
- `create_avatar_knowledge_document` / `update_avatar_knowledge_document` / `delete_avatar_knowledge_document` — manage domain knowledge when requested; confirm deletion first.

## Docs

- https://docs.dev.runwayml.com/llms.txt
- Characters: https://docs.dev.runwayml.com/_llms-txt/characters.txt
- Avatar SDK: https://github.com/runwayml/avatar-sdk-react
