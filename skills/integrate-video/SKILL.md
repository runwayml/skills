---
name: integrate-video
description: "Help users integrate Runway video generation APIs (text-to-video, image-to-video, video-to-video)"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Integrate Video Generation

> **PREREQUISITE:** Run `+check-compatibility` first. Run `+fetch-api-reference` to load the latest API reference before integrating. Requires `+setup-api-key` for API credentials. Requires `+integrate-uploads` when the user has local files to use as input.

Help users add Runway video generation to their server-side code.

## Available Models

| Model | Best For | Input | Cost | Speed |
|-------|----------|-------|------|-------|
| `gen4.5` | Highest quality, general purpose | Text and/or Image | 12 credits/sec | Standard |
| `gen4_turbo` | Fast, image-driven | Image required | 5 credits/sec | Fast |
| `gen4_aleph` | Video editing/transformation | Video + Text/Image | 15 credits/sec | Standard |
| `veo3` | Premium Google model | Text/Image | 40 credits/sec | Standard |
| `veo3.1` | High quality Google model | Text/Image | 20-40 credits/sec | Standard |
| `veo3.1_fast` | Fast Google model | Text/Image | 10-15 credits/sec | Fast |

**Model selection guidance:**
- Default recommendation: **`gen4.5`** — best balance of quality and cost
- Budget-conscious: **`gen4_turbo`** (requires image) or **`veo3.1_fast`**
- Highest quality: **`veo3`** (most expensive)
- Video-to-video editing: **`gen4_aleph`** (only option)

## Endpoints

### Text-to-Video: `POST /v1/text_to_video`

Generate video from a text prompt only.

**Compatible models:** `gen4.5`, `veo3`, `veo3.1`, `veo3.1_fast`

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

**Compatible models:** `gen4.5`, `gen4_turbo`, `veo3`, `veo3.1`, `veo3.1_fast`

```javascript
// Node.js SDK
const task = await client.imageToVideo.create({
  model: 'gen4.5',
  promptImage: 'https://example.com/landscape.jpg',
  promptText: 'Camera slowly pans right revealing a mountain range',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();
```

```python
# Python SDK
task = client.image_to_video.create(
    model='gen4.5',
    prompt_image='https://example.com/landscape.jpg',
    prompt_text='Camera slowly pans right revealing a mountain range',
    ratio='1280:720',
    duration=5
).wait_for_task_output()
```

**If the user has a local image file**, use `+integrate-uploads` first to upload it:

```javascript
// Upload local file first
import fs from 'fs';

const upload = await client.uploads.createEphemeral(
  fs.createReadStream('/path/to/image.jpg')
);

const task = await client.imageToVideo.create({
  model: 'gen4.5',
  promptImage: upload.runwayUri,  // Use the runway:// URI
  promptText: 'The scene comes to life with gentle wind',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();
```

### Video-to-Video: `POST /v1/video_to_video`

Transform an existing video with a text prompt and/or reference image.

**Compatible models:** `gen4_aleph`

```javascript
// Node.js SDK
const task = await client.videoToVideo.create({
  model: 'gen4_aleph',
  promptVideo: 'https://example.com/source.mp4',
  promptText: 'Transform into an animated cartoon style',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();
```

### Character Performance: `POST /v1/character_performance`

Animate a character with facial/body performance.

**Compatible models:** `act_two`

```javascript
const task = await client.characterPerformance.create({
  model: 'act_two',
  promptImage: 'https://example.com/character.jpg',
  promptPerformance: 'https://example.com/performance.mp4',
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
| `duration` | number | Video length in seconds (2-10) |

## Integration Pattern

When helping the user integrate, follow this pattern:

1. **Determine the use case** — What type of video generation? (text-to-video, image-to-video, etc.)
2. **Check for local files** — If the user has local images/videos, use `+integrate-uploads` first
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
        promptImage: imageUrl
      }).waitForTaskOutput();
    } else {
      task = await client.textToVideo.create(params).waitForTaskOutput();
    }

    res.json({ videoUrl: task.output[0] });
  } catch (error) {
    console.error('Video generation failed:', error);
    res.status(500).json({ error: error.message });
  }
});
```

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
- **`gen4_aleph` is the only video-to-video model** — use it for editing/transforming existing videos.
- **Duration range is 2-10 seconds.** Longer videos require chaining multiple generations.
- **`waitForTaskOutput()` has a default 10-minute timeout.** For long-running generations, you may want to implement your own polling loop or increase the timeout.
- **For local files**, always use `+integrate-uploads` to upload first, then pass the `runway://` URI.
