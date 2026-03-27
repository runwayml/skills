---
name: setup-global-auth
description: "Set up global authentication for direct Runway API access from the agent"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node */scripts/runway-api.mjs auth status)
---

# Setup Global Auth

Set up user-level authentication so the agent can call the Runway API directly — without configuring per-project `.env` files.

> **When to use this skill:** Use this when the user wants the agent to manage Runway resources directly (create avatars, upload files, trigger generations, etc.) rather than writing integration code into their app. For project-level `.env` setup, use `+setup-api-key` instead.

## Agent Flow

Follow these steps in order. **The API key must never appear in the chat.**

### 1. Check existing auth

Run:

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

If `authenticated` is `true`, you're done — tell the user they're already set up and proceed with whatever they asked for.

### 2. If not authenticated, guide the user

Tell the user:

> You need to authenticate with Runway. Here's what to do:
>
> 1. Open the Runway developer portal: **https://dev.runwayml.com/**
> 2. Go to **Organization Settings → API Keys**
> 3. Create a new API key (or use an existing one) and copy it
> 4. Run this command **in your terminal** (not here in the chat):
>
> ```
> node <path-to-skills-repo>/scripts/runway-api.mjs auth login YOUR_KEY_HERE
> ```
>
> Replace `YOUR_KEY_HERE` with the key you copied. The command will verify the key and store it securely.

Fill in the actual absolute path to `scripts/runway-api.mjs` so the user can copy-paste directly.

Remind the user:
- API keys require **prepaid credits** ($10 minimum) to work.
- The key is stored at `~/.config/runwayml/credentials.json` with restrictive permissions — it never enters any repo.

### 3. Verify

After the user says they've run the command, verify:

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

If it shows `authenticated: true`, confirm success and continue with whatever the user originally asked for.

If it still shows `false`, ask the user to check the terminal output from the login command for errors.

## Non-production environments

If the user wants to target staging or another environment, the login command accepts `--base-url`:

```
node <path-to-skills-repo>/scripts/runway-api.mjs auth login YOUR_KEY_HERE --base-url https://api.dev-stage.runwayml.com
```

## Removing credentials

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth logout
```

## How It Works

- Credentials are stored at `~/.config/runwayml/credentials.json` with `0600` permissions.
- `RUNWAYML_API_SECRET` environment variable always overrides stored credentials for one-off calls.
- The login command verifies the key against the API before persisting it.
- The agent should **never** print, echo, or request the full API key in the chat.

## Next Steps

Once authenticated, use `+use-api` to call the Runway API directly from the agent.
