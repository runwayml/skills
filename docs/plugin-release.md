# Runway Dev plugin release

The repository root is the v4 plugin. Edit `plugin.json`, native host manifests, MCP configuration, and active `skills/` directly. No generated copies or synchronization are needed. `scripts/build-dev-plugin.ts` exports an allowlisted ZIP from those files; update the allowlist when adding skill resources. Legacy generation and utility skills and their helper scripts are archived under `legacy/`, outside active discovery. Their source is preserved; the archive README documents explicit legacy use.

## Validate and build

Use Node.js 24.12 or newer. Node runs the TypeScript scripts and tests directly; dependencies are development-only:

```sh
npm ci --ignore-scripts
npm run check
npm run typecheck
mkdir -p .build/schemas
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/plugin.schema.json -o .build/schemas/plugin.schema.json
curl --fail --silent --show-error https://agent-plugins.org/schemas/1.0.0/mcp.schema.json -o .build/schemas/mcp.schema.json
npm test
npm run build:plugin
npm run validate:plugin
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

CI runs the packaging checks; it does not install plugins, authenticate, publish, or run billable generations. Review the exact ZIP inventory, including hidden files, before submission.

## Maintaining a release

Keep versions aligned in `plugin.json`, both native host manifests, and `.claude-plugin/marketplace.json`. The packaging tests catch version drift. When adding a skill or resource, update the export allowlist and Cursor's explicit skill paths, then rerun the checks above. Keep model contracts in current linked docs rather than copying a catalog into the package. Release from a recorded Git commit and inspect that commit's ZIP; archive validation is separate from native-host testing and marketplace approval.

The TypeScript conversion on October 15, 2026 passed Biome, type checking, six packaging/validation tests, and ZIP/schema validation. The exporter selects the same 15 files and bytes as its Python predecessor and produces byte-identical archives across UTC and Honolulu timezones. Node/npm replace the Python development tooling; archived Python helpers are unchanged.

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

| Material | Current state | Host requirement |
| --- | --- | --- |
| Logo and composer icon | Existing square 320×320 PNG is bundled and referenced | OpenAI icon requirements are met; Cursor logo is included |
| Listing copy and release notes | Drafted in `plugin.json`; final copy review pending | Use the same Runway Dev positioning across the three listings |
| Review cases | Five positive and three negative cases drafted | Run with the dedicated account before OpenAI submission |
| Walkthrough video | Rehearsal below is prepared; recording and accessible URL are missing | Required for OpenAI MCP review; no duration is specified in its submission guide |
| Screenshots | No custom UI is shipped | OpenAI disallows screenshots without custom UI; no screenshot asset is needed for this release |
| Reviewer access | Dedicated account and sample project with failed-task/router fixtures are missing | Provide working sign-in through secure portal fields, never the public ZIP |

See the current [OpenAI review materials](https://developers.openai.com/plugins/deploy/submission), [UI screenshot rules](https://developers.openai.com/plugins/deploy/app-review), and [Cursor submission checklist](https://cursor.com/docs/reference/plugins). Use the verified Runway logo; new artwork is not needed for this release. Cursor takes the public repository through its marketplace publish flow. Anthropic updates the existing Claude Code entry after the final commit lands.

Before calling the package submission-ready:

- Confirm the verified Runway publishing identity and intended country availability.
- Confirm that the linked support and policies cover the Dev plugin and its current data handling. The package links existing Runway pages; it makes no new legal commitments.
- Confirm the commerce declaration. This plugin has no payment or purchasing tool; app generations may consume the account's credits.
- Prepare a dedicated reviewer account, accessible sample project, failed task, and existing router. Supply credentials and sign-in instructions only through secure portal fields.
- Rehearse and record the actual host walkthrough, verify playback and absence of secrets, host it at a reviewer-accessible URL, then add that URL to `extensions.com.openai.review.demo_recording_url`.
- Run the review cases and record results; rebuild and inspect the ZIP.
- Complete OpenAI's domain-verification challenge, current production tool scan, skill scans, and required attestations. Verify the scanned annotation values against the actual tool behavior and prepare any justifications required by the portal; see [submission checks](https://developers.openai.com/plugins/deploy/submission-errors). Check OAuth on the saved submission independently of the successful Codex connection.

No country targeting, commerce declaration, demo URL, or reviewer credentials have been invented. Upload, submission for review, marketplace listing updates, and public publication are separate actions. The current repository changes do not perform them.

### Questions to resolve together

1. Who owns submission access for the verified Runway publisher in OpenAI, Cursor, and the existing Claude Code listing?
2. Which countries should the public listing be available in?
3. Who can provide the dedicated reviewer account and sample project, including an existing failed task and Model Router?
4. Do the existing Runway support, privacy, and terms pages cover this developer plugin and its current account/connection telemetry?
5. Is the intended commerce declaration that the plugin has no purchasing flow, while application API generations consume the account's credits?
6. Who should record the host walkthrough, and where should the reviewer-accessible video be hosted?
7. Who will coordinate the official Claude Code listing's commit-pin and display-metadata update?

## Suggested recording

Use the dedicated reviewer account and fixtures to rehearse these prompts in an actual installed host before recording:

1. "Help me connect my Runway Dev account and choose a project." Show the installed version, complete browser consent privately, and return to real identity/project results.
2. "Which video models can this project use, and what are their input limits and credit costs?" Then ask for its credit balance. Show the returned values without generating media.
3. Supply the prepared failed task ID and ask why it failed. Show the actual failure and proposed correction without resubmission.
4. "Show me this project's Model Routers and explain the settings of the one I choose." Select the prepared router and inspect it without edits.
5. "Cancel my Runway subscription and refund last month's charge." Show the unsupported-action explanation without a billing action. Exercise the remaining negative cases from the manifest as well.

Keep prompts and results readable and credentials off screen. Capture actual interactions, play back the saved video, verify reviewer access to its hosted URL, then add that URL to the manifest and rebuild. A script or screenshot sequence is not recording evidence. The dedicated reviewer account is the next prerequisite; publisher and availability decisions can be resolved separately.
