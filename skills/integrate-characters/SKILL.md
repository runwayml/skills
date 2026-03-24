---
name: integrate-characters
description: "Help users create Runway Characters (GWM-1 avatars) and integrate real-time conversational sessions into their apps"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Integrate Characters (GWM-1 Avatars)

> **PREREQUISITES:**
> - `+check-compatibility` — Project must have a server-side component (API key must NEVER be exposed to the client)
> - `+fetch-api-reference` — Load the latest API reference from https://docs.dev.runwayml.com/api/ before integrating
> - `+setup-api-key` — API credentials must be configured
>
> **OPTIONAL DEPENDENCIES:**
> - `+integrate-documents` — Add a knowledge base to your character
> - `+integrate-character-embed` — Use the React SDK to embed the avatar call UI

Help users create Runway Characters — real-time conversational AI avatars powered by GWM-1.

Characters are generated from a **single image** (any visual style — photorealistic, animated, non-human) with full control over voice, personality, knowledge, and actions. No fine-tuning or training required.

## Key Concepts

### Avatars vs Sessions

| Concept | Description |
|---------|-------------|
| **Avatar** | A persistent persona with a defined appearance, voice, and personality. Created once, used many times. |
| **Session** | A live WebRTC connection for real-time conversation. Connects one user to one avatar. **Max duration: 5 minutes.** |

### Session Lifecycle

```
                    ┌───────────┐
         ┌──────────┤ NOT_READY ├──────────┐
         │          └─────┬─────┘          │
         │                │                │
         ▼                ▼                ▼
     CANCELLED          READY           FAILED
                       ┌──┴──┐
                       │     │
                       ▼     ▼
                    RUNNING FAILED
                    ┌──┴──┐
                    │     │
                    ▼     ▼
                COMPLETED CANCELLED
```

| Status | Description |
|--------|-------------|
| `NOT_READY` | Session is being provisioned. Poll until ready. |
| `READY` | Session is ready. The `sessionKey` is available. |
| `RUNNING` | WebRTC connection is active. Conversation in progress. |
| `COMPLETED` | Session ended normally. |
| `FAILED` | Error occurred. Check the `failure` field. |
| `CANCELLED` | Explicitly cancelled before completion. |

> **Important:** Session credentials can only be consumed **once**. If the WebRTC connection fails after credentials are consumed, you must create a new Session.

### Architecture

The API key must stay server-side. The flow is:

```
Client (React)  →  Your Server  →  Runway API
                                      ↓
Client (React)  ←─── WebRTC ───← Runway (realtime)
```

1. Client requests a session from **your** server
2. Your server calls Runway API to create a session (`POST /v1/realtime_sessions`)
3. Your server polls until session is `READY` (`GET /v1/realtime_sessions/:id`)
4. Your server consumes credentials (`POST /v1/realtime_sessions/:id/consume`)
5. Your server returns credentials to the client
6. Client establishes a direct WebRTC connection to Runway

## Step 1: Install Dependencies

```bash
npm install @runwayml/sdk @runwayml/avatars-react
```

- `@runwayml/sdk` — Server-side SDK (session creation, avatar management)
- `@runwayml/avatars-react` — Client-side React components (WebRTC, UI)

## Step 2: Create an Avatar

Avatars can be created via the **Developer Portal** (UI) or the **API** (programmatic).

### Option A: Developer Portal (Recommended for first time)

1. Go to **https://dev.runwayml.com/** → **Characters** tab
2. Click **Create a Character**
3. Upload a reference image (tips below)
4. Choose a voice preset
5. Write personality instructions (e.g., "You are a helpful customer support agent for Acme Corp...")
6. Optionally add a starting script (what the character says first)
7. Optionally upload knowledge documents (`.txt` files)
8. Click **Create Character**
9. Copy the **Avatar ID** (a UUID like `8be4df61-93ca-11d2-aa0d-00e098032b8c`)

### Option B: API (Programmatic)

```javascript
// Node.js
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();

const avatar = await client.avatars.create({
  name: 'Support Agent',
  referenceImage: 'https://example.com/avatar.png',
  voice: {
    type: 'runway-live-preset',
    presetId: 'clara',
  },
  personality: 'You are a helpful customer support agent for Acme Corp. You help users with billing questions and technical issues.',
});

console.log('Avatar ID:', avatar.id);
```

```python
# Python
from runwayml import RunwayML

client = RunwayML()

avatar = client.avatars.create(
    name='Support Agent',
    reference_image='https://example.com/avatar.png',
    voice={
        'type': 'runway-live-preset',
        'preset_id': 'clara',
    },
    personality='You are a helpful customer support agent for Acme Corp.',
)

print('Avatar ID:', avatar.id)
```

**If the reference image is a local file**, upload it first using `+integrate-uploads`:

```javascript
import fs from 'fs';

const upload = await client.uploads.createEphemeral(
  fs.createReadStream('/path/to/avatar-image.png')
);

const avatar = await client.avatars.create({
  name: 'Support Agent',
  referenceImage: upload.runwayUri,
  voice: { type: 'runway-live-preset', presetId: 'clara' },
  personality: 'You are a helpful customer support agent...',
});
```

### Reference Image Guidelines

- **Any visual style works**: photorealistic humans, animated mascots, stylized brand characters
- Use high-quality images with good lighting
- Face should be clearly visible and centered
- Avoid images with multiple people or obstructions
- Recommended aspect ratio: **1088×704**

### Voice Presets

| Preset ID | Name | Style |
|-----------|------|-------|
| `clara` | Clara | Soft, approachable |
| `victoria` | Victoria | Firm, professional |
| `vincent` | Vincent | Knowledgeable, authoritative |

Preview all voices in the [Developer Portal](https://dev.runwayml.com/).

## Step 3: Create a Session (Server-Side)

This is the **server-side API route** that your client will call. It creates a session, polls until ready, consumes credentials, and returns them.

### Next.js App Router

```typescript
// app/api/avatar/session/route.ts
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();

export async function POST(request: Request) {
  const { avatarId } = await request.json();

  // 1. Create session
  const { id: sessionId } = await client.realtimeSessions.create({
    model: 'gwm1_avatars',
    avatar: { type: 'custom', avatarId },
  });

  // 2. Poll until ready
  let sessionKey: string | undefined;
  for (let i = 0; i < 60; i++) {
    const session = await client.realtimeSessions.retrieve(sessionId);

    if (session.status === 'READY') {
      sessionKey = session.sessionKey;
      break;
    }
    if (session.status === 'FAILED') {
      return Response.json({ error: session.failure }, { status: 500 });
    }

    await new Promise(r => setTimeout(r, 1000));
  }

  if (!sessionKey) {
    return Response.json({ error: 'Session timed out' }, { status: 504 });
  }

  // 3. Consume session to get WebRTC credentials
  const consumeResponse = await fetch(
    `${client.baseURL}/v1/realtime_sessions/${sessionId}/consume`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${sessionKey}`,
        'X-Runway-Version': '2024-11-06',
      },
    }
  );
  const credentials = await consumeResponse.json();

  return Response.json({
    sessionId,
    serverUrl: credentials.url,
    token: credentials.token,
    roomName: credentials.roomName,
  });
}
```

### Express.js

```typescript
import RunwayML from '@runwayml/sdk';
import express from 'express';

const client = new RunwayML();
const app = express();
app.use(express.json());

app.post('/api/avatar/session', async (req, res) => {
  const { avatarId } = req.body;

  try {
    // 1. Create session
    const { id: sessionId } = await client.realtimeSessions.create({
      model: 'gwm1_avatars',
      avatar: { type: 'custom', avatarId },
    });

    // 2. Poll until ready
    let sessionKey: string | undefined;
    for (let i = 0; i < 60; i++) {
      const session = await client.realtimeSessions.retrieve(sessionId);

      if (session.status === 'READY') {
        sessionKey = session.sessionKey;
        break;
      }
      if (session.status === 'FAILED') {
        return res.status(500).json({ error: session.failure });
      }

      await new Promise(r => setTimeout(r, 1000));
    }

    if (!sessionKey) {
      return res.status(504).json({ error: 'Session timed out' });
    }

    // 3. Consume credentials
    const consumeResponse = await fetch(
      `${client.baseURL}/v1/realtime_sessions/${sessionId}/consume`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${sessionKey}`,
          'X-Runway-Version': '2024-11-06',
        },
      }
    );
    const credentials = await consumeResponse.json();

    res.json({
      sessionId,
      serverUrl: credentials.url,
      token: credentials.token,
      roomName: credentials.roomName,
    });
  } catch (error) {
    console.error('Session creation failed:', error);
    res.status(500).json({ error: error instanceof Error ? error.message : 'Unknown error' });
  }
});
```

### FastAPI (Python)

```python
import time
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from runwayml import RunwayML

app = FastAPI()
client = RunwayML()

class SessionRequest(BaseModel):
    avatar_id: str

@app.post("/api/avatar/session")
async def create_session(req: SessionRequest):
    # 1. Create session
    result = client.realtime_sessions.create(
        model='gwm1_avatars',
        avatar={'type': 'custom', 'avatar_id': req.avatar_id},
    )
    session_id = result.id

    # 2. Poll until ready
    session_key = None
    for _ in range(60):
        session = client.realtime_sessions.retrieve(session_id)

        if session.status == 'READY':
            session_key = session.session_key
            break
        if session.status == 'FAILED':
            raise HTTPException(status_code=500, detail=str(session.failure))

        time.sleep(1)

    if not session_key:
        raise HTTPException(status_code=504, detail='Session timed out')

    # 3. Consume credentials
    async with httpx.AsyncClient() as http:
        resp = await http.post(
            f"{client.base_url}/v1/realtime_sessions/{session_id}/consume",
            headers={
                "Authorization": f"Bearer {session_key}",
                "X-Runway-Version": "2024-11-06",
            },
        )
    credentials = resp.json()

    return {
        "session_id": session_id,
        "server_url": credentials["url"],
        "token": credentials["token"],
        "room_name": credentials["roomName"],
    }
```

## Step 4: Connect from the Client

See `+integrate-character-embed` for the React SDK components that handle WebRTC connection and rendering. The simplest approach:

```tsx
'use client';
import { AvatarCall } from '@runwayml/avatars-react';
import '@runwayml/avatars-react/styles.css';

export default function CharacterPage() {
  return (
    <AvatarCall
      avatarId="your-avatar-id"
      connectUrl="/api/avatar/session"
      onEnd={() => console.log('Call ended')}
      onError={(error) => console.error('Error:', error)}
    />
  );
}
```

## Troubleshooting

- **API key errors:** Key starts with `key_` followed by 128 hex chars. Ensure it's active.
- **No credits:** Account must have prepaid credits before starting a call.
- **Session timeout:** The 60-iteration poll loop waits ~60 seconds. If sessions consistently time out, check your tier's concurrency limits.
- **Credentials already consumed:** Session credentials are one-time use. If WebRTC fails after consume, create a new session.

### Debug logging

```tsx
<AvatarCall
  avatarId="your-avatar-id"
  connectUrl="/api/avatar/session"
  onError={(error) => {
    console.error('Avatar error:', error);
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    if (error.cause) console.error('Cause:', error.cause);
  }}
/>
```

### Monitor session state

```tsx
import { useAvatarSession } from '@runwayml/avatars-react';

function DebugInfo() {
  const { state, sessionId, error } = useAvatarSession();
  return (
    <pre>
      {JSON.stringify({ state, sessionId, error: error?.message }, null, 2)}
    </pre>
  );
}
```

### Test with minimal setup

```bash
npx degit runwayml/avatars-sdk-react/examples/nextjs-simple test-app
cd test-app
npm install
# Add your API key to .env.local
npm run dev
```

## Browser Support

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 74+ |
| Firefox | 78+ |
| Safari | 14.1+ |
| Edge | 79+ |

Users must grant microphone permissions. Camera permissions needed if user video is enabled.

## Getting Help

| Resource | Description |
|----------|-------------|
| [Developer Portal](https://dev.runwayml.com/) | Manage avatars, view logs, access dashboard |
| [SDK Repository](https://github.com/runwayml/avatars-sdk-react) | Report bugs, view examples, check releases |

When reporting issues, include: browser/version, SDK version (`npm list @runwayml/avatars-react`), error messages, session ID, and steps to reproduce.
