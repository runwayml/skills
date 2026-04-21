---
name: rw-integrate-video
description: "Help users integrate Runway video generation APIs (text-to-video, image-to-video, video-to-video)"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Integrate Video Generation

> **PREREQUISITE:** Run `+rw-check-compatibility` first. Run `+rw-fetch-api-reference` to load the latest API reference before integrating. Requires `+rw-setup-api-key` for API credentials. Requires `+rw-integrate-uploads` when the user has local files to use as input.

Help users add Runway video generation to their server-side code.

## Available Models

| Model | Best For | Input | Cost | Speed |
|-------|----------|-------|------|-------|
| `seedance2` | Reference image and video, long duration | Text, Image, and/or Video | 36 credits/sec | Standard |
| `gen4.5` | High quality, general purpose | Text and/or Image | 12 credits/sec | Standard |
| `gen4_turbo` | Fast, image-driven | Image required | 5 credits/sec | Fast |
| `gen4_aleph` | Video editing/transformation | Video + Text/Image | 15 credits/sec | Standard |
| `veo3` | Premium Google model | Text/Image | 40 credits/sec | Standard |
| `veo3.1` | High quality Google model | Text/Image | 20-40 credits/sec | Standard |
| `veo3.1_fast` | Fast Google model | Text/Image | 10-15 credits/sec | Fast |

**Model selection guidance:**
- Default recommendation: **`gen4.5`** — best balance of quality and cost
- **Product ads / e-commerce:** **`seedance2`** — up to 15s, supports reference image and video
- Budget-conscious: **`gen4_turbo`** (requires image) or **`veo3.1_fast`**
- Highest quality: **`veo3`** (most expensive)
- Video-to-video editing: **`gen4_aleph`** or **`seedance2`**

## Security

`promptImage`, `promptVideo`, `videoUri`, and `references[].uri` are **fetched server-side by the Runway API** — treat them like any outbound fetch:

- **Prefer `runway://` URIs** from `+rw-integrate-uploads` — scoped to your account, no arbitrary web content.
- **If accepting URLs from clients**, validate first: require `https://`, allowlist trusted hosts, reject private addresses. See the Express.js example below.
- **Never forward `req.body.imageUrl`** (or similar) straight into `promptImage` / `promptVideo`. The SDK snippets below use raw URLs for brevity — they aren't production templates.
- Treat generated outputs as untrusted when piping into downstream automations — ingested media influences the result.

## Endpoints

### Text-to-Video: `POST /v1/text_to_video`

Generate video from a text prompt only.

**Compatible models:** `seedance2`, `gen4.5`, `veo3`, `veo3.1`, `veo3.1_fast`

```javascript
// Node.js SDK
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();

const task = await client.textToVideo.create({
  model: 'gen4.5',
  promptText: 'A golden retriever running through a field of wildflowers at sunset',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();

// task.output is an array of signed URLs
const videoUrl = task.output[0];
```

```python
# Python SDK
from runwayml import RunwayML

client = RunwayML()

task = client.text_to_video.create(
    model='gen4.5',
    prompt_text='A golden retriever running through a field of wildflowers at sunset',
    ratio='1280:720',
    duration=5
).wait_for_task_output()

video_url = task.output[0]
```

### Image-to-Video: `POST /v1/image_to_video`

Animate a still image into a video.

**Compatible models:** `seedance2`, `gen4.5`, `gen4_turbo`, `veo3`, `veo3.1`, `veo3.1_fast`

**Recommended:** upload via `+rw-integrate-uploads` and pass the returned `runway://` URI.

```javascript
// Node.js SDK — preferred flow
import fs from 'fs';

const upload = await client.uploads.createEphemeral(
  fs.createReadStream('/path/to/image.jpg')
);

const task = await client.imageToVideo.create({
  model: 'gen4.5',
  promptImage: upload.runwayUri,
  promptText: 'The scene comes to life with gentle wind',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();
```

External URLs also work — only pass origins you control (see Security):

```javascript
const task = await client.imageToVideo.create({
  model: 'gen4.5',
  promptImage: 'https://cdn.yourapp.com/landscape.jpg',
  promptText: 'Camera slowly pans right revealing a mountain range',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();
```

```python
# Python SDK
task = client.image_to_video.create(
    model='gen4.5',
    prompt_image='https://cdn.yourapp.com/landscape.jpg',
    prompt_text='Camera slowly pans right revealing a mountain range',
    ratio='1280:720',
    duration=5
).wait_for_task_output()
```

### Video-to-Video: `POST /v1/video_to_video`

Transform an existing video with a text prompt and/or reference image.

**Compatible models:** `gen4_aleph`, `seedance2`

```javascript
// Node.js SDK — gen4_aleph
const task = await client.videoToVideo.create({
  model: 'gen4_aleph',
  videoUri: 'https://cdn.yourapp.com/source.mp4',
  promptText: 'Transform into an animated cartoon style',
}).waitForTaskOutput();
```

```javascript
// Node.js SDK — seedance2 video-to-video (with optional image reference)
const task = await client.videoToVideo.create({
  model: 'seedance2',
  promptVideo: 'https://cdn.yourapp.com/input.mp4',
  promptText: 'Transform into a warm golden sunset scene',
  references: [{ type: 'image', uri: 'https://cdn.yourapp.com/style_ref.jpg' }]
}).waitForTaskOutput();
```

> **seedance2 VTV input requirements:** max 15 seconds, max 32 MB, min 720p resolution, MP4 recommended.

### Seedance 2

Seedance 2 supports text-to-video, image-to-video (two modes), and video-to-video. It uses pixel-based ratios: `1280:720`, `720:1280`, `960:960`, `1112:834`, `834:1112`, `1470:630`, `992:432`, `864:496`, `752:560`, `640:640`, `560:752`, `496:864`.

#### Text-to-Video

```javascript
const task = await client.textToVideo.create({
  model: 'seedance2',
  promptText: 'A calm ocean wave gently crashing on a sandy beach at sunset',
  duration: 5,
  ratio: '1280:720'
}).waitForTaskOutput();
```

#### Image-to-Video — Mode 1: First / Last Frame

Use a specific image as the first and/or last frame. The `references` field **cannot** be used in this mode.

```javascript
const task = await client.imageToVideo.create({
  model: 'seedance2',
  promptText: 'Smooth transition from day to night in a cozy mountain cabin',
  promptImage: [
    { uri: 'https://cdn.yourapp.com/image.jpg', position: 'first' },
    { uri: 'https://cdn.yourapp.com/image2.jpg', position: 'last' }
  ],
  duration: 4,
  ratio: '1280:720'
}).waitForTaskOutput();
```

`promptImage` is an array of objects with `uri` (required) and `position` (`"first"` or `"last"`, defaults to first).

#### Image-to-Video — Mode 2: Image Reference

Use an image as a stylistic/content reference rather than a literal frame. `promptImage` is still required (as a URI string or single-item array).

```javascript
const task = await client.imageToVideo.create({
  model: 'seedance2',
  promptText: 'Smooth transition from day to night in a cozy mountain cabin',
  promptImage: 'https://cdn.yourapp.com/image.jpg',
  references: [{ type: 'image', uri: 'https://cdn.yourapp.com/reference.jpg' }],
  duration: 4,
  ratio: '1280:720'
}).waitForTaskOutput();
```

> These two ITV modes are **mutually exclusive** — you cannot use `position` in `promptImage` and `references` in the same request.

#### Video-to-Video

Transform an existing video guided by a text prompt, optionally with an image reference.

```python
task = client.video_to_video.create(
    model='seedance2',
    prompt_video='https://cdn.yourapp.com/input.mp4',
    prompt_text='Transform into a warm golden sunset scene',
    references=[{'type': 'image', 'uri': 'https://cdn.yourapp.com/style_ref.jpg'}]
).wait_for_task_output()
```

> **VTV input requirements:** max 15 seconds, max 32 MB, min 720p resolution, MP4 recommended.

#### Seedance 2 Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Must be `"seedance2"` |
| `promptText` | string | Yes | Text description of the desired video |
| `duration` | number | Yes (TTV/ITV) | Duration in seconds |
| `ratio` | string | Yes (TTV/ITV) | `1280:720`, `720:1280`, `960:960`, `1112:834`, `834:1112`, `1470:630` |
| `promptImage` | string or array | Yes (ITV) | URI string or array of `{ uri, position? }` objects |
| `promptVideo` | string | Yes (seedance2 VTV) | Input video URI (seedance2 only) |
| `videoUri` | string | Yes (gen4_aleph VTV) | Input video URI (gen4_aleph only) |
| `references` | array | No | Image references — `[{ type: "image", uri: "..." }]` (ITV Mode 2 and VTV only) |

### Character Performance: `POST /v1/character_performance`

Animate a character with facial/body performance.

**Compatible models:** `act_two`

```javascript
const task = await client.characterPerformance.create({
  model: 'act_two',
  promptImage: 'https://cdn.yourapp.com/character.jpg',
  promptPerformance: 'https://cdn.yourapp.com/performance.mp4',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (required) |
| `promptText` | string | Text prompt describing the video |
| `promptImage` | string | URL, data URI, or `runway://` URI of input image |
| `ratio` | string | Aspect ratio, e.g. `'1280:720'`, `'720:1280'` |
| `duration` | number | Video length in seconds (2-15, model-dependent) |

## Integration Pattern

When helping the user integrate, follow this pattern:

1. **Determine the use case** — What type of video generation? (text-to-video, image-to-video, etc.)
2. **Prefer uploads over URLs** — Default to `+rw-integrate-uploads` so inputs are `runway://` URIs. External URLs only from origins you control (see Security).
3. **Select the model** — Recommend based on quality/cost/speed needs
4. **Write the server-side handler** — Create an API route or server function
5. **Handle the output** — Download and store the video, don't serve signed URLs to clients
6. **Add error handling** — Wrap in try/catch, handle `TaskFailedError`

### Example: Express.js API Route

```javascript
import RunwayML from '@runwayml/sdk';
import express from 'express';

const client = new RunwayML();
const app = express();
app.use(express.json());

// `runway://` URIs bypass this check; external URLs must match the allowlist.
const ALLOWED_MEDIA_HOSTS = new Set(['cdn.yourapp.com', 'uploads.yourapp.com']);

function assertTrustedMediaUrl(raw) {
  const u = new URL(raw);
  if (u.protocol !== 'https:') throw new Error('https required');
  if (!ALLOWED_MEDIA_HOSTS.has(u.hostname)) throw new Error('untrusted media host');
  return u.toString();
}

app.post('/api/generate-video', async (req, res) => {
  try {
    const { prompt, imageUrl, model = 'gen4.5', duration = 5 } = req.body;

    const params = {
      model,
      promptText: prompt,
      ratio: '1280:720',
      duration
    };

    let task;
    if (imageUrl) {
      task = await client.imageToVideo.create({
        ...params,
        promptImage: assertTrustedMediaUrl(imageUrl)
      }).waitForTaskOutput();
    } else {
      task = await client.textToVideo.create(params).waitForTaskOutput();
    }

    res.json({ videoUrl: task.output[0] });
  } catch (error) {
    console.error('Video generation failed:', error);
    res.status(400).json({ error: error.message });
  }
});
```

> For browser uploads: POST files to your server, upload via `+rw-integrate-uploads`, and pass the `runway://` URI. Don't accept raw URLs from the browser.

### Example: Next.js API Route

```typescript
// app/api/generate-video/route.ts
import RunwayML from '@runwayml/sdk';
import { NextRequest, NextResponse } from 'next/server';

const client = new RunwayML();

export async function POST(request: NextRequest) {
  const { prompt, imageUrl } = await request.json();

  try {
    const task = imageUrl
      ? await client.imageToVideo.create({
          model: 'gen4.5',
          promptImage: imageUrl,
          promptText: prompt,
          ratio: '1280:720',
          duration: 5
        }).waitForTaskOutput()
      : await client.textToVideo.create({
          model: 'gen4.5',
          promptText: prompt,
          ratio: '1280:720',
          duration: 5
        }).waitForTaskOutput();

    return NextResponse.json({ videoUrl: task.output[0] });
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

class VideoRequest(BaseModel):
    prompt: str
    image_url: str | None = None
    model: str = "gen4.5"
    duration: int = 5

@app.post("/api/generate-video")
async def generate_video(req: VideoRequest):
    try:
        if req.image_url:
            task = client.image_to_video.create(
                model=req.model,
                prompt_image=req.image_url,
                prompt_text=req.prompt,
                ratio="1280:720",
                duration=req.duration
            ).wait_for_task_output()
        else:
            task = client.text_to_video.create(
                model=req.model,
                prompt_text=req.prompt,
                ratio="1280:720",
                duration=req.duration
            ).wait_for_task_output()

        return {"video_url": task.output[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Tips

- **Output URLs expire in 24-48 hours.** Download videos to your own storage (S3, GCS, local filesystem) immediately after generation.
- **`gen4_turbo` requires an image** — it cannot do text-only generation.
- **Video-to-video models:** `gen4_aleph` and `seedance2` — use for editing/transforming existing videos.
- **Duration varies by model.** Most models support 2-10 seconds; seedance2 supports up to 15 seconds.
- **`waitForTaskOutput()` has a default 10-minute timeout.** For long-running generations, you may want to implement your own polling loop or increase the timeout.
- **For local files**, always use `+rw-integrate-uploads` to upload first, then pass the `runway://` URI.
