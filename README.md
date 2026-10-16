# Runway Dev

Build AI video, image, audio, and real-time Character features into applications with Runway Dev MCP and the official SDKs. This repository is the plugin: `plugin.json`, native host manifests, MCP configuration, and `skills/` live at the root. Its install ID remains `runway-api`; its display name is Runway Dev.

The v4 plugin is in development. The official Claude marketplace is pinned to an earlier commit; Anthropic must refresh its pin and listing before it supplies v4. The repository URL and root source remain the same.

For local Claude Code testing:

```sh
claude plugin marketplace add /absolute/path/to/skills
claude plugin install runway-api@runway-dev
```

For local Codex testing:

```sh
codex plugin marketplace add /absolute/path/to/skills
codex plugin add runway-api@runway-dev
```

Cursor uses the root `.cursor-plugin/plugin.json`. Public directory submissions are pending. Replit can use a [Dev MCP connection](https://docs.dev.runwayml.com/guides/mcp/) and standalone skills.

The plugin includes `runway-dev` plus skills for models, Model Routers, Characters, Recipes, and published Workflows. Standalone installation is also supported:

```sh
npx skills add runwayml/skills --skill runway-dev --skill runway-dev-models
```

MCP uses browser OAuth at `https://dev.runwayml.com/mcp`. Your application uses its own server-side `RUNWAYML_API_SECRET`, created in [Developer Portal](https://dev.runway.com/). Keep keys out of chat, browser code, and source control. Dev MCP does not generate media or create application API keys; application generations may consume credits.

Legacy generation and utility skills are archived under [`legacy/`](legacy/README.md), outside the active plugin. They have not been refreshed for this release.

Use the [current API documentation](https://docs.dev.runwayml.com/), [agent context](https://docs.dev.runwayml.com/ai-context.md), and [Runway support](https://help.runwayml.com/hc/en-us).

Licensed under [MIT](LICENSE).
