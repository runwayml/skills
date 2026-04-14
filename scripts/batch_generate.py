# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Run multi-step Runway API pipelines. Chain video, image, and audio generation in one command."""

import argparse
import json
import os
import re
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runway_helpers import (
    get_api_key,
    api_post,
    poll_task,
    download_file,
    ensure_url,
    output_path,
    estimate_video_credits,
    estimate_image_credits,
    send_notification,
    VIDEO_MODELS,
    IMAGE_MODELS,
)

VALID_ACTIONS = {"generate_video", "generate_image", "generate_audio", "fan_out"}

# ── Template variable substitution ──────────────────────

def substitute_vars(obj, variables):
    """Recursively replace {{key}} in all string values."""
    if isinstance(obj, str):
        for key, val in variables.items():
            obj = obj.replace("{{" + key + "}}", val)
        return obj
    elif isinstance(obj, dict):
        return {k: substitute_vars(v, variables) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [substitute_vars(item, variables) for item in obj]
    return obj


def find_template_vars(obj):
    found = set()
    if isinstance(obj, str):
        found.update(re.findall(r"\{\{(\w+)\}\}", obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            found.update(find_template_vars(v))
    elif isinstance(obj, list):
        for item in obj:
            found.update(find_template_vars(item))
    return found

# ── Manifest for --resume ────────────────────────────────

def manifest_path(out_dir):
    base = out_dir or "."
    return os.path.join(base, ".pipeline-state.json")


def load_manifest(out_dir):
    path = manifest_path(out_dir)
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)
    return {"steps": {}}


def save_manifest(out_dir, manifest):
    path = manifest_path(out_dir)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)

# ── Validation ───────────────────────────────────────────

def validate_pipeline(steps):
    errors = []
    for i, step in enumerate(steps, 1):
        action = step.get("action")
        if not action:
            errors.append(f"Step {i}: missing 'action' field")
            continue
        if action not in VALID_ACTIONS:
            errors.append(f"Step {i}: invalid action '{action}'. Must be: {', '.join(sorted(VALID_ACTIONS))}")
            continue
        if action in ("generate_video", "generate_image") and "prompt" not in step:
            errors.append(f"Step {i} ({action}): missing 'prompt' field")
        if action == "fan_out":
            if not step.get("use_previous") and not step.get("sources"):
                errors.append(f"Step {i} (fan_out): needs 'use_previous: true' or 'sources' list")
            if "step" not in step:
                errors.append(f"Step {i} (fan_out): missing 'step' template")
        if step.get("use_previous") and i == 1:
            errors.append(f"Step {i}: 'use_previous' cannot be used on the first step")
    if errors:
        print("Pipeline validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

# ── Dry-run cost estimation ──────────────────────────────

def estimate_cu(steps, fan_out_multiplier=4):
    total = 0
    for i, step in enumerate(steps, 1):
        action = step.get("action", "generate_video")
        if action == "fan_out":
            sub = step.get("step", {})
            sub_action = sub.get("action", "generate_video")
            model = sub.get("model", "gen4.5")
            if sub_action == "generate_video":
                cu = estimate_video_credits(model, sub.get("duration", 5))
            elif sub_action == "generate_image":
                cu = estimate_image_credits(model)
            else:
                cu = None
            if cu is not None:
                step_cu = cu * fan_out_multiplier
                total += step_cu
                print(f"  Step {i} (fan_out x ~{fan_out_multiplier}): {sub_action} [{model}] ~{cu} x {fan_out_multiplier} = ~{step_cu} credits", file=sys.stderr)
            else:
                print(f"  Step {i} (fan_out x ~{fan_out_multiplier}): {sub_action} [{model}] = ? credits", file=sys.stderr)
        else:
            model = step.get("model", "gen4.5" if action == "generate_video" else "gen4_image")
            if action == "generate_video":
                cu = estimate_video_credits(model, step.get("duration", 5))
            elif action == "generate_image":
                cu = estimate_image_credits(model)
            else:
                cu = None
            if cu is not None:
                total += cu
                print(f"  Step {i}: {action} [{model}] ~{cu} credits", file=sys.stderr)
            else:
                print(f"  Step {i}: {action} [{model}] = ? credits", file=sys.stderr)

    print(f"\n  Estimated total: ~{total} credits", file=sys.stderr)
    return total

# ── Progress tracker ─────────────────────────────────────

class ProgressTracker:
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.credits_spent = 0
        self.files_saved = 0

    def step_start(self, step_num, action, model=None):
        model_str = f" ({model})" if model else ""
        print(f"\n[Step {step_num}/{self.total_steps}] {action}{model_str}", file=sys.stderr)

    def add_files(self, count):
        self.files_saved += count

    def summary(self):
        print(f"\n  {self.files_saved} files saved", file=sys.stderr)

# ── Parallel fan_out ─────────────────────────────────────

def _run_single_job(api_key, endpoint, body, interval):
    task = api_post(api_key, endpoint, body)
    return poll_task(api_key, task["id"], interval=interval)


def run_fan_out_parallel(api_key, sub_jobs, max_parallel):
    results = [None] * len(sub_jobs)
    semaphore = threading.Semaphore(max_parallel)

    def worker(idx, endpoint, body, interval):
        with semaphore:
            print(f"  --- fan_out {idx + 1}/{len(sub_jobs)} (parallel) ---", file=sys.stderr)
            results[idx] = _run_single_job(api_key, endpoint, body, interval)

    threads = []
    for i, (endpoint, body, interval) in enumerate(sub_jobs):
        t = threading.Thread(target=worker, args=(i, endpoint, body, interval))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results

# ── Build endpoint + body for a step ─────────────────────

def build_request(step, prev_urls, api_key):
    """Return (endpoint, body, poll_interval) for a generation step."""
    action = step.get("action", "generate_video")
    model = step.get("model", "gen4.5" if action == "generate_video" else "gen4_image")

    if action == "generate_video":
        image_url = step.get("image_url")
        if step.get("use_previous") and prev_urls:
            image_url = prev_urls[0]

        if image_url:
            endpoint = "/v1/image_to_video"
            body = {
                "model": model,
                "promptImage": ensure_url(image_url, api_key),
                "promptText": step.get("prompt", ""),
                "ratio": step.get("ratio", "1280:720"),
                "duration": step.get("duration", 5),
            }
        else:
            endpoint = "/v1/text_to_video"
            body = {
                "model": model,
                "promptText": step.get("prompt", ""),
                "ratio": step.get("ratio", "1280:720"),
                "duration": step.get("duration", 5),
            }
        return endpoint, body, 5

    elif action == "generate_image":
        body = {
            "model": model,
            "promptText": step.get("prompt", ""),
            "ratio": step.get("ratio", "1280:720"),
        }
        if step.get("referenceImages"):
            body["referenceImages"] = step["referenceImages"]
        return "/v1/text_to_image", body, 3

    elif action == "generate_audio":
        audio_model = step.get("model", "eleven_multilingual_v2")
        audio_type = step.get("audio_type", "tts")
        endpoint_map = {
            "tts": "/v1/text_to_speech",
            "sfx": "/v1/sound_effect",
            "isolate": "/v1/voice_isolation",
            "dub": "/v1/voice_dubbing",
            "sts": "/v1/speech_to_speech",
        }
        endpoint = endpoint_map.get(audio_type, "/v1/text_to_speech")
        body = {"model": audio_model}
        if audio_type == "tts":
            body["text"] = step.get("text", step.get("prompt", ""))
        elif audio_type == "sfx":
            body["promptText"] = step.get("text", step.get("prompt", ""))
        return endpoint, body, 3

    print(f"Error: Unknown action '{action}'", file=sys.stderr)
    sys.exit(1)

# ── Step execution ───────────────────────────────────────

def run_step(api_key, step, step_num, total, prev_urls, out_dir, progress, max_parallel):
    action = step.get("action", "generate_video")
    model = step.get("model", "")

    if progress:
        progress.step_start(step_num, action, model or None)

    result_urls = []

    if action == "fan_out":
        sources = prev_urls if step.get("use_previous") else step.get("sources", [])
        sub_template = step.get("step")
        if not sub_template or not sources:
            print("Error: fan_out needs 'step' template and sources", file=sys.stderr)
            sys.exit(1)

        parallel = step.get("parallel", False)

        if parallel:
            sub_jobs = []
            sub_infos = []
            for i, src in enumerate(sources):
                sub = dict(sub_template)
                iteration = str(i + 1)
                if "prompt" in sub and "{i}" in sub["prompt"]:
                    sub["prompt"] = sub["prompt"].replace("{i}", iteration)
                if "text" in sub and "{i}" in sub["text"]:
                    sub["text"] = sub["text"].replace("{i}", iteration)
                if "filename" in sub and "{i}" in sub["filename"]:
                    sub["filename"] = sub["filename"].replace("{i}", iteration)

                sub["image_url"] = src
                sub["use_previous"] = False
                endpoint, body, interval = build_request(sub, [src], api_key)
                sub_jobs.append((endpoint, body, interval))
                sub_infos.append(sub)

            results = run_fan_out_parallel(api_key, sub_jobs, max_parallel)

            for i, (result, sub) in enumerate(zip(results, sub_infos)):
                urls = result.get("output", [])
                result_urls.extend(urls)

                ext = ".mp4" if sub.get("action", "generate_video") == "generate_video" else ".png"
                base_name = sub.get("filename", f"step-{step_num}-{i + 1}")
                for j, url in enumerate(urls):
                    fname = f"{base_name}{ext}" if not base_name.endswith(ext) else base_name
                    path = download_file(url, output_path(fname, out_dir))
                    print(f"  Saved: {path}", file=sys.stderr)
                    if progress:
                        progress.add_files(1)
        else:
            for i, src in enumerate(sources):
                print(f"\n  --- fan_out {i + 1}/{len(sources)} ---", file=sys.stderr)
                sub = dict(sub_template)
                iteration = str(i + 1)
                if "prompt" in sub and "{i}" in sub["prompt"]:
                    sub["prompt"] = sub["prompt"].replace("{i}", iteration)
                if "text" in sub and "{i}" in sub["text"]:
                    sub["text"] = sub["text"].replace("{i}", iteration)
                if "filename" in sub and "{i}" in sub["filename"]:
                    sub["filename"] = sub["filename"].replace("{i}", iteration)

                sub["image_url"] = src
                sub["use_previous"] = False
                endpoint, body, interval = build_request(sub, [src], api_key)
                task = api_post(api_key, endpoint, body)
                result = poll_task(api_key, task["id"], interval=interval)
                urls = result.get("output", [])
                result_urls.extend(urls)

                ext = ".mp4" if sub.get("action", "generate_video") == "generate_video" else ".png"
                base_name = sub.get("filename", f"step-{step_num}-{i + 1}")
                for url in urls:
                    fname = f"{base_name}{ext}" if not base_name.endswith(ext) else base_name
                    path = download_file(url, output_path(fname, out_dir))
                    print(f"  Saved: {path}", file=sys.stderr)
                    if progress:
                        progress.add_files(1)
    else:
        endpoint, body, interval = build_request(step, prev_urls, api_key)
        task = api_post(api_key, endpoint, body)
        task_id = task["id"]
        result = poll_task(api_key, task_id, interval=interval)
        urls = result.get("output", [])
        result_urls.extend(urls)

        ext = ".mp4" if action == "generate_video" else ".png" if action == "generate_image" else ".mp3"
        base_name = step.get("filename", f"step-{step_num}")
        for i, url in enumerate(urls):
            if len(urls) == 1:
                fname = f"{base_name}{ext}" if not base_name.endswith(ext) else base_name
            else:
                fname = f"{base_name}-{i + 1}{ext}"
            path = download_file(url, output_path(fname, out_dir))
            print(f"  Saved: {path}", file=sys.stderr)
            if progress:
                progress.add_files(1)

    return result_urls


def main():
    parser = argparse.ArgumentParser(
        description="Run multi-step Runway API pipelines",
        epilog='Example: batch_generate.py --pipeline \'{"steps":[{"action":"generate_video","prompt":"a cat","filename":"cat"}]}\'',
    )
    parser.add_argument("--pipeline", required=True, help="Path to pipeline JSON file, or inline JSON string")
    parser.add_argument("--api-key", help="Runway API key (or set RUNWAYML_API_SECRET)")
    parser.add_argument("--dry-run", action="store_true", help="Estimate credit cost without executing")
    parser.add_argument("--resume", action="store_true", help="Skip completed steps (uses .pipeline-state.json)")
    parser.add_argument("--output-dir", help="Output directory for all generated files")
    parser.add_argument("--max-parallel", type=int, default=3, help="Max concurrent jobs for parallel fan_out (default: 3)")
    parser.add_argument("--var", action="append", metavar="key=value", help="Template variable (repeatable)")
    parser.add_argument("--notify", action="store_true", help="Desktop notification when pipeline finishes")
    args = parser.parse_args()

    if os.path.isfile(args.pipeline):
        with open(args.pipeline) as f:
            raw = f.read()
    else:
        raw = args.pipeline

    variables = {}
    if args.var:
        for v in args.var:
            if "=" not in v:
                print(f"Error: --var must be key=value, got: {v}", file=sys.stderr)
                sys.exit(1)
            key, val = v.split("=", 1)
            variables[key] = val

    if variables:
        for key, val in variables.items():
            raw = raw.replace("{{" + key + "}}", val)

    pipeline = json.loads(raw)

    unresolved = find_template_vars(pipeline)
    if unresolved:
        print(f"Error: Unresolved template variables: {', '.join('{{' + v + '}}' for v in sorted(unresolved))}", file=sys.stderr)
        sys.exit(1)

    steps = pipeline.get("steps", [])
    if not steps:
        print("Error: Pipeline has no steps.", file=sys.stderr)
        sys.exit(1)

    validate_pipeline(steps)

    if args.dry_run:
        print("\n=== Dry Run: Credit Cost Estimate ===\n", file=sys.stderr)
        estimate_cu(steps)
        return

    api_key = get_api_key(args.api_key)
    manifest = load_manifest(args.output_dir) if args.resume else {"steps": {}}

    prev_urls = []
    all_results = []
    progress = ProgressTracker(len(steps))

    for i, step in enumerate(steps, 1):
        step_key = str(i)

        if args.resume and step_key in manifest["steps"]:
            saved = manifest["steps"][step_key]
            saved_urls = saved.get("urls", [])
            print(f"\n[Step {i}/{len(steps)}] Skipping (completed) — {len(saved_urls)} URLs from manifest", file=sys.stderr)
            prev_urls = saved_urls
            all_results.append({"step": i, "action": step.get("action"), "skipped": True, "urls": saved_urls})
            continue

        urls = run_step(api_key, step, i, len(steps), prev_urls, args.output_dir, progress, args.max_parallel)
        prev_urls = urls
        all_results.append({"step": i, "action": step.get("action"), "urls": urls})

        manifest["steps"][step_key] = {"urls": urls, "action": step.get("action")}
        save_manifest(args.output_dir, manifest)

    print("\n=== Pipeline Complete ===", file=sys.stderr)
    progress.summary()
    print(json.dumps(all_results, indent=2))

    if args.notify:
        send_notification("Runway Pipeline Complete", f"{progress.files_saved} files generated")


if __name__ == "__main__":
    main()
