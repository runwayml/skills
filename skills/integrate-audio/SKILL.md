---
name: integrate-audio
description: "Help users integrate Runway audio APIs (TTS, sound effects, voice isolation, dubbing)"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Integrate Audio Generation

> **PREREQUISITE:** Run `+check-compatibility` first. Run `+fetch-api-reference` to load the latest API reference before integrating. Requires `+setup-api-key` for API credentials. Requires `+integrate-uploads` for local audio/video files.

Help users add Runway audio generation to their server-side code.

## Available Models

| Model | Endpoint | Use Case | Cost |
|-------|----------|----------|------|
| `eleven_multilingual_v2` | `POST /v1/text_to_speech` | Text to speech | 1 credit/50 chars |
| `eleven_text_to_sound_v2` | `POST /v1/sound_effect` | Sound effect generation | 1-2 credits |
| `eleven_voice_isolation` | `POST /v1/voice_isolation` | Isolate voice from audio | 1 credit/6 sec |
| `eleven_voice_dubbing` | `POST /v1/voice_dubbing` | Dub audio to other languages | 1 credit/2 sec |
| `eleven_multilingual_sts_v2` | `POST /v1/speech_to_speech` | Voice conversion | 1 credit/3 sec |

## Text-to-Speech

Generate speech from text using the ElevenLabs multilingual model.

### Node.js SDK

```javascript
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();

const task = await client.textToSpeech.create({
  model: 'eleven_multilingual_v2',
  text: 'Hello, welcome to our application!',
  voiceId: 'voice_id_here'  // See voice listing endpoint
}).waitForTaskOutput();

const audioUrl = task.output[0];
```

### Python SDK

```python
from runwayml import RunwayML

client = RunwayML()

task = client.text_to_speech.create(
    model='eleven_multilingual_v2',
    text='Hello, welcome to our application!',
    voice_id='voice_id_here'
).wait_for_task_output()

audio_url = task.output[0]
```

## Sound Effects

Generate sound effects from text descriptions.

```javascript
const task = await client.soundEffect.create({
  model: 'eleven_text_to_sound_v2',
  promptText: 'Thunder rolling across a stormy sky'
}).waitForTaskOutput();
```

```python
task = client.sound_effect.create(
    model='eleven_text_to_sound_v2',
    prompt_text='Thunder rolling across a stormy sky'
).wait_for_task_output()
```

## Voice Isolation

Extract voice from audio with background noise.

```javascript
// If using a local file, upload first
const upload = await client.uploads.createEphemeral(
  fs.createReadStream('/path/to/noisy-audio.mp3')
);

const task = await client.voiceIsolation.create({
  model: 'eleven_voice_isolation',
  audio: upload.runwayUri
}).waitForTaskOutput();
```

## Voice Dubbing

Dub audio/video into other languages.

```javascript
const task = await client.voiceDubbing.create({
  model: 'eleven_voice_dubbing',
  audio: 'https://example.com/speech.mp3',
  targetLanguage: 'es'  // Spanish
}).waitForTaskOutput();
```

## Speech-to-Speech

Convert one voice to another.

```javascript
const task = await client.speechToSpeech.create({
  model: 'eleven_multilingual_sts_v2',
  audio: 'https://example.com/original-speech.mp3',
  voiceId: 'target_voice_id'
}).waitForTaskOutput();
```

## Integration Pattern

### Express.js — Text-to-Speech Endpoint

```javascript
import RunwayML from '@runwayml/sdk';
import express from 'express';

const client = new RunwayML();
const app = express();
app.use(express.json());

app.post('/api/text-to-speech', async (req, res) => {
  try {
    const { text, voiceId } = req.body;

    const task = await client.textToSpeech.create({
      model: 'eleven_multilingual_v2',
      text,
      voiceId
    }).waitForTaskOutput();

    res.json({ audioUrl: task.output[0] });
  } catch (error) {
    console.error('TTS failed:', error);
    res.status(500).json({ error: error.message });
  }
});
```

### FastAPI — Sound Effects

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from runwayml import RunwayML

app = FastAPI()
client = RunwayML()

class SoundRequest(BaseModel):
    prompt: str

@app.post("/api/sound-effect")
async def generate_sound(req: SoundRequest):
    try:
        task = client.sound_effect.create(
            model='eleven_text_to_sound_v2',
            prompt_text=req.prompt
        ).wait_for_task_output()
        return {"audio_url": task.output[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Tips

- **Output URLs expire in 24-48 hours.** Download audio files to your own storage.
- **For local audio files** (voice isolation, dubbing, speech-to-speech), upload via `+integrate-uploads` first.
- **Voice IDs** can be listed via the voices endpoint — see `+api-reference` for details.
- **Text-to-speech cost** scales with text length: 1 credit per 50 characters.
