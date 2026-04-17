# Changelog

## 2.1.0

- **`use-runway-api`:** Runtime script moved from `scripts/runway-api.mjs` (repo root) to `skills/use-runway-api/scripts/runway-api.mjs` so it ships with the skill when installed via `npx skills add`, Claude plugins, or Cursor plugins. SKILL.md now documents a concrete `<skill-dir>` resolution strategy with fallback locations.
- **`use-runway-api`:** Added opinionated **Presenting Generation Output** section — lead with model + cost, embed images as Markdown, proactively offer to download locally, avoid pasting raw signed URLs.
- **`use-runway-api`:** Added `RUNWAY_SKILLS_DIR` env var as a fallback hint for the skill path.
- **`rw-api-reference`:** Added **Request Body Reference (raw JSON)** section with minimal POST bodies for every generation endpoint (text_to_image, text_to_video, image_to_video, video_to_video, text_to_speech, sound_effect, voice_isolation, voice_dubbing, speech_to_speech), plus `avatars`, `documents`, and `realtime_sessions`.
- **`AUTH.md`:** Fixed env var names (`RUNWAY_SKILLS_API_SECRET`, `RUNWAY_SKILLS_API_SECRET_STAGE`, `RUNWAY_SKILLS_BASE_URL`) to match the runtime script.

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
