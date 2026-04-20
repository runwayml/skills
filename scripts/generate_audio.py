# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Generate audio using the Runway API (TTS, sound effects, voice isolation, dubbing)."""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runway_helpers import (
    get_api_key,
    api_post,
    poll_task,
    download_file,
    ensure_url,
    output_path,
)

AUDIO_TYPES = {
    "tts": {
        "endpoint": "/v1/text_to_speech",
        "model": "eleven_multilingual_v2",
        "description": "Text to speech",
    },
    "sfx": {
        "endpoint": "/v1/sound_effect",
        "model": "eleven_text_to_sound_v2",
        "description": "Sound effect generation",
    },
    "isolate": {
        "endpoint": "/v1/voice_isolation",
        "model": "eleven_voice_isolation",
        "description": "Isolate voice from audio",
    },
    "dub": {
        "endpoint": "/v1/voice_dubbing",
        "model": "eleven_voice_dubbing",
        "description": "Dub to another language",
    },
    "sts": {
        "endpoint": "/v1/speech_to_speech",
        "model": "eleven_multilingual_sts_v2",
        "description": "Voice conversion",
    },
}


def main():
    parser = argparse.ArgumentParser(description="Generate audio with the Runway API")
    parser.add_argument("--filename", required=True, help="Output filename (e.g. output.mp3)")
    parser.add_argument(
        "--type",
        required=True,
        choices=list(AUDIO_TYPES.keys()),
        help="Audio type: tts, sfx, isolate, dub, sts",
    )
    parser.add_argument("--text", help="Text input (required for tts and sfx)")
    parser.add_argument("--audio-url", help="Audio URL or local path (for isolate, dub, sts)")
    parser.add_argument("--voice-id", help="Voice ID (for tts and sts)")
    parser.add_argument("--target-language", help="Target language code (for dub, e.g. 'es')")
    parser.add_argument("--output-dir", help="Output directory (default: cwd)")
    args = parser.parse_args()

    api_key = get_api_key()
    audio_type = AUDIO_TYPES[args.type]
    endpoint = audio_type["endpoint"]
    model = audio_type["model"]

    body = {"model": model}

    if args.type == "tts":
        if not args.text:
            print("Error: --text is required for tts.", file=sys.stderr)
            sys.exit(1)
        body["promptText"] = args.text
        body["voice"] = {"type": "runway-preset", "presetId": args.voice_id or "Maya"}

    elif args.type == "sfx":
        if not args.text:
            print("Error: --text is required for sfx.", file=sys.stderr)
            sys.exit(1)
        body["promptText"] = args.text

    elif args.type == "isolate":
        if not args.audio_url:
            print("Error: --audio-url is required for isolate.", file=sys.stderr)
            sys.exit(1)
        body["audioUri"] = ensure_url(args.audio_url, api_key)

    elif args.type == "sts":
        if not args.audio_url:
            print("Error: --audio-url is required for sts.", file=sys.stderr)
            sys.exit(1)
        audio_uri = ensure_url(args.audio_url, api_key)
        body["media"] = {"type": "audio", "uri": audio_uri}
        body["voice"] = {"type": "runway-preset", "presetId": args.voice_id or "Maya"}

    elif args.type == "dub":
        if not args.audio_url:
            print("Error: --audio-url is required for dub.", file=sys.stderr)
            sys.exit(1)
        if not args.target_language:
            print("Error: --target-language is required for dub.", file=sys.stderr)
            sys.exit(1)
        body["audioUri"] = ensure_url(args.audio_url, api_key)
        body["targetLang"] = args.target_language

    print(f"Generating audio ({args.type}) with {model}...", file=sys.stderr)
    task = api_post(api_key, endpoint, body)
    task_id = task.get("id")
    print(f"Task created: {task_id}", file=sys.stderr)

    result = poll_task(api_key, task_id)
    urls = result.get("output", [])

    if not urls:
        print("Error: No output URLs in result.", file=sys.stderr)
        sys.exit(1)

    out = output_path(args.filename, args.output_dir)
    path = download_file(urls[0], out)
    print(path)
    print(f"Saved: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
