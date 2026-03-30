#!/usr/bin/env node

/**
 * Generates the "Available Skills" section in README.md from skill frontmatter.
 * Hand-written content outside the markers is preserved.
 *
 * Usage:
 *   node scripts/build-readme.mjs          # write README.md
 *   node scripts/build-readme.mjs --check  # exit 1 if section is stale
 */

import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = resolve(ROOT, "skills");
const README_PATH = resolve(ROOT, "README.md");

const START_MARKER = "<!-- GENERATED:SKILLS:START -->";
const END_MARKER = "<!-- GENERATED:SKILLS:END -->";

const CATEGORIES = [
  {
    title: "Getting Started",
    skills: ["recipe-full-setup", "check-compatibility", "setup-api-key", "check-org-details"],
  },
  {
    title: "Generation",
    skills: ["integrate-video", "integrate-image", "integrate-audio"],
  },
  {
    title: "Characters (Real-Time Avatars)",
    skills: ["integrate-characters", "integrate-character-embed", "integrate-documents"],
  },
  {
    title: "Utilities",
    skills: ["integrate-uploads", "api-reference", "fetch-api-reference"],
  },
];

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const fields = {};
  for (const line of match[1].split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let value = line.slice(colonIdx + 1).trim();
    if (value.startsWith('"') && value.endsWith('"')) {
      value = value.slice(1, -1);
    }
    fields[key] = value;
  }
  return fields;
}

function loadSkills() {
  const skills = new Map();
  const dirs = readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);

  for (const dir of dirs) {
    try {
      const content = readFileSync(resolve(SKILLS_DIR, dir, "SKILL.md"), "utf-8");
      const fm = parseFrontmatter(content);
      if (fm) {
        skills.set(dir, fm);
      }
    } catch {
      // skip directories without SKILL.md
    }
  }
  return skills;
}

function padColumn(rows, colIdx) {
  return Math.max(...rows.map((row) => row[colIdx].length));
}

function buildTable(headers, rows) {
  const widths = headers.map((_, i) => padColumn([headers, ...rows], i));
  const formatRow = (row) =>
    "| " + row.map((cell, i) => cell.padEnd(widths[i])).join(" | ") + " |";

  return [
    formatRow(headers),
    "| " + widths.map((w) => "-".repeat(w)).join(" | ") + " |",
    ...rows.map(formatRow),
  ].join("\n");
}

function generateSection(skills) {
  const categorized = new Set();
  const sections = [];

  for (const category of CATEGORIES) {
    const rows = [];
    for (const name of category.skills) {
      const fm = skills.get(name);
      if (!fm) continue;
      rows.push([`\`${name}\``, fm.description]);
      categorized.add(name);
    }
    if (rows.length > 0) {
      sections.push(`### ${category.title}\n\n${buildTable(["Skill", "Description"], rows)}`);
    }
  }

  const uncategorized = [...skills.entries()]
    .filter(([name]) => !categorized.has(name))
    .map(([name, fm]) => [`\`${name}\``, fm.description]);

  if (uncategorized.length > 0) {
    sections.push(`### Other\n\n${buildTable(["Skill", "Description"], uncategorized)}`);
  }

  return sections.join("\n\n");
}

const skills = loadSkills();
const generated = generateSection(skills);

const readme = readFileSync(README_PATH, "utf-8");

const startIdx = readme.indexOf(START_MARKER);
const endIdx = readme.indexOf(END_MARKER);

let newReadme;

if (startIdx !== -1 && endIdx !== -1) {
  newReadme =
    readme.slice(0, startIdx + START_MARKER.length) +
    "\n\n" +
    generated +
    "\n\n" +
    readme.slice(endIdx);
} else {
  console.error(
    `Markers not found in README.md. Add these markers around the skills section:\n  ${START_MARKER}\n  ${END_MARKER}`,
  );
  process.exit(1);
}

const isCheck = process.argv.includes("--check");

if (isCheck) {
  if (readme !== newReadme) {
    console.error("STALE: README.md skills section — run `node scripts/build-readme.mjs` to regenerate");
    process.exit(1);
  }
  console.log("README.md skills section is up to date.");
} else {
  writeFileSync(README_PATH, newReadme);
  console.log("wrote README.md skills section");
}
