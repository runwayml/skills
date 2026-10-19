# Maintaining the Runway Dev plugin

Edit the root manifests, MCP configuration, and active `skills/` directly. The MCP server is hosted separately; this repository packages its connection and skills. Legacy skills remain available at the pinned revision linked in the README, outside the current plugin files.

## Validate and build

Use Node.js 24.12 or newer:

```sh
npm --prefix tooling ci --ignore-scripts
npm --prefix tooling run check
npm --prefix tooling run typecheck
mkdir -p .build/schemas
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/plugin.schema.json -o .build/schemas/plugin.schema.json
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/mcp.schema.json -o .build/schemas/mcp.schema.json
shasum -a 256 -c tooling/scripts/portable-schemas.sha256
npm --prefix tooling test
npm --prefix tooling run build:plugin
npm --prefix tooling run validate:plugin
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

The exporter writes `.build/runway-api-<version>.zip` from an explicit allowlist. CI checks the package; installation, OAuth, and marketplace acceptance require separate verification.

If schema checksums change, review the upstream schema diff before updating `tooling/scripts/portable-schemas.sha256`.

## Updating a release

- Keep the version aligned in `plugin.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `.claude-plugin/marketplace.json`. Update the changelog and manifest release notes.
- When adding skill resources, update the export allowlist in `tooling/scripts/build-dev-plugin.ts` and Cursor's explicit skill paths. Keep model contracts in linked current docs.
- Test installation, setup, authenticated tool calls, and reconnect behavior in each supported host. Keep the manifest's reviewer cases aligned with supported behavior; record results against the release commit outside the package.

## Distribution

The install ID is `runway-api`; the display name is Runway Dev.

- Codex and ChatGPT use the portable ZIP; Codex also supports `.agents/plugins/marketplace.json`.
- Claude Code uses the root `.claude-plugin/` manifests. Anthropic manages its official listing and commit pin, so merging here does not update that listing automatically.
- Cursor uses the root `.cursor-plugin/plugin.json` and native `.mcp.json`.

Keep MCP configuration free of credentials. Check current [OpenAI](https://developers.openai.com/plugins/deploy/submission) and [Cursor](https://cursor.com/docs/reference/plugins) requirements when publishing an update.
