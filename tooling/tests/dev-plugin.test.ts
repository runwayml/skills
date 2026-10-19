import assert from "node:assert/strict";
import {
  copyFileSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  renameSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join } from "node:path";
import { test } from "node:test";
import AdmZip from "adm-zip";
import {
  buildFiles,
  FILES,
  REPO_ROOT,
  SKILLS,
  writeArchive,
} from "../scripts/build-dev-plugin.ts";

function fixture(run: (root: string, directory: string) => void) {
  const directory = mkdtempSync(join(tmpdir(), "runway-dev-plugin-"));
  const root = join(directory, "repo");
  try {
    for (const relative of FILES) {
      const target = join(root, relative);
      mkdirSync(dirname(target), { recursive: true });
      copyFileSync(join(REPO_ROOT, relative), target);
    }
    run(root, directory);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

test("hosts load the same root plugin", () => {
  const { manifest, files } = buildFiles();
  const json = (path: string) => JSON.parse(files.get(path)?.toString() ?? "");
  for (const host of ["claude", "cursor"]) {
    const native = json(`.${host}-plugin/plugin.json`);
    assert.equal(native.name, manifest.name);
    assert.equal(native.version, manifest.version);
    assert.equal(native.displayName, "Runway Dev");
  }
  const cursor = json(".cursor-plugin/plugin.json");
  assert.deepEqual(
    new Set(cursor.skills.map((path: string) => basename(path))),
    new Set(SKILLS),
  );
  for (const directory of cursor.skills) {
    assert(files.has(`${directory.replace(/^\.\//, "")}/SKILL.md`));
  }
  assert.equal(
    json(cursor.mcpServers.replace(/^\.\//, "")).mcpServers["runway-dev"].url,
    json("mcp.json").mcpServers["runway-dev"].url,
  );
  const active = readdirSync(join(REPO_ROOT, "skills"), { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
  assert.deepEqual(new Set(active), new Set(SKILLS));
  for (const path of [
    ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
  ]) {
    const entry = JSON.parse(readFileSync(join(REPO_ROOT, path), "utf8"))
      .plugins[0];
    assert.equal(
      typeof entry.source === "string" ? entry.source : entry.source.path,
      "./",
    );
    assert.equal(entry.name, manifest.name);
    if (entry.version !== undefined) {
      assert.equal(entry.version, manifest.version);
    }
  }
});

test("export is reproducible and excludes unselected files", () => {
  fixture((root, directory) => {
    for (const relative of [
      ".env",
      "skills/runway-dev/.env",
      "skills/runway-dev/extra.md",
      "legacy/skills/old/SKILL.md",
    ]) {
      const target = join(root, relative);
      mkdirSync(dirname(target), { recursive: true });
      writeFileSync(target, "not selected\n");
    }
    const { manifest, files } = buildFiles(root);
    const first = join(directory, "first.zip");
    const second = join(directory, "second.zip");
    writeArchive(first, manifest.name, files);
    writeArchive(second, manifest.name, files);
    assert.deepEqual(readFileSync(first), readFileSync(second));
    const entries = new AdmZip(first).getEntries();
    assert.deepEqual(
      new Set(entries.map((entry) => entry.entryName)),
      new Set(FILES.map((path) => `runway-api/${path}`)),
    );
    for (const entry of entries) {
      assert.deepEqual(
        entry.getData(),
        files.get(entry.entryName.replace(/^runway-api\//, "")),
      );
    }
  });
});

test("export rejects symlink files and parent directories", () => {
  for (const relative of ["plugin.json", "skills"]) {
    fixture((root, directory) => {
      const target = join(root, relative);
      const outside = join(directory, "outside");
      renameSync(target, outside);
      symlinkSync(outside, target, relative === "skills" ? "dir" : "file");
      assert.throws(() => buildFiles(root), /Symlinks cannot be bundled/);
    });
  }
});
