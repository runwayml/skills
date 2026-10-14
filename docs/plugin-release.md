# Runway Dev plugin release

The repository root is the v4 plugin. Edit `plugin.json`, native host manifests, MCP configuration, and active `skills/` directly. No generated copies or synchronization are needed. `scripts/build_dev_plugin.py` exports an allowlisted ZIP from those files; update the allowlist when adding skill resources. Legacy generation and utility skills and their helper scripts are archived under `legacy/`, outside active discovery. Their source is preserved; the archive README documents explicit legacy use.

## Validate and build

Use Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/ruff check scripts/build_dev_plugin.py scripts/validate_dev_plugin.py tests/test_dev_plugin.py
.venv/bin/ruff format --check scripts/build_dev_plugin.py scripts/validate_dev_plugin.py tests/test_dev_plugin.py
python3 -m unittest discover -s tests
python3 scripts/build_dev_plugin.py
mkdir -p .build/schemas
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/plugin.schema.json -o .build/schemas/plugin.schema.json
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/mcp.schema.json -o .build/schemas/mcp.schema.json
.venv/bin/python scripts/validate_dev_plugin.py .build/runway-api-4.0.0.zip
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

CI runs the packaging checks; it does not install plugins, authenticate, publish, or run billable generations. Review the exact ZIP inventory, including hidden files, before submission.

Local validation on October 14, 2026 passed portable JSON Schema/ZIP checks, packaging unit tests, and Python lint/format checks. Codex CLI `0.162.0-alpha.17.2` discovered and installed v4 with all seven skills and the onboarding entrypoint. Claude Code `2.1.231` validated and installed the package; its component inventory reported seven skills, one MCP server, and no hooks. Temporary test installs and marketplace registrations were removed afterward. Skills CLI discovery listed exactly seven active skills from the repository root and five archived skills only when explicitly pointed at `legacy/`. These checks did not authenticate the new connection or run review cases. Cursor native inspection did not produce a usable plugin-management view; runtime validation remains pending.

An additional validation pass on October 14 checked the corrected Recipe SDK guidance and the boundaries around fetched references and account actions:

| Check | Observed result | Remaining validation |
| --- | --- | --- |
| Updated Codex and Claude installation | Seven current Dev skills, one MCP connection; temporary installs removed | Claude authenticated tool calls and reconnect behavior |
| Production unauthenticated initialization | 401 with the Runway protected-resource metadata challenge | Incomplete-account recovery through each host |
| Production invalid bearer token | 401 with an OAuth recovery challenge | Token refresh and expiration through each host |
| Production OAuth discovery | Resource and authorization-server metadata return 200; authorization server advertises CIMD and PKCE S256 | OAuth through the other hosts |
| Native Codex OAuth and account access | Native CIMD authorization, callback, and token exchange completed; `whoami` and `list_projects` succeeded using a temporary server URL override matching the plugin endpoint | Token refresh and incomplete-account recovery |
| Installed Codex plugin authentication | `codex mcp login runway-dev` authenticated the bundled connection; a fresh native CLI session successfully called its `whoami` and `list_projects` tools; temporary plugin installation removed afterward | Token refresh, incomplete-account recovery, and project-specific reviewer cases |
| Claude agent runtime | Client rejected the request because its Claude OAuth token was expired | Reauthenticate Claude before testing the Runway connection |
| Cursor CLI local plugin loading | `--plugin-dir` exposes Runway Dev MCP as requiring authentication | Cursor client login, Runway consent, skill activation and tool calls |
| Replit skill distribution | Skills CLI installed all seven current skills into an isolated Replit project's `.agents/skills`; install-link payload matches the HTTPS MCP endpoint | Replit Project Editor authorization and tool calls |

These results establish packaging, distribution, unauthenticated protocol behavior, and read-only authenticated account access through both a temporary native Codex connection and the installed plugin's bundled connection. Codex credentials are associated with the configured connection; the successful temporary login did not authenticate the bundled `runway-dev` entry. A pre-existing manual connection was disabled only for the bundled runtime test through a per-invocation override, leaving the user's saved configuration unchanged. Native-host handling of the incomplete-account 403, the full dedicated-account review cases, and marketplace acceptance remain unverified. Complete browser sign-in and consent in the user's normal browser; do not collect passwords, callback URLs, OAuth codes, or application API keys in chat. No account changes or billable generations were performed, and no account identifiers or credentials are included in this record.

## Host distribution

| Host | Source | Identity |
| --- | --- | --- |
| Codex / ChatGPT | Portable package ZIP or `.agents/plugins/marketplace.json` | `runway-api`, displayed as Runway Dev |
| Claude Code | `.claude-plugin/marketplace.json` points at `./` | `runway-api@runway-dev` |
| Cursor | Root `.cursor-plugin/plugin.json` selects the root Dev skills and native MCP config | `runway-api`, displayed as Runway Dev |
| Replit | MCP install link plus selected standalone Dev skills | Runway Dev MCP |

The root Claude manifest keeps `name: runway-api` and declares `displayName: Runway Dev`; portable and Cursor manifests use the same identity. Anthropic's official `runway-api` entry currently points at this repository root and pins an older commit. After merging and validating v4, Anthropic must refresh the commit pin and listing metadata. No repository move, subdirectory source, or second plugin is needed. The Runway-maintained marketplace also loads this same root plugin.

Cursor's root manifest selects only active skills; its native MCP configuration contains the same endpoint as the portable package. For OpenAI public uploads, export the allowlisted ZIP with the build script. Do not ZIP the entire checkout, which includes archived code and development files, or add registered-app bindings or credentials to the public archive.

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
7. Who will coordinate the official Claude listing's commit-pin and display-metadata update and the separate Claude connector listing?

## Suggested recording

Show the v4 install and setup prompt, successful browser connection, identity/project selection, current video models and credits, failure diagnosis for the prepared task, and read-only router inspection. Finish with an unsupported subscription-refund request showing that no billing action occurs. Keep project data, prompts, and results readable. Stop or hide the recorder for credentials and OAuth codes. A walkthrough script is not a completed recording.
