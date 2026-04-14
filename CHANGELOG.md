# Changelog

## 2.0.0

- **Agent-first rebrand:** Runway API Skills is now an agent-first media generation platform
- **New runnable scripts:** `generate_video.py`, `generate_image.py`, `generate_audio.py` for direct generation via CLI
- **Pipeline system:** `batch_generate.py` with fan_out, parallel execution, `--dry-run`, `--resume`, template variables
- **Shopify integration:** `shopify_products.py` fetches all products from a store for batch ad generation
- **Utility scripts:** `list_models.py`, `get_task.py`
- **New skills:** `rw-generate-video`, `rw-generate-image`, `rw-generate-audio` (agent-first runnable skills)
- **Batch skills:** `rw-batch-campaign` for high-volume campaigns, `rw-shopify-product-ads` for Shopify product video ads
- **COOKBOOK.md:** 5 production recipes -- Shopify ads, localization, product-to-video, storyboard, creative iteration
- **PIPELINES.md:** Pipeline JSON format reference with examples
- All scripts use `uv run` with inline dependencies (zero install)

## 1.1.0

- **Breaking change:** Every skill is now named with an `rw-` prefix (skill folder under `skills/`, `name` in each `SKILL.md`, and `+…` invocations). Examples: `setup-api-key` → `rw-setup-api-key`, `integrate-video` → `rw-integrate-video`. Update any documentation, shortcuts, or automation that referenced the previous names or paths.

## 1.0.1

- Added Characters integration skills (`integrate-characters`, `integrate-character-embed`, `integrate-documents`)
- Improved compatibility check and integration skills
- Added Cursor marketplace plugin packaging (`.cursor-plugin/plugin.json`)

## 1.0.0

- Initial release with core skills: `check-compatibility`, `setup-api-key`, `recipe-full-setup`
- Integration skills for video, image, audio, and uploads
- rw-api-reference and rw-fetch-api-reference skills
