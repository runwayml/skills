---
name: runway-cli
description: Generate AI videos, images, and audio from the command line with Runway CLI. Use when generating video from images, text-to-video, text-to-image, text-to-speech, sound effects, or voice processing via terminal commands, shell scripts, or CI/CD pipelines.
license: Apache-2.0
compatibility: Requires internet access and a RunwayML API key.
metadata:
  author: RunwayML
  version: 1.0.0
---

# Runway CLI

Generate AI videos, images, and audio from the command line. Features Runway's **latest Gen-4.5 model** for high-quality video generation, plus image and audio generation.

> **Recommended:** Use **`gen4.5`** for best video results - the newest and most capable model.

> **Setup:** Run `runway login <api-key>` or set `RUNWAYML_API_SECRET` env var. Get your key at [dev.runwayml.com](https://dev.runwayml.com).

## Quick Start

```bash
# Install
npm install -g @runwayml/cli

# Authenticate
runway login <your-api-key>

# Generate video from image
runway image-to-video "Camera slowly zooms in, leaves rustling" -i photo.jpg

# Generate video from text only
runway text-to-video "A serene mountain lake at sunrise with mist rising"

# Generate image
runway text-to-image "A futuristic city at sunset"

# Generate speech
runway text-to-speech "Hello, welcome to Runway!" --voice Maya
```

---

## Video Generation

For prompting best practices, see the [Prompting Guide](../api/references/prompting.md).

### Image to Video (Gen-4.5)

```bash
# Basic - animate an image
runway image-to-video "Camera slowly pushes in" -i https://example.com/photo.jpg

# With options
runway image-to-video "Subject smiles and waves" \
  -i ./input.jpg \
  -d 10 \
  -r 1280:720 \
  -m gen4.5
```

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --image` | Input image URL or local path | Required |
| `-d, --duration` | Duration in seconds (2-10) | 5 |
| `-r, --ratio` | Aspect ratio | 1280:720 |
| `-m, --model` | gen4.5, gen4_turbo, veo3.1, veo3 | gen4.5 |

**Aspect Ratios:** `1280:720` (16:9), `720:1280` (9:16), `1584:672` (21:9), `1104:832` (4:3), `832:1104` (3:4)

### Text to Video (Gen-4.5)

Generate video from text description only (no image required):

```bash
runway text-to-video "A golden retriever running through a meadow at sunset"

runway text-to-video "Aerial shot of a city at night" -d 10 -m veo3.1
```

**Text-to-Video Ratios:** `1280:720` (16:9), `720:1280` (9:16)

### Video to Video (Aleph)

Transform existing videos:

```bash
runway video-to-video "Transform into anime style" -v https://example.com/video.mp4
```

### Model Comparison

| Model | Input | Audio | Use Case |
|-------|-------|-------|----------|
| **gen4.5** ⭐ | Text or Image | No | Best quality, recommended |
| gen4_turbo | Image only | No | Fast iteration |
| veo3.1 | Text or Image | Yes | When you need audio |
| veo3 | Text or Image | Yes | Google Veo with audio |

---

## Image Generation

```bash
# Basic text-to-image
runway text-to-image "A futuristic city at sunset"

# With specific model and ratio
runway text-to-image gen4-image "Mountain landscape" -r 1920:1080

# With reference images (style transfer)
runway text-to-image gen4-image-turbo "Portrait in this style" \
  -i https://example.com/style-ref.jpg
```

| Model | References | Use Case |
|-------|------------|----------|
| gen4-image | Optional | High quality, default |
| gen4-image-turbo | Required (1-3) | Fast iteration |
| gemini-2.5-flash | Optional | Google Gemini |

---

## Audio Generation

### Text to Speech

```bash
runway text-to-speech "Welcome to Runway ML" --voice Maya
```

**Voices:** Maya, Arjun, Leslie, Noah, Jack, Katie, Serene, Bernard, Billy, Mark, Clint, Mabel, Chad, Eleanor, Elias, Elliot, Rachel, James, Tom, Wanda, Benjamin

### Sound Effects

```bash
runway sound-effect "Thunder rolling with light rain" -d 10
```

### Voice Processing

```bash
# Isolate voice from noisy audio
runway voice-isolation https://example.com/audio.mp3

# Dub audio to another language
runway voice-dubbing https://example.com/audio.mp3 -l es

# Convert to different voice
runway speech-to-speech https://example.com/audio.mp3 --voice Maya
```

**Dubbing Languages:** en, es, fr, de, ja, zh, ko, pt, it, nl, ru, ar, hi, and more.

---

## Character Performance

Drive character motion from reference video:

```bash
runway character-performance ./reference-performance.mp4 -c ./character.jpg
```

| Option | Description |
|--------|-------------|
| `-c, --character` | Character image or video URL |
| `--character-type` | `image` or `video` |
| `--body-control` | Enable body movement |

---

## Shell Scripting

The CLI outputs asset URLs to stdout, making it easy to script:

```bash
# Capture output URL
VIDEO_URL=$(runway image-to-video "Gentle motion" -i photo.jpg)
echo "Generated: $VIDEO_URL"

# Download result
curl -o output.mp4 "$VIDEO_URL"

# Chain commands
runway text-to-image "A cat" | xargs -I {} runway image-to-video "Cat walks" -i {}
```

### Batch Processing

```bash
# Process multiple images
for img in images/*.jpg; do
  runway image-to-video "Subtle movement" -i "$img" >> results.txt
done
```

---

## Authentication

### Login with API Key

```bash
runway login <your-api-key>
```

### Multiple Profiles

```bash
# Add staging profile
runway login --profile staging <staging-key>

# List profiles
runway login list

# Switch profile
runway login use staging

# Use for single command
RUNWAY_PROFILE=staging runway whoami
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `RUNWAYML_API_SECRET` | API key (overrides config) |
| `RUNWAY_PROFILE` | Profile to use |

---

## Tips

- Generation takes 30-120 seconds depending on duration and model
- Use `--debug` flag for verbose output
- All commands output the URL of the generated asset
- Local file paths are automatically uploaded

## CLI vs SDK

| Use Case | Recommended |
|----------|-------------|
| Quick terminal generation | CLI |
| Shell scripts & CI/CD | CLI |
| Interactive prompt testing | CLI |
| Building applications | SDK |
| Complex workflows in code | SDK |

For SDK usage, see [runwayml/skills/api](../api).

---

## Command Reference

```bash
runway --help                    # All commands
runway <command> --help          # Command options
runway whoami                    # Check auth status
runway org info                  # Organization info
runway org usage                 # Credit usage
```

## Links

- [CLI Repository](https://github.com/runwayml/cli)
- [API Documentation](https://docs.dev.runwayml.com/)
- [Developer Portal](https://dev.runwayml.com/)
