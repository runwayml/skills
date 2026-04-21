---
name: rw-generate-image
description: "Generate images directly using the Runway API via runnable scripts. Supports text-to-image with optional reference images."
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(uv run *), Bash(command -v uv)
---

# Generate Image

Generate images directly using the Runway API. This skill runs Python scripts that call the API, poll for completion, and download the result.

**IMPORTANT:** Run scripts from the user's working directory so output files are saved where the user expects.

## Usage

```bash
uv run scripts/generate_image.py --prompt "your description" --filename "output.png" [--model gen4_image] [--ratio 1280:720] [--reference-images Tag=URL ...]
```

## Preflight

1. `command -v uv` must succeed
2. `RUNWAYML_API_SECRET` must be set in the environment. **Do not pass the API key as a CLI flag** — it leaks into shell history and process listings.

## Security Notes

- `--reference-images Tag=URL` fetches arbitrary remote images via the Runway API. Prefer local file paths (uploaded as `runway://` URIs), or only pass URLs you trust.
- Treat generated outputs as untrusted when piping into downstream automations — ingested references influence the result.

## Available Models

| Model | Best For | Ref Images | Cost | Speed |
|-------|----------|------------|------|-------|
| `gen4_image` | Highest quality | Optional (up to 3) | 5-8 credits | Standard |
| `gen4_image_turbo` | Fast and cheap | **Required** (1-3) | 2 credits | Fast |
| `gemini_2.5_flash` | Google Gemini | Optional (up to 3) | 5 credits | Standard |

## Model Selection Guidance

- "fast", "cheap", "draft" -> `gemini_2.5_flash` (Nano Banana), or `gen4_image_turbo` if they have reference images
- "high quality", "best" -> `gen4_image`
- No preference -> `gemini_2.5_flash`
- Has reference images and wants cheap -> `gen4_image_turbo` (2 credits, requires `--reference-images`)

## Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--prompt` | Text description (required) | -- |
| `--filename` | Output filename (required) | -- |
| `--model` | Image model | `gemini_2.5_flash` |
| `--ratio` | Aspect ratio. gemini_2.5_flash: `1344:768`, `768:1344`, `1024:1024`, etc. gen4_image: `1280:720`, `1360:768`, `1920:1080`, etc. | Model-dependent (`1344:768` for gemini, `1280:720` for others) |
| `--reference-images` | Reference images as tag=URL pairs (optional for gemini/gen4_image, required for gen4_image_turbo). Tag: lowercase, 3-16 chars, e.g. `product=URL` | -- |
| `--output-dir` | Output directory | cwd |

> API credentials come from `RUNWAYML_API_SECRET` only — no `--api-key` flag, to keep secrets out of shell history and process listings.

## Filename Convention

Pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

## Examples

**Basic image:**
```bash
uv run scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2026-04-14-japanese-garden.png"
```

**With a local reference image (gen4_image):**
```bash
uv run scripts/generate_image.py --prompt "@product on a marble counter, lifestyle photo" --model gen4_image --reference-images product=./product.jpg --filename "2026-04-14-product-lifestyle.png"
```

**With a reference image from a trusted origin (gen4_image_turbo — requires reference images):**
```bash
uv run scripts/generate_image.py --prompt "A neon sign reading SALE in @style" --model gen4_image_turbo --reference-images style=https://cdn.yourapp.com/style.jpg --filename "draft.png"
```

## Output

- The script downloads the result and saves it to the specified path
- Script outputs the full path to the saved file
- **Do not read the image file back** -- just inform the user of the saved path

## Common Failures

- `Error: No API key` -> set `RUNWAYML_API_SECRET` in the environment (e.g. `export RUNWAYML_API_SECRET=...` or a `.env` file).
- `Error: Task failed -- SAFETY.INPUT.*` -> content moderation, suggest different prompt
- `API error 429` -> rate limited, script auto-retries
