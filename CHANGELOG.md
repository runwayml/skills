# Changelog

## 4.0.1

- Added tool title annotations and improved skill instructions.

## 4.0.0

- Runway Dev plugin bundles the hosted Dev MCP and seven refreshed integration/setup skills for Codex, Claude Code, and Cursor. Replit can use the same skills and a separate MCP install link.
- Setup guides browser sign-in or signup, account/project verification, and server-side application credentials.
- **Migration:** The repository root is the Dev plugin, keeping the `runway-api` install ID and using the Runway Dev display name. Earlier skills and helpers are no longer shipped; older commit-pinned installs stay on their prior version until updated.
- **Claude plugin:** Claude installs load `claude/`, which connects to the `/mcp/claude` endpoint without `create_avatar` and uses skill copies that leave live generations, Sessions, Recipe calls and Workflow invocations to the user's application.
- Allowlisted reproducible ZIP export without copied plugin trees, portable schema validation, packaging tests, and draft review cases.

## 3.0.0

- **Breaking:** Removed legacy `rw-integrate-*`, setup, compatibility, and static API-reference skills. Use `runway-dev` with the relevant `runway-dev-*` surface skill for application integration.
- **Durable guidance:** Moved server-boundary, API-key, uploads, Characters UI, and lifecycle guidance into the new Dev Platform skill set.

## 2.2.0

- **Dev Platform integration:** Added `runway-dev` foundation plus focused skills for models, Model Routers, Characters, recipes, and workflows using Dev MCP for live context and the SDK for app integration.

## 2.1.0

- **`use-runway-api`:** Runtime script moved from `scripts/runway-api.mjs` (repo root) to `skills/use-runway-api/scripts/runway-api.mjs` so it ships with the skill when installed via `npx skills add`, Claude plugins, or Cursor plugins. SKILL.md now documents a concrete `<skill-dir>` resolution strategy with fallback locations.
- **`use-runway-api`:** Added opinionated **Presenting Generation Output** section — lead with model + cost, embed images as Markdown, proactively offer to download locally, avoid pasting raw signed URLs.
- **`use-runway-api`:** Added `RUNWAY_SKILLS_DIR` env var as a fallback hint for the skill path.
- **`rw-api-reference`:** Added **Request Body Reference (raw JSON)** section with minimal POST bodies for every generation endpoint (text_to_image, text_to_video, image_to_video, video_to_video, text_to_speech, sound_effect, voice_isolation, voice_dubbing, speech_to_speech), plus `avatars`, `documents`, and `realtime_sessions`.
- **`AUTH.md`:** Fixed env var names (`RUNWAY_SKILLS_API_SECRET`, `RUNWAY_SKILLS_API_SECRET_STAGE`, `RUNWAY_SKILLS_BASE_URL`) to match the runtime script.

## 2.0.0

- **Seedance 2 support:** Added `seedance2` model documentation (TTV, ITV, VTV, 36 credits/sec)
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
