# Runway Dev plugin release

The v4 package lives at `plugins/runway-api/`. Canonical developer skills remain in `skills/runway-dev*/`; listing and package README source lives in `plugin/`. Run `python3 scripts/build_dev_plugin.py` after editing either. Generated files are committed for Git-backed marketplaces; `--check` fails if those copies drift. The plugin includes only the seven Dev skills. Legacy generation and utility skills remain separately installable from the repository.

## Validate and build

Use Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/ruff check scripts/build_dev_plugin.py scripts/validate_dev_plugin.py tests/test_dev_plugin.py
.venv/bin/ruff format --check scripts/build_dev_plugin.py scripts/validate_dev_plugin.py tests/test_dev_plugin.py
python3 -m unittest discover -s tests
python3 scripts/build_dev_plugin.py --check --zip
mkdir -p .build/schemas
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/plugin.schema.json -o .build/schemas/plugin.schema.json
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/mcp.schema.json -o .build/schemas/mcp.schema.json
.venv/bin/python scripts/validate_dev_plugin.py .build/runway-api-4.0.0.zip
claude plugin validate plugins/runway-api
claude plugin validate .claude-plugin/marketplace.json
```

CI runs the packaging checks; it does not install plugins, authenticate, publish, or run billable generations. Review the exact ZIP inventory, including hidden files, before submission.

Local validation on October 14, 2026 passed portable JSON Schema/ZIP checks, generated-file drift checks, packaging unit tests, and Python lint/format checks. Codex CLI `0.162.0-alpha.17.2` discovered and installed v4 with all seven skills and the onboarding entrypoint. Claude Code `2.1.231` validated and installed the package; its component inventory reported seven skills, one MCP server, and no hooks. Temporary test installs and marketplace registrations were removed afterward. These checks did not authenticate the new connection or run review cases. Cursor native inspection did not produce a usable plugin-management view; runtime validation remains pending.

## Host distribution

| Host | Source | Identity |
| --- | --- | --- |
| Codex / ChatGPT | Portable package ZIP or `.agents/plugins/marketplace.json` | `runway-api`, displayed as Runway Dev |
| Claude Code | `.claude-plugin/marketplace.json` points at `plugins/runway-api/` | `runway-api@runway-dev` |
| Cursor | Root `.cursor-plugin/plugin.json` selects the nested Dev skills and native MCP config | `runway-dev` |
| Replit | MCP install link plus selected standalone Dev skills | Runway Dev MCP |

The root `.claude-plugin/plugin.json` remains the legacy v3 package for existing Git-root consumers. It is not the v4 Dev-only package. Anthropic's official `runway-api` entry currently uses a commit-pinned Git-root source. After merging and validating v4, its owner must update both the pinned SHA and the source to a Git-subdirectory source pointing at `plugins/runway-api`. Preserve the existing `runway-api` identity. Updating only the SHA would continue loading root legacy skills. The custom Runway marketplace offers the nested v4 package independently.

Cursor's root manifest explicitly selects nested skills; its MCP configuration contains the same endpoint as the portable package. For OpenAI public uploads, ZIP the generated plugin directory, not the repository root. Do not add registered-app bindings or credentials to the public archive.

## Authentication compatibility

The portable `mcp.json` is URL-only and uses standard MCP OAuth discovery. Public discovery currently advertises the Runway login authorization server. The native `.mcp.json` uses HTTP transport for Claude and Cursor. No API key, client secret, or fixed bearer token is bundled.

OpenAI's packaging guide documents an OAuth extension on individual MCP servers, but the Agent Plugins 1.0 MCP schema and current Codex portable loader reject those extra server fields. Keep the common file schema-valid. Test authentication in Codex and in the ChatGPT plugin connection flow independently; if the submission portal needs additional connection details, provide them there and preserve its generated finalized configuration. Do not claim ZIP validity establishes OAuth or portal acceptance. See [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [portable schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json), and [Codex compatibility issue](https://github.com/openai/codex/issues/51092).

The setup skill handles older deployed MCP versions that lack `signup_url`: use the connection and account-setup docs and the existing `login_url`. The companion server change adds explicit signup recovery to `developer_not_found`; it does not automatically provision accounts or resume a pending OAuth callback.

## Real-host checks

Use a dedicated test account and sample project. Record client versions and results separately from schema/CLI validation.

1. Install and confirm exactly the seven Dev skills and one Runway Dev MCP server. Check a fresh session and installation during an existing conversation where supported.
2. Run setup. Test existing-account login, new-account signup, and a valid identity whose Developer Portal setup is incomplete. Complete browser consent yourself; return to the same coding client and check `whoami` and `list_projects`.
3. Cancel login, retry, expire/refresh a token, and reconnect. Confirm helpful errors and no duplicated MCP connections or skill installations.
4. Test an app with an existing server-side API key and an app without one. Verify setup never prints a key or puts it in browser code or MCP config.
5. Run the five positive and three negative review cases declared in the manifest. Prepare the real failed task and existing router fixtures first. Do not run generations just to fill a review fixture without approved usage.

For a first application generation, use a small explicitly approved request, inspect current model inputs and the project balance, and confirm that the application handles the task result. This is distinct from installing the plugin or testing read-only MCP tools.

## Submission preparation

Listing copy, existing branding, support/policy links, release notes, and draft review cases are included. The five positive and three negative cases are **not yet run against a reviewer account**.

Before calling the package submission-ready:

- Confirm the verified Runway publishing identity and intended country availability.
- Confirm that the linked support and policies cover the Dev plugin and its current data handling. The package links existing Runway pages; it makes no new legal commitments.
- Confirm the commerce declaration. This plugin has no payment or purchasing tool; app generations may consume the account's credits.
- Prepare a dedicated reviewer account, accessible sample project, failed task, and existing router. Supply credentials and sign-in instructions only through secure portal fields.
- Rehearse and record the actual host walkthrough, verify playback and absence of secrets, host it at a reviewer-accessible URL, then add that URL to `extensions.com.openai.review.demo_recording_url`.
- Run the review cases and record results; rebuild and inspect the ZIP.

No country targeting, commerce declaration, demo URL, or reviewer credentials have been invented. Upload, submission for review, marketplace listing updates, and public publication are separate actions. The current repository changes do not perform them.

### Questions to resolve together

1. Who owns submission access for the verified Runway publisher in OpenAI, Anthropic, Cursor, and Replit?
2. Which countries should the public listing be available in?
3. Who can provide the dedicated reviewer account and sample project, including an existing failed task and Model Router?
4. Do the existing Runway support, privacy, and terms pages cover this developer plugin and its current account/connection telemetry?
5. Is the intended commerce declaration that the plugin has no purchasing flow, while application API generations consume the account's credits?
6. Who should record the host walkthrough, and where should the reviewer-accessible video be hosted?
7. Who will coordinate the official Claude listing's source/SHA update and the separate Claude connector listing?

## Suggested recording

Show the v4 install and setup prompt, successful browser connection, identity/project selection, current video models and credits, failure diagnosis for the prepared task, and read-only router inspection. Finish with an unsupported subscription-refund request showing that no billing action occurs. Keep project data, prompts, and results readable. Stop or hide the recorder for credentials and OAuth codes. A walkthrough script is not a completed recording.
