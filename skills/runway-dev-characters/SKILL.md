---
name: runway-dev-characters
description: "Integrate Runway Characters: preset or custom avatar live Sessions via SDK. Use with +runway-dev. UI says Characters; MCP/API use avatars. Not for avatar video generation endpoints or embed-only UI without server session."
user-invocable: true
---

# Runway Dev — Characters

> **Prerequisite:** Load and follow `+runway-dev` first.

## Terminology

- Dev Portal **Characters** = API **avatars** (`list_avatars`, `get_avatar`).
- **Character ID** in quickstart = avatar UUID.
- **live Session** = realtime conversation via `POST /v1/realtime_sessions`.
- Default preset when none pinned: `influencer` (`{ type: 'runway-preset', presetId: 'influencer' }`).

## List surface (no pinned character)

1. Do not ask preset vs create vs video vs embed unless user already specified another path.
2. Start with preset `influencer`; follow Characters session docs from `llms.txt`.
3. One working Session end-to-end: create session, poll for `sessionKey`, confirm lifecycle.

## Detail surface (pinned avatar UUID)

1. `get_avatar` for status and attached knowledge document ids.
2. Start Session with that character id; do not substitute another avatar.
3. If status is `PROCESSING`, poll until `READY` or stop on `FAILED`.

## Optional MCP resources

- `list_avatars` / `get_avatar` — inspect custom avatars in project.
- Knowledge docs: `list_avatar_knowledge_documents`, create/update via MCP write tools when user wants domain knowledge.

For React embed UI, also see `+rw-integrate-character-embed`. For server-side session management patterns, `+rw-integrate-characters`.

## Docs

- https://docs.dev.runwayml.com/llms.txt
- Avatar SDK: https://github.com/runwayml/avatar-sdk-react
