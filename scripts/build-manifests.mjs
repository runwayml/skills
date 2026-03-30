#!/usr/bin/env node

/**
 * Generates platform-specific plugin manifests from the shared
 * plugin-metadata.json so the two files never drift apart.
 *
 * Usage:
 *   node scripts/build-manifests.mjs          # write manifests
 *   node scripts/build-manifests.mjs --check  # exit 1 if manifests are stale
 */

import { readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const META_PATH = resolve(ROOT, "plugin-metadata.json");

const meta = JSON.parse(readFileSync(META_PATH, "utf-8"));

function cursorManifest(meta) {
  return {
    name: meta.name,
    displayName: meta.displayName,
    version: meta.version,
    description: meta.description,
    author: meta.author,
    homepage: meta.homepage,
    repository: meta.repository,
    license: meta.license,
    logo: meta.logo,
    keywords: meta.keywords,
    category: meta.category,
    tags: meta.tags,
    skills: "./skills/",
  };
}

function claudeManifest(meta) {
  return {
    name: meta.name,
    description: meta.description,
    version: meta.version,
    author: meta.author,
    keywords: meta.keywords,
  };
}

const manifests = [
  {
    path: resolve(ROOT, ".cursor-plugin/plugin.json"),
    data: cursorManifest(meta),
  },
  {
    path: resolve(ROOT, ".claude-plugin/plugin.json"),
    data: claudeManifest(meta),
  },
];

const isCheck = process.argv.includes("--check");
let stale = false;

for (const { path, data } of manifests) {
  const content = JSON.stringify(data, null, 2) + "\n";

  if (isCheck) {
    let existing = "";
    try {
      existing = readFileSync(path, "utf-8");
    } catch {
      // file missing counts as stale
    }
    if (existing !== content) {
      const rel = path.replace(ROOT + "/", "");
      console.error(`STALE: ${rel} — run \`node scripts/build-manifests.mjs\` to regenerate`);
      stale = true;
    }
  } else {
    writeFileSync(path, content);
    const rel = path.replace(ROOT + "/", "");
    console.log(`wrote ${rel}`);
  }
}

if (isCheck && stale) {
  process.exit(1);
}
