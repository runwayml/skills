---
name: runwayml
description: Generate AI videos, images, and audio with Runway API. Use when generating video from images, text-to-video, video-to-video, character performance, text-to-image, text-to-speech, sound effects, or voice processing with Runway.
license: MIT
compatibility: Requires internet access and a RunwayML API key (RUNWAYML_API_SECRET).
metadata:
  author: RunwayML
  version: 1.0.0
---

# Runway API

Generate AI videos, images, and audio using Runway's API. Features Runway's **latest Gen-4.5 model** for high-quality text-to-video and image-to-video generation, plus Gen-4 variants and third-party models from Google (Veo, Gemini) and ElevenLabs.

> **Recommended:** Use **`gen4.5`** for best results - the newest and most capable video generation model.

> **Setup:** See [Installation Guide](references/installation.md). API key goes in `RUNWAYML_API_SECRET` env var.

## Quick Start

### Python

```python
from runwayml import RunwayML

client = RunwayML()

# Image-to-video with latest Gen-4.5 model
task = client.image_to_video.create(
    model="gen4.5",
    prompt_image="https://example.com/image.jpg",
    prompt_text="A timelapse on a sunny day with clouds flying by",
    ratio="1280:720",
    duration=10
).wait_for_task_output()

print(f"Video URL: {task.output[0]}")

# Text-to-video (no image required)
task = client.image_to_video.create(
    model="gen4.5",
    prompt_text="A serene mountain landscape at sunset with clouds drifting",
    ratio="1280:720",
    duration=10
).wait_for_task_output()
```

### Node.js

```javascript
import RunwayML from "@runwayml/sdk";

const client = new RunwayML();

// Image-to-video with latest Gen-4.5 model
const task = await client.imageToVideo
  .create({
    model: "gen4.5",
    promptImage: "https://example.com/image.jpg",
    promptText: "A timelapse on a sunny day with clouds flying by",
    ratio: "1280:720",
    duration: 10,
  })
  .waitForTaskOutput();

console.log(`Video URL: ${task.output[0]}`);

// Text-to-video (no image required)
const textTask = await client.imageToVideo
  .create({
    model: "gen4.5",
    promptText: "A serene mountain landscape at sunset",
    ratio: "1280:720",
    duration: 10,
  })
  .waitForTaskOutput();
```

### cURL

```bash
# Image-to-video
curl -X POST "https://api.dev.runwayml.com/v1/image_to_video" \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gen4.5",
    "promptImage": "https://example.com/image.jpg",
    "promptText": "A timelapse on a sunny day",
    "ratio": "1280:720",
    "duration": 10
  }'

# Text-to-video (no image required)
curl -X POST "https://api.dev.runwayml.com/v1/image_to_video" \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gen4.5",
    "promptText": "A serene mountain landscape at sunset",
    "ratio": "1280:720",
    "duration": 10
  }'

# Poll for result (use returned task id)
curl "https://api.dev.runwayml.com/v1/tasks/{task_id}" \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06"
```

---

## All Available Models

### Video Generation

| Model | Input | Pricing | Use Case |
|-------|-------|---------|----------|
| **`gen4.5`** ⭐ | Text or Image | 12 credits/sec | **Newest & recommended** - Best quality text/image-to-video (no audio) |
| `gen4_turbo` | Image | 5 credits/sec | Fast image-to-video (no audio), iteration |
| `gen4_aleph` | Video + Text/Image | 15 credits/sec | Video-to-video transformation (no audio) |
| `act_two` | Image or Video | 5 credits/sec | Character performance/motion (no audio) |
| `veo3` | Text or Image | 40 credits/sec | Google Veo high-quality video **with audio** |
| `veo3.1` | Text or Image | 40 credits/sec | Google Veo 3.1 with keyframes **& audio** |
| `veo3.1_fast` | Text or Image | 15 credits/sec | Google Veo 3.1 faster/cheaper **& audio** |

### Image Generation

| Model | Input | Pricing | Use Case |
|-------|-------|---------|----------|
| `gen4_image` | Text + References (optional) | 5 credits/720p, 8 credits/1080p | High-quality with style transfer |
| `gen4_image_turbo` | Text + References (required) | 2 credits/image (any res) | Fast iteration |
| `gemini_2.5_flash` | Text + References | 5 credits/image | Google Gemini image gen |

### Audio Generation (ElevenLabs)

| Model | Input → Output | Pricing |
|-------|----------------|---------|
| `eleven_multilingual_v2` | Text → Speech | 1 credit/50 chars |
| `eleven_text_to_sound_v2` | Text → Sound Effects | 1 credit/6 sec |
| `eleven_voice_isolation` | Audio → Clean Audio | 1 credit/6 sec |
| `eleven_voice_dubbing` | Audio → Dubbed Audio | 1 credit/2 sec |
| `eleven_multilingual_sts_v2` | Speech → Speech | 1 credit/2 sec |

> 1 credit = $0.01. Get credits at [dev.runwayml.com](https://dev.runwayml.com)

---

## Video Generation

### Gen-4.5 (Text-to-Video and Image-to-Video)

**The latest and most capable Runway model** supporting both text-only and image-to-video generation.

#### Text-to-Video

Generate videos from text descriptions only:

```python
task = client.image_to_video.create(
    model="gen4.5",
    prompt_text="A serene mountain lake at sunrise with mist rising from the water",
    ratio="1280:720",
    duration=10,
    seed=12345  # Optional: reproducibility
).wait_for_task_output()
```

**Text-to-Video Aspect Ratios:** Landscape `1280:720` (16:9) | Portrait `720:1280` (9:16)

#### Image-to-Video

Animate existing images with motion:

```python
task = client.image_to_video.create(
    model="gen4.5",
    prompt_image="https://example.com/image.jpg",
    prompt_text="Camera slowly pushes in, leaves rustling in the breeze",
    ratio="1584:672",
    duration=10,
    seed=12345
).wait_for_task_output()
```

**Image-to-Video Aspect Ratios:**
- Widescreen: `1280:720` (16:9), `1584:672` (21:9 ultra-wide)
- Standard: `1104:832` (4:3)
- Portrait: `720:1280` (9:16), `832:1104` (3:4)

**Duration:** 2-10 seconds | **Pricing:** 12 credits/second (60 credits minimum for 5 sec)

### Gen-4 Turbo (Image-to-Video)

```python
task = client.image_to_video.create(
    model="gen4_turbo",
    prompt_image="https://example.com/image.jpg",
    prompt_text="Camera slowly pushes in, leaves rustling",
    ratio="1280:720",
    duration=5,
    seed=12345           # Optional: reproducibility
).wait_for_task_output()
```

**Aspect Ratios:** Landscape `1280:720`, `1584:672`, `1104:832` | Portrait `720:1280`, `832:1104` | Square `960:960`

### Aleph (Video-to-Video)

Transform existing videos with text/image guidance:

```python
task = client.video_to_video.create(
    model="gen4_aleph",
    video_uri="https://example.com/source.mp4",
    prompt_text="Transform to anime style",
    references=[{"uri": "https://example.com/style_ref.jpg"}]  # Optional style reference
).wait_for_task_output()
```

**Aspect Ratios:** Adds `848:480` (landscape) and `480:848` (portrait) to Gen-4 options.

### Act-Two (Character Performance)

Drive character motion from reference performance. Objects require `type` discriminators:

```python
task = client.character_performance.create(
    model="act_two",
    character={"type": "image", "uri": "https://example.com/character.jpg"},  # or type: "video"
    reference={"type": "video", "uri": "https://example.com/performance.mp4"}
).wait_for_task_output()
```

**Character types:** `image` (character performs in static environment) or `video` (character performs with some of its own movement)

### Veo (Google)

Google's Veo models for text-to-video and image-to-video. **Veo models include audio generation** - making them ideal when you need video with sound.

```python
# Text-to-video with audio (no image required)
task = client.image_to_video.create(
    model="veo3.1",  # or "veo3", "veo3.1_fast"
    prompt_text="A cinematic shot of a rocket launching at sunset with roaring engines"
).wait_for_task_output()

# Image-to-video with audio
task = client.image_to_video.create(
    model="veo3.1",
    prompt_image="https://example.com/starting_frame.jpg",
    prompt_text="Smooth camera movement through the scene with ambient nature sounds"
).wait_for_task_output()
```

> **Note:** Gen-4.5 and Gen-4 models produce silent video. Use Veo if you need audio, or add audio separately with ElevenLabs models (see Audio Generation section).

---

## Image Generation

### Gen-4 Image with References

Use reference images with @mention syntax in prompts:

```python
# gen4_image - reference_images is optional
task = client.text_to_image.create(
    model="gen4_image",
    ratio="1920:1080",
    prompt_text="A beautiful mountain landscape at sunset"
).wait_for_task_output()

# With references
task = client.text_to_image.create(
    model="gen4_image",
    ratio="1920:1080",
    prompt_text="@EiffelTower painted in the style of @StarryNight",
    reference_images=[
        {"uri": "https://example.com/eiffel.jpg", "tag": "EiffelTower"},
        {"uri": "https://example.com/starry.jpg", "tag": "StarryNight"}
    ]
).wait_for_task_output()
```

**Note:** `gen4_image_turbo` requires `reference_images` (at least one). Use `gen4_image` for text-only generation.

Untagged references apply as general style:

```python
reference_images=[
    {"uri": "https://example.com/subject.jpg", "tag": "subject"},
    {"uri": "https://example.com/style.jpg"}  # No tag = style reference
]
```

---

## Audio Generation

ElevenLabs models for text-to-speech, sound effects, and voice processing.

**Voice Presets:** `Maya`, `Arjun`, `Serene`, `Bernard`, `Billy`, `Mark`, `Clint`, `Mabel`, `Chad`, `Leslie`, `Eleanor`, `Elias`, `Elliot`, `Noah`, `Rachel`, `James`, `Katie`, `Tom`, `Wanda`, `Benjamin`

### Text-to-Speech

```python
task = client.text_to_speech.create(
    model="eleven_multilingual_v2",
    prompt_text="Hello, welcome to RunwayML!",
    voice={"type": "runway-preset", "preset_id": "Maya"}
).wait_for_task_output()
```

### Sound Effects

```python
task = client.sound_effect.create(
    model="eleven_text_to_sound_v2",
    prompt_text="Thunder rumbling in the distance, rain on a window"
).wait_for_task_output()
```

### Voice Isolation

```python
task = client.voice_isolation.create(
    model="eleven_voice_isolation",
    audio_uri="https://example.com/noisy_audio.mp3"
).wait_for_task_output()
```

### Voice Dubbing

```python
task = client.voice_dubbing.create(
    model="eleven_voice_dubbing",
    audio_uri="https://example.com/speech.mp3",
    target_lang="es"  # Spanish
).wait_for_task_output()
```

**Supported languages:** `en`, `hi`, `pt`, `zh`, `es`, `fr`, `de`, `ja`, `ar`, `ru`, `ko`, `id`, `it`, `nl`, `tr`, `pl`, `sv`, `fil`, `ms`, `ro`, `uk`, `el`, `cs`, `da`, `fi`, `bg`, `hr`, `sk`, `ta`

### Speech-to-Speech

Convert speech to a different voice. Requires `type` discriminators:

```python
task = client.speech_to_speech.create(
    model="eleven_multilingual_sts_v2",
    media={"type": "audio", "uri": "https://example.com/original.mp3"},  # or type: "video"
    voice={"type": "runway-preset", "preset_id": "Maya"}
).wait_for_task_output()
```

---

## Input Requirements

### Size Limits

| Type | URL Limit | Data URI Limit | Ephemeral Upload |
|------|-----------|----------------|------------------|
| Image | 16MB | 5MB (3.3MB pre-encoding) | 200MB |
| Video | 32MB | 16MB | 200MB |
| Audio | 32MB | 16MB | 200MB |

### Supported Formats

**Images:** JPEG, PNG, WebP (no GIF)

**Videos:** MP4 (H.264/H.265/AV1), MOV (ProRes), MKV, WebM

**Audio:** MP3, WAV, FLAC, M4A, AAC

### Base64 Data URIs

```python
import base64

with open("image.jpg", "rb") as f:
    data_uri = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"

task = client.image_to_video.create(
    model="gen4_turbo",
    prompt_image=data_uri,
    prompt_text="Gentle movement"
).wait_for_task_output()
```

---

## Task Management

All operations are async. Use `wait_for_task_output()` (polls automatically, 10 min timeout).

**Statuses:** `PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED` / `CANCELED`

`THROTTLED` = rate-limited, treat as `PENDING`

### Canceling/Deleting Tasks

```python
# Cancel running task or delete completed task
client.tasks.delete(task.id)
```

See [Task Management](references/task-management.md) for manual polling and batch processing.

---

## Prompting Tips

**Gen-4 thrives on simplicity.** Start simple, iterate.

- Describe single scenes (5-10 sec clips)
- Use clear physical descriptions, not conceptual language
- Reference subjects generically: "the subject", "she"
- **Avoid negative phrasing** - "no blur" produces unpredictable results

See [Prompting Guide](references/prompting.md) for camera movements and advanced techniques.

---

## Error Handling

```python
from runwayml import RunwayML, APIError, RateLimitError

client = RunwayML()

try:
    task = client.image_to_video.create(...).wait_for_task_output()
    if task.status == "FAILED":
        print(f"Generation failed: {task.failure}")
except RateLimitError:
    print("Rate limited - SDK retries automatically")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Invalid input | Fix request parameters |
| 401 | Invalid API key | Check RUNWAYML_API_SECRET |
| 429 | Rate limit | SDKs auto-retry with backoff |
| 503 | Service unavailable | SDKs auto-retry |

---

## Parameters Quick Reference

### Video (gen4.5)

| Parameter | Type | Options |
|-----------|------|---------|
| `model` | string | `"gen4.5"`, `"gen4_turbo"`, `"veo3"`, `"veo3.1"` |
| `duration` | number | `2` to `10` (seconds) |
| `ratio` | string | Text-to-video: `"1280:720"` (16:9), `"720:1280"` (9:16)<br>Image-to-video adds: `"1584:672"` (21:9), `"1104:832"` (4:3), `"832:1104"` (3:4) |
| `prompt_text` | string | Motion/scene description (required) |
| `prompt_image` | string | URL or base64 (optional for text-to-video, required for image-to-video) |
| `seed` | number | Optional, for reproducibility |

### Image (gen4_image)

| Parameter | Type | Options |
|-----------|------|---------|
| `model` | string | `"gen4_image"`, `"gen4_image_turbo"` |
| `ratio` | string | `"1920:1080"`, `"1280:720"`, etc. |
| `prompt_text` | string | Image description |
| `reference_images` | array | `[{"uri": "...", "tag": "..."}]` |

---

## References

- [Installation Guide](references/installation.md) - SDK setup
- [Prompting Guide](references/prompting.md) - Advanced prompting
- [Task Management](references/task-management.md) - Polling, batching

## Official Documentation

- [Runway API Documentation](https://docs.dev.runwayml.com/) - Complete API reference
- [Model Guide](https://docs.dev.runwayml.com/guides/models/) - All available models
- [Developer Portal](https://dev.runwayml.com/) - API keys and account management
