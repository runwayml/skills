---
name: rw-api-reference
description: "Complete reference for Runway's public API: models, endpoints, costs, limits, and types"
user-invocable: false
---

# Runway Public API Reference

> **PREREQUISITE:** Run `+rw-check-compatibility` first to ensure the project has server-side capability.

Base URL: `https://api.dev.runwayml.com`

All requests require these headers:
```
Authorization: Bearer <RUNWAYML_API_SECRET>
X-Runway-Version: 2024-11-06
```

---

## Models & Endpoints

### Video Generation

| Model | Endpoint | Input | Cost (credits/sec) |
|-------|----------|-------|---------------------|
| `gen4.5` | `POST /v1/image_to_video` or `POST /v1/text_to_video` | Text and/or Image | 12 |
| `gen4_turbo` | `POST /v1/image_to_video` | Image required | 5 |
| `gen4_aleph` | `POST /v1/video_to_video` | Video + Text/Image | 15 |
| `act_two` | `POST /v1/character_performance` | Image/Video | 5 |
| `veo3` | `POST /v1/image_to_video` or `POST /v1/text_to_video` | Text/Image | 40 |
| `veo3.1` | `POST /v1/image_to_video` or `POST /v1/text_to_video` | Text/Image | 20-40 |
| `veo3.1_fast` | `POST /v1/image_to_video` or `POST /v1/text_to_video` | Text/Image | 10-15 |
| `seedance2` | `POST /v1/text_to_video`, `POST /v1/image_to_video`, or `POST /v1/video_to_video` | Text, Image, and/or Video | 36 |

Video duration: **2-15 seconds** (model-dependent). Aspect ratios are pixel-based: `1280:720`, `720:1280`, `1104:832`, `960:960`, `832:1104`, `1584:672`, etc.

**Seedance 2 specifics:**
- Modes: text-to-video, image-to-video (first/last frame or image reference), video-to-video
- Duration: required for TTV and ITV (in seconds)
- Aspect ratios (pixel-based): `1280:720`, `720:1280`, `960:960`, `1112:834`, `834:1112`, `1470:630`, `992:432`, `864:496`, `752:560`, `640:640`, `560:752`, `496:864`
- ITV supports two mutually exclusive modes: first/last frame (`promptImage` array with `position`) or image reference (`references` array)
- VTV input requirements: max 15 seconds, max 32 MB, min 720p resolution, MP4 recommended

### Image Generation

| Model | Endpoint | Cost (credits) |
|-------|----------|----------------|
| `gen4_image` | `POST /v1/text_to_image` | 5 (720p), 8 (1080p) |
| `gen4_image_turbo` | `POST /v1/text_to_image` | 2 |
| `gemini_2.5_flash` | `POST /v1/text_to_image` | 5 |

### Audio Generation

| Model | Endpoint | Use Case | Cost |
|-------|----------|----------|------|
| `eleven_multilingual_v2` | `POST /v1/text_to_speech` | Text to speech | 1 credit/50 chars |
| `eleven_text_to_sound_v2` | `POST /v1/sound_effect` | Sound effects | 1-2 credits |
| `eleven_voice_isolation` | `POST /v1/voice_isolation` | Isolate voice from audio | 1 credit/6 sec |
| `eleven_voice_dubbing` | `POST /v1/voice_dubbing` | Dub audio to other languages | 1 credit/2 sec |
| `eleven_multilingual_sts_v2` | `POST /v1/speech_to_speech` | Voice conversion | 1 credit/3 sec |

### Characters (Real-Time Avatars)

| Model | Description | Session Max Duration |
|-------|-------------|----------------------|
| `gwm1_avatars` | Real-time conversational avatars powered by GWM-1 | 5 minutes |

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/avatars` | Create a new Avatar |
| `GET` | `/v1/avatars/{id}` | Retrieve an Avatar |
| `PATCH` | `/v1/avatars/{id}` | Update an Avatar (name, voice, personality, documentIds) |
| `DELETE` | `/v1/avatars/{id}` | Delete an Avatar |
| `POST` | `/v1/realtime_sessions` | Create a new real-time session |
| `GET` | `/v1/realtime_sessions/{id}` | Retrieve session status (poll until `READY`) |
| `POST` | `/v1/realtime_sessions/{id}/consume` | Consume session credentials for WebRTC (one-time use) |

**Avatar creation parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Display name for the avatar |
| `referenceImage` | string | URL or `runway://` URI of the character image |
| `voice` | object | `{ type: 'runway-live-preset', presetId: 'clara' }` |
| `personality` | string | System prompt / personality instructions |
| `documentIds` | string[] | Optional. IDs of knowledge base documents to attach |

**Voice presets:** `clara` (soft), `victoria` (firm), `vincent` (authoritative). Preview all at [dev.runwayml.com](https://dev.runwayml.com/).

**Session statuses:** `NOT_READY` → `READY` → `RUNNING` → `COMPLETED` (or `FAILED` / `CANCELLED`)

### Documents (Knowledge Base)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/documents` | Create a document (plain text or Markdown) |
| `GET` | `/v1/documents/{id}` | Retrieve a document |
| `DELETE` | `/v1/documents/{id}` | Delete a document |

Each Avatar supports up to **50,000 tokens** of knowledge. Link documents to an Avatar via `client.avatars.update(id, { documentIds: [...] })`.

---

## Request Body Reference (raw JSON)

Use these when calling the API directly (e.g. through `use-runway-api`'s `request` command) rather than via an SDK. Only required + common fields shown — consult `+rw-fetch-api-reference` for the full schema.

### `POST /v1/text_to_image`

```json
{
  "model": "gen4_image",
  "promptText": "A serene Japanese garden with cherry blossoms",
  "ratio": "1920:1080"
}
```

- `model`: `gen4_image` | `gen4_image_turbo` | `gemini_2.5_flash` (required)
- `promptText`: string, up to ~1000 chars (required)
- `ratio`: one of `1920:1080`, `1080:1920`, `1024:1024`, `1360:768`, `1080:1080`, `1168:880`, `1440:1080`, `1080:1440`, `1808:768`, `2112:912` (required; 720p or 1080p variants depending on model)
- `referenceImages`: optional `[{ "uri": "https://...", "tag": "MyTag" }]` — reference by `@MyTag` in `promptText`
- `seed`: optional integer for reproducibility

### `POST /v1/text_to_video`

```json
{
  "model": "gen4.5",
  "promptText": "A golden retriever running through wildflowers at sunset",
  "ratio": "1280:720",
  "duration": 5
}
```

- `model`: `gen4.5` | `veo3` | `veo3.1` | `veo3.1_fast` | `seedance2` (required)
- `duration`: integer seconds, 2–10 (required; model-specific valid values — e.g. veo3 only accepts 8)
- `ratio`: e.g. `1280:720`, `720:1280`, `1104:832`, `832:1104`, `960:960` (required)

### `POST /v1/image_to_video`

```json
{
  "model": "gen4.5",
  "promptImage": "https://example.com/cover.jpg",
  "promptText": "A slow dolly-in shot",
  "ratio": "1280:720",
  "duration": 5
}
```

- `model`: `gen4.5` | `gen4_turbo` | `veo3` | `veo3.1` | `veo3.1_fast` | `seedance2` (required)
- `promptImage`: HTTPS URL, data URI, or `runway://` URI (required). Can also be `[{ "uri": "...", "position": "first" | "last" }]` for keyframes.
- `promptText`: optional for most models, required for `gen4_turbo` when no image motion is obvious

### `POST /v1/video_to_video`

```json
{
  "model": "gen4_aleph",
  "videoUri": "https://example.com/source.mp4",
  "promptText": "Change the season to winter with snowfall",
  "ratio": "1280:720"
}
```

### `POST /v1/text_to_speech`

```json
{
  "model": "eleven_multilingual_v2",
  "text": "Hello, welcome to Runway.",
  "voice": { "type": "runway-preset", "presetId": "clara" }
}
```

- `voice`: `{ type: "runway-preset", presetId: "clara" | "victoria" | "vincent" | ... }` or a provider-specific voice object
- `languageCode`: optional ISO code (auto-detected by default)

### `POST /v1/sound_effect`

```json
{
  "model": "eleven_text_to_sound_v2",
  "promptText": "Thunderclap followed by heavy rain",
  "duration": 5
}
```

### `POST /v1/voice_isolation`

```json
{
  "model": "eleven_voice_isolation",
  "audioUri": "https://example.com/noisy.mp3"
}
```

### `POST /v1/voice_dubbing`

```json
{
  "model": "eleven_voice_dubbing",
  "audioUri": "https://example.com/english.mp3",
  "targetLanguage": "es"
}
```

### `POST /v1/speech_to_speech`

```json
{
  "model": "eleven_multilingual_sts_v2",
  "audioUri": "https://example.com/source.mp3",
  "voice": { "type": "runway-preset", "presetId": "victoria" }
}
```

### `POST /v1/avatars`

```json
{
  "name": "Support Agent",
  "referenceImage": "https://example.com/portrait.jpg",
  "voice": { "type": "runway-live-preset", "presetId": "clara" },
  "personality": "You are a friendly support agent.",
  "documentIds": []
}
```

### `POST /v1/documents`

```json
{
  "avatarId": "<avatar-id>",
  "name": "FAQ",
  "content": "Q: What is your return policy?\nA: 30 days, no questions asked."
}
```

### `POST /v1/realtime_sessions`

```json
{
  "avatarId": "<avatar-id>"
}
```

---

### Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/tasks/{id}` | Get task status and output |
| `DELETE` | `/v1/tasks/{id}` | Cancel/delete a task |
| `POST` | `/v1/uploads` | Create ephemeral upload |
| `GET` | `/v1/organization` | Organization info & credit balance |
| `POST` | `/v1/organization/usage` | Credit usage history (up to 90 days) |

---

## Task Lifecycle

All generation endpoints return a task object. The flow is:

1. **Submit** — `POST /v1/<endpoint>` → returns `{ "id": "task_xxx" }`
2. **Poll** — `GET /v1/tasks/{id}` → returns task with `status`
3. **Retrieve output** — When `status === "SUCCEEDED"`, the `output` array contains signed URLs

### Task Statuses

| Status | Meaning |
|--------|---------|
| `PENDING` | Queued, waiting to start |
| `RUNNING` | Currently generating |
| `SUCCEEDED` | Complete — output URLs available |
| `FAILED` | Generation failed — check `failure` field |
| `THROTTLED` | Concurrency limit hit — auto-queued |

### SDK Polling (Recommended)

The SDKs provide a `waitForTaskOutput()` method that handles polling automatically:

```javascript
// Node.js — polls until complete (default 10 min timeout)
const task = await client.imageToVideo.create({
  model: 'gen4.5',
  promptImage: 'https://example.com/image.jpg',
  promptText: 'A sunset timelapse',
  ratio: '1280:720',
  duration: 5
}).waitForTaskOutput();

console.log(task.output); // Array of signed URLs
```

```python
# Python
task = client.image_to_video.create(
    model='gen4.5',
    prompt_image='https://example.com/image.jpg',
    prompt_text='A sunset timelapse',
    ratio='1280:720',
    duration=5
).wait_for_task_output()

print(task.output)
```

### Manual Polling (REST)

```javascript
async function pollTask(taskId) {
  while (true) {
    const response = await fetch(`https://api.dev.runwayml.com/v1/tasks/${taskId}`, {
      headers: {
        'Authorization': `Bearer ${process.env.RUNWAYML_API_SECRET}`,
        'X-Runway-Version': '2024-11-06'
      }
    });
    const task = await response.json();

    if (task.status === 'SUCCEEDED') return task;
    if (task.status === 'FAILED') throw new Error(task.failure);

    await new Promise(r => setTimeout(r, 5000)); // poll every 5 seconds
  }
}
```

---

## Output Handling

- Successful tasks return an `output` array with **signed URLs** to generated content
- Output URLs **expire within 24-48 hours**
- **Download and store outputs** in your own storage — do not serve signed URLs to end users
- Video outputs are MP4, image outputs are PNG/JPEG

---

## Input Requirements

### Size Limits

| Type | Via URL | Via Data URI | Via Upload |
|------|---------|-------------|------------|
| Image | 16 MB | 5 MB | 200 MB |
| Video | 32 MB | 16 MB | 200 MB |
| Audio | 32 MB | 16 MB | 200 MB |

### Supported Formats

- **Images:** JPEG, PNG, WebP (no GIF)
- **Video codecs:** H.264, H.265/HEVC, AV1, VP8/VP9, Apple ProRes, Theora
- **Audio:** MP3, AAC, FLAC, PCM, ALAC

### URL Requirements

If providing assets via URL:
- HTTPS only (no HTTP)
- Domain names only (no IP addresses)
- No redirects
- Must support HTTP HEAD requests
- Must return valid `Content-Type` and `Content-Length` headers
- Max URL length: 2,048 characters

---

## Rate Limits & Tiers

| Tier | Concurrency | Daily Gens | Monthly Cap | Unlock |
|------|-------------|------------|-------------|--------|
| 1 (default) | 1-2 | 50-200 | $100 | — |
| 2 | 3 | 500-1,000 | $500 | 1 day + $50 |
| 3 | 5 | 1,000-2,000 | $2,000 | 7 days + $100 |
| 4 | 10 | 5,000-10,000 | $20,000 | 14 days + $1,000 |
| 5 | 20 | 25,000-30,000 | $100,000 | 7 days + $5,000 |

- No requests-per-minute limit — only daily generation quotas
- Exceeding concurrency → `THROTTLED` status (auto-queued, not rejected)
- Exceeding daily limit → `429 Too Many Requests`
- Daily limits use a **rolling 24-hour window**

---

## Error Handling

### HTTP Errors

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Input validation failure | Fix input, do not retry |
| 401 | Invalid API key | Check key, do not retry |
| 429 | Rate limited | Retry with exponential backoff + jitter |
| 502/503/504 | Server overload | Retry with exponential backoff + jitter |

### Task Failure Codes

| Code | Meaning | Retry? |
|------|---------|--------|
| `SAFETY.INPUT.*` | Input content moderation | No — not refundable |
| `SAFETY.OUTPUT.*` | Output content moderation | Yes — try different prompt |
| `INTERNAL.BAD_OUTPUT` | Quality issue | Yes |
| `ASSET.INVALID` | Bad input format | Fix input |
| `INTERNAL` | Server error | Yes |

The SDKs handle retries for transient errors automatically.

---

## Data URI Support

Base64-encoded images can be passed instead of URLs:

```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
```

Useful for small images or when you don't want to host the file. Subject to the data URI size limits above.
