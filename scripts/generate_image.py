# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Generate images using the Runway API."""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runway_helpers import (
    get_api_key,
    api_post,
    poll_task,
    download_file,
    output_path,
    IMAGE_MODELS,
)


def main():
    parser = argparse.ArgumentParser(description="Generate images with the Runway API")
    parser.add_argument("--prompt", required=True, help="Text description of the image")
    parser.add_argument(
        "--filename", required=True, help="Output filename (e.g. output.png)"
    )
    parser.add_argument(
        "--model",
        default="gemini_2.5_flash",
        choices=list(IMAGE_MODELS.keys()),
        help="Image model (default: gemini_2.5_flash / Nano Banana)",
    )
    parser.add_argument(
        "--ratio", default=None, help="Aspect ratio. gemini_2.5_flash: 1344:768, 768:1344, 1024:1024, etc. Others: 1280:720"
    )
    parser.add_argument(
        "--reference-images",
        nargs="*",
        metavar="TAG=URL",
        help="Reference images as Tag=URL pairs (e.g. Style=https://...)",
    )
    parser.add_argument("--output-dir", help="Output directory (default: cwd)")
    parser.add_argument("--api-key", help="Runway API key (or set RUNWAYML_API_SECRET)")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)

    if args.ratio:
        ratio = args.ratio
    elif args.model == "gemini_2.5_flash":
        ratio = "1344:768"
    else:
        ratio = "1280:720"

    body = {
        "model": args.model,
        "promptText": args.prompt,
        "ratio": ratio,
    }

    if args.reference_images:
        refs = []
        for pair in args.reference_images:
            if "=" not in pair:
                print(
                    f"Error: Reference image must be Tag=URL, got: {pair}",
                    file=sys.stderr,
                )
                sys.exit(1)
            tag, uri = pair.split("=", 1)
            refs.append({"tag": tag, "uri": uri})
        body["referenceImages"] = refs
    elif args.model == "gen4_image_turbo":
        print("Error: gen4_image_turbo requires --reference-images.", file=sys.stderr)
        sys.exit(1)

    print(f"Generating image with {args.model}...", file=sys.stderr)
    task = api_post(api_key, "/v1/text_to_image", body)
    task_id = task.get("id")
    print(f"Task created: {task_id}", file=sys.stderr)

    result = poll_task(api_key, task_id)
    urls = result.get("output", [])

    if not urls:
        print("Error: No output URLs in result.", file=sys.stderr)
        sys.exit(1)

    for i, url in enumerate(urls):
        if len(urls) == 1:
            out = output_path(args.filename, args.output_dir)
        else:
            base, ext = os.path.splitext(args.filename)
            out = output_path(f"{base}-{i + 1}{ext}", args.output_dir)
        path = download_file(url, out)
        print(path)
        print(f"Saved: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
