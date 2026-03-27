---
name: use-api
description: "Call the Runway public API directly to manage resources, trigger generations, and inspect state"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node */scripts/runway-api.mjs *)
---

# Use Runway API

Call the Runway public API directly from the agent to manage resources, trigger generations, and inspect account state.

> **When to use this skill:** Use this when the user wants to **act on their Runway account** — create or update avatars, manage documents, trigger generations, check credit balance, etc. For writing integration code into a project, use the `+integrate-*` skills instead.

> **Prerequisites:** Global auth must be configured first. Run `+setup-global-auth` if `auth status` shows `authenticated: false`.

## Runtime Location

The runtime script is at `scripts/runway-api.mjs` in this skills repository. It has zero dependencies — only Node.js 20+ is required. All commands below assume you have resolved the path to it.

## Generic Request

Call any public API endpoint:

```bash
node <path>/scripts/runway-api.mjs request <METHOD> <path> [--body '<json>']
```

All output is JSON. Errors go to stderr with a non-zero exit code.

### Examples

**Get organization info:**
```bash
node <path>/scripts/runway-api.mjs request GET /v1/organization
```

**List avatars:**
```bash
node <path>/scripts/runway-api.mjs request GET /v1/avatars
```

**Get a specific avatar:**
```bash
node <path>/scripts/runway-api.mjs request GET /v1/avatars/<id>
```

**Create an avatar:**
```bash
node <path>/scripts/runway-api.mjs request POST /v1/avatars --body '{
  "name": "Support Agent",
  "referenceImage": "https://example.com/headshot.jpg",
  "personality": "Friendly and helpful support agent",
  "voicePresetId": "victoria"
}'
```

**Update an avatar:**
```bash
node <path>/scripts/runway-api.mjs request PATCH /v1/avatars/<id> --body '{
  "personality": "Updated personality text"
}'
```

**Delete an avatar:**
```bash
node <path>/scripts/runway-api.mjs request DELETE /v1/avatars/<id>
```

**List knowledge documents for an avatar:**
```bash
node <path>/scripts/runway-api.mjs request GET "/v1/documents?avatarId=<avatar-id>"
```

**Create a knowledge document:**
```bash
node <path>/scripts/runway-api.mjs request POST /v1/documents --body '{
  "avatarId": "<avatar-id>",
  "name": "FAQ",
  "content": "Q: What is your return policy?\nA: 30 days, no questions asked."
}'
```

**List voices:**
```bash
node <path>/scripts/runway-api.mjs request GET /v1/voices
```

**Generate an image:**
```bash
node <path>/scripts/runway-api.mjs request POST /v1/text_to_image --body '{
  "model": "gen4_image",
  "promptText": "A red door in a white wall"
}'
```

**Generate a video:**
```bash
node <path>/scripts/runway-api.mjs request POST /v1/image_to_video --body '{
  "model": "gen4_turbo",
  "promptImage": "https://example.com/photo.jpg",
  "promptText": "Slow push in",
  "ratio": "1280:720"
}'
```

## Waiting for Tasks

Generation endpoints return a task ID. Poll until completion:

```bash
node <path>/scripts/runway-api.mjs wait <task-id>
```

Prints progress to stderr and the final task object (with output URLs) to stdout on completion. Exits with code 1 if the task fails.

## Common Workflows

### Create an avatar and add knowledge

1. Create the avatar → note the returned `id`
2. Create documents with `avatarId` set to that `id`
3. Verify with `GET /v1/avatars/<id>` and `GET /v1/documents?avatarId=<id>`

### Generate and retrieve output

1. Call a generation endpoint (e.g. `POST /v1/text_to_image`) → note the `id`
2. Run `wait <id>` → get the final task with output URLs
3. Output URLs expire — download or use them promptly

### Check account state

- `GET /v1/organization` — credit balance, tier, rate limits
- `GET /v1/organization/usage` — daily generation counts

## API Reference

- **Base URL:** `https://api.dev.runwayml.com`
- **Auth header:** `Authorization: Bearer <RUNWAYML_API_SECRET>`
- **Version header:** `X-Runway-Version: 2024-11-06`
- **Full docs:** [docs.dev.runwayml.com/api](https://docs.dev.runwayml.com/api/)

For the latest endpoint details, parameter names, and accepted values, use `+fetch-api-reference` or consult `+api-reference`.

## Environment Variable Override

To make a one-off call with a different key or base URL without changing stored credentials:

```bash
RUNWAYML_API_SECRET=<key> node <path>/scripts/runway-api.mjs request GET /v1/organization
RUNWAYML_BASE_URL=https://api.dev-stage.runwayml.com node <path>/scripts/runway-api.mjs request GET /v1/organization
```

## Related Skills

| Skill | When to use |
|-------|-------------|
| `+setup-global-auth` | First-time auth setup or switching environments |
| `+api-reference` | Full API reference — models, endpoints, costs, rate limits |
| `+fetch-api-reference` | Fetch latest docs from docs.dev.runwayml.com |
| `+integrate-video` | Write video generation code into a project |
| `+integrate-image` | Write image generation code into a project |
| `+integrate-audio` | Write audio generation code into a project |
| `+integrate-characters` | Write avatar session code into a project |
| `+integrate-documents` | Write knowledge document code into a project |
