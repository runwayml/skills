---
name: rw-integrate-character-embed
description: "Help users embed Runway Character avatar calls in React apps using the @runwayml/avatars-react SDK"
user-invocable: false
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Embed Characters in React (Avatars React SDK)

> **PREREQUISITES:**
> - `+rw-check-compatibility` — Project must have server-side capability (API key must never be exposed to the client)
> - `+rw-fetch-api-reference` — Load the latest API reference from https://docs.dev.runwayml.com/api/ before integrating
> - `+rw-integrate-characters` — Character (Avatar) must be created and session endpoint must exist
> - Project must use **React** (Next.js, Vite+React, Remix, etc.)
>
> **OPTIONAL:**
> - `+rw-integrate-documents` — Add knowledge base before embedding

Embed real-time avatar video calls in React applications using the `@runwayml/avatars-react` SDK.

## Installation

```bash
npm install @runwayml/avatars-react
```

This is a **client-side** package. The server-side `@runwayml/sdk` should already be installed from `+rw-integrate-characters`.

## Option A: Simple — `AvatarCall` Component

The fastest way to embed a character. Handles WebRTC connection and renders a default UI automatically.

```tsx
'use client';

import { AvatarCall } from '@runwayml/avatars-react';
import '@runwayml/avatars-react/styles.css';

export default function CharacterPage() {
  return (
    <AvatarCall
      avatarId="your-avatar-id-here"
      connectUrl="/api/avatar/session"
      onEnd={() => console.log('Call ended')}
      onError={(error) => console.error('Error:', error)}
    />
  );
}
```

### `AvatarCall` Props

| Prop | Type | Description |
|------|------|-------------|
| `avatarId` | `string` | The Avatar UUID from the Developer Portal or API |
| `connectUrl` | `string` | Your server-side session endpoint (e.g., `/api/avatar/session`) |
| `onEnd` | `() => void` | Called when the call ends normally |
| `onError` | `(error: Error) => void` | Called on connection or runtime errors |

**For custom avatars** created in the Developer Portal, use the Avatar UUID as `avatarId`.

## Option B: Fully Custom — Hooks

For full control over the UI, use `AvatarSession` with hooks.

### Components & Hooks

| Export | Type | Description |
|--------|------|-------------|
| `AvatarSession` | Component | Provider that manages the WebRTC session |
| `AvatarVideo` | Component | Renders the avatar's video stream |
| `UserVideo` | Component | Renders the user's camera feed |
| `useAvatarSession` | Hook | Access session state: `state`, `sessionId`, `error`, `end()` |
| `useLocalMedia` | Hook | Control user's media: `isMicEnabled`, `toggleMic()` |

### Custom UI Example

```tsx
'use client';

import {
  AvatarSession,
  AvatarVideo,
  UserVideo,
  useAvatarSession,
  useLocalMedia,
} from '@runwayml/avatars-react';
import type { SessionCredentials } from '@runwayml/avatars-react';

function CallUI() {
  const { state, end } = useAvatarSession();
  const { isMicEnabled, toggleMic } = useLocalMedia();

  return (
    <div className="relative w-full h-screen">
      {/* Avatar video takes full screen */}
      <AvatarVideo className="w-full h-full object-cover" />

      {/* User's camera in a small overlay */}
      <UserVideo className="absolute bottom-4 right-4 w-48 rounded-lg" />

      {/* Controls */}
      <div className="absolute bottom-4 left-4 flex gap-2">
        <button onClick={toggleMic}>
          {isMicEnabled ? 'Mute' : 'Unmute'}
        </button>
        <button onClick={end}>End Call</button>
      </div>

      {/* Connection state */}
      {state === 'connecting' && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
          Connecting...
        </div>
      )}
    </div>
  );
}

export function CustomAvatar({ credentials }: { credentials: SessionCredentials }) {
  return (
    <AvatarSession credentials={credentials} audio video>
      <CallUI />
    </AvatarSession>
  );
}
```

### Fetching Credentials for Custom UI

When using the hooks approach, you need to fetch credentials from your server endpoint and pass them to `AvatarSession`:

```tsx
'use client';

import { useState, useCallback } from 'react';
import type { SessionCredentials } from '@runwayml/avatars-react';
import { CustomAvatar } from './CustomAvatar';

export default function CharacterPage() {
  const [credentials, setCredentials] = useState<SessionCredentials | null>(null);
  const [loading, setLoading] = useState(false);

  const startCall = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/avatar/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ avatarId: 'your-avatar-id-here' }),
      });
      const data = await res.json();
      setCredentials(data);
    } catch (error) {
      console.error('Failed to connect:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  if (credentials) {
    return <CustomAvatar credentials={credentials} />;
  }

  return (
    <button onClick={startCall} disabled={loading}>
      {loading ? 'Connecting...' : 'Start Conversation'}
    </button>
  );
}
```

## Integration Patterns

### Next.js App Router (Full Example)

**Server route** (`app/api/avatar/session/route.ts`):
See `+rw-integrate-characters` for the complete server-side session creation code.

**Client page** (`app/character/page.tsx`):

```tsx
'use client';

import { AvatarCall } from '@runwayml/avatars-react';
import '@runwayml/avatars-react/styles.css';

const AVATAR_ID = process.env.NEXT_PUBLIC_AVATAR_ID || 'your-avatar-id';

export default function CharacterPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <AvatarCall
        avatarId={AVATAR_ID}
        connectUrl="/api/avatar/session"
        onEnd={() => window.location.reload()}
        onError={(error) => {
          console.error('Avatar error:', error);
          alert('Connection failed. Please try again.');
        }}
      />
    </div>
  );
}
```

### Conditional Rendering (Show/Hide)

```tsx
'use client';

import { useState } from 'react';
import { AvatarCall } from '@runwayml/avatars-react';
import '@runwayml/avatars-react/styles.css';

export default function SupportPage() {
  const [showAvatar, setShowAvatar] = useState(false);

  return (
    <div>
      <h1>Customer Support</h1>

      {!showAvatar ? (
        <button onClick={() => setShowAvatar(true)}>
          Talk to an Agent
        </button>
      ) : (
        <AvatarCall
          avatarId="support-agent-id"
          connectUrl="/api/avatar/session"
          onEnd={() => setShowAvatar(false)}
          onError={(error) => {
            console.error(error);
            setShowAvatar(false);
          }}
        />
      )}
    </div>
  );
}
```

## Error Handling

### Verbose Error Logging

```tsx
<AvatarCall
  avatarId="your-avatar-id"
  connectUrl="/api/avatar/session"
  onError={(error) => {
    console.error('Avatar error:', error);
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    if (error.cause) {
      console.error('Cause:', error.cause);
    }
  }}
/>
```

### Debug Session State

```tsx
import { useAvatarSession } from '@runwayml/avatars-react';

function DebugPanel() {
  const { state, sessionId, error } = useAvatarSession();

  return (
    <pre style={{ fontSize: 12, position: 'fixed', top: 0, right: 0 }}>
      {JSON.stringify({ state, sessionId, error: error?.message }, null, 2)}
    </pre>
  );
}
```

## Browser Support

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 74+ |
| Firefox | 78+ |
| Safari | 14.1+ |
| Edge | 79+ |

Users must grant **microphone permissions** when prompted. **Camera permissions** are needed if user video is enabled.

## Tips

- **Always import the styles**: `import '@runwayml/avatars-react/styles.css'` when using `AvatarCall`
- **`'use client'` directive** is required in Next.js App Router for all components using the React SDK
- **Session max duration is 5 minutes** — handle the `onEnd` callback to show a reconnect option
- **Credentials are one-time use** — if connection fails, fetch new credentials (create a new session)
- For the full SDK source, examples, and issue tracking: [github.com/runwayml/avatars-sdk-react](https://github.com/runwayml/avatars-sdk-react)
