import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


SCRIPT = Path(__file__).resolve().parent.parent / "scripts/build_dev_plugin.py"
SPEC = importlib.util.spec_from_file_location("build_dev_plugin", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class DevPluginPackagingTests(unittest.TestCase):
    def test_host_manifests_resolve_the_same_dev_bundle(self):
        manifest, package, files = builder.generated_files(builder.REPO_ROOT)
        cursor = json.loads(files[Path(".cursor-plugin/plugin.json")])
        self.assertEqual(cursor["version"], manifest["version"])
        selected = set()
        for directory in cursor["skills"]:
            path = Path(directory.removeprefix("./"))
            self.assertIn(path / "SKILL.md", files)
            selected.add(path.name)
        self.assertEqual(selected, set(builder.SKILLS))
        native = json.loads(files[Path(cursor["mcpServers"].removeprefix("./"))])
        portable = json.loads(package[Path("mcp.json")])
        self.assertEqual(
            native["mcpServers"]["runway-dev"]["url"],
            portable["mcpServers"]["runway-dev"]["url"],
        )
        for marketplace_path in (
            ".claude-plugin/marketplace.json",
            ".agents/plugins/marketplace.json",
        ):
            entry = json.loads(files[Path(marketplace_path)])["plugins"][0]
            source = entry["source"]
            source_path = source if isinstance(source, str) else source["path"]
            self.assertEqual(entry["name"], manifest["name"])
            self.assertIn(Path(source_path.removeprefix("./")) / "plugin.json", files)

    def test_archive_contains_only_dev_package_and_is_reproducible(self):
        manifest, package = builder.build_files(builder.REPO_ROOT)
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            builder.write_archive(first, manifest["name"], package)
            builder.write_archive(second, manifest["name"], package)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                names = set(archive.namelist())
                self.assertEqual(
                    names, {f"{manifest['name']}/{path.as_posix()}" for path in package}
                )
                self.assertIn("runway-api/.mcp.json", names)
                self.assertIn("runway-api/.claude-plugin/plugin.json", names)
                skills = {
                    name.split("/")[2]
                    for name in names
                    if name.startswith("runway-api/skills/")
                }
                self.assertEqual(skills, set(builder.SKILLS))
                self.assertFalse(any("rw-generate" in name for name in names))
                self.assertFalse(any(".env" in name or "._" in name for name in names))

    def test_check_rejects_stale_and_extra_generated_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {builder.PLUGIN_PATH / "README.md": b"Current docs\n"}
            builder.write_generated(root, files)
            self.assertEqual(builder.check_generated(root, files), [])
            (root / builder.PLUGIN_PATH / "README.md").write_text("Old docs\n")
            (root / builder.PLUGIN_PATH / "unexpected.env").write_text("private\n")
            errors = builder.check_generated(root, files)
            self.assertEqual(len(errors), 2)

    def test_rejects_file_and_parent_directory_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside"
            outside.mkdir()
            (outside / "SKILL.md").write_text("unrelated content\n")
            (root / "skills").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.contained_path(root, Path("skills/SKILL.md"))
            package = root / "package"
            package.mkdir()
            (package / "SKILL.md").symlink_to(outside / "SKILL.md")
            with self.assertRaises(ValueError):
                builder.read_tree(package)


if __name__ == "__main__":
    unittest.main()
