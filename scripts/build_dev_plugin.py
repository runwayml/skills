#!/usr/bin/env python3
"""Build the Dev-only plugin from the repository's canonical skills and metadata."""

import argparse
import json
import shutil
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_PATH = Path("plugins/runway-api")
SKILLS = (
    "runway-dev",
    "runway-dev-setup",
    "runway-dev-models",
    "runway-dev-model-routers",
    "runway-dev-characters",
    "runway-dev-recipes",
    "runway-dev-workflows",
)
MCP_URL = "https://dev.runwayml.com/mcp"


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def contained_path(root, relative):
    path = root
    for part in relative.parts:
        if part in ("..", "/"):
            raise ValueError(f"Path must stay inside the repository: {relative}")
        path = path / part
        if path.is_symlink():
            raise ValueError(f"Symlinks cannot be bundled or overwritten: {path}")
    return path


def read_tree(directory):
    if directory.is_symlink():
        raise ValueError(f"Symlinks cannot be bundled: {directory}")
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks cannot be bundled: {path}")
        if path.is_file():
            files[path.relative_to(directory)] = path.read_bytes()
    return files


def build_files(root):
    manifest = json.loads(contained_path(root, Path("plugin/plugin.json")).read_text())
    files = {
        Path("plugin.json"): json_bytes(manifest),
        Path("README.md"): contained_path(root, Path("plugin/README.md")).read_bytes(),
        Path("LICENSE"): contained_path(root, Path("LICENSE")).read_bytes(),
        Path("assets/logo.png"): contained_path(
            root, Path("assets/logo.png")
        ).read_bytes(),
        Path("mcp.json"): json_bytes(
            {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {
                    "runway-dev": {"type": "streamable-http", "url": MCP_URL}
                },
            }
        ),
        Path(".mcp.json"): json_bytes(
            {"mcpServers": {"runway-dev": {"type": "http", "url": MCP_URL}}}
        ),
        Path(".claude-plugin/plugin.json"): json_bytes(
            {
                key: manifest[key]
                for key in (
                    "name",
                    "version",
                    "description",
                    "author",
                    "homepage",
                    "repository",
                    "license",
                    "keywords",
                )
            }
        ),
    }
    for skill in SKILLS:
        source = contained_path(root, Path("skills") / skill)
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Missing skill: {skill}")
        files.update(
            {
                Path("skills") / skill / path: data
                for path, data in read_tree(source).items()
            }
        )
    return manifest, files


def generated_files(root):
    manifest, package = build_files(root)
    files = {PLUGIN_PATH / path: data for path, data in package.items()}
    files[Path(".claude-plugin/marketplace.json")] = json_bytes(
        {
            "name": "runway-dev",
            "owner": {"name": "Runway"},
            "metadata": {
                "description": "Runway Dev MCP and application integration skills"
            },
            "plugins": [
                {
                    "name": manifest["name"],
                    "source": "./plugins/runway-api",
                    "version": manifest["version"],
                    "description": manifest["description"],
                }
            ],
        }
    )
    files[Path(".agents/plugins/marketplace.json")] = json_bytes(
        {
            "name": "runway-dev",
            "interface": {"displayName": "Runway Dev"},
            "plugins": [
                {
                    "name": manifest["name"],
                    "source": {"source": "local", "path": "./plugins/runway-api"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
                    "category": "Developer Tools",
                }
            ],
        }
    )
    files[Path(".cursor-plugin/plugin.json")] = json_bytes(
        {
            "name": "runway-dev",
            "displayName": "Runway Dev",
            "version": manifest["version"],
            "description": manifest["description"],
            "author": manifest["author"],
            "homepage": manifest["homepage"],
            "repository": manifest["repository"],
            "license": manifest["license"],
            "logo": "./assets/logo.png",
            "keywords": manifest["keywords"],
            "category": "design",
            "tags": ["api-integration", "sdk", "mcp", "video", "image", "audio"],
            "skills": [f"./plugins/runway-api/skills/{skill}" for skill in SKILLS],
            "mcpServers": "./plugins/runway-api/.mcp.json",
        }
    )
    return manifest, package, files


def check_generated(root, files):
    actual_package = {
        PLUGIN_PATH / path for path in read_tree(contained_path(root, PLUGIN_PATH))
    }
    expected_package = {path for path in files if path.is_relative_to(PLUGIN_PATH)}
    errors = [
        f"Unexpected generated file: {path}"
        for path in sorted(actual_package - expected_package)
    ]
    for path, expected in files.items():
        target = contained_path(root, path)
        if (
            target.is_symlink()
            or not target.is_file()
            or target.read_bytes() != expected
        ):
            errors.append(f"Generated file is missing or stale: {path}")
    return errors


def write_generated(root, files):
    for path in files:
        contained_path(root, path)
    destination = contained_path(root, PLUGIN_PATH)
    if destination.exists():
        shutil.rmtree(destination)
    for path, data in files.items():
        target = contained_path(root, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            raise ValueError(f"Generated file path is a symlink: {target}")
        target.write_bytes(data)


def write_archive(output, name, package):
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path, data in sorted(package.items()):
            info = ZipInfo(f"{name}/{path.as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail on stale generated files"
    )
    parser.add_argument(
        "--zip", action="store_true", help="Also write a reproducible ZIP"
    )
    parser.add_argument("--output", type=Path, help="ZIP output path")
    args = parser.parse_args()
    if args.output and not args.zip:
        parser.error("--output requires --zip")
    manifest, package, files = generated_files(REPO_ROOT)
    if args.check:
        errors = check_generated(REPO_ROOT, files)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
    else:
        write_generated(REPO_ROOT, files)
    if args.zip:
        output = (
            args.output
            or REPO_ROOT / ".build" / f"{manifest['name']}-{manifest['version']}.zip"
        )
        write_archive(output, manifest["name"], package)
        print(output)
    print(f"Verified {len(SKILLS)} Dev skills and {len(package)} package files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
