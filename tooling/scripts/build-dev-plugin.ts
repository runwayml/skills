import { lstatSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { parseArgs } from "node:util";
import AdmZip from "adm-zip";

export const REPO_ROOT = resolve(import.meta.dirname, "../..");
export const SKILLS = [
  "runway-dev",
  "runway-dev-setup",
  "runway-dev-models",
  "runway-dev-model-routers",
  "runway-dev-characters",
  "runway-dev-recipes",
  "runway-dev-workflows",
];
export const FILES = [
  "plugin.json",
  "mcp.json",
  ".mcp.json",
  ".claude-plugin/plugin.json",
  ".cursor-plugin/plugin.json",
  "README.md",
  "LICENSE",
  "assets/logo.png",
  ...SKILLS.map((skill) => `skills/${skill}/SKILL.md`),
];

export function buildFiles(root = REPO_ROOT) {
  const files = new Map<string, Buffer>();
  for (const relative of FILES) {
    let path = root;
    for (const part of relative.split("/")) {
      path = resolve(path, part);
      if (lstatSync(path).isSymbolicLink()) {
        throw new Error(`Symlinks cannot be bundled: ${path}`);
      }
    }
    files.set(relative, readFileSync(path));
  }
  const manifest = JSON.parse(files.get("plugin.json")?.toString() ?? "") as {
    name: string;
    version: string;
  };
  return { manifest, files };
}

export function writeArchive(
  output: string,
  name: string,
  files: Map<string, Buffer>,
) {
  const archive = new AdmZip(undefined, { noSort: true });
  for (const path of [...files.keys()].sort()) {
    const entry = archive.addFile(
      `${name}/${path}`,
      files.get(path) as Buffer,
      "",
      0o644,
    );
    entry.header.time = new Date(2026, 0, 1);
  }
  mkdirSync(dirname(output), { recursive: true });
  archive.writeZip(output);
}

if (import.meta.main) {
  const { values } = parseArgs({ options: { output: { type: "string" } } });
  const { manifest, files } = buildFiles();
  const output = resolve(
    values.output ??
      `${REPO_ROOT}/.build/${manifest.name}-${manifest.version}.zip`,
  );
  writeArchive(output, manifest.name, files);
  console.log(`Exported ${files.size} root plugin files to ${output}`);
}
