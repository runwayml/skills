# Runway Skills

Agent skills for the [Runway API](https://dev.runwayml.com) - generate AI videos, images, and audio.

## Available Skills

### CLI vs SDK

| | CLI | SDK |
|---|-----|-----|
| **Best for** | Shell scripts, CI/CD, quick generation | Building applications |
| **Output** | URLs to stdout | Programmatic task objects |
| **File handling** | Local paths auto-uploaded | URLs or base64 required |
| **Install** | `npm install -g @runwayml/cli` | `pip install runwayml` / `npm install @runwayml/sdk` |

---

### Runway CLI

Command-line interface for quick generation, shell scripts, and CI/CD pipelines.

```bash
# Generate video from local image
runway video generate --model gen4.5 --image ./photo.jpg --prompt "Camera pushes in slowly"

# Capture URL for scripting
VIDEO_URL=$(runway video generate --model gen4.5 --prompt "A sunset over mountains")
```

**Install:**
```bash
claude skill add runwayml/skills/cli
```

[View Documentation](./cli/SKILL.md)

---

### Runway API (SDK)

Complete SDK skill for Python and Node.js applications.

**Video Generation:**
- **Gen-4.5** (latest) - Text-to-video and image-to-video
- **Gen-4 Turbo** - Fast image-to-video
- **Gen-4 Aleph** - Video-to-video transformation
- **Act-Two** - Character performance
- **Google Veo** - Text/image-to-video with audio

**Image Generation:**
- **Gen-4 Image** - High-quality text-to-image with style references
- **Gen-4 Image Turbo** - Fast iteration
- **Gemini 2.5 Flash** - Google image generation

**Audio Generation (ElevenLabs):**
- **Text-to-Speech** - Natural voice synthesis
- **Sound Effects** - Generate audio from descriptions
- **Voice Isolation** - Remove background noise
- **Voice Dubbing** - Translate audio to 28+ languages
- **Speech-to-Speech** - Voice conversion

**Install:**
```bash
claude skill add runwayml/skills/api
```

[View Documentation](./api/SKILL.md)

---

## Installation

### Install the Runway CLI Skill
```bash
claude skill add runwayml/skills/cli
```

### Install the Runway API Skill
```bash
claude skill add runwayml/skills/api
```

### Install All Skills
```bash
claude skill add runwayml/skills
```

## Configuration

Set your Runway API key as an environment variable:

```bash
export RUNWAYML_API_SECRET="your_api_key_here"
```

Or for CLI, use the login command:

```bash
runway login <your-api-key>
```

Get your API key at [dev.runwayml.com](https://dev.runwayml.com).

## Package Installation

### Python
```bash
pip install runwayml
```

### Node.js
```bash
npm install @runwayml/sdk
```

### CLI
```bash
npm install -g @runwayml/cli
```

## Quick Example

```python
from runwayml import RunwayML

client = RunwayML()

# Text-to-video with latest Gen-4.5 model
task = client.text_to_video.create(
    model="gen4.5",
    prompt_text="A serene mountain lake at sunrise with mist rising",
    ratio="1280:720",
    duration=10
).wait_for_task_output()

print(f"Video URL: {task.output[0]}")
```

## Documentation

- [Complete API Documentation](https://docs.dev.runwayml.com/)
- [Model Guide](https://docs.dev.runwayml.com/guides/models/)
- [Developer Portal](https://dev.runwayml.com/) (API keys & account)

## License

MIT
