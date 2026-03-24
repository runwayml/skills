# Runway API Skills

A set of skills that gives your AI coding agent the knowledge and tools to integrate [Runway's public API](https://docs.dev.runwayml.com/api/) into any server-side project — video generation, image generation, audio, file uploads, and real-time conversational avatars.

Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://openai.com/index/codex/), and other compatible agents.

## What It Does

When you ask your agent to add Runway capabilities to your project, these skills guide it through the full workflow:

1. **Verify compatibility** — confirm your project has a server-side component (the API key must never be exposed to the client).
2. **Set up credentials** — walk you through creating a Runway developer account, installing the SDK, and configuring `RUNWAYML_API_SECRET`.
3. **Write integration code** — generate server-side API routes for the exact capability you need, with framework-specific examples for Next.js, Express, FastAPI, and more.
4. **Handle edge cases** — upload local files, poll for task completion, download expiring output URLs, and manage rate limits.

## Installation

```bash
npx skills add runwayml/skills
```

## Prerequisites

- A [Runway developer account](https://dev.runwayml.com/) with prepaid credits ($10 minimum)
- A server-side project — Node.js 18+ or Python 3.8+ with a backend framework (Express, Next.js, FastAPI, etc.)

## Available Skills

### Getting Started

| Skill                 | Description                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------------- |
| `recipe-full-setup`   | End-to-end setup: compatibility check → API key → SDK install → integration code → test        |
| `check-compatibility` | Analyze your project to verify it can safely call the Runway API server-side                   |
| `setup-api-key`       | Guide through account creation, SDK installation, and environment variable configuration       |
| `check-org-details`   | Query your organization's rate limits, credit balance, usage tier, and daily generation counts |

### Generation

| Skill             | Description                                                                         |
| ----------------- | ----------------------------------------------------------------------------------- |
| `integrate-video` | Text-to-video, image-to-video, video-to-video, and character performance generation |
| `integrate-image` | Text-to-image generation with optional reference images via `@Tag` syntax           |
| `integrate-audio` | Text-to-speech, sound effects, voice isolation, dubbing, and speech-to-speech       |

### Characters (Real-Time Avatars)

| Skill                       | Description                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `integrate-characters`      | Create GWM-1 avatars and set up server-side session management for real-time conversations |
| `integrate-character-embed` | Embed avatar call UI in React apps using `@runwayml/avatars-react`                         |
| `integrate-documents`       | Add knowledge base documents to avatars for domain-specific conversations                  |

### Utilities

| Skill                 | Description                                                                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `integrate-uploads`   | Upload local files to get `runway://` URIs for use as generation inputs                                               |
| `api-reference`       | Complete API reference — models, endpoints, costs, rate limits, and error codes                                       |
| `fetch-api-reference` | Fetch the latest API docs from [docs.dev.runwayml.com/api](https://docs.dev.runwayml.com/api/) as the source of truth |

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

Ask your agent to set everything up:

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

## Supported Frameworks

The skills generate framework-specific code for:

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
