#!/usr/bin/env python3
"""Export the root Runway Dev plugin as a reproducible, allowlisted ZIP."""

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = (
    "runway-dev",
    "runway-dev-setup",
    "runway-dev-models",
    "runway-dev-model-routers",
    "runway-dev-characters",
    "runway-dev-recipes",
    "runway-dev-workflows",
)
FILES = (
    "plugin.json",
    "mcp.json",
    ".mcp.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    "README.md",
    "LICENSE",
    "assets/logo.png",
    *(f"skills/{skill}/SKILL.md" for skill in SKILLS),
)


def build_files(root):
    files = {}
    for relative in FILES:
        path = root
        for part in Path(relative).parts:
            path = path / part
            if path.is_symlink():
                raise ValueError(f"Symlinks cannot be bundled: {path}")
        files[Path(relative)] = path.read_bytes()
    return json.loads(files[Path("plugin.json")]), files


def write_archive(output, name, files):
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path, data in sorted(files.items()):
            info = ZipInfo(f"{name}/{path.as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="ZIP output path")
    args = parser.parse_args()
    manifest, files = build_files(REPO_ROOT)
    output = (
        args.output
        or REPO_ROOT / ".build" / f"{manifest['name']}-{manifest['version']}.zip"
    )
    write_archive(output, manifest["name"], files)
    print(f"Exported {len(files)} root plugin files to {output}")


if __name__ == "__main__":
    main()
