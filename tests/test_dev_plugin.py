import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


SCRIPT = Path(__file__).resolve().parent.parent / "scripts/build_dev_plugin.py"
SPEC = importlib.util.spec_from_file_location("build_dev_plugin", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class DevPluginPackagingTests(unittest.TestCase):
    def test_hosts_load_the_same_root_plugin(self):
        manifest, files = builder.build_files(builder.REPO_ROOT)
        for host in ("claude", "cursor"):
            native = json.loads(files[Path(f".{host}-plugin/plugin.json")])
            self.assertEqual(native["name"], manifest["name"])
            self.assertEqual(native["version"], manifest["version"])
            self.assertEqual(native["displayName"], "Runway Dev")
        cursor = json.loads(files[Path(".cursor-plugin/plugin.json")])
        self.assertEqual({Path(p).name for p in cursor["skills"]}, set(builder.SKILLS))
        for directory in cursor["skills"]:
            self.assertIn(Path(directory) / "SKILL.md", files)
        self.assertEqual(
            json.loads(files[Path(cursor["mcpServers"])])["mcpServers"]["runway-dev"][
                "url"
            ],
            json.loads(files[Path("mcp.json")])["mcpServers"]["runway-dev"]["url"],
        )
        active = {
            p.parent.name for p in (builder.REPO_ROOT / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(active, set(builder.SKILLS))
        for path in (
            ".claude-plugin/marketplace.json",
            ".agents/plugins/marketplace.json",
        ):
            entry = json.loads((builder.REPO_ROOT / path).read_text())["plugins"][0]
            source = entry["source"]
            self.assertEqual(
                source if isinstance(source, str) else source["path"], "./"
            )
            self.assertEqual(entry["name"], manifest["name"])

    def test_export_is_reproducible_and_excludes_unselected_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            shutil.copytree(
                builder.REPO_ROOT, root, ignore=shutil.ignore_patterns(".git", ".build")
            )
            (root / ".env").write_text("private\n")
            (root / "skills/runway-dev/.env").write_text("private\n")
            (root / "skills/runway-dev/extra.md").write_text("not selected\n")
            manifest, files = builder.build_files(root)
            first, second = (
                Path(directory) / "first.zip",
                Path(directory) / "second.zip",
            )
            builder.write_archive(first, manifest["name"], files)
            builder.write_archive(second, manifest["name"], files)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(
                    set(archive.namelist()), {f"runway-api/{p}" for p in builder.FILES}
                )
                for path, data in files.items():
                    self.assertEqual(archive.read(f"runway-api/{path}"), data)

    def test_export_rejects_symlink_files_and_parent_directories(self):
        for relative in ("plugin.json", "skills"):
            with (
                self.subTest(relative=relative),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory) / "repo"
                shutil.copytree(
                    builder.REPO_ROOT,
                    root,
                    ignore=shutil.ignore_patterns(".git", ".build"),
                )
                target = root / relative
                outside = Path(directory) / "outside"
                target.rename(outside)
                target.symlink_to(outside, target_is_directory=outside.is_dir())
                with self.assertRaisesRegex(ValueError, "Symlinks cannot be bundled"):
                    builder.build_files(root)


if __name__ == "__main__":
    unittest.main()
