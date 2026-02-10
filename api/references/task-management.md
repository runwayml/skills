# Task Management

## Automatic Polling

The simplest approach - SDKs handle polling automatically:

```python
task = client.image_to_video.create(
    model="gen4_turbo",
    prompt_image="https://example.com/image.jpg",
    prompt_text="gentle movement"
).wait_for_task_output()  # Polls until complete (10 min timeout)

print(task.output[0])  # Video URL
```

## Manual Polling

For more control:

```python
import time

# Create task
task = client.image_to_video.create(
    model="gen4_turbo",
    prompt_image="https://example.com/image.jpg",
    prompt_text="gentle movement"
)

# Poll manually
while task.status not in ["SUCCEEDED", "FAILED", "CANCELED"]:
    time.sleep(5)  # Wait 5 seconds between polls
    task = client.tasks.retrieve(task.id)

if task.status == "SUCCEEDED":
    print(f"Video: {task.output[0]}")
else:
    print(f"Failed: {task.failure}")
```

## Task Statuses

| Status | Meaning |
|--------|---------|
| `PENDING` | Task queued, waiting to start |
| `THROTTLED` | Rate limited, treat as PENDING |
| `RUNNING` | Generation in progress |
| `SUCCEEDED` | Complete, output available |
| `FAILED` | Error occurred |
| `CANCELED` | Task was canceled |

## Canceling/Deleting Tasks

```python
# Cancel a running/pending task, or delete a completed task
client.tasks.delete(task.id)
```

## Batch Processing

Process multiple items efficiently:

```python
import asyncio
from runwayml import AsyncRunwayML

async def generate_video(client, image_url, prompt):
    task = await client.image_to_video.create(
        model="gen4_turbo",
        prompt_image=image_url,
        prompt_text=prompt
    )
    return await task.wait_for_task_output()

async def main():
    client = AsyncRunwayML()

    jobs = [
        ("https://example.com/img1.jpg", "Camera pushes in slowly"),
        ("https://example.com/img2.jpg", "Gentle wind movement"),
        ("https://example.com/img3.jpg", "Timelapse clouds"),
    ]

    # Process up to 10 concurrent (rate limit)
    tasks = [generate_video(client, img, prompt) for img, prompt in jobs]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result.output[0])

asyncio.run(main())
```

## Error Recovery

```python
from runwayml import APIError

try:
    task = client.image_to_video.create(...).wait_for_task_output()
except APIError as e:
    if e.status_code == 429:
        # Rate limited - SDK auto-retries, but you can add custom logic
        print("Rate limited, waiting...")
    elif e.status_code == 400:
        # Invalid input
        print(f"Bad request: {e.message}")
    else:
        raise
```
