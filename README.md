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

<!-- GENERATED:SKILLS:START -->

### Getting Started

| Skill                 | Description                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `recipe-full-setup`   | Complete Runway API setup: check compatibility, configure API key, and integrate generation endpoints               |
| `check-compatibility` | Analyze a user's codebase to verify it can use Runway's public API (server-side requirement)                        |
| `setup-api-key`       | Guide users through obtaining and configuring a Runway API key                                                      |
| `check-org-details`   | Query the Runway API for organization details: rate limits, credit balance, usage tier, and daily generation counts |

### Generation

| Skill             | Description                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| `integrate-video` | Help users integrate Runway video generation APIs (text-to-video, image-to-video, video-to-video) |
| `integrate-image` | Help users integrate Runway image generation APIs (text-to-image with reference images)           |
| `integrate-audio` | Help users integrate Runway audio APIs (TTS, sound effects, voice isolation, dubbing)             |

### Characters (Real-Time Avatars)

| Skill                       | Description                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `integrate-characters`      | Help users create Runway Characters (GWM-1 avatars) and integrate real-time conversational sessions into their apps |
| `integrate-character-embed` | Help users embed Runway Character avatar calls in React apps using the @runwayml/avatars-react SDK                  |
| `integrate-documents`       | Help users add knowledge base documents to Runway Characters for domain-specific conversations                      |

### Utilities

| Skill                 | Description                                                                                                                            |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `integrate-uploads`   | Help users upload local files to Runway for use as inputs to generation models                                                         |
| `api-reference`       | Complete reference for Runway's public API: models, endpoints, costs, limits, and types                                                |
| `fetch-api-reference` | Retrieve the latest Runway API reference from docs.dev.runwayml.com and use it as the authoritative source before any integration work |

<!-- GENERATED:SKILLS:END -->

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
