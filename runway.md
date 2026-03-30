# Runway API — Shared Context

Durable platform rules that apply across all Runway API skills. Individual skills reference this document for common guidance instead of restating it.

## Authentication

- **Environment variable:** `RUNWAYML_API_SECRET`
- **Server-side only.** The API key must never appear in client-side code, browser bundles, or public repositories.
- Obtain a key at [dev.runwayml.com/settings/api-keys](https://dev.runwayml.com/settings/api-keys).
- For staging environments, also set `RUNWAYML_BASE_URL=https://api.dev-stage.runwayml.com`.

## Request Headers

All REST requests require:

```
Authorization: Bearer <RUNWAYML_API_SECRET>
X-Runway-Version: 2024-11-06
Content-Type: application/json
```

SDK clients (`@runwayml/sdk` for Node.js, `runwayml` for Python) set these automatically.

## Base URLs

| Environment | URL |
|-------------|-----|
| Production  | `https://api.dev.runwayml.com` |
| Staging     | `https://api.dev-stage.runwayml.com` |

## Output URLs and Storage

- Generated output URLs (video, image, audio) **expire within 24–48 hours**.
- `runway://` upload URIs expire after **24 hours**.
- Always download outputs to your own storage (S3, GCS, local filesystem) immediately after generation.
- Never serve signed output URLs directly to end users.

## Task Polling

Generation endpoints return a task ID. The task must be polled until it reaches a terminal status.

**SDK (recommended):**
```javascript
const task = await client.textToVideo.create({ ... }).waitForTaskOutput();
```

`waitForTaskOutput()` has a default 10-minute timeout. For long-running generations, implement a custom polling loop or increase the timeout.

**REST:**
```
GET /v1/tasks/{id}
```

Poll until `status` is `SUCCEEDED`, `FAILED`, or `CANCELLED`. Use 5-second intervals with exponential backoff.

## Credits and Billing

- A Runway developer account with **prepaid credits** is required (minimum $10).
- Credit costs vary by model — see individual skill docs or the `api-reference` skill for current pricing.
- Manage billing at [dev.runwayml.com](https://dev.runwayml.com/).

## Rate Limits

- Rate limits are per-organization and vary by tier and model.
- Check current limits via `GET /v1/organization`.
- On `429 Too Many Requests`, retry with exponential backoff.

## Content Moderation

- Both inputs and outputs are subject to content moderation.
- Safety-flagged inputs are **non-refundable** — credits are still consumed.
- If a generation is rejected, try a different prompt.

## API Reference

- **Official docs:** [docs.dev.runwayml.com](https://docs.dev.runwayml.com/)
- **API reference:** [docs.dev.runwayml.com/api](https://docs.dev.runwayml.com/api/)
- **Developer portal:** [dev.runwayml.com](https://dev.runwayml.com/)
