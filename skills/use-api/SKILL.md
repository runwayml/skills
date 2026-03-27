---
name: use-api
description: "Call the Runway public API directly to manage resources, trigger generations, and inspect state"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node */scripts/runway-api.mjs *)
---

# Use Runway API

Call the Runway public API directly from the agent to manage resources, trigger generations, and inspect account state.

> **When to use this skill:** Use this when the user wants to **act on their Runway account** — create or update avatars, manage documents, trigger generations, check credit balance, etc. For writing integration code into a project, use the `+integrate-*` skills instead.

## Before Your First Call

**Always check auth before making API calls.** Run:

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

If `authenticated` is `false`, follow the `+setup-global-auth` skill to walk the user through authentication. Do not proceed with API calls until auth is confirmed.

## Runtime Location

The runtime script is at `scripts/runway-api.mjs` in this skills repository. It has zero dependencies — only Node.js 20+ is required. All commands below assume you have resolved the path to it.

## Generic Request

Call any public API endpoint:

```bash
node <path>/scripts/runway-api.mjs request <METHOD> <path> [--body '<json>']
```

All output is JSON. Errors go to stderr with a non-zero exit code.

> **Before constructing a POST or PATCH body**, consult `+api-reference` for exact field names and required parameters. For the very latest schema, use `+fetch-api-reference`. The examples below cover simple, stable operations only — endpoints with richer schemas (avatar creation, generation) are documented in the reference skills.

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

## Waiting for Tasks

Generation endpoints return a task ID. **Always run `wait` immediately after a generation call** — do not ask the user whether to wait. Return the final output URLs in your response.

```bash
node <path>/scripts/runway-api.mjs wait <task-id>
```

Prints progress to stderr and the final task object (with output URLs) to stdout on completion. Exits with code 1 if the task fails.

## Common Workflows

### Create an avatar and add knowledge

1. Consult `+api-reference` for the current avatar creation schema
2. Create the avatar → note the returned `id`
3. Create documents with `avatarId` set to that `id`
4. Verify with `GET /v1/avatars/<id>` and `GET /v1/documents?avatarId=<id>`

### Generate and retrieve output

1. Consult `+api-reference` for the endpoint's required fields
2. Call the generation endpoint → note the returned `id`
3. Run `wait <id>` → return the output URLs to the user
4. Remind the user that output URLs expire within 24-48 hours

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
