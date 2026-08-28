# Runway API Skills

Media Generation at scale. One platform to run the best image, video, audio and real-time models. Generate videos, images, and audio with Runway's API — batch Ad campaigns, product videos, multishot stories, and creative iteration. Supports seedance2, gen4.5, veo3, Nano, Banana Pro, and more.

Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.com), [Codex](https://openai.com/index/codex/), and other compatible agents.

## Two Ways to Use

### 1. Generate media at scale

Tell your agent what to create and it handles the rest — calls the API, polls for completion, downloads the result. Generate one asset or orchestrate hundreds.

```
Generate a 15-second product video from this image using seedance2
```

```
Generate a video for each of these 5 product photos, 9:16 ratio for Instagram Reels
```

```
Create a voiceover for this ad script, then generate a sound effect of applause
```

### 2. Build Runway into your app

Use Dev MCP for live project context and the official SDK for application code. The agent inspects the existing backend and UI, follows current docs, implements the relevant product surface, and verifies it safely.

```
Set up Runway video generation in my Next.js app
```

## Installation

### Claude Code (community marketplace)

```bash
claude plugin marketplace add anthropics/claude-plugins-community
claude plugin install runway-api-skills@claude-community
```

You can also run `/plugin` in Claude Code, open **Discover**, search for **runway-api-skills**, and install from there. After installing or updating plugins, run `/reload-plugins` if skills do not appear immediately.

### Other agents (`npx skills`)

```bash
npx skills add runwayml/skills
```

Select all the skills with your keyboard (Space to select, arrow keys to navigate), then press Enter to install.

For Dev Platform integration, install the foundation plus the skill for your surface:

```bash
npx skills add runwayml/skills --skill runway-dev --skill runway-dev-models --agent cursor claude-code codex -y
```

## Prerequisites

- A [Runway developer account](https://dev.runwayml.com/) with prepaid credits ($10 minimum)
- For generation skills: [uv](https://docs.astral.sh/uv/) (Python package runner) and `RUNWAYML_API_SECRET` env var
- For integration skills: a server-side project — Node.js 18+ or Python 3.8+ with a backend framework

## Available Skills

### Dev Platform (integrate via Dev MCP + SDK)

These skills use Dev MCP for live project context and the SDK for server-side integration.

| Skill                      | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| `runway-dev`               | Shared MCP, docs, auth, task polling, and error flow   |
| `runway-dev-models`        | Model endpoint integration                             |
| `runway-dev-model-routers` | Model Router setup and routed SDK calls                |
| `runway-dev-characters`    | Characters and realtime avatar sessions                |
| `runway-dev-recipes`       | Recipe pipeline integration                            |
| `runway-dev-workflows`     | Runway app workflows exposed through API endpoints     |

### Generation (run directly)

Generate media assets directly — your agent runs the scripts, polls for completion, and saves the output.

| Skill                | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| `rw-generate-video`  | Generate videos: text-to-video, image-to-video, video-to-video                     |
| `rw-generate-image`  | Generate images: text-to-image with optional reference images                       |
| `rw-generate-audio`  | Generate audio: TTS, sound effects, voice isolation, dubbing, voice conversion      |

### Utilities

| Skill                  | Description                                                                                    |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| `use-runway-api`       | Call public API endpoints directly to manage resources, trigger generations, and inspect state |
| `rw-check-org-details` | Query organization rate limits, credit balance, usage tier, and generation counts              |

## Supported Models

### Video

| Model                    | Use Case                                 | Cost              |
| ------------------------ | ---------------------------------------- | ----------------- |
| `seedance2`              | Reference image and video, long duration | 36 credits/sec    |
| `gen4.5`                 | High quality, general purpose            | 12 credits/sec    |
| `gen4_turbo`             | Fast, image-driven (image required)      | 5 credits/sec     |
| `gen4_aleph`             | Video-to-video editing                   | 15 credits/sec    |
| `veo3`                   | Premium quality                          | 40 credits/sec    |
| `veo3.1` / `veo3.1_fast` | High quality / fast Google models       | 10–40 credits/sec |

### Image

| Model              | Cost        |
| ------------------ | ----------- |
| `gen4_image`       | 5–8 credits |
| `gen4_image_turbo` | 2 credits   |
| `gemini_2.5_flash` | 5 credits   |

### Audio

| Model                        | Use Case                     |
| ---------------------------- | ---------------------------- |
| `eleven_multilingual_v2`     | Text-to-speech               |
| `eleven_text_to_sound_v2`    | Sound effects                |
| `eleven_voice_isolation`     | Isolate voice from audio     |
| `eleven_voice_dubbing`       | Dub audio to other languages |
| `eleven_multilingual_sts_v2` | Voice conversion             |

### Characters

| Model          | Description                                          |
| -------------- | ---------------------------------------------------- |
| `gwm1_avatars` | Real-time conversational avatars (5-min max session) |

## Quick Start

### Generate media directly

```
Generate a 10-second video of a sunset over the ocean
```

```
Generate an image of a red door in a white wall
```

```
Create a voiceover saying "Welcome to our store" and save it as welcome.mp3
```

### Integrate into a project

```
Use Dev MCP to add Runway video generation to my existing Next.js app
```

```
Add a Runway Character with domain knowledge to this support app
```

## Supported Frameworks

The Dev Platform skills inspect and integrate with server-side stacks including:

- **Node.js** — Express, Fastify, Next.js (App Router & Pages Router), Remix, SvelteKit, Nuxt, Astro
- **Python** — FastAPI, Flask, Django
- **Serverless** — Vercel Functions, AWS Lambda, Cloudflare Workers

## API Reference

- **Base URL:** `https://api.dev.runwayml.com`
- **Auth header:** `Authorization: Bearer <RUNWAYML_API_SECRET>`
- **Version header:** `X-Runway-Version: 2024-11-06`
- **Official docs:** [docs.dev.runwayml.com](https://docs.dev.runwayml.com/)
- **API Reference:** [docs.dev.runwayml.com/api](https://docs.dev.runwayml.com/api)
- **Developer portal:** [dev.runwayml.com](https://dev.runwayml.com/)

## License

[MIT](LICENSE)
