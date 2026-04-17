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

## Runtime Location

The runtime script ships **inside this skill** at `scripts/runway-api.mjs` (co-located with this `SKILL.md`). It has zero dependencies — Node.js 20+ is required.

**Resolving the absolute path.** Every shell command below uses the placeholder `<skill-dir>`. Replace it with the absolute directory of the `SKILL.md` you are currently reading — you already have this path from the tool that loaded this file. Do **not** guess the path, run `find` from `$HOME`, or search the whole filesystem.

If `<skill-dir>` is not known from context, check these locations in order with `ls` before giving up:

1. `$RUNWAY_SKILLS_DIR/skills/use-runway-api/scripts/runway-api.mjs` (if the env var is set)
2. `~/.claude/plugins/cache/*/runway-api/skills/use-runway-api/scripts/runway-api.mjs` (Claude Code plugin install)
3. `~/.cursor/plugins/cache/*/runway-api/skills/use-runway-api/scripts/runway-api.mjs` (Cursor plugin install)
4. `~/.claude/skills/use-runway-api/scripts/runway-api.mjs` (`npx skills add` install)
5. `~/.agents/skills/use-runway-api/scripts/runway-api.mjs` (generic agent install)
6. `~/Documents/github/runway/skills/skills/use-runway-api/scripts/runway-api.mjs` (source checkout)

Pick the first match and use it as `<skill-dir>/scripts/runway-api.mjs` for the rest of the session. Do not re-resolve between commands.

## Before Your First Call

Set a session ID so all requests in this chat can be correlated, then verify credentials:

```bash
export RUNWAY_SKILLS_CLIENT_ID=$(node -e "console.log(crypto.randomUUID())")
node <skill-dir>/scripts/runway-api.mjs auth status
```

- If `authenticated` is `true` → proceed to the API call. Do not re-check.
- If `authenticated` is `false` → tell the user to set `RUNWAY_SKILLS_API_SECRET` (see `AUTH.md` for details), then **stop and wait for the user to confirm**. Do not retry or re-check in a loop.

> **Staging caveat:** `auth status` hits `/v1/organization` which may 500 on stage even when data endpoints work fine. If stage `auth status` fails but you have `RUNWAY_SKILLS_API_SECRET_STAGE` set, try a data endpoint like `avatars list --stage` to confirm the key works before giving up.

## Fast Paths

For plain list requests, use the compact list commands first instead of the generic `request` command:

- list avatars → `node <skill-dir>/scripts/runway-api.mjs avatars list`
- list voices → `node <skill-dir>/scripts/runway-api.mjs voices list`
- list documents → `node <skill-dir>/scripts/runway-api.mjs documents list [--avatar-id <id>]`

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
node <skill-dir>/scripts/runway-api.mjs request <METHOD> <path> [--body '<json>'] [--stdin] [--dry-run]
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
node <skill-dir>/scripts/runway-api.mjs request GET /v1/organization
```

**List avatars:**
```bash
node <skill-dir>/scripts/runway-api.mjs avatars list
```

**Get a specific avatar:**
```bash
node <skill-dir>/scripts/runway-api.mjs request GET /v1/avatars/<id>
```

**Update an avatar:**
```bash
node <skill-dir>/scripts/runway-api.mjs request PATCH /v1/avatars/<id> --body '{
  "personality": "Updated personality text"
}'
```

**Delete an avatar (preview first):**
```bash
node <skill-dir>/scripts/runway-api.mjs request DELETE /v1/avatars/<id> --dry-run
node <skill-dir>/scripts/runway-api.mjs request DELETE /v1/avatars/<id>
```

**List knowledge documents for an avatar:**
```bash
node <skill-dir>/scripts/runway-api.mjs documents list --avatar-id <avatar-id>
```

**Create a knowledge document:**
```bash
node <skill-dir>/scripts/runway-api.mjs request POST /v1/documents --body '{
  "avatarId": "<avatar-id>",
  "name": "FAQ",
  "content": "Q: What is your return policy?\nA: 30 days, no questions asked."
}'
```

**List voices:**
```bash
node <skill-dir>/scripts/runway-api.mjs voices list
```

## Waiting for Tasks

Generation endpoints return a task ID. Always run `wait` immediately after a generation call — do not ask the user whether to wait.

```bash
node <skill-dir>/scripts/runway-api.mjs wait <task-id>
```

## Generation Requests

When the user asks to generate an image, video, or audio:

1. Read `+api-reference` once before the first generation POST. It is the canonical source for model options, request body shapes, and valid field values.
2. Choose the model from `+api-reference` and tell the user which one you picked, briefly.
3. Build the request body from `+api-reference`. Do not guess field names.
4. Call the generation endpoint once with that body.
5. Run `wait` automatically.
6. Present the result following the rules in **Presenting Generation Output** below.

For generation requests, never skip the `+api-reference` read. For simple list/get/delete requests, do not load it unless needed.

If the user says only "generate an image" but the surrounding context is clearly about Runway account actions or this skill, still use the Runway API rather than a generic built-in image tool.

## Presenting Generation Output

The `wait` command returns a task with an `output` array of signed URLs. These URLs **expire in 24–48 hours** and are long signed JWT blobs that are awkward to read inline.

After a successful generation, do all of the following:

1. **Lead with what was generated** — one short line stating the model and cost, e.g.
   `Generated with gen4_image (1080p, 8 credits).`
2. **Embed images inline as Markdown** so the user can see them without clicking:
   ```markdown
   ![Fox in a snowy forest](https://storage.runway.../signed-url)
   ```
   For videos, link them as plain Markdown links (`[fox.mp4](...)`) since inline video does not render in most chat UIs.
3. **Offer to save a local copy** in the same message, proactively. Suggest a predictable path (`./generated/` or `./runway-outputs/`) and infer a filename from the prompt when possible. Example:
   > Want me to save it to `./generated/fox.png`? The signed URL expires in ~24–48h.
4. **Do not paste the full signed URL as raw text** unless the user asks for it. The Markdown image/link already contains it.

If the user confirms a download, fetch with `curl -L -o <path> '<url>'` (quote the URL — it contains `&`).

## API Reference

Use `+api-reference` for the canonical API contract. Use `+fetch-api-reference` only when you specifically need the latest docs content from `docs.dev.runwayml.com`.

## Staging (--stage)

Add `--stage` to any command to target the staging API:

```bash
node <skill-dir>/scripts/runway-api.mjs --stage avatars list
node <skill-dir>/scripts/runway-api.mjs --stage request GET /v1/avatars
```

With `--stage`, the CLI checks `RUNWAY_SKILLS_API_SECRET_STAGE` first, then falls back to `RUNWAY_SKILLS_API_SECRET`. The base URL defaults to `https://api.dev-stage.runwayml.com`.

## Large Payloads (--stdin)

When creating resources with data URIs (e.g. base64-encoded images for avatar `referenceImage`), the body can exceed shell argument limits. Use `--stdin` to pipe the body:

```bash
python3 -c "
import json, base64
with open('image.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
body = json.dumps({'name': 'My Avatar', 'referenceImage': f'data:image/png;base64,{b64}', ...})
with open('/tmp/body.json', 'w') as f:
    f.write(body)
" && cat /tmp/body.json | node <skill-dir>/scripts/runway-api.mjs request POST /v1/avatars --stdin
```

Alternatively, write the JSON to a file and use `curl -d @file` directly. The `--body` flag is fine for small JSON payloads but will hit `argument list too long` for data URIs of images over ~200KB.

## Environment Variables

The runtime reads credentials from the process environment:

| Variable | Description |
|----------|-------------|
| `RUNWAY_SKILLS_API_SECRET` | Production API key |
| `RUNWAY_SKILLS_API_SECRET_STAGE` | Stage API key (used with `--stage`) |
| `RUNWAY_SKILLS_BASE_URL` | Override the base URL for any environment |
| `RUNWAY_SKILLS_DIR` | Optional. Absolute path to the source checkout of this skills repo — used by the agent as a fallback when resolving `<skill-dir>`. |

If the agent cannot see `RUNWAY_SKILLS_API_SECRET`, the editor likely needs to be restarted after the variable is set.

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
