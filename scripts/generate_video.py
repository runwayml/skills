# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Generate videos using the Runway API."""

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
    VIDEO_MODELS,
)


def main():
    parser = argparse.ArgumentParser(description="Generate videos with the Runway API")
    parser.add_argument("--prompt", required=True, help="Text description of the video")
    parser.add_argument("--filename", required=True, help="Output filename (e.g. output.mp4)")
    parser.add_argument(
        "--model",
        default="gen4.5",
        choices=list(VIDEO_MODELS.keys()),
        help="Video model (default: gen4.5)",
    )
    parser.add_argument("--ratio", default="1280:720", help="Aspect ratio (default: 1280:720). seedance2 uses shorthands: 16:9, 9:16, 1:1, etc.")
    parser.add_argument("--duration", type=int, default=5, help="Duration in seconds (default: 5)")
    parser.add_argument("--image-url", help="Input image URL or local path for image-to-video")
    parser.add_argument("--video-url", help="Input video URL or local path for video-to-video (gen4_aleph, seedance2)")
    parser.add_argument("--output-dir", help="Output directory (default: cwd)")
    parser.add_argument("--api-key", help="Runway API key (or set RUNWAYML_API_SECRET)")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    model_info = VIDEO_MODELS[args.model]

    if args.video_url:
        if "video_to_video" not in model_info["endpoints"]:
            print(f"Error: {args.model} does not support video-to-video.", file=sys.stderr)
            sys.exit(1)
        endpoint = "/v1/video_to_video"
        video_uri = ensure_url(args.video_url, api_key)
        body = {
            "model": args.model,
            "promptVideo": video_uri,
            "promptText": args.prompt,
        }
        if args.model != "seedance2":
            body["ratio"] = args.ratio
            body["duration"] = args.duration
    elif args.image_url:
        if "image_to_video" not in model_info["endpoints"]:
            print(f"Error: {args.model} does not support image-to-video.", file=sys.stderr)
            sys.exit(1)
        endpoint = "/v1/image_to_video"
        image_uri = ensure_url(args.image_url, api_key)
        body = {
            "model": args.model,
            "promptImage": image_uri,
            "promptText": args.prompt,
            "ratio": args.ratio,
            "duration": args.duration,
        }
    else:
        if "text_to_video" not in model_info["endpoints"]:
            print(
                f"Error: {args.model} requires an input image (--image-url). "
                "It does not support text-only generation.",
                file=sys.stderr,
            )
            sys.exit(1)
        endpoint = "/v1/text_to_video"
        body = {
            "model": args.model,
            "promptText": args.prompt,
            "ratio": args.ratio,
            "duration": args.duration,
        }

    print(f"Generating video with {args.model} ({args.duration}s, {args.ratio})...", file=sys.stderr)
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
