#!/usr/bin/env node

/**
 * Validates skill metadata and cross-references.
 *
 * Usage: node scripts/validate-skills.mjs
 */

import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SKILLS_DIR = resolve(ROOT, 'skills');

const errors = [];

function error(message) {
  errors.push(message);
  console.error(`ERROR: ${message}`);
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) {
    return null;
  }

  const fields = {};
  for (const line of match[1].split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) {
      continue;
    }
    const key = line.slice(0, colonIdx).trim();
    let value = line.slice(colonIdx + 1).trim();
    if (value.startsWith('"') && value.endsWith('"')) {
      value = value.slice(1, -1);
    }
    fields[key] = value;
  }
  return fields;
}

const skillDirs = readdirSync(SKILLS_DIR, { withFileTypes: true })
  .filter(entry => entry.isDirectory())
  .map(entry => entry.name);

const validSkillNames = new Set();
const skillFiles = new Map();

for (const dir of skillDirs) {
  const skillPath = resolve(SKILLS_DIR, dir, 'SKILL.md');

  if (!existsSync(skillPath)) {
    error(`${dir}: missing SKILL.md`);
    continue;
  }

  const content = readFileSync(skillPath, 'utf-8');

  if (content.includes('<<<<<<<')) {
    error(`${dir}/SKILL.md: contains unresolved merge conflict markers`);
  }

  const frontmatter = parseFrontmatter(content);

  if (!frontmatter) {
    error(`${dir}/SKILL.md: missing or invalid frontmatter`);
    continue;
  }

  if (!frontmatter.name) {
    error(`${dir}/SKILL.md: frontmatter missing required field "name"`);
  } else if (frontmatter.name !== dir) {
    error(
      `${dir}/SKILL.md: frontmatter name "${frontmatter.name}" does not match directory "${dir}"`
    );
  }

  if (!frontmatter.description) {
    error(`${dir}/SKILL.md: frontmatter missing required field "description"`);
  }

  validSkillNames.add(dir);
  skillFiles.set(dir, content);
}

const SKILL_REF_PATTERN = /`\+([a-z][-a-z0-9]+)`|\b\+([a-z][-a-z0-9]+)(?=[\s,.;:|)\]]|$)/g;

for (const [dir, content] of skillFiles) {
  let match;
  while ((match = SKILL_REF_PATTERN.exec(content)) !== null) {
    const refName = match[1] ?? match[2];
    if (!validSkillNames.has(refName)) {
      error(`${dir}/SKILL.md: references non-existent skill "+${refName}"`);
    }
  }
}

if (errors.length > 0) {
  console.error(`\n${errors.length} error(s) found.`);
  process.exit(1);
}

console.log(`Validated ${validSkillNames.size} skills — all checks passed.`);
