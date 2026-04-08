---
name: rw-check-org-details
description: "Query the Runway API for organization details: rate limits, credit balance, usage tier, and daily generation counts"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node *), Bash(python3 *), Bash(curl *)
---

# Check Organization Details

> **PREREQUISITE:** Run `+rw-setup-api-key` first to ensure the API key is configured.

Query the Runway API to retrieve the user's organization details — credit balance, usage tier, rate limits, current daily generation counts, and historical credit usage.

## Step 1: Verify API Key Is Available

Before making any requests, confirm the API key is accessible:

1. Check for a `.env` file containing `RUNWAYML_API_SECRET`
2. Or check if the environment variable is set: `echo $RUNWAYML_API_SECRET`

If the key is not found, tell the user to run `+rw-setup-api-key` first and stop.

## Step 2: Query Organization Info

Call `GET /v1/organization` to retrieve the org's tier, credit balance, and current usage.

### Node.js

```javascript
import RunwayML from '@runwayml/sdk';

const client = new RunwayML();
const details = await client.organization.retrieve();
console.log(JSON.stringify(details, null, 2));
```

### Python

```python
from runwayml import RunwayML

client = RunwayML()
details = client.organization.retrieve()
print(details)
```

### cURL / fetch (no SDK)

```bash
curl -s https://api.dev.runwayml.com/v1/organization \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06" | python3 -m json.tool
```

### Response Shape

```json
{
  "tier": {
    "maxMonthlyCreditSpend": 10000,
    "models": {
      "gen4.5": {
        "maxConcurrentGenerations": 2,
        "maxDailyGenerations": 200
      }
    }
  },
  "creditBalance": 5000,
  "usage": {
    "models": {
      "gen4.5": {
        "dailyGenerations": 12
      }
    }
  }
}
```

## Step 3: Present the Results

Format the output as a clear summary for the user:

```
## Organization Overview

**Credit Balance:** X credits ($X.XX at $0.01/credit)
**Monthly Spend Cap:** X credits

### Rate Limits (by model)

| Model | Concurrency | Daily Limit | Used Today | Remaining |
|-------|-------------|-------------|------------|-----------|
| gen4.5 | 2 | 200 | 12 | 188 |
| veo3.1 | 2 | 100 | 5 | 95 |
| ... | ... | ... | ... | ... |
```

Key things to highlight:
- **Credit balance** — convert to dollar value (`credits × $0.01`)
- **Per-model daily limits** — show how many generations remain today (rolling 24-hour window)
- **Concurrency** — how many tasks can run simultaneously per model
- **Monthly cap** — the max credit spend per month for their tier

## Step 4 (Optional): Query Credit Usage History

If the user wants to see historical usage, call `POST /v1/organization/usage`.

### Node.js

```javascript
const usage = await client.organization.retrieveUsage({
  startDate: '2026-02-15',   // ISO-8601, up to 90 days back
  beforeDate: '2026-03-17'   // exclusive end date
});
console.log(JSON.stringify(usage, null, 2));
```

### Python

```python
usage = client.organization.retrieve_usage(
    start_date="2026-02-15",
    before_date="2026-03-17"
)
print(usage)
```

### cURL / fetch (no SDK)

```bash
curl -s -X POST https://api.dev.runwayml.com/v1/organization/usage \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-02-15", "beforeDate": "2026-03-17"}' \
  | python3 -m json.tool
```

### Response Shape

```json
{
  "results": [
    {
      "date": "2026-03-16",
      "usedCredits": [
        { "model": "gen4.5", "amount": 120 },
        { "model": "veo3.1", "amount": 400 }
      ]
    }
  ],
  "models": ["gen4.5", "veo3.1"]
}
```

Present this as a usage breakdown:

```
### Credit Usage (Feb 15 – Mar 17)

| Date | Model | Credits Used |
|------|-------|-------------|
| 2026-03-16 | gen4.5 | 120 |
| 2026-03-16 | veo3.1 | 400 |
| ... | ... | ... |

**Total:** X credits
```

## Tier Reference

If the user asks about upgrading, share the tier breakdown:

| Tier | Concurrency | Daily Gens | Monthly Cap | Unlock Requirement |
|------|-------------|------------|-------------|---------------------|
| 1 (default) | 1–2 | 50–200 | $100 | — |
| 2 | 3 | 500–1,000 | $500 | 1 day + $50 spent |
| 3 | 5 | 1,000–2,000 | $2,000 | 7 days + $100 spent |
| 4 | 10 | 5,000–10,000 | $20,000 | 14 days + $1,000 spent |
| 5 | 20 | 25,000–30,000 | $100,000 | 7 days + $5,000 spent |

Tiers upgrade automatically once the spend and time requirements are met.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid or missing API key | Re-run `+rw-setup-api-key` |
| `creditBalance` is 0 | No credits purchased | Purchase at https://dev.runwayml.com/ → Billing (min $10) |
| Daily limit reached | Rolling 24-hour quota exhausted | Wait for the window to reset, or upgrade tier |
| All models show 0 daily limit | Tier 1 restrictions | Check that credits have been purchased |
