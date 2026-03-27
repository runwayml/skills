# Auth Setup

Use environment variables for direct Runway API actions. The API key must never appear in the chat.

## Default setup

1. Open the API keys page: `https://dev.runwayml.com/settings/api-keys`
2. Create or copy an API key
3. Set it in the environment that launches your editor

Current shell before launching the editor:

```bash
export RUNWAYML_API_SECRET=YOUR_KEY_HERE
cursor .
```

Or add it to your shell profile, then restart the editor:

```bash
echo 'export RUNWAYML_API_SECRET=YOUR_KEY_HERE' >> ~/.zshrc
source ~/.zshrc
```

Replace `YOUR_KEY_HERE` locally in the terminal. Never paste the key into the chat.

## Verify

```bash
node <path-to-skills-repo>/scripts/runway-api.mjs auth status
```

If `authenticated` is still `false`, restart the editor or launch it from a shell that already has `RUNWAYML_API_SECRET` set.

## Non-production environments

Set `RUNWAYML_BASE_URL` alongside the API key:

```bash
export RUNWAYML_BASE_URL=https://api.dev-stage.runwayml.com
```

## Notes

- API keys require prepaid credits to work.
- `RUNWAYML_BASE_URL` defaults to `https://api.dev.runwayml.com`.
- `auth status` verifies that the current environment can reach the API successfully.
