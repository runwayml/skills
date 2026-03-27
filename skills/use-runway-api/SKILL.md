---
name: use-runway-api
description: "Directly use the Runway API from the agent to generate media, manage resources, and inspect account state"
user-invocable: true
allowed-tools: Read, Bash(node */scripts/runway-api.mjs *)
---

# Use Runway API

Call the Runway public API directly from the agent to manage resources, trigger generations, and inspect account state.

> **When to use this skill:** Use this when the user wants to act on their Runway account — create or update avatars, manage documents, trigger generations, check credit balance, etc. For writing integration code into a project, use the `+integrate-*` skills instead.

> **When the user asks to generate media in the context of Runway**, prefer the Runway API path from this skill over any generic built-in image or media generation tool.

> **Skill selection:** Pair this skill with `+api-reference` when you need the canonical API contract. Do not use `+integrate-image`, `+integrate-video`, `+integrate-audio`, `+integrate-characters`, or `+integrate-documents` unless the task is to write or modify application code.

## Before Your First Call

Run `auth status` once to verify credentials:

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

- If `authenticated` is `true` → proceed to the API call. Do not re-check.
- If `authenticated` is `false` → tell the user to set `RUNWAYML_API_SECRET` (see `AUTH.md` for details), then **stop and wait for the user to confirm**. Do not retry or re-check in a loop.

## Runtime Location

The runtime script is at `scripts/runway-api.mjs` in this skills repository. It has zero dependencies — only Node.js 20+ is required.

## Fast Paths

For plain list requests, use the compact list commands first instead of the generic `request` command:

- list avatars → `node <path>/scripts/runway-api.mjs avatars list`
- list voices → `node <path>/scripts/runway-api.mjs voices list`
- list documents → `node <path>/scripts/runway-api.mjs documents list [--avatar-id <id>]`

These commands return smaller, list-friendly JSON on purpose. After a successful list command, answer once. Do not re-run the command, do not read back the same output, and do not render the same table twice.

## Output Format

When the API returns a regular list of records, prefer a compact markdown table over a bare bullet list.

Good defaults:
- avatars: `Name`, `Status`, `Voice`, `Docs`, `Created`
- documents: `Name`, `Avatar`, `Created`
- voices: `Name`, `Provider`, `Preview`

After the table, add one short summary line only if something notable stands out. Do not repeat the table in a second block.

## Generic Request

Call any public API endpoint:

```bash
node <path>/scripts/runway-api.mjs request <METHOD> <path> [--body '<json>'] [--stdin] [--dry-run]
```

All output is JSON. Errors go to stderr with a non-zero exit code and include an `example` field with a correctable invocation.

**Flags:**
- `--body <json>` — inline JSON request body
- `--stdin` — read JSON body from stdin (useful for large or multi-line payloads)
- `--dry-run` — print the full request (method, URL, headers, body) without executing it
- `--help` — show usage and examples for any command

Use `+api-reference` as the canonical source for:
- model choices
- endpoint details
- exact POST/PATCH body shapes
- required and optional fields

Do not duplicate or invent request schemas in this skill. For simple GET/DELETE calls and the list fast paths above, you do not need to load `+api-reference`.

### Examples

**Get organization info:**
```bash
node <path>/scripts/runway-api.mjs request GET /v1/organization
```

**List avatars:**
```bash
node <path>/scripts/runway-api.mjs avatars list
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

**Delete an avatar (preview first):**
```bash
node <path>/scripts/runway-api.mjs request DELETE /v1/avatars/<id> --dry-run
node <path>/scripts/runway-api.mjs request DELETE /v1/avatars/<id>
```

**List knowledge documents for an avatar:**
```bash
node <path>/scripts/runway-api.mjs documents list --avatar-id <avatar-id>
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
node <path>/scripts/runway-api.mjs voices list
```

## Waiting for Tasks

Generation endpoints return a task ID. Always run `wait` immediately after a generation call — do not ask the user whether to wait.

```bash
node <path>/scripts/runway-api.mjs wait <task-id>
```

Return the final output URLs in your response.

## Generation Requests

When the user asks to generate an image, video, or audio:

1. Read `+api-reference` once before the first generation POST. It is the canonical source for model options and exact request fields.
2. Choose the model from `+api-reference` and tell the user which one you picked, briefly.
3. Build the request body from `+api-reference`. Do not guess field names.
4. Call the generation endpoint once with that body.
5. Run `wait` automatically.
6. Return the output URL(s) and model used.

For generation requests, never skip the `+api-reference` read. For simple list/get/delete requests, do not load it unless needed.

If the user says only "generate an image" but the surrounding context is clearly about Runway account actions or this skill, still use the Runway API rather than a generic built-in image tool.

## API Reference

Use `+api-reference` for the canonical API contract. Use `+fetch-api-reference` only when you specifically need the latest docs content from `docs.dev.runwayml.com`.

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
