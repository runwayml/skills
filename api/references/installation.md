# Installation Guide

## Python SDK

```bash
pip install runwayml
```

Set your API key:

```bash
export RUNWAYML_API_SECRET="your_api_key_here"
```

Or pass it directly:

```python
from runwayml import RunwayML

client = RunwayML(api_key="your_api_key_here")
```

## Node.js SDK

```bash
npm install @runwayml/sdk
```

Set your API key:

```bash
export RUNWAYML_API_SECRET="your_api_key_here"
```

Or pass it directly:

```javascript
import RunwayML from "@runwayml/sdk";

const client = new RunwayML({ apiKey: "your_api_key_here" });
```

## Getting an API Key

1. Go to [dev.runwayml.com](https://dev.runwayml.com)
2. Sign in or create an account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy and store securely

## Rate Limits

- **10 concurrent tasks** per organization
- **500 tasks/minute** rate limit
- SDKs handle rate limiting automatically with exponential backoff

## Pricing

1 credit = $0.01

| Model Type | Cost |
|------------|------|
| gen4_turbo | 5 credits/sec |
| gen4_aleph | 15 credits/sec |
| gen4_image | 5-8 credits/image |
| gen4_image_turbo | 2 credits/image |
| ElevenLabs audio | 1 credit/50 chars or 1 credit/2-6 sec |

Purchase credits at [dev.runwayml.com](https://dev.runwayml.com)
