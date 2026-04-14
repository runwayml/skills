---
name: rw-batch-campaign
description: "Generate large batches of videos or images using Runway API pipelines. Fan-out, parallel execution, localization, A/B testing at scale."
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(uv run *), Bash(command -v uv)
---

# Batch Campaign Generation

Generate large batches of videos or images using the Runway API pipeline system. Supports fan_out for parallel generation, template variables, cost estimation, and resumable pipelines.

**IMPORTANT:** Run scripts from the user's working directory. Always use `--output-dir` to organize batch output.

## Usage

```bash
uv run scripts/batch_generate.py --pipeline pipeline.json [--output-dir output/campaign] [--max-parallel 3] [--dry-run] [--resume] [--var key=value] [--api-key KEY]
```

## Preflight

1. `command -v uv` must succeed
2. `RUNWAYML_API_SECRET` must be set, or pass `--api-key`

## Pipeline JSON Format

```json
{
  "steps": [
    {
      "action": "generate_video | generate_image | generate_audio | fan_out",
      "model": "gen4.5",
      "prompt": "...",
      "filename": "base-name",
      "use_previous": true,
      "duration": 5,
      "ratio": "1280:720"
    }
  ]
}
```

### Actions

- `generate_video` -- generate a single video
- `generate_image` -- generate a single image
- `generate_audio` -- generate audio (tts, sfx)
- `fan_out` -- run a sub-step for EACH source, enabling batch generation

### Special Fields

- `use_previous: true` -- use output URLs from the previous step as input
- `fan_out` has a `step` field containing the template to run per source
- In fan_out prompts/filenames, `{i}` is replaced with the iteration number (1, 2, 3...)
- `parallel: true` on fan_out runs all sub-jobs concurrently (up to `--max-parallel`)

## Pipeline Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--pipeline` | Path to JSON file or inline JSON string (required) | -- |
| `--api-key` | Runway API key | env `RUNWAYML_API_SECRET` |
| `--output-dir` | Output directory for all generated files | cwd |
| `--dry-run` | Estimate credit cost without executing | false |
| `--resume` | Skip completed steps (uses .pipeline-state.json) | false |
| `--max-parallel` | Max concurrent jobs for parallel fan_out | 3 |
| `--var` | Template variable (repeatable): `--var key=value` | -- |
| `--notify` | Desktop notification when pipeline finishes | false |

## Use Case 1: Generate 100 Ad Variants

Generate video ads across multiple angles and formats:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["lifestyle", "feature", "testimonial", "comparison", "ugc"],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product_name}} -- {i} angle, professional ad, clean background",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "ad-{i}"
    }
  }]
}
```

Run with:
```bash
uv run scripts/batch_generate.py --pipeline campaign.json --var product_name="Acme Serum" --output-dir output/ads --notify
```

## Use Case 2: Localize for Every Major City

Same product, different city backdrops:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["New York", "Tokyo", "London", "Paris", "Dubai", "Sydney", "Mumbai", "Berlin"],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product_name}} advertisement set in {i}, local landmarks visible, cinematic",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "ad-{i}"
    }
  }]
}
```

## Use Case 3: Image-to-Video Pipeline

Generate an image, then animate it:

```json
{
  "steps": [
    {
      "action": "generate_image",
      "model": "gen4_image",
      "prompt": "A luxury watch on marble surface, studio lighting",
      "ratio": "1280:720",
      "filename": "watch-hero"
    },
    {
      "action": "generate_video",
      "use_previous": true,
      "model": "gen4.5",
      "prompt": "Camera slowly orbits the watch, light reflections dance across the surface",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "watch-reveal"
    }
  ]
}
```

## Use Case 4: A/B Test Creative Angles

Generate multiple variants with different models and prompts for testing:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} creative variant {i} -- each with different mood, lighting, and composition",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "variant-{i}"
    }
  }]
}
```

## Workflow: Draft -> Iterate -> Final

1. **Draft (cheap):** use `veo3.1_fast` for quick iteration
2. **Iterate:** adjust prompts, try different angles
3. **Final (quality):** switch to `gen4.5` or `veo3` for the winning variants

## Cost Estimation

Always run `--dry-run` first to estimate costs before a big batch:

```bash
uv run scripts/batch_generate.py --pipeline campaign.json --dry-run
```

## Resume Interrupted Pipelines

If a pipeline is interrupted, re-run with `--resume` to skip completed steps:

```bash
uv run scripts/batch_generate.py --pipeline campaign.json --output-dir output/ads --resume
```

The pipeline saves a `.pipeline-state.json` manifest after each step.

## Building Pipelines for Users

When a user asks for batch generation:

1. Understand the dimensions: how many variants, what varies (prompt, model, location, format)
2. Write a pipeline JSON with `fan_out` for the varying dimension
3. Save the JSON to a file in the current directory
4. Run `--dry-run` first to show estimated cost
5. Run the pipeline with `--output-dir` and `--notify`
6. Report the output file paths when done

## For Shopify Product Ads

See `+rw-shopify-product-ads` for a specialized workflow that fetches products from a Shopify store and generates a video ad for each one.
