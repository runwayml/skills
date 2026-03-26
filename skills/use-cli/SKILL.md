---
name: use-cli
description: "Use the Runway CLI for quick generation, scripting, CI/CD, and MCP"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(runway *), Bash(which runway), Bash(npm list -g @runwayml/cli)
---

# Runway CLI

Terminal interface to the [Runway ML API](https://docs.dev.runwayml.com/). This skill covers **CLI-specific** usage only — models, parameters, SDK code, and API details live in sibling skills (`+api-reference`, `+integrate-video`, etc.) and the [API docs](https://docs.dev.runwayml.com/).

## Prerequisites

```bash
which runway          # already installed?
npm install -g @runwayml/cli   # if not
runway --version
```

## Setup

```bash
runway login <api-key>
```

Or set `RUNWAYML_API_SECRET` as an environment variable (overrides file-based config).

### Profiles and staging

- **`runway login list`** — show saved profiles (current profile marked with `*`).
- **`runway login use <profile>`** — switch the active profile for subsequent commands.
- **`RUNWAY_PROFILE=<name>`** — use a profile for a single command without switching.

To log in to a non-production API (e.g. staging), set **`--profile`** and **`-u` / `--url`**:

```bash
runway login <staging-api-key> --profile staging -u https://api.dev-stage.runwayml.com
runway login list
runway login use staging
```

- **`--profile`** is on `runway login` only — names the profile to create or update (default: `default`).
- **`-u` / `--url`** is on `runway login` only — sets the API base URL for that profile.
- There is no global `--profile` flag on other commands; use `RUNWAY_PROFILE` or `runway login use`.

## Discovering commands

```bash
runway --help                         # top-level commands
runway schema                         # structured introspection (all commands)
runway schema <command>               # single command detail
runway schema --format json           # machine-readable
runway <command> --help               # flags for a specific command
```

Do **not** rely on this markdown for exhaustive options — **`runway schema` is the ground truth** and always matches the generated CLI.

## Minimal examples

```bash
runway image-to-video "Slow push in" -i https://example.com/photo.jpg -m gen4.5
runway text-to-video "Misty forest at dawn"
runway text-to-image "A red door in a white wall"
runway text-to-speech "Hello world" --voice-id victoria
runway avatars create --name "Host" --reference-image <url> --personality "Friendly guide" --voice-preset-id victoria
runway avatars list
runway documents list --avatar-id <id>
```

Audio, upscaling, dubbing, workflows, org usage, etc. follow the same pattern: `runway <name>` then `--help` / `runway schema`.

For SDK equivalents and full parameter docs, see `+integrate-video`, `+integrate-audio`, `+integrate-image`, and `+integrate-characters`.

## MCP

`runway mcp` exposes the full API as MCP tools over stdio — no hand-written HTTP needed.

```bash
runway mcp                    # start MCP server on stdio
```

Wire it into your editor (Cursor, Claude Code, etc.) as an MCP server command. The tool schemas match `runway schema --format json`.

## Avatar design tips

Behavioral guidance for creating effective avatars. For server-side session code, see `+integrate-characters`. For knowledge documents, see `+integrate-documents`.

### Core components

| Component | Required | Description |
|-----------|----------|-------------|
| **Reference Image** | Yes | The avatar's visual appearance |
| **Personality** | Yes | Instructions for how the avatar behaves |
| **Voice** | Yes | Preset voice for speech |
| **Greeting** | No | Initial message when conversation starts |
| **Knowledge** | No | Documents for domain-specific information |

### Reference image

- **Aspect ratio**: 16:9 (e.g. 1920x1080) works best
- **Framing**: Head and shoulders, facing camera
- **Background**: Simple, non-distracting
- Stylized/illustrated images work well — doesn't need to be photorealistic

### Personality

Keep under 500 characters. Include: who the avatar is, tone/style, what they help with.

```
You are a friendly barista at a coffee shop. Be warm and casual, like chatting
with a regular customer. Help with menu questions and recommendations.
```

### Voice presets

| Voice | Style |
|-------|-------|
| victoria, clara | Professional, warm |
| maya, emma | Friendly, approachable |
| drew, vincent | Confident, authoritative |
| skye, summer | Energetic, upbeat |

Full voice list: `runway voices list`.

### Greeting

Keep it short and natural. Avoid long introductions or listing capabilities.

```
Hey! Welcome to the shop. What can I get started for you?
```

## Developer portal (deep link)

```
https://<host>/organization/<org-id>/characters/<avatar-id>
```

- Production: `dev.runwayml.com`
- Staging: `dev-stage.runwayml.com`

The org ID appears in the browser URL when viewing the dev portal while signed in.

## Tips

- Generation tasks often take 30–120 seconds; the CLI polls automatically and prints the asset URL.
- `--format json` — machine-readable output (default when piped).
- `--dry-run` — print the request payload without calling the API.
- `--json <payload>` — pass the full API body as JSON, bypassing individual flags.

## Related skills

| Skill | What it covers |
|-------|----------------|
| `+integrate-video` | SDK code for text-to-video, image-to-video, video-to-video |
| `+integrate-image` | SDK code for text-to-image with reference images |
| `+integrate-audio` | SDK code for TTS, sound effects, dubbing, voice conversion |
| `+integrate-characters` | Server-side avatar session management |
| `+integrate-character-embed` | React embed component for avatar calls |
| `+integrate-documents` | Knowledge base documents for avatars |
| `+integrate-uploads` | Upload local files to get `runway://` URIs |
| `+api-reference` | Full API reference — models, endpoints, costs, rate limits |
| `+fetch-api-reference` | Fetch latest API docs from docs.dev.runwayml.com |
| `+setup-api-key` | Guided API key and SDK setup walkthrough |
| `+check-compatibility` | Verify project can use the Runway API server-side |

## Docs

- [API docs](https://docs.dev.runwayml.com/) — authoritative for behavior
- [Help center](https://help.runwayml.com/)
