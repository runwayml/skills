---
name: setup-global-auth
description: "Set up global authentication for direct Runway API access from the agent"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node */scripts/runway-api.mjs auth *), Bash(cat ~/.config/runwayml/credentials.json)
---

# Setup Global Auth

Set up user-level authentication so the agent can call the Runway API directly — without configuring per-project `.env` files.

> **When to use this skill:** Use this when the user wants the agent to manage Runway resources directly (create avatars, upload files, trigger generations, etc.) rather than writing integration code into their app. For project-level `.env` setup, use `+setup-api-key` instead.

## How It Works

Credentials are stored at `~/.config/runwayml/credentials.json` with restrictive file permissions (`0600`). The file contains an API key and base URL — never committed to any repo.

**Precedence:** The `RUNWAYML_API_SECRET` environment variable always overrides the stored credentials. This lets users do one-off calls against a different key without changing their global config.

## Step 1: Obtain an API Key

Direct the user to:

1. Go to **https://dev.runwayml.com/**
2. Create an organization (or use an existing one)
3. Navigate to **Organization Settings → API Keys**
4. Click **Create API Key**
5. **Copy the key immediately** — it is only shown once

Remind the user:
- API keys are **organization-scoped**, not user-scoped.
- They must **prepay for credits** ($10 minimum) before the API works.

## Step 2: Authenticate

Locate the `scripts/runway-api.mjs` script in this skills repository. Run:

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth login <api-key>
```

The command verifies the key against the API and stores it on success. It prints the organization name and the credentials file path.

### Non-production environments

To authenticate against a non-production API (e.g. staging):

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth login <api-key> --base-url https://api.dev-stage.runwayml.com
```

## Step 3: Verify

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

Expected output:

```json
{
  "authenticated": true,
  "source": "credentials-file",
  "baseUrl": "https://api.dev.runwayml.com",
  "keyPrefix": "rw_live_..."
}
```

## Removing Credentials

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth logout
```

## Security Notes

- The credentials file is stored with `0600` permissions (owner read/write only).
- Never pass the API key as a visible command-line argument in shared environments — use `RUNWAYML_API_SECRET` instead.
- The agent should **never** print or echo the full API key in its output.

## Next Steps

Once authenticated, use `+use-api` to call the Runway API directly from the agent.
