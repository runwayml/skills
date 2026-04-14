# Runway API Skills

Generate 100 product videos from a single Shopify URL. Agent-first media generation at scale.

Runway API Skills gives AI agents the power to generate videos, images, and audio using [Runway's API](https://docs.dev.runwayml.com/) -- directly from your terminal. Batch-generate ad campaigns, localize content for every market, and automate creative production at volume.

Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.com), [Codex](https://openai.com/index/codex/), and other compatible agents.

## What You Can Do

**Generate a video ad for every product in your Shopify store:**
```
Generate a video ad for every product in my Shopify store at myshop.myshopify.com
```

**Localize the same ad for 15 cities worldwide:**
```
Generate a localized video ad for Acme Watch in New York, Tokyo, London, Paris, and Dubai
```

**Batch-generate 20 creative variants for A/B testing:**
```
Generate 20 different video ad variants for my product and save them to output/variants/
```

**Animate a product photo into a video:**
```
Turn this product image into a cinematic reveal video
```

## Installation

### Claude Code (community marketplace)

```bash
claude plugin marketplace add anthropics/claude-plugins-community
claude plugin install runway-api-skills@claude-community
```

### Other agents (`npx skills`)

```bash
npx skills add runwayml/skills
```

## Quick Start

1. Get your API key at [dev.runwayml.com](https://dev.runwayml.com/)
2. Set `RUNWAYML_API_SECRET` environment variable
3. Ensure `uv` is installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
4. Ask your agent to generate something

```bash
export RUNWAYML_API_SECRET="your-key-here"
```

Then ask your agent:

```
Generate a 5-second video of a sunset over the ocean
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `scripts/generate_video.py` | Generate videos with gen4.5, veo3, gen4_turbo, and more |
| `scripts/generate_image.py` | Generate images with gen4_image, gen4_image_turbo |
| `scripts/generate_audio.py` | TTS, sound effects, voice isolation, dubbing |
| `scripts/batch_generate.py` | Multi-step pipelines with fan_out, parallel execution |
| `scripts/shopify_products.py` | Fetch all products from a Shopify store |
| `scripts/list_models.py` | List available models and costs |
| `scripts/get_task.py` | Check task status |
| `scripts/runway_helpers.py` | Shared helpers (retry, polling, error handling) |

All scripts use `uv run` (inline dependencies, no install needed).

## Available Skills

### Generate (Agent-First)

| Skill | Description |
|-------|-------------|
| `rw-generate-video` | Generate videos directly -- text-to-video, image-to-video, video-to-video |
| `rw-generate-image` | Generate images directly -- text-to-image with optional references |
| `rw-generate-audio` | Generate audio -- TTS, sound effects, voice isolation, dubbing |

### Batch & Campaign

| Skill | Description |
|-------|-------------|
| `rw-batch-campaign` | Fan-out pipelines for batch generation -- 100 ad variants, A/B tests |
| `rw-shopify-product-ads` | Fetch Shopify products and generate a video ad for each one |

### Integration (SDK Guides)

| Skill | Description |
|-------|-------------|
| `rw-integrate-video` | Add Runway video generation to your server-side code |
| `rw-integrate-image` | Add Runway image generation to your server-side code |
| `rw-integrate-audio` | Add Runway audio to your server-side code |
| `rw-integrate-characters` | Real-time conversational avatars (GWM-1) |
| `rw-integrate-character-embed` | Embed avatar UI with `@runwayml/avatars-react` |
| `rw-integrate-documents` | Knowledge base documents for avatars |

### Setup & Utilities

| Skill | Description |
|-------|-------------|
| `rw-recipe-full-setup` | End-to-end setup: compatibility check, API key, integration |
| `rw-check-compatibility` | Verify your project can safely call the Runway API |
| `rw-setup-api-key` | API key and SDK setup guide |
| `rw-check-org-details` | Query rate limits, credit balance, usage tier |
| `rw-integrate-uploads` | Upload local files for use as generation inputs |
| `rw-api-reference` | Complete API reference |
| `rw-fetch-api-reference` | Fetch latest API docs from docs.dev.runwayml.com |

## Supported Models

### Video

| Model | Best For | Cost |
|-------|----------|------|
| `gen4.5` | Highest quality, general purpose | 12 credits/sec |
| `gen4_turbo` | Fast, image-driven (image required) | 5 credits/sec |
| `gen4_aleph` | Video editing/transformation | 15 credits/sec |
| `veo3` | Premium quality | 40 credits/sec |
| `veo3.1` / `veo3.1_fast` | High quality / fast Google models | 10-40 credits/sec |

### Image

| Model | Cost |
|-------|------|
| `gen4_image` | 5-8 credits |
| `gen4_image_turbo` | 2 credits |
| `gemini_2.5_flash` | 5 credits |

### Audio

| Model | Use Case |
|-------|----------|
| `eleven_multilingual_v2` | Text-to-speech |
| `eleven_text_to_sound_v2` | Sound effects |
| `eleven_voice_isolation` | Isolate voice from audio |
| `eleven_voice_dubbing` | Dub to other languages |
| `eleven_multilingual_sts_v2` | Voice conversion |

## Documentation

- **[COOKBOOK.md](COOKBOOK.md)** -- Production recipes: Shopify product ads, localization, storyboards, creative iteration
- **[PIPELINES.md](PIPELINES.md)** -- Pipeline JSON format, fan_out, template variables, parallel execution
- **[Skills reference](skills/)** -- All skill files with detailed parameters and examples

## Quick Examples

```bash
# Generate a video
uv run scripts/generate_video.py --prompt "A cyberpunk city at night" --filename "city.mp4"

# Generate an image
uv run scripts/generate_image.py --prompt "A serene mountain lake" --filename "lake.png"

# Text-to-speech
uv run scripts/generate_audio.py --type tts --text "Welcome to our product" --filename "voiceover.mp3"

# List available models
uv run scripts/list_models.py

# Fetch Shopify products
uv run scripts/shopify_products.py --store "myshop.myshopify.com" --output products.json

# Run a batch pipeline (dry-run first)
uv run scripts/batch_generate.py --pipeline campaign.json --dry-run

# Run it for real
uv run scripts/batch_generate.py --pipeline campaign.json --output-dir output/ads --notify
```

## Use Cases

### For Performance Marketers
Generate 100 ad variants across creative angles and formats. A/B test at scale. Iterate on winners.

### For E-Commerce
Connect a Shopify store and generate a video ad for every product automatically. Localize for every market.

### For Agencies
Automate the first sprint of creative production. One brief in, full campaign out.

### For B2B2C Platforms
Integrate Runway's generation SDK into your platform to enable your customers to generate content programmatically.

## API Reference

- **Base URL:** `https://api.dev.runwayml.com`
- **Auth header:** `Authorization: Bearer <RUNWAYML_API_SECRET>`
- **Version header:** `X-Runway-Version: 2024-11-06`
- **Official docs:** [docs.dev.runwayml.com](https://docs.dev.runwayml.com/)
- **Developer portal:** [dev.runwayml.com](https://dev.runwayml.com/)

## License

[MIT](LICENSE)
