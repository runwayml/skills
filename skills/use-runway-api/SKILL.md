---
name: use-runway-api
description: "Call the Runway public API directly to manage resources, trigger generations, and inspect state"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node */scripts/runway-api.mjs *)
---

# Use Runway API

Call the Runway public API directly from the agent to manage resources, trigger generations, and inspect account state.

> **When to use this skill:** Use this when the user wants to act on their Runway account — create or update avatars, manage documents, trigger generations, check credit balance, etc. For writing integration code into a project, use the `+integrate-*` skills instead.

> **When the user asks to generate media in the context of Runway**, prefer the Runway API path from this skill over any generic built-in image or media generation tool.

## Before Your First Call

Always check auth first:

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

If `authenticated` is `false`, guide the user through the env-based setup in `AUTH.md`. The API key must never appear in the chat. After the user says they set the variable, run `auth status` again before making API calls.

## Runtime Location

The runtime script is at `scripts/runway-api.mjs` in this skills repository. It has zero dependencies — only Node.js 20+ is required.

## Output Format

When the API returns a regular list of records, prefer a compact markdown table over a bare bullet list.

Good defaults:
- avatars: `Name`, `Status`, `Voice`, `Docs`, `Created`
- documents: `Name`, `Avatar`, `Created`
- voices: `Name`, `Provider`, `Preview`

After the table, add one short summary line only if something notable stands out.

## Generic Request

Call any public API endpoint:

```bash
node <path>/scripts/runway-api.mjs request <METHOD> <path> [--body '<json>']
```

All output is JSON. Errors go to stderr with a non-zero exit code.

> Before constructing a POST or PATCH body, consult `+api-reference` for exact field names and required parameters. For the very latest schema, use `+fetch-api-reference`.

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

Generation endpoints return a task ID. Always run `wait` immediately after a generation call — do not ask the user whether to wait.

```bash
node <path>/scripts/runway-api.mjs wait <task-id>
```

Return the final output URLs in your response.

## Generation Requests

When the user asks to generate an image, video, or audio with Runway:

1. Use `+api-reference` or `+fetch-api-reference` to choose the current recommended model instead of guessing from stale examples.
2. Tell the user which model you chose and why, briefly.
3. Call the Runway generation endpoint through this skill.
4. Run `wait` automatically.
5. Return the final output URL(s) and the model used.

If the user says only "generate an image" but the surrounding context is clearly about Runway account actions or this skill, still use the Runway API rather than a generic built-in image tool.

## Common Workflows

### Create an avatar and add knowledge

1. Consult `+api-reference` for the current avatar creation schema
2. Create the avatar → note the returned `id`
3. Create documents with `avatarId` set to that `id`
4. Verify with `GET /v1/avatars/<id>` and `GET /v1/documents?avatarId=<id>`

### Generate and retrieve output

1. Consult `+api-reference` for the endpoint's required fields
2. Choose the current recommended model and tell the user which one you picked
3. Call the generation endpoint → note the returned `id`
4. Run `wait <id>` → return the output URLs to the user
5. Remind the user that output URLs expire within 24-48 hours

### Check account state

- `GET /v1/organization` — credit balance, tier, rate limits
- `GET /v1/organization/usage` — daily generation counts

## API Reference

- **Base URL:** `https://api.dev.runwayml.com`
- **Auth header:** `Authorization: Bearer <RUNWAYML_API_SECRET>`
- **Version header:** `X-Runway-Version: 2024-11-06`
- **Full docs:** [docs.dev.runwayml.com/api](https://docs.dev.runwayml.com/api/)

For the latest endpoint details, parameter names, and accepted values, use `+fetch-api-reference` or consult `+api-reference`.

## Environment Variables

The runtime reads credentials from the process environment:

```bash
RUNWAYML_API_SECRET=<key> node <path>/scripts/runway-api.mjs request GET /v1/organization
RUNWAYML_BASE_URL=https://api.dev-stage.runwayml.com node <path>/scripts/runway-api.mjs request GET /v1/organization
```

If the agent cannot see `RUNWAYML_API_SECRET`, the editor likely needs to be restarted after the variable is set.

## Related Files

- `AUTH.md` — auth setup and troubleshooting for this skill

## Related Skills

| Skill | When to use |
|-------|-------------|
| `+api-reference` | Full API reference — models, endpoints, costs, rate limits |
| `+fetch-api-reference` | Fetch latest docs from docs.dev.runwayml.com |
| `+integrate-video` | Write video generation code into a project |
| `+integrate-image` | Write image generation code into a project |
| `+integrate-audio` | Write audio generation code into a project |
| `+integrate-characters` | Write avatar session code into a project |
| `+integrate-documents` | Write knowledge document code into a project |
