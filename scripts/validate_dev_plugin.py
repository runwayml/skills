#!/usr/bin/env python3
"""Validate the exact plugin ZIP against portable schemas and listing requirements."""

import argparse
import json
import re
import struct
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

import jsonschema
import yaml

from build_dev_plugin import REPO_ROOT, SKILLS


def validate(archive_path, schemas):
    with ZipFile(archive_path) as archive:
        assert archive.testzip() is None, "Corrupt archive"
        names = archive.namelist()
        assert len(names) == len(set(names)), "Duplicate archive members"
        assert all(
            not PurePosixPath(name).is_absolute()
            and ".." not in PurePosixPath(name).parts
            for name in names
        ), "Unsafe archive paths"
        roots = {name.split("/")[0] for name in names}
        assert len(roots) == 1, "Archive needs exactly one plugin root"
        prefix = f"{next(iter(roots))}/"
        members = {name[len(prefix) :]: archive.read(name) for name in names}
        assert not any(
            name == ".app.json" or name.startswith(("scripts/", "node_modules/"))
            for name in members
        ), "Unexpected plugin contents"
        manifest = json.loads(members["plugin.json"])
        mcp = json.loads(members["mcp.json"])
        for document, schema_name in ((manifest, "plugin"), (mcp, "mcp")):
            schema = json.loads((schemas / f"{schema_name}.schema.json").read_text())
            jsonschema.Draft202012Validator(schema).validate(document)
        assert prefix == f"{manifest['name']}/", "Plugin folder and identity differ"
        assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), (
            "Use an explicit release version"
        )
        openai = manifest["extensions"]["com.openai"]
        assert not openai.get("apps"), "Public upload cannot include app bindings"
        assert openai["onboardingSkill"].removeprefix("./") in members
        interface = openai["interface"]
        for key, maximum in (
            ("displayName", 30),
            ("shortDescription", 30),
            ("longDescription", 4000),
            ("developerName", 80),
        ):
            assert 0 < len(interface[key]) <= maximum, f"Invalid {key} length"
        for key in (
            "websiteURL",
            "supportURL",
            "privacyPolicyURL",
            "termsOfServiceURL",
        ):
            assert interface[key].startswith("https://") and len(interface[key]) <= 1024
        prompts = interface["defaultPrompt"]
        assert 1 <= len(prompts) <= 3 and len(set(prompts)) == len(prompts)
        assert all(0 < len(prompt) <= 128 and "\n" not in prompt for prompt in prompts)
        for key in ("logo", "composerIcon"):
            image = members[interface[key].removeprefix("./")]
            assert image.startswith(b"\x89PNG\r\n\x1a\n"), "Expected PNG branding"
            width, height = struct.unpack(">II", image[16:24])
            assert (
                width == height
                and 256 <= width <= 4096
                and len(image) <= 5 * 1024 * 1024
            )
        included_skills = set()
        for name, data in members.items():
            if name.startswith("skills/") and name.endswith("/SKILL.md"):
                frontmatter = data.decode().split("---", 2)[1]
                metadata = yaml.safe_load(frontmatter)
                skill = name.split("/")[1]
                assert metadata["name"] == skill and metadata["description"].strip()
                included_skills.add(skill)
        assert included_skills == set(SKILLS), "Unexpected or missing skills"
        cases = openai["review"]["test_cases"]
        assert len(cases["positive"]) == 5 and len(cases["negative"]) == 3
        for kind, items in cases.items():
            for case in items:
                for key in ("description", "prompt", "expected_behavior"):
                    assert isinstance(case[key], str) and case[key].strip()
                if kind == "positive":
                    assert (
                        isinstance(case["tools_triggered"], str)
                        and case["tools_triggered"].strip()
                    )
        native = json.loads(members[".claude-plugin/plugin.json"])
        assert (
            native["name"] == manifest["name"]
            and native["version"] == manifest["version"]
        )
        return manifest["name"], manifest["version"], len(members)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--schemas", type=Path, default=REPO_ROOT / ".build/schemas")
    args = parser.parse_args()
    name, version, count = validate(args.archive, args.schemas)
    print(
        f"Validated {name} {version}: {count} files, 7 skills, 5 positive and 3 negative review cases"
    )
    print(
        "Package validation does not establish host OAuth, reviewer access, or submission readiness."
    )


if __name__ == "__main__":
    main()
