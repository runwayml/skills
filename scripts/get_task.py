# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Check the status of a Runway API task."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runway_helpers import get_api_key, api_get


def main():
    parser = argparse.ArgumentParser(description="Check Runway task status")
    parser.add_argument("--task-id", required=True, help="Task ID to check")
    parser.add_argument("--api-key", help="Runway API key (or set RUNWAYML_API_SECRET)")
    parser.add_argument("--wait", action="store_true", help="Poll until the task completes")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)

    if args.wait:
        from runway_helpers import poll_task
        result = poll_task(api_key, args.task_id)
        print(json.dumps(result, indent=2))
    else:
        task = api_get(api_key, f"/v1/tasks/{args.task_id}")
        print(json.dumps(task, indent=2))


if __name__ == "__main__":
    main()
