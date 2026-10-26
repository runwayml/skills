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

const CLAUDE_ROOT = join(REPO_ROOT, "claude");
const CLAUDE_MCP_URL = "https://dev.runwayml.com/mcp/claude";

function repoJson(path: string) {
  return JSON.parse(readFileSync(join(REPO_ROOT, path), "utf8"));
}

function skillName(markdown: string) {
  return markdown.match(/^---\nname: (\S+)\n/)?.[1];
}

test("hosts load the same plugin identity", () => {
  const { manifest, files } = buildFiles();
  const json = (path: string) => JSON.parse(files.get(path)?.toString() ?? "");
  for (const native of [
    json(".cursor-plugin/plugin.json"),
    repoJson("claude/.claude-plugin/plugin.json"),
  ]) {
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
  for (const [path, source] of [
    [".claude-plugin/marketplace.json", "./claude"],
    [".agents/plugins/marketplace.json", "./"],
  ]) {
    const entry = repoJson(path).plugins[0];
    assert.equal(
      typeof entry.source === "string" ? entry.source : entry.source.path,
      source,
    );
    assert.equal(entry.name, manifest.name);
    if (entry.version !== undefined) {
      assert.equal(entry.version, manifest.version);
    }
  }
});

test("Claude plugin uses its own MCP endpoint and skill copies", () => {
  assert.equal(
    repoJson("claude/.mcp.json").mcpServers["runway-dev"].url,
    CLAUDE_MCP_URL,
  );
  const claudeSkills = readdirSync(join(CLAUDE_ROOT, "skills"), {
    withFileTypes: true,
  })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
  assert.deepEqual(new Set(claudeSkills), new Set(SKILLS));
  for (const skill of SKILLS) {
    const markdown = readFileSync(
      join(CLAUDE_ROOT, "skills", skill, "SKILL.md"),
      "utf8",
    );
    assert.equal(skillName(markdown), skill);
    for (const forbidden of [
      /create_avatar\b/,
      /requested or approved/i,
      /approved billable/i,
      /dev\.runwayml\.com\/mcp(?!\/claude)\b/,
    ]) {
      assert.doesNotMatch(markdown, forbidden, `${skill}: ${forbidden}`);
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
