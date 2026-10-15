# Runway Dev

Build AI video, image, audio, and real-time Character features into applications with Runway Dev. The developer plugin combines the hosted Dev MCP with seven skills for setup, official SDK integration, models, Model Routers, Characters, Recipes, and published Workflows.

This repository is the plugin: root manifests and MCP configuration load the seven active skills in `skills/`. The install ID remains `runway-api`; the display name is Runway Dev.

The v4 plugin in this branch is in development. Public directory submissions and the existing official Claude listing update are pending. Installing a plugin does not configure an application's API key or automatically create a Runway account.

## Claude Code

Use the Runway-maintained marketplace to install the Dev-only package after these changes are merged:

```sh
claude plugin marketplace add runwayml/skills
claude plugin install runway-api@runway-dev
```

For local testing before merge:

```sh
claude plugin marketplace add /absolute/path/to/skills
claude plugin install runway-api@runway-dev
```

Ask Claude to help connect your Runway Dev account, or run `/runway-api:runway-dev-setup`. Complete browser sign-in and consent yourself.

The existing `runway-api@claude-plugins-official` listing is pinned to the legacy package. Anthropic must refresh its commit pin and listing metadata before that install command supplies v4. The repository URL and root source stay the same. The older community listing is separate. See [release instructions](https://github.com/runwayml/skills/blob/main/docs/plugin-release.md).

## Codex and ChatGPT

For local development, register this repository and install its plugin:

```sh
codex plugin marketplace add /absolute/path/to/skills
codex plugin add runway-api@runway-dev
```

Once merged, the Git-backed equivalent is `codex plugin marketplace add runwayml/skills`. The package declares an onboarding skill; run setup or ask the agent to help connect your Runway Dev account. Public directory availability requires submission and review.

For an OpenAI package export, use Node.js 24.12 or newer:

```sh
npm ci --ignore-scripts
npm run build:plugin
```

This creates `.build/runway-api-4.0.0.zip`. It exports the root plugin files and active Dev skills from an explicit allowlist, excluding the legacy archive and development files. Package validation and native authentication are separate checks.

## Cursor

The root `.cursor-plugin/plugin.json` defines **Runway Dev** (`runway-api`) and selects the root developer skills and MCP connection. Submit this public repository to the Cursor Marketplace after local testing. The new listing is not yet published.

For testing, use Cursor's local plugin workflow or its repository install flow with the branch containing this package. A standalone [MCP connection](https://docs.dev.runwayml.com/guides/mcp/) remains available; adding only MCP does not install skills.

## Replit

Replit distributes MCP connections and Agent Skills separately:

1. [Add Runway Dev MCP to Replit](https://replit.com/integrations?mcp=eyJkaXNwbGF5TmFtZSI6IlJ1bndheSBEZXYiLCJiYXNlVXJsIjoiaHR0cHM6Ly9kZXYucnVud2F5bWwuY29tL21jcCJ9) and complete browser authorization.
2. Install the setup, foundation, and relevant surface skills:

```sh
npx skills add runwayml/skills --skill runway-dev-setup --skill runway-dev --skill runway-dev-models -a replit
```

The link uses Replit's documented MCP install format; its Runway OAuth flow still needs real-host validation. This is not a published Replit plugin bundle.

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

## Legacy generation and utility skills

The older `rw-generate-*`, `use-runway-api`, and `rw-check-org-details` skills and their helpers are archived under [`legacy/`](https://github.com/runwayml/skills/tree/main/legacy). They are retired from the active plugin and have not been refreshed. The archive explains explicit standalone installation for self-contained skills and the repository checkout needed for shared Python helpers. Existing marketplace installs pinned to an older commit keep that version until updated.

## Credentials and usage

MCP uses browser OAuth at `https://dev.runwayml.com/mcp`; do not put an API key in its configuration. Your application uses its own server-side `RUNWAYML_API_SECRET`. Create the key in [Developer Portal](https://dev.runway.com/) and keep it out of browser bundles, chat, and source control. API generations may consume credits.

Use the [current docs](https://docs.dev.runwayml.com/), [MCP connection guide](https://docs.dev.runwayml.com/guides/mcp/), and [agent context](https://docs.dev.runwayml.com/ai-context.md) for current contracts. No model catalog or prices are pinned in this README.

## Development and release

Edit the root manifests and active `skills/` directly. There is no generated plugin copy or sync step. Run `npm run build:plugin` to export a ZIP; add any new skill resources to its explicit file allowlist. CI checks the export, cross-host paths, and portable schemas. See [validation, host testing, and submission preparation](https://github.com/runwayml/skills/blob/main/docs/plugin-release.md).

Licensed under [MIT](LICENSE).
