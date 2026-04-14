# Pipelines -- Multi-Step Workflows

Use `batch_generate.py` to chain multiple generation steps. Each step's output feeds into the next. Write a JSON pipeline and run it in one command.

```bash
uv run scripts/batch_generate.py --pipeline pipeline.json [--api-key KEY]
```

## Pipeline JSON Format

```json
{
  "steps": [
    {
      "action": "generate_video | generate_image | generate_audio | fan_out",
      "model": "gen4.5",
      "prompt": "...",
      "filename": "base-name",
      "use_previous": true
    }
  ]
}
```

**Actions:**
- `generate_video` -- generate a video (text-to-video or image-to-video)
- `generate_image` -- generate an image
- `generate_audio` -- generate audio (tts, sfx)
- `fan_out` -- run a sub-step for EACH result from the previous step (branching)

**Special fields:**
- `use_previous: true` -- use the output URL(s) from the previous step as input
- `fan_out` has a `step` field containing the template to run per source
- In fan_out prompts/filenames, `{i}` is replaced with the iteration number (1, 2, 3...)

## Pipeline Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--pipeline` | Path to JSON file or inline JSON string (required) | -- |
| `--api-key` | Runway API key | env `RUNWAYML_API_SECRET` |
| `--output-dir` | Output directory for all generated files | cwd |
| `--dry-run` | Estimate credit cost without executing | false |
| `--resume` | Skip completed steps (uses `.pipeline-state.json` manifest) | false |
| `--max-parallel` | Max concurrent jobs for parallel fan_out | 3 |
| `--var` | Template variable (repeatable): `--var key=value` | -- |
| `--notify` | Desktop notification when pipeline finishes | false |

## Example: Image -> Video

Generate a hero image, then animate it:

```json
{
  "steps": [
    {
      "action": "generate_image",
      "model": "gen4_image",
      "prompt": "A red sports car on an empty highway, golden hour, cinematic",
      "ratio": "1280:720",
      "filename": "car-hero"
    },
    {
      "action": "generate_video",
      "use_previous": true,
      "model": "gen4.5",
      "prompt": "The car accelerates down the highway, camera tracking alongside, dust kicks up",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "car-drive"
    }
  ]
}
```

```bash
uv run scripts/batch_generate.py --pipeline car-pipeline.json --output-dir output/car
```

## Example: Fan Out for Multi-Variant Ads

Generate 5 ad variants from different creative angles:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["lifestyle", "feature-highlight", "social-proof", "comparison", "ugc-style"],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} advertisement, {i} creative angle, professional, cinematic",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "ad-{i}"
    }
  }]
}
```

```bash
uv run scripts/batch_generate.py --pipeline ads.json --var product="Acme Skincare Serum" --output-dir output/ads
```

## Example: City Localization

Same product, localized for 8 cities:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["New York", "Tokyo", "London", "Paris", "Dubai", "Sydney", "Mumbai", "Sao Paulo"],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} in a cinematic setting in {i}, local architecture and atmosphere, golden hour, professional ad",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "localized-{i}"
    }
  }]
}
```

```bash
uv run scripts/batch_generate.py --pipeline localize.json --var product="Acme Watch" --output-dir output/localized --notify
```

## Example: Multi-Format Campaign

Generate TikTok (vertical), Instagram (square), and YouTube (landscape) versions:

```json
{
  "steps": [
    {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} -- lifestyle ad, person using the product outdoors",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "tiktok"
    },
    {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} -- lifestyle ad, person using the product outdoors",
      "ratio": "1080:1080",
      "duration": 5,
      "filename": "instagram"
    },
    {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} -- lifestyle ad, person using the product outdoors, wide cinematic shot",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "youtube"
    }
  ]
}
```

## Inline Pipeline (No File Needed)

For quick one-off pipelines, pass JSON directly:

```bash
uv run scripts/batch_generate.py --pipeline '{"steps":[{"action":"generate_video","model":"gen4.5","prompt":"a cat astronaut floating in space","duration":5,"filename":"space-cat"}]}'
```

## Template Variables

Use `{{variable}}` in pipeline JSON and pass values at runtime:

```bash
uv run scripts/batch_generate.py --pipeline template.json --var product="Red Sports Car" --var style="cinematic"
```

All variables must be provided or the pipeline exits with an error.

## Parallel Fan Out

Add `"parallel": true` to a fan_out step to run all sub-jobs concurrently:

```json
{
  "action": "fan_out",
  "parallel": true,
  "sources": ["1", "2", "3", "4", "5"],
  "step": {
    "action": "generate_video",
    "model": "gen4.5",
    "prompt": "Creative variant {i}",
    "filename": "variant-{i}"
  }
}
```

Control concurrency with `--max-parallel N` (default: 3). Set this based on your API tier's concurrency limit.

## Resume Interrupted Pipelines

Use `--resume` to skip already-completed steps. The pipeline saves a `.pipeline-state.json` manifest after each step. On resume, `use_previous` chains are correctly restored from the manifest.

## Dry Run

Use `--dry-run` to estimate credit cost without executing:

```bash
uv run scripts/batch_generate.py --pipeline big-campaign.json --dry-run
```

## Tips

- Use `fan_out` to branch -- it runs the sub-step once per source
- `use_previous: true` chains steps automatically
- Start with `veo3.1_fast` or `gen4_turbo` for drafts, switch to `gen4.5` for finals
- Set `--max-parallel` to match your API tier concurrency (Tier 1: 1-2, Tier 3: 5, Tier 5: 20)
- Use `{i}` in prompts and filenames inside `fan_out` to vary per iteration
- Always `--dry-run` before large batches
