import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import AdmZip from "adm-zip";
import { buildFiles, writeArchive } from "../scripts/build-dev-plugin.ts";
import { validateArchive } from "../scripts/validate-dev-plugin.ts";

function fixture(run: (archive: string, files: Map<string, Buffer>) => void) {
  const directory = mkdtempSync(join(tmpdir(), "runway-dev-validation-"));
  try {
    const archive = join(directory, "plugin.zip");
    const { manifest, files } = buildFiles();
    writeArchive(archive, manifest.name, files);
    run(archive, files);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

test("validator accepts the exported release", () => {
  fixture((archive) => {
    assert.deepEqual(validateArchive(archive), {
      name: "runway-api",
      version: "4.0.0",
      files: 15,
    });
  });
});

test("validator rejects invalid schemas, skills, and review cases", () => {
  const mutations = [
    (files: Map<string, Buffer>) => {
      const mcp = JSON.parse(files.get("mcp.json")?.toString() ?? "");
      mcp.unexpected = true;
      files.set("mcp.json", Buffer.from(JSON.stringify(mcp)));
    },
    (files: Map<string, Buffer>) => {
      const path = "skills/runway-dev/SKILL.md";
      files.set(
        path,
        Buffer.from("---\nname: wrong\ndescription: example\n---\n"),
      );
    },
    (files: Map<string, Buffer>) => {
      const manifest = JSON.parse(files.get("plugin.json")?.toString() ?? "");
      manifest.extensions["com.openai"].review = {
        test_cases: { positive: [], negative: [] },
      };
      files.set("plugin.json", Buffer.from(JSON.stringify(manifest)));
    },
  ];
  for (const mutate of mutations) {
    fixture((archive, files) => {
      mutate(files);
      writeArchive(archive, "runway-api", files);
      assert.throws(() => validateArchive(archive));
    });
  }
});

test("validator rejects unsafe names, unselected files, and corrupt payloads", () => {
  fixture((archive) => {
    const zip = new AdmZip(archive);
    const entry = zip.getEntry("runway-api/README.md");
    assert(entry);
    entry.entryName = "../README.md";
    zip.writeZip(archive);
    assert.throws(() => validateArchive(archive), /Unsafe archive paths/);
  });
  fixture((archive, files) => {
    files.set(".env", Buffer.from("private\n"));
    writeArchive(archive, "runway-api", files);
    assert.throws(() => validateArchive(archive), /Unexpected plugin contents/);
  });
  fixture((archive) => {
    const data = readFileSync(archive);
    const first = new AdmZip(archive).getEntries()[0];
    const offset = first.header.offset;
    const payload =
      offset +
      30 +
      data.readUInt16LE(offset + 26) +
      data.readUInt16LE(offset + 28);
    data[payload] ^= 0xff;
    writeFileSync(archive, data);
    assert.throws(() => validateArchive(archive));
  });
});
