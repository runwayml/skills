# Changelog

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
