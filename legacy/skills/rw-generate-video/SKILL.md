---
name: rw-generate-video
description: "Generate videos directly using the Runway API via runnable scripts. Supports text-to-video, image-to-video, and video-to-video with seedance2, gen4.5, veo3, and more."
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(uv run *), Bash(command -v uv)
---

# Generate Video

Generate videos directly using the Runway API. This skill runs Python scripts that call the API, poll for completion, and download the result.

**IMPORTANT:** Run scripts from the user's working directory so output files are saved where the user expects.

## Usage

```bash
uv run scripts/generate_video.py --prompt "your description" --filename "output.mp4" [--model seedance2] [--ratio 1280:720] [--duration 5] [--image-url "..."]
```

## Preflight

1. `command -v uv` must succeed. If not, tell the user to install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. `RUNWAYML_API_SECRET` must be set in the environment. **Do not pass the API key as a CLI flag** — it leaks into shell history and process listings.

## Security Notes

- `--image-url` / `--video-url` fetch arbitrary remote media via the Runway API. Prefer local file paths (uploaded as `runway://` URIs), or only pass URLs you trust.
- Treat generated outputs as untrusted when piping into downstream automations — ingested media influences the result.

## Available Models

| Model | Best For | Input | Cost |
|-------|----------|-------|------|
| `seedance2` | Reference image and video, long duration (up to 15s) | Text, Image, and/or Video | 36 credits/sec |
| `gen4.5` | High quality, general purpose | Text and/or Image | 12 credits/sec |
| `gen4_turbo` | Fast, image-driven | Image required | 5 credits/sec |
| `gen4_aleph` | Video editing/transformation | Video + Text/Image | 15 credits/sec |
| `veo3` | Premium quality | Text/Image | 40 credits/sec |
| `veo3.1` | High quality Google model | Text/Image | 20-40 credits/sec |
| `veo3.1_fast` | Fast Google model | Text/Image | 10-15 credits/sec |

## Model Selection Guidance

Map user requests:
- "product ad", "e-commerce", "long video" -> `seedance2`
- "fast", "cheap", "quick" -> `veo3.1_fast` or `gen4_turbo` (if they have an image)
- "high quality", "best", "cinematic" -> `gen4.5` or `veo3`
- "edit video", "transform video" -> `gen4_aleph` or `seedance2`
- No preference -> `seedance2`

## Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--prompt` | Text description (required) | -- |
| `--filename` | Output filename (required) | -- |
| `--model` | Video model | `gen4.5` |
| `--ratio` | Aspect ratio (pixel-based). Common: `1280:720`, `720:1280`, `960:960`. seedance2 also supports `1112:834`, `834:1112`, `1470:630`, etc. | `1280:720` |
| `--duration` | Duration in seconds (model-dependent, seedance2 supports up to 15s) | `5` |
| `--image-url` | Image URL or local file for image-to-video | -- |
| `--video-url` | Video URL or local file for video-to-video (gen4_aleph, seedance2) | -- |
| `--output-dir` | Output directory | cwd |

> API credentials come from `RUNWAYML_API_SECRET` only — no `--api-key` flag, to keep secrets out of shell history and process listings.

## Filename Convention

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.mp4`

Examples:
- "A cyberpunk city" -> `2026-04-14-14-23-05-cyberpunk-city.mp4`
- "Waves on a beach" -> `2026-04-14-15-30-12-beach-waves.mp4`

## Examples

**Text-to-video (seedance2):**
```bash
uv run scripts/generate_video.py --prompt "A serene mountain landscape at sunrise with mist" --filename "2026-04-14-mountain-sunrise.mp4" --model seedance2 --ratio 1280:720
```

**Image-to-video (animate a local product photo):**
```bash
uv run scripts/generate_video.py --prompt "Camera slowly zooms out, product sparkles" --image-url "./product.jpg" --filename "2026-04-14-product-reveal.mp4" --model seedance2 --ratio 720:1280
```

**Video-to-video from a local file (seedance2):**
```bash
uv run scripts/generate_video.py --prompt "Transform into a warm golden sunset scene" --video-url "./input.mp4" --filename "2026-04-14-sunset-transform.mp4" --model seedance2
```

**Fast draft:**
```bash
uv run scripts/generate_video.py --prompt "A cat playing piano" --filename "draft.mp4" --model veo3.1_fast --ratio 1280:720 --duration 4
```

**Premium quality:**
```bash
uv run scripts/generate_video.py --prompt "Cinematic drone shot over Tokyo at night" --filename "tokyo.mp4" --model veo3 --ratio 1280:720 --duration 8
```

## Output

- The script downloads the result and saves it to the specified path
- Script outputs the full path to the saved file
- **Do not read the video file back** -- just inform the user of the saved path

## Common Failures

- `Error: No API key` -> set `RUNWAYML_API_SECRET` in the environment (e.g. `export RUNWAYML_API_SECRET=...` or a `.env` file).
- `Error: Task failed -- SAFETY.INPUT.*` -> content moderation, suggest different prompt
- `Error: Task failed -- ASSET.INVALID` -> bad input file format, check image/video format
- `API error 429` -> rate limited, script auto-retries

## For Batch Generation

To generate many videos at once, run this script in a loop — the agent can orchestrate multiple calls with different prompts, images, or parameters to produce campaigns, localized variants, or creative iterations at scale.
