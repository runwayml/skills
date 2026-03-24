---
name: setup-api-key
description: "Guide users through obtaining and configuring a Runway API key"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(npm install *), Bash(pip install *), Bash(pip3 install *)
---

# Setup API Key

Guide the user through obtaining a Runway API key, installing the SDK, and configuring their project for API access.

> **PREREQUISITE:** Run `+check-compatibility` first to ensure the project has server-side capability.

## Step 1: Create a Runway Developer Account

Direct the user to:

1. Go to **https://dev.runwayml.com/**
2. Create an organization (or use an existing one)
3. Navigate to **Organization Settings → API Keys**
4. Click **Create API Key**
5. **Copy the key immediately** — it is only shown once and cannot be recovered

**Important warnings to tell the user:**
- Lost keys cannot be retrieved. If lost, disable the old key and create a new one.
- API keys are **organization-scoped**, not user-scoped.
- You must **prepay for credits** before the API will work. Minimum purchase is **$10** (1,000 credits at $0.01/credit). Do this at https://dev.runwayml.com/ under billing.

## Step 2: Install the SDK

### Node.js
```bash
npm install @runwayml/sdk
```
Requires **Node.js 18+**. The SDK includes TypeScript type definitions.

### Python
```bash
pip install runwayml
```
Requires **Python 3.8+**. Includes MyPy type annotations.

## Step 3: Configure the Environment Variable

The SDK automatically reads the API key from the `RUNWAYML_API_SECRET` environment variable.

### Option A: `.env` file (recommended for development)

Check if the project already has a `.env` file. If so, append to it. If not, create one.

```
RUNWAYML_API_SECRET=your_api_key_here
```

**For Node.js projects:** Ensure the project loads `.env` files:
- **Next.js, Remix, Vite** — built-in `.env` support, no extra setup needed
- **Express/Fastify/plain Node** — install `dotenv`:
  ```bash
  npm install dotenv
  ```
  Add to the entry point:
  ```javascript
  import 'dotenv/config';
  ```

**For Python projects:** Ensure `python-dotenv` is installed if not using a framework with built-in support:
```bash
pip install python-dotenv
```
Add to the entry point:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Option B: System environment variable

```bash
export RUNWAYML_API_SECRET=your_api_key_here
```

### Option C: Pass directly to the client (not recommended)

```javascript
// Node.js
const client = new RunwayML({ apiKey: 'your_api_key_here' });
```
```python
# Python
client = RunwayML(api_key='your_api_key_here')
```

**Warn the user:** Never hardcode keys in source code. Use environment variables or a secrets manager.

## Step 4: Update .gitignore

Ensure `.env` is in `.gitignore` to prevent accidentally committing the API key:

```
.env
.env.local
.env.*.local
```

Check the existing `.gitignore` and add the entry if it's missing.

## Step 5: Verify the Setup

Suggest the user run a quick verification:

### Node.js
```javascript
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();
// If no error is thrown, the API key is configured correctly
console.log('Runway SDK initialized successfully');
```

### Python
```python
from runwayml import RunwayML

client = RunwayML()
# If no error is thrown, the API key is configured correctly
print('Runway SDK initialized successfully')
```

## Step 6: Confirm Credit Balance

Remind the user:
- The API requires **prepaid credits** to function
- Minimum purchase: **$10** (1,000 credits)
- Purchase at: **https://dev.runwayml.com/** → Billing
- They can check their balance via the API:

```javascript
// Node.js - check organization info
const response = await fetch('https://api.dev.runwayml.com/v1/organization', {
  headers: {
    'Authorization': `Bearer ${process.env.RUNWAYML_API_SECRET}`,
    'X-Runway-Version': '2024-11-06'
  }
});
const org = await response.json();
console.log('Credits:', org.creditBalance);
```

## Security Checklist

Before moving on, verify:
- [ ] API key is stored in an environment variable, not hardcoded
- [ ] `.env` file is in `.gitignore`
- [ ] API calls will only happen server-side (not in browser-executed code)
- [ ] User has purchased credits

## Next Steps

Once the API key is configured, the user can proceed with integration:
- `+integrate-video` — Video generation (text-to-video, image-to-video)
- `+integrate-image` — Image generation
- `+integrate-audio` — Audio generation (TTS, sound effects, voice)
- `+integrate-uploads` — File upload for models that require image/video input
