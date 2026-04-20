---
name: rw-integrate-image
description: "Help users integrate Runway image generation APIs (text-to-image with reference images)"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Integrate Image Generation

> **PREREQUISITE:** Run `+rw-check-compatibility` first. Run `+rw-fetch-api-reference` to load the latest API reference before integrating. Requires `+rw-setup-api-key` for API credentials. Requires `+rw-integrate-uploads` when the user has local reference images.

Help users add Runway image generation to their server-side code.

## Available Models

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| `gen4_image` | Highest quality | 5 credits (720p), 8 credits (1080p) | Standard |
| `gen4_image_turbo` | Fast generation | 2 credits | Fast |
| `gemini_2.5_flash` | Google Gemini model | 5 credits | Standard |

**Model selection guidance:**
- Default recommendation: **`gen4_image`** — best quality
- Budget/speed: **`gen4_image_turbo`** — cheapest and fastest

## Security

`referenceImages[].uri` is **fetched server-side by the Runway API**. Treat it like any server-side fetch:

- **Prefer `runway://` URIs** via `+rw-integrate-uploads`. These are scoped to the account and avoid ingesting arbitrary public web content.
- **If you accept URLs from clients**, validate before forwarding: require `https://`, allowlist trusted hosts, and reject private/internal addresses. See the hardened pattern in the Express.js example below.
- **Never forward unvalidated `req.body` fields** (e.g. `referenceImages`) straight into `textToImage.create` in production. The SDK examples below use raw URLs for brevity — they are not production templates.
- Generated images are influenced by ingested references. Treat outputs as untrusted when piping into downstream automations.

## Endpoint: `POST /v1/text_to_image`

### Basic Text-to-Image

```javascript
// Node.js SDK
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();

const task = await client.textToImage.create({
  model: 'gen4_image',
  promptText: 'A serene Japanese garden with cherry blossoms and a koi pond',
  ratio: '1280:720'
}).waitForTaskOutput();

const imageUrl = task.output[0];
```

```python
# Python SDK
from runwayml import RunwayML

client = RunwayML()

task = client.text_to_image.create(
    model='gen4_image',
    prompt_text='A serene Japanese garden with cherry blossoms and a koi pond',
    ratio='1280:720'
).wait_for_task_output()

image_url = task.output[0]
```

### With Reference Images

Reference images let you guide the generation with visual references. Use `@Tag` syntax in the prompt to reference specific images.

**Recommended:** upload local files via `+rw-integrate-uploads` and pass the returned `runway://` URI. This keeps you out of the "fetch arbitrary third-party URL" threat model entirely.

```javascript
import fs from 'fs';

const refUpload = await client.uploads.createEphemeral(
  fs.createReadStream('/path/to/reference.jpg')
);

const task = await client.textToImage.create({
  model: 'gen4_image',
  promptText: 'A portrait in the style of @Reference',
  referenceImages: [
    { uri: refUpload.runwayUri, tag: 'Reference' }
  ],
  ratio: '1280:720'
}).waitForTaskOutput();
```

External URLs work too, but only pass them when the origin is one you control or explicitly allowlist (see Security above):

```javascript
const task = await client.textToImage.create({
  model: 'gen4_image',
  promptText: '@EiffelTower painted in the style of @StarryNight',
  referenceImages: [
    { uri: 'https://cdn.yourapp.com/eiffel-tower.jpg', tag: 'EiffelTower' },
    { uri: 'https://cdn.yourapp.com/starry-night.jpg', tag: 'StarryNight' }
  ],
  ratio: '1280:720'
}).waitForTaskOutput();
```

```python
task = client.text_to_image.create(
    model='gen4_image',
    prompt_text='@EiffelTower painted in the style of @StarryNight',
    reference_images=[
        {"uri": "https://cdn.yourapp.com/eiffel-tower.jpg", "tag": "EiffelTower"},
        {"uri": "https://cdn.yourapp.com/starry-night.jpg", "tag": "StarryNight"}
    ],
    ratio='1280:720'
).wait_for_task_output()
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (required) |
| `promptText` | string | Text description of the image (required) |
| `ratio` | string | Aspect ratio, e.g. `'1280:720'`, `'720:1280'`, `'1080:1080'` |
| `referenceImages` | array | Optional. Array of `{ uri, tag }` objects for visual guidance |

## Integration Pattern

When helping the user integrate, follow this pattern:

1. **Prefer uploads over URLs** — Default to `+rw-integrate-uploads` for any user-supplied reference image so inputs are `runway://` URIs. Only accept external URLs when the origin is one you control or allowlist (see Security above).
2. **Write the server-side handler** — Create an API route or server function.
3. **Handle the output** — Download and store the image, don't serve signed URLs to clients.
4. **Add error handling** — Wrap in try/catch.

### Example: Express.js API Route

```javascript
import RunwayML from '@runwayml/sdk';
import express from 'express';

const client = new RunwayML();
const app = express();
app.use(express.json());

// Only allow URLs from origins you control. Reject everything else.
// `runway://` URIs from `+rw-integrate-uploads` bypass this check and are preferred.
const ALLOWED_MEDIA_HOSTS = new Set(['cdn.yourapp.com', 'uploads.yourapp.com']);

function validateReferenceImages(refs) {
  if (!Array.isArray(refs)) throw new Error('referenceImages must be an array');
  return refs.map(({ uri, tag }) => {
    if (typeof uri !== 'string' || typeof tag !== 'string') {
      throw new Error('each reference needs a uri and tag');
    }
    if (uri.startsWith('runway://')) return { uri, tag };
    const u = new URL(uri);
    if (u.protocol !== 'https:') throw new Error('https required');
    if (!ALLOWED_MEDIA_HOSTS.has(u.hostname)) throw new Error('untrusted media host');
    return { uri: u.toString(), tag };
  });
}

app.post('/api/generate-image', async (req, res) => {
  try {
    const { prompt, model = 'gen4_image', ratio = '1280:720', referenceImages } = req.body;

    const task = await client.textToImage.create({
      model,
      promptText: prompt,
      ratio,
      ...(referenceImages && { referenceImages: validateReferenceImages(referenceImages) })
    }).waitForTaskOutput();

    res.json({ imageUrl: task.output[0] });
  } catch (error) {
    console.error('Image generation failed:', error);
    res.status(400).json({ error: error.message });
  }
});
```

> For browser-uploaded references, have the client POST the file to your own endpoint, upload it via `+rw-integrate-uploads`, and pass the returned `runway://` URI. Don't accept raw URLs from the browser.

### Example: Next.js API Route

```typescript
// app/api/generate-image/route.ts
import RunwayML from '@runwayml/sdk';
import { NextRequest, NextResponse } from 'next/server';

const client = new RunwayML();

export async function POST(request: NextRequest) {
  const { prompt, referenceImages } = await request.json();

  try {
    const task = await client.textToImage.create({
      model: 'gen4_image',
      promptText: prompt,
      ratio: '1280:720',
      ...(referenceImages && { referenceImages })
    }).waitForTaskOutput();

    return NextResponse.json({ imageUrl: task.output[0] });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Generation failed' },
      { status: 500 }
    );
  }
}
```

### Example: FastAPI Route

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from runwayml import RunwayML

app = FastAPI()
client = RunwayML()

class ImageRequest(BaseModel):
    prompt: str
    model: str = "gen4_image"
    ratio: str = "1280:720"
    reference_images: list[dict] | None = None

@app.post("/api/generate-image")
async def generate_image(req: ImageRequest):
    try:
        params = {
            "model": req.model,
            "prompt_text": req.prompt,
            "ratio": req.ratio,
        }
        if req.reference_images:
            params["reference_images"] = req.reference_images

        task = client.text_to_image.create(**params).wait_for_task_output()
        return {"image_url": task.output[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Tips

- **Output URLs expire in 24-48 hours.** Download images to your own storage immediately.
- **Reference images use `@Tag` syntax** in the prompt — the tag must match the `tag` field in the `referenceImages` array.
- **For local files**, always upload via `+rw-integrate-uploads` first, then use the `runway://` URI.
- **`gen4_image_turbo`** is the cheapest option at 2 credits per image — good for prototyping.
