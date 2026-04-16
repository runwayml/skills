# Changelog

## 2.0.0

- **Media generation:** New `rw-generate-video`, `rw-generate-image`, `rw-generate-audio` skills that run Python scripts directly via `uv run` — no SDK setup required
- **Runnable scripts:** Added `scripts/` directory with `generate_video.py`, `generate_image.py`, `generate_audio.py`, `list_models.py`, `get_task.py`, and shared `runway_helpers.py`
- **Seedance 2 support:** Added `seedance2` model across all generation scripts and skills (TTV, ITV, VTV, 36 credits/sec)
- **Plugin metadata:** Updated descriptions and keywords for both Claude and Cursor plugins

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
