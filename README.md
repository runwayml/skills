# Runway Dev

Runway Dev helps your coding agent build AI video, image and audio generation into your apps with Runway’s API, including Runway’s own models alongside the best from other labs.

## What’s included

- **The Runway Dev MCP** connects your agent to your Runway Developer Portal account. It can look up available models, prices and limits; set up Model Routers based on cost, speed or quality, with an optional credit cap; and manage real-time avatars. It can also inspect failed tasks and routing decisions to help you work out what to check next.
- **Skills** show your agent how to integrate the API with the official SDKs, and how to build with models, Model Routers, Recipes, Workflows and real-time avatars.

This repository is the plugin: root manifests and MCP configuration load the seven active skills in `skills/`. Claude uses a separate plugin folder, `claude/`, described below. The install ID remains `runway-api`; the display name is Runway Dev.

Installing a plugin does not configure an application's API key or automatically create a Runway account. Public directory availability depends on each host's listing.

## Claude Code

The Claude plugin lives in `claude/`, with its own manifest, MCP configuration and copies of the seven skills. It connects to `https://dev.runwayml.com/mcp/claude`, which omits the `create_avatar` tool; users create new avatars in the Developer Portal. Its skills validate integrations with local checks and leave live generations, Sessions, Recipe calls and Workflow invocations to the user's application.

Install from the Runway-maintained marketplace:

```sh
claude plugin marketplace add runwayml/skills
claude plugin install runway-api@runway-dev
```

For local testing:

```sh
claude plugin marketplace add /absolute/path/to/skills
claude plugin install runway-api@runway-dev
```

Ask Claude to help connect your Runway Dev account, or run `/runway-api:runway-dev-setup`. Complete browser sign-in and consent yourself.

The `runway-api@claude-plugins-official` listing is managed by Anthropic and may pin a different version from the Runway-maintained marketplace.

## Codex and ChatGPT

For local development, register this repository and install its plugin:

```sh
codex plugin marketplace add /absolute/path/to/skills
codex plugin add runway-api@runway-dev
```

The Git-backed equivalent is `codex plugin marketplace add runwayml/skills`. The package declares an onboarding skill; run setup or ask the agent to help connect your Runway Dev account. Public directory availability requires submission and review.

For an OpenAI package export, use Node.js 24.12 or newer:

```sh
npm --prefix tooling ci --ignore-scripts
npm --prefix tooling run build:plugin
```

This creates `.build/runway-api-4.0.0.zip`. It exports the root plugin files and active Dev skills from an explicit allowlist, excluding the Claude plugin folder and development files. Package validation and native authentication are separate checks.

## Cursor

The root `.cursor-plugin/plugin.json` defines **Runway Dev** (`runway-api`) and selects the root developer skills and MCP connection. For testing, use Cursor's local plugin workflow or its repository install flow with the branch containing this package. A standalone [MCP connection](https://docs.dev.runwayml.com/guides/mcp/) remains available; adding only MCP does not install skills.

## Replit

Replit distributes MCP connections and Agent Skills separately:

1. [Add Runway Dev MCP to Replit](https://replit.com/integrations?mcp=eyJkaXNwbGF5TmFtZSI6IlJ1bndheSBEZXYiLCJiYXNlVXJsIjoiaHR0cHM6Ly9kZXYucnVud2F5bWwuY29tL21jcCJ9) and complete browser authorization.
2. Install the setup, foundation, and relevant surface skills:

```sh
npx skills add runwayml/skills --skill runway-dev-setup --skill runway-dev --skill runway-dev-models -a replit
```

The MCP link and standalone skills are separate installations.

## Skills

| Skill | Purpose |
| --- | --- |
| `runway-dev-setup` | Connect an account and project; guide application key setup when needed |
| `runway-dev` | Shared server boundary, current docs, credentials, SDK tasks, and errors |
| `runway-dev-models` | Integrate direct model endpoints |
| `runway-dev-model-routers` | Configure and integrate Model Routers |
| `runway-dev-characters` | Integrate real-time Characters and Sessions |
| `runway-dev-recipes` | Implement documented Recipe pipelines |
| `runway-dev-workflows` | Call published Runway app Workflows through the API |

Standalone installation works for compatible agents without the plugin:

```sh
npx skills add runwayml/skills --skill runway-dev --skill runway-dev-models --agent cursor claude-code codex
```

Standalone skills do not automatically configure MCP. Use one installation path for each skill to avoid duplicate copies.

## Credentials and usage

MCP uses browser OAuth at `https://dev.runwayml.com/mcp`; do not put an API key in its configuration. Your application uses its own server-side `RUNWAYML_API_SECRET`. Create the key in [Developer Portal](https://dev.runway.com/) and keep it out of browser bundles, chat, and source control. API generations may consume credits.

Use the [current docs](https://docs.dev.runwayml.com/), [MCP connection guide](https://docs.dev.runwayml.com/guides/mcp/), and [agent context](https://docs.dev.runwayml.com/ai-context.md) for current contracts. No model catalog or prices are pinned in this README.

## Development and release

Edit the root manifests and active `skills/` directly. When a skill changes, make the matching change in `claude/skills/` unless it conflicts with the Claude variant's differences above; there is no generated copy or sync step. Build and test dependencies live under `tooling/` so plugin installation does not install development packages. Run `npm --prefix tooling run build:plugin` to export a ZIP; add any new skill resources to its explicit file allowlist. CI checks the export, cross-host paths, and portable schemas. See [the maintainer guide](https://github.com/runwayml/skills/blob/main/docs/plugin-release.md).

Licensed under [MIT](LICENSE).
