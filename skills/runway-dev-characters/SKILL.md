---
name: runway-dev-characters
description: "Build, modify, debug, or verify Runway Characters integrations: inspect preset or custom avatars with MCP and manage live Sessions via SDK. Use with +runway-dev. UI says Characters; MCP/API use avatars. Not for avatar video generation endpoints or embed-only UI without server sessions."
user-invocable: true
---

# Runway Dev — Characters

> **Prerequisite:** Load and follow `+runway-dev` first.

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
3. Implement, modify, debug, or verify the Session flow based on the user's goal. For end-to-end verification, create one session, poll for `sessionKey`, and confirm lifecycle.

## Character specified

1. `get_avatar` for status and attached knowledge document ids.
2. Use that character id; do not substitute another avatar.
3. If status is `PROCESSING`, poll until `READY` or stop on `FAILED`.

## MCP tools

- `list_avatars` / `get_avatar` — inspect custom avatars in project.
- `create_avatar` / `update_avatar` / `delete_avatar` — manage custom characters; confirm destructive changes before applying them.
- `list_avatar_knowledge_documents` / `get_avatar_knowledge_document` — inspect attached knowledge.
- `create_avatar_knowledge_document` / `update_avatar_knowledge_document` / `delete_avatar_knowledge_document` — manage domain knowledge when requested; confirm deletion first.

For React embed UI, also see `+rw-integrate-character-embed`. For server-side session management patterns, `+rw-integrate-characters`.

## Docs

- https://docs.dev.runwayml.com/llms.txt
- Avatar SDK: https://github.com/runwayml/avatar-sdk-react
