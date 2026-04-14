# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""List available Runway API models and their costs."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runway_helpers import VIDEO_MODELS, IMAGE_MODELS, AUDIO_MODELS


def print_table(title, models, extra_cols=None):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    for name, info in models.items():
        desc = info.get("description", "")
        cost = info.get("cost", "")
        print(f"  {name:<30} {cost:<20} {desc}")
    print()


def main():
    parser = argparse.ArgumentParser(description="List available Runway API models")
    parser.add_argument("--type", choices=["video", "image", "audio", "all"], default="all", help="Model type to list")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    data = {}
    if args.type in ("video", "all"):
        data["video"] = VIDEO_MODELS
    if args.type in ("image", "all"):
        data["image"] = IMAGE_MODELS
    if args.type in ("audio", "all"):
        data["audio"] = AUDIO_MODELS

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if "video" in data:
        print_table("Video Models", VIDEO_MODELS)
    if "image" in data:
        print_table("Image Models", IMAGE_MODELS)
    if "audio" in data:
        print_table("Audio Models", AUDIO_MODELS)


if __name__ == "__main__":
    main()
