---
name: rw-check-compatibility
description: "Analyze a user's codebase to verify it can use Runway's public API (server-side requirement)"
user-invocable: false
allowed-tools: Read, Grep, Glob, Bash(node --version), Bash(python3 --version), Bash(pip show *), Bash(npm ls *)
---

# Check Compatibility

Analyze the user's project to determine whether it is compatible with Runway's public API.

## Why This Matters

Runway's public API **requires server-side invocation**. The API key must never be exposed in client-side code. Projects that are purely frontend (static HTML/JS, client-only SPAs without a backend) cannot safely call the API.

## Analysis Steps

### Step 1: Identify the Project Type

Search the project root for these files to determine the stack:

| File | Indicates |
|------|-----------|
| `package.json` | Node.js project |
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` | Python project |
| `go.mod` | Go project |
| `Cargo.toml` | Rust project |
| `pom.xml`, `build.gradle` | Java/Kotlin project |
| `Gemfile` | Ruby project |
| `composer.json` | PHP project |

If none of these exist, flag the project as **unknown** and ask the user what language/runtime they're using.

### Step 2: Check for Server-Side Capability

Look for indicators of a server/backend:

**Node.js projects — check `package.json` dependencies for:**
- `express`, `fastify`, `koa`, `hapi`, `nest`, `hono` → HTTP server framework
- `next` → Next.js (has API routes — compatible)
- `nuxt` → Nuxt.js (has server routes — compatible)
- `remix` → Remix (has loaders/actions — compatible)
- `@sveltejs/kit` → SvelteKit (has server routes — compatible)
- `astro` → Astro (has API endpoints if SSR enabled)

**Python projects — check for:**
- `flask`, `django`, `fastapi`, `starlette`, `tornado`, `aiohttp`, `sanic` → web server framework
- `streamlit`, `gradio` → can make server-side calls

**Red flags (frontend-only):**
- `package.json` with only `react`, `vue`, `svelte`, `angular` and NO server framework
- `vite.config.ts` or `webpack.config.js` with no server/SSR configuration
- Static site generators without server routes (e.g., plain Gatsby, plain Eleventy)
- `index.html` as the only entry point with inline `<script>` tags

### Step 3: Check for Existing Runway SDK

Search for existing Runway SDK installations:

**Node.js:**
- Check `package.json` for `@runwayml/sdk`
- Search for `import RunwayML` or `require('@runwayml/sdk')` in source files

**Python:**
- Check `requirements.txt` / `pyproject.toml` for `runwayml`
- Search for `from runwayml import RunwayML` or `import runwayml` in source files

### Step 4: Check Runtime Version

**Node.js:** Must be version 18 or higher (`node --version`)
**Python:** Must be version 3.8 or higher (`python3 --version`)

### Step 5: Check for Environment Variable Support

Look for `.env` file, `.env.example`, `.env.local`, or dotenv configuration:
- Node.js: `dotenv` in dependencies, or framework-native env support (Next.js, etc.)
- Python: `python-dotenv` in dependencies, or framework-native support

## Report Format

After analysis, provide a clear report:

```
## Runway API Compatibility Report

**Project type:** [Node.js / Python / etc.]
**Server-side capable:** [Yes / No / Partial]
**Runtime version:** [version] — [Compatible / Needs upgrade]
**Runway SDK installed:** [Yes / No]
**Environment variable support:** [Yes / No / Needs setup]

### Verdict: [COMPATIBLE / NEEDS CHANGES / INCOMPATIBLE]

[If COMPATIBLE]
Your project is ready for Runway API integration. Proceed with API key setup.

[If NEEDS CHANGES]
Your project needs the following changes:
1. [List specific changes needed]

[If INCOMPATIBLE]
Your project is frontend-only and cannot safely call Runway's API. Options:
1. **Add a backend** — Add an Express/FastAPI server or use a framework with server routes (Next.js, SvelteKit, etc.)
2. **Use a serverless function** — Add API routes via Vercel Functions, AWS Lambda, Cloudflare Workers, etc.
3. **Create a separate backend** — Build a thin API proxy that your frontend calls
```

## Important Notes

- **Never suggest embedding the API key in client-side code.** This is a security risk.
- If the project uses Next.js, Remix, SvelteKit, Nuxt, or Astro with SSR, it IS compatible — the server-side route handlers can call the API.
- Serverless platforms (Vercel, Netlify, AWS Lambda, Cloudflare Workers) are compatible.
- Docker/containerized apps are compatible if they run a server process.

## After Compatibility Check

If the project is compatible, suggest the user proceed with `+rw-setup-api-key` to configure their API credentials.
