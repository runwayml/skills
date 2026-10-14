---
name: rw-generate-audio
description: "Generate audio using the Runway API via runnable scripts. Supports TTS, sound effects, voice isolation, dubbing, and voice conversion."
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(uv run *), Bash(command -v uv)
---

# Generate Audio

Generate audio directly using the Runway API. Supports text-to-speech, sound effects, voice isolation, dubbing, and speech-to-speech voice conversion.

**IMPORTANT:** Run scripts from the user's working directory so output files are saved where the user expects.

## Usage

```bash
uv run scripts/generate_audio.py --type tts --text "Hello world" --filename "greeting.mp3" [--voice-id ID] [--api-key KEY]
```

## Preflight

1. `command -v uv` must succeed
2. `RUNWAYML_API_SECRET` must be set, or pass `--api-key`

## Audio Types

| Type | Description | Required Args |
|------|-------------|---------------|
| `tts` | Text to speech | `--text` |
| `sfx` | Sound effect generation | `--text` |
| `isolate` | Isolate voice from audio | `--audio-url` |
| `dub` | Dub to another language | `--audio-url`, `--target-language` |
| `sts` | Voice conversion | `--audio-url` |

## Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--type` | Audio type (required): tts, sfx, isolate, dub, sts | -- |
| `--filename` | Output filename (required) | -- |
| `--text` | Text input (for tts and sfx) | -- |
| `--audio-url` | Audio URL or local path (for isolate, dub, sts) | -- |
| `--voice-id` | Voice preset (for tts and sts, e.g. Maya, Noah, Leslie) | Maya |
| `--target-language` | Language code (for dub, e.g. "es") | -- |
| `--output-dir` | Output directory | cwd |
| `--api-key` | Runway API key | env `RUNWAYML_API_SECRET` |

## Examples

**Text-to-speech:**
```bash
uv run scripts/generate_audio.py --type tts --text "Welcome to our product showcase" --filename "voiceover.mp3"
```

**Sound effect:**
```bash
uv run scripts/generate_audio.py --type sfx --text "Thunder rolling across a stormy sky" --filename "thunder.mp3"
```

**Voice isolation:**
```bash
uv run scripts/generate_audio.py --type isolate --audio-url "noisy-recording.mp3" --filename "clean-voice.mp3"
```

**Speech-to-speech (voice conversion):**
```bash
uv run scripts/generate_audio.py --type sts --audio-url "recording.mp3" --voice-id Noah --filename "converted.mp3"
```

**Dubbing:**
```bash
uv run scripts/generate_audio.py --type dub --audio-url "english-narration.mp3" --target-language es --filename "spanish-dub.mp3"
```

## Output

- The script downloads the result and saves it to the specified path
- Script outputs the full path to the saved file
