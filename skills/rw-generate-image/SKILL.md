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
uv run scripts/generate_image.py --prompt "your description" --filename "output.png" [--model gen4_image] [--ratio 1280:720] [--reference-images Tag=URL ...] [--api-key KEY]
```

## Preflight

1. `command -v uv` must succeed
2. `RUNWAYML_API_SECRET` must be set, or pass `--api-key`

## Available Models

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| `gen4_image` | Highest quality | 5-8 credits | Standard |
| `gen4_image_turbo` | Fast and cheap | 2 credits | Fast |
| `gemini_2.5_flash` | Google Gemini | 5 credits | Standard |

## Model Selection Guidance

- "fast", "cheap", "draft" -> `gemini_2.5_flash` (Nano Banana)
- "high quality", "best" -> `gen4_image`
- No preference -> `gemini_2.5_flash`

## Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--prompt` | Text description (required) | -- |
| `--filename` | Output filename (required) | -- |
| `--model` | Image model | `gemini_2.5_flash` |
| `--ratio` | Aspect ratio (e.g. 1280:720, 1080:1080) | `1280:720` |
| `--reference-images` | Reference images as Tag=URL pairs | -- |
| `--output-dir` | Output directory | cwd |
| `--api-key` | Runway API key | env `RUNWAYML_API_SECRET` |

## Filename Convention

Pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

## Examples

**Basic image:**
```bash
uv run scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2026-04-14-japanese-garden.png"
```

**With reference images:**
```bash
uv run scripts/generate_image.py --prompt "@Product on a marble counter, lifestyle photo" --reference-images Product=https://example.com/product.jpg --filename "2026-04-14-product-lifestyle.png"
```

**Fast draft:**
```bash
uv run scripts/generate_image.py --prompt "A neon sign reading SALE" --filename "draft.png" --model gen4_image_turbo
```

## Output

- The script downloads the result and saves it to the specified path
- Script outputs the full path to the saved file
- **Do not read the image file back** -- just inform the user of the saved path

## Common Failures

- `Error: No API key` -> set `RUNWAYML_API_SECRET` or pass `--api-key`
- `Error: Task failed -- SAFETY.INPUT.*` -> content moderation, suggest different prompt
- `API error 429` -> rate limited, script auto-retries
