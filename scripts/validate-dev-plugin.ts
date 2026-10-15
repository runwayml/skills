import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { parseArgs } from "node:util";
import AdmZip from "adm-zip";
import { Ajv2020 } from "ajv/dist/2020.js";
import { parse } from "yaml";
import { FILES, REPO_ROOT, SKILLS } from "./build-dev-plugin.ts";

export function validateArchive(
  archivePath: string,
  schemas = resolve(REPO_ROOT, ".build/schemas"),
) {
  const entries = new AdmZip(archivePath).getEntries();
  const names = entries.map((entry) => entry.entryName);
  assert.equal(names.length, new Set(names).size, "Duplicate archive members");
  assert(
    names.every(
      (name) =>
        !name.startsWith("/") &&
        !name.includes("\\") &&
        !name.split("/").some((part) => part === ".." || part === "."),
    ),
    "Unsafe archive paths",
  );
  const roots = new Set(names.map((name) => name.split("/")[0]));
  assert.equal(roots.size, 1, "Archive needs exactly one plugin root");
  const prefix = `${[...roots][0]}/`;
  const members = new Map(
    entries.map((entry) => {
      const data = entry.getData();
      assert(
        data.length > 0 && data.length === entry.header.size,
        "Empty or corrupt archive member",
      );
      return [entry.entryName.slice(prefix.length), data];
    }),
  );
  assert.deepEqual(
    [...members.keys()].sort(),
    [...FILES].sort(),
    "Unexpected plugin contents",
  );
  const bytes = (name: string) => {
    const data = members.get(name);
    assert(data, `Missing ${name}`);
    return data;
  };
  const json = (name: string) => JSON.parse(bytes(name).toString());
  const manifest = json("plugin.json");
  const ajv = new Ajv2020({ allErrors: true });
  for (const [document, schemaName] of [
    [manifest, "plugin"],
    [json("mcp.json"), "mcp"],
  ]) {
    const schema = JSON.parse(
      readFileSync(resolve(schemas, `${schemaName}.schema.json`), "utf8"),
    );
    const valid = ajv.compile(schema);
    assert(valid(document), ajv.errorsText(valid.errors));
  }
  assert.equal(
    prefix,
    `${manifest.name}/`,
    "Plugin folder and identity differ",
  );
  assert.match(
    manifest.version,
    /^\d+\.\d+\.\d+$/,
    "Use an explicit release version",
  );
  const openai = manifest.extensions["com.openai"];
  assert(!openai.apps, "Public upload cannot include app bindings");
  assert(members.has(openai.onboardingSkill.replace(/^\.\//, "")));
  const ui = openai.interface;
  for (const [key, maximum] of Object.entries({
    displayName: 30,
    shortDescription: 30,
    longDescription: 4000,
    developerName: 80,
  })) {
    assert(
      typeof ui[key] === "string" &&
        ui[key].length > 0 &&
        [...ui[key]].length <= maximum,
      `Invalid ${key} length`,
    );
  }
  for (const key of [
    "websiteURL",
    "supportURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
  ]) {
    assert(
      typeof ui[key] === "string" &&
        ui[key].startsWith("https://") &&
        ui[key].length <= 1024,
      `Invalid ${key}`,
    );
  }
  const prompts = ui.defaultPrompt;
  assert(Array.isArray(prompts) && prompts.length >= 1 && prompts.length <= 3);
  assert.equal(
    new Set(prompts).size,
    prompts.length,
    "Duplicate starter prompts",
  );
  assert(
    prompts.every(
      (prompt) =>
        typeof prompt === "string" &&
        prompt.length > 0 &&
        [...prompt].length <= 128 &&
        !prompt.includes("\n"),
    ),
  );
  for (const key of ["logo", "composerIcon"]) {
    const image = bytes(ui[key].replace(/^\.\//, ""));
    assert(
      image.subarray(0, 8).equals(Buffer.from("89504e470d0a1a0a", "hex")),
      "Expected PNG branding",
    );
    const width = image.readUInt32BE(16);
    const height = image.readUInt32BE(20);
    assert(
      width === height &&
        width >= 256 &&
        width <= 4096 &&
        image.length <= 5 * 1024 * 1024,
      "Invalid branding dimensions or size",
    );
  }
  const includedSkills = new Set<string>();
  for (const [name, data] of members) {
    if (name.startsWith("skills/") && name.endsWith("/SKILL.md")) {
      const metadata = parse(data.toString().split("---", 3)[1]);
      const skill = name.split("/")[1];
      assert(
        metadata.name === skill &&
          typeof metadata.description === "string" &&
          metadata.description.trim(),
        `Invalid skill metadata: ${skill}`,
      );
      includedSkills.add(skill);
    }
  }
  assert.deepEqual(
    includedSkills,
    new Set(SKILLS),
    "Unexpected or missing skills",
  );
  const cases = openai.review?.test_cases;
  if (cases != null) {
    assert.equal(cases.positive.length, 5);
    assert.equal(cases.negative.length, 3);
    for (const [kind, items] of Object.entries(cases)) {
      assert(Array.isArray(items));
      for (const item of items) {
        for (const key of [
          "description",
          "prompt",
          "expected_behavior",
          ...(kind === "positive" ? ["tools_triggered"] : []),
        ]) {
          assert(
            typeof item[key] === "string" && item[key].trim(),
            `Missing review case ${key}`,
          );
        }
      }
    }
  }
  const native = json(".claude-plugin/plugin.json");
  assert(
    native.name === manifest.name && native.version === manifest.version,
    "Native Claude identity differs",
  );
  return {
    name: manifest.name,
    version: manifest.version,
    files: members.size,
  };
}

if (import.meta.main) {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: { schemas: { type: "string" } },
  });
  assert(
    positionals.length <= 1,
    "Usage: validate-dev-plugin.ts [archive] [--schemas directory]",
  );
  const result = validateArchive(
    positionals[0] ?? resolve(REPO_ROOT, ".build/runway-api-4.0.0.zip"),
    values.schemas,
  );
  console.log(
    `Validated ${result.name} ${result.version}: ${result.files} files, ${SKILLS.length} skills`,
  );
  console.log(
    "Package validation does not establish host OAuth, reviewer access, or submission readiness.",
  );
}
