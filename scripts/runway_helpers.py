# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Shared helpers for Runway API scripts: API calls, task polling, retry, download, error handling."""

import json
import os
import platform
import shutil
import subprocess
import sys
import time
import mimetypes
import requests

API_BASE = "https://api.dev.runwayml.com"
API_VERSION = "2024-11-06"

# ── Models registry ──────────────────────────────────────

VIDEO_MODELS = {
    "seedance2": {
        "endpoints": ["text_to_video", "image_to_video", "video_to_video"],
        "cost": "36 credits/sec",
        "description": "Reference image and video, long duration (up to 15s)",
        "input": "Text, Image, and/or Video",
    },
    "gen4.5": {
        "endpoints": ["text_to_video", "image_to_video"],
        "cost": "12 credits/sec",
        "description": "High quality, general purpose",
        "input": "Text and/or Image",
    },
    "gen4_turbo": {
        "endpoints": ["image_to_video"],
        "cost": "5 credits/sec",
        "description": "Fast, image-driven (image required)",
        "input": "Image required",
    },
    "gen4_aleph": {
        "endpoints": ["video_to_video"],
        "cost": "15 credits/sec",
        "description": "Video editing/transformation",
        "input": "Video + Text/Image",
    },
    "veo3": {
        "endpoints": ["text_to_video", "image_to_video"],
        "cost": "40 credits/sec",
        "description": "Premium quality",
        "input": "Text/Image",
        "durations": [8],
    },
    "veo3.1": {
        "endpoints": ["text_to_video", "image_to_video"],
        "cost": "20-40 credits/sec",
        "description": "High quality Google model",
        "input": "Text/Image",
        "durations": [4, 6, 8],
    },
    "veo3.1_fast": {
        "endpoints": ["text_to_video", "image_to_video"],
        "cost": "10-15 credits/sec",
        "description": "Fast Google model",
        "input": "Text/Image",
        "durations": [4, 6, 8],
    },
}

IMAGE_MODELS = {
    "gen4_image": {
        "endpoint": "text_to_image",
        "cost": "5-8 credits",
        "description": "Highest quality",
    },
    "gen4_image_turbo": {
        "endpoint": "text_to_image",
        "cost": "2 credits",
        "description": "Fast and cheap",
    },
    "gemini_2.5_flash": {
        "endpoint": "text_to_image",
        "cost": "5 credits",
        "description": "Google Gemini model",
    },
}

AUDIO_MODELS = {
    "eleven_multilingual_v2": {
        "endpoint": "text_to_speech",
        "cost": "1 credit/50 chars",
        "description": "Text to speech",
    },
    "eleven_text_to_sound_v2": {
        "endpoint": "sound_effect",
        "cost": "1-2 credits",
        "description": "Sound effect generation",
    },
    "eleven_voice_isolation": {
        "endpoint": "voice_isolation",
        "cost": "1 credit/6 sec",
        "description": "Isolate voice from audio",
    },
    "eleven_voice_dubbing": {
        "endpoint": "voice_dubbing",
        "cost": "1 credit/2 sec",
        "description": "Dub to other languages",
    },
    "eleven_multilingual_sts_v2": {
        "endpoint": "speech_to_speech",
        "cost": "1 credit/3 sec",
        "description": "Voice conversion",
    },
}

# ── API key ──────────────────────────────────────────────

def get_api_key(args_key=None):
    key = args_key or os.environ.get("RUNWAYML_API_SECRET")
    if not key:
        print(
            "Error: No API key. Set RUNWAYML_API_SECRET or pass --api-key.\n"
            "Get your key at https://dev.runwayml.com/",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def _headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "X-Runway-Version": API_VERSION,
        "Content-Type": "application/json",
    }

# ── Error formatting ─────────────────────────────────────

def format_api_error(status_code, response_text):
    msg = f"API error {status_code}"
    try:
        data = json.loads(response_text)
        error = data.get("error", data.get("message", ""))
        issues = data.get("issues", [])
    except (json.JSONDecodeError, TypeError):
        error = response_text[:500] if response_text else ""
        issues = []

    if status_code == 400:
        detail = error
        if issues:
            parts = [f"{i.get('path', ['?'])[-1]}: {i.get('message', '')}" for i in issues]
            detail = f"{error} [{'; '.join(parts)}]"
        return f"{msg}: Invalid input — {detail}"
    elif status_code == 401:
        return f"{msg}: Authentication failed. Check RUNWAYML_API_SECRET."
    elif status_code == 429:
        return f"{msg}: Rate limited. Will retry..."
    elif status_code in (502, 503, 504):
        return f"{msg}: Server overload. Will retry..."
    return f"{msg}: {error}"

# ── API calls with retry ─────────────────────────────────

def api_post(api_key, endpoint, body, max_retries=3):
    """POST to the Runway API with automatic retry on 429/5xx."""
    headers = _headers(api_key)
    delays = [5, 15, 45]

    for attempt in range(max_retries + 1):
        r = requests.post(f"{API_BASE}{endpoint}", headers=headers, json=body)
        if r.ok:
            return r.json()
        if r.status_code in (429, 502, 503, 504) and attempt < max_retries:
            delay = delays[min(attempt, len(delays) - 1)]
            print(
                f"  {format_api_error(r.status_code, r.text)}\n"
                f"  Retrying in {delay}s (attempt {attempt + 1}/{max_retries})...",
                file=sys.stderr,
            )
            time.sleep(delay)
            continue
        msg = format_api_error(r.status_code, r.text)
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)


def api_get(api_key, path, max_retries=3):
    """GET from the Runway API with automatic retry on 429/5xx."""
    headers = _headers(api_key)
    delays = [5, 15, 45]

    for attempt in range(max_retries + 1):
        r = requests.get(f"{API_BASE}{path}", headers=headers)
        if r.ok:
            return r.json()
        if r.status_code in (429, 502, 503, 504) and attempt < max_retries:
            delay = delays[min(attempt, len(delays) - 1)]
            print(f"  Retrying in {delay}s...", file=sys.stderr)
            time.sleep(delay)
            continue
        msg = format_api_error(r.status_code, r.text)
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)

# ── Task polling ─────────────────────────────────────────

def poll_task(api_key, task_id, interval=5, timeout=600):
    """Poll a Runway task until it reaches a terminal state."""
    start = time.time()
    while time.time() - start < timeout:
        task = api_get(api_key, f"/v1/tasks/{task_id}")
        status = task.get("status", "")

        if status == "SUCCEEDED":
            return task
        if status == "FAILED":
            failure = task.get("failure", "Unknown error")
            failure_code = task.get("failureCode", "")
            detail = f"{failure_code}: {failure}" if failure_code else str(failure)
            print(f"Error: Task failed — {detail}", file=sys.stderr)
            sys.exit(1)
        if status == "CANCELLED":
            print("Error: Task was cancelled.", file=sys.stderr)
            sys.exit(1)

        elapsed = int(time.time() - start)
        print(f"  [{task_id[:12]}] {status} ({elapsed}s)...", file=sys.stderr)
        time.sleep(interval)

    print(f"Error: Task timed out after {timeout}s.", file=sys.stderr)
    sys.exit(1)

# ── File download ────────────────────────────────────────

def download_file(url, filename):
    """Download a URL to a local file."""
    parent = os.path.dirname(filename)
    if parent:
        os.makedirs(parent, exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return os.path.abspath(filename)

# ── Upload helper ────────────────────────────────────────

def upload_file(api_key, local_path):
    """Upload a local file to Runway and return the runway:// URI."""
    if not os.path.isfile(local_path):
        print(f"Error: File not found: {local_path}", file=sys.stderr)
        sys.exit(1)

    mime_type = mimetypes.guess_type(local_path)[0] or "application/octet-stream"
    headers = _headers(api_key)
    del headers["Content-Type"]

    with open(local_path, "rb") as f:
        r = requests.post(
            f"{API_BASE}/v1/uploads",
            headers=headers,
            files={"file": (os.path.basename(local_path), f, mime_type)},
        )

    if not r.ok:
        msg = format_api_error(r.status_code, r.text)
        print(f"Error uploading: {msg}", file=sys.stderr)
        sys.exit(1)

    data = r.json()
    uri = data.get("runwayUri") or data.get("url")
    if not uri:
        print(f"Error: Upload returned no URI: {json.dumps(data)}", file=sys.stderr)
        sys.exit(1)

    print(f"  Uploaded: {uri}", file=sys.stderr)
    return uri


def ensure_url(path_or_url, api_key):
    """If input is a local file, upload it. Otherwise return as-is."""
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    if path_or_url.startswith("runway://"):
        return path_or_url
    return upload_file(api_key, path_or_url)

# ── Output path helper ───────────────────────────────────

def output_path(filename, output_dir=None):
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, os.path.basename(filename))
    return filename

# ── Cost estimation ──────────────────────────────────────

def estimate_video_credits(model, duration):
    """Rough credit estimate for a video generation."""
    cost_str = VIDEO_MODELS.get(model, {}).get("cost", "")
    try:
        per_sec = int(cost_str.split()[0].replace("-", "").strip("~"))
    except (ValueError, IndexError):
        return None
    return per_sec * duration


def estimate_image_credits(model):
    cost_str = IMAGE_MODELS.get(model, {}).get("cost", "")
    try:
        return int(cost_str.split()[0].replace("-", "").strip("~"))
    except (ValueError, IndexError):
        return None

# ── Desktop notification ─────────────────────────────────

def send_notification(title, message):
    try:
        system = platform.system()
        if system == "Linux" and shutil.which("notify-send"):
            subprocess.run(["notify-send", title, message], timeout=5)
        elif system == "Darwin":
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], timeout=5)
        else:
            print("\a", end="", file=sys.stderr)
    except Exception:
        pass
