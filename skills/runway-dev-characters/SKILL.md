---
name: runway-dev-characters
description: "Build, modify, debug, or verify Runway Characters integrations: inspect preset or custom avatars with MCP and manage live Sessions via SDK. Use with +runway-dev. UI says Characters; MCP/API use avatars. Not for avatar video generation endpoints or embed-only UI without server sessions."
user-invocable: true
---

# Runway Dev — Characters

> **Prerequisite:** Load and follow `+runway-dev` first.

## Goal

Keep a Characters integration and its live Session lifecycle correct. Verify changes end-to-end when safe.

## Terminology

- Dev Portal **Characters** = API **avatars** (`list_avatars`, `get_avatar`).
- **Character ID** = avatar UUID.
- **live Session** = realtime conversation via `POST /v1/realtime_sessions`.
- Default preset when none specified: `influencer` (`{ type: 'runway-preset', presetId: 'influencer' }`).

## No character specified

1. Do not ask preset vs create vs video vs embed unless user already specified another path.
2. Start with preset `influencer`; follow Characters session docs from `llms.txt`.
3. Implement, modify, debug, or verify the Session flow based on the user's goal. For end-to-end verification, create one session, poll for `sessionKey`, and confirm lifecycle.

## Character specified

1. `get_avatar` for status and attached knowledge document ids.
2. Use that character id; do not substitute another avatar.
3. If status is `PROCESSING`, poll until `READY` or stop on `FAILED`.

## Optional MCP resources

- `list_avatars` / `get_avatar` — inspect custom avatars in project.
- Knowledge docs: `list_avatar_knowledge_documents`, create/update via MCP write tools when user wants domain knowledge.

For React embed UI, also see `+rw-integrate-character-embed`. For server-side session management patterns, `+rw-integrate-characters`.

## Docs

- https://docs.dev.runwayml.com/llms.txt
- Avatar SDK: https://github.com/runwayml/avatar-sdk-react
