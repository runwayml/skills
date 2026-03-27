# Runway API Skills

A set of skills that gives your AI coding agent the knowledge and tools to work with [Runway's public API](https://docs.dev.runwayml.com/api/) — integrate video, image, and audio generation into server-side projects, or manage Runway resources directly from the editor.

Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://openai.com/index/codex/), and other compatible agents.

## Two Ways to Use

### 1. Integrate into your app

Guide your agent through adding Runway capabilities to a server-side project: verify compatibility, set up credentials, write framework-specific routes, and handle edge cases like file uploads and task polling.

```
Set up Runway video generation in my Next.js app
```

### 2. Act on your Runway account directly

Let your agent call the Runway API to manage resources — create avatars, update knowledge documents, trigger generations, check credit balance — without writing app code.

```
Create a new avatar called "Support Agent" with a friendly personality
```

```
List my knowledge documents for avatar abc123
```

## Installation

### Claude Code (community marketplace)

Add the [Anthropic community plugins](https://github.com/anthropics/claude-plugins-community) marketplace, then install this plugin.

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

## Prerequisites

- A [Runway developer account](https://dev.runwayml.com/) with prepaid credits ($10 minimum)
- For integration skills: a server-side project — Node.js 18+ or Python 3.8+ with a backend framework
- For direct API actions: Node.js 20+ (zero dependencies — just the runtime script)

## Available Skills

### Getting Started

| Skill                    | Description                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------- |
| `rw-recipe-full-setup`   | End-to-end setup: compatibility check → API key → SDK install → integration code → test        |
| `rw-check-compatibility` | Analyze your project to verify it can safely call the Runway API server-side                   |
| `rw-setup-api-key`       | Guide through account creation, SDK installation, and environment variable configuration       |
| `rw-check-org-details`   | Query your organization's rate limits, credit balance, usage tier, and daily generation counts |

### Direct API Actions

| Skill               | Description                                                                        |
| -------------------- | ---------------------------------------------------------------------------------- |
| `use-runway-api`     | Call any public API endpoint to manage resources, trigger generations, and inspect state |

### Generation (Integration)

| Skill                | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| `rw-integrate-video` | Text-to-video, image-to-video, video-to-video, and character performance generation |
| `rw-integrate-image` | Text-to-image generation with optional reference images via `@Tag` syntax           |
| `rw-integrate-audio` | Text-to-speech, sound effects, voice isolation, dubbing, and speech-to-speech       |

### Characters (Real-Time Avatars)

| Skill                          | Description                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------------ |
| `rw-integrate-characters`      | Create GWM-1 avatars and set up server-side session management for real-time conversations |
| `rw-integrate-character-embed` | Embed avatar call UI in React apps using `@runwayml/avatars-react`                         |
| `rw-integrate-documents`       | Add knowledge base documents to avatars for domain-specific conversations                  |

### Utilities

| Skill                    | Description                                                                                                           |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `rw-integrate-uploads`   | Upload local files to get `runway://` URIs for use as generation inputs                                               |
| `rw-api-reference`       | Complete API reference — models, endpoints, costs, rate limits, and error codes                                       |
| `rw-fetch-api-reference` | Fetch the latest API docs from [docs.dev.runwayml.com/api](https://docs.dev.runwayml.com/api/) as the source of truth |

## Supported Models

### Video

| Model                    | Use Case                            | Cost              |
| ------------------------ | ----------------------------------- | ----------------- |
| `gen4.5`                 | Highest quality, general purpose    | 12 credits/sec    |
| `gen4_turbo`             | Fast, image-driven (image required) | 5 credits/sec     |
| `gen4_aleph`             | Video-to-video editing              | 15 credits/sec    |
| `veo3`                   | Premium quality                     | 40 credits/sec    |
| `veo3.1` / `veo3.1_fast` | High quality / fast Google models   | 10–40 credits/sec |

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

### Integrate into a project

```
Set up Runway video generation in my Next.js app
```

Or go step by step:

```
Check if my project is compatible with the Runway API
```

```
Help me set up my Runway API key
```

```
Add an endpoint to generate videos from text prompts
```

### Direct API actions

```
List all my avatars
```

```
Using the Runway API, generate an image of a red door in a white wall and tell me which model you used
```

## Supported Frameworks

The integration skills generate framework-specific code for:

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
