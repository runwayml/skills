#!/usr/bin/env node

import { readFile, writeFile, mkdir, unlink, chmod } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";

const CONFIG_DIR = join(homedir(), ".config", "runwayml");
const CREDENTIALS_FILE = join(CONFIG_DIR, "credentials.json");
const DEFAULT_BASE_URL = "https://api.dev.runwayml.com";
const API_VERSION = "2024-11-06";

// ---------------------------------------------------------------------------
// Auth persistence
// ---------------------------------------------------------------------------

async function readCredentials() {
  try {
    return JSON.parse(await readFile(CREDENTIALS_FILE, "utf-8"));
  } catch {
    return null;
  }
}

async function writeCredentials(config) {
  await mkdir(CONFIG_DIR, { recursive: true });
  await writeFile(
    CREDENTIALS_FILE,
    JSON.stringify(config, null, 2) + "\n",
    { mode: 0o600 },
  );
  try {
    await chmod(CONFIG_DIR, 0o700);
  } catch {
    // best-effort on platforms where chmod is unsupported
  }
}

async function deleteCredentials() {
  try {
    await unlink(CREDENTIALS_FILE);
  } catch {
    // already gone
  }
}

// ---------------------------------------------------------------------------
// Auth resolution
// ---------------------------------------------------------------------------

async function resolveAuth() {
  const envKey = process.env.RUNWAYML_API_SECRET;
  const envUrl = process.env.RUNWAYML_BASE_URL;

  if (envKey) {
    return {
      apiKey: envKey,
      baseUrl: envUrl || DEFAULT_BASE_URL,
      source: "environment",
    };
  }

  const creds = await readCredentials();
  if (creds?.apiKey) {
    return {
      apiKey: creds.apiKey,
      baseUrl: creds.baseUrl || DEFAULT_BASE_URL,
      source: "credentials-file",
    };
  }

  return null;
}

async function requireAuth() {
  const auth = await resolveAuth();
  if (!auth) {
    printError(
      "Not authenticated. Run: node scripts/runway-api.mjs auth login <api-key>",
    );
    process.exit(1);
  }
  return auth;
}

// ---------------------------------------------------------------------------
// HTTP client
// ---------------------------------------------------------------------------

const MAX_RETRIES = 2;
const RETRYABLE_STATUSES = new Set([408, 429, 500, 502, 503, 504]);

async function apiFetch(method, path, { body, auth } = {}) {
  const resolvedAuth = auth ?? (await requireAuth());
  const url = `${resolvedAuth.baseUrl}${path}`;

  const headers = {
    Authorization: `Bearer ${resolvedAuth.apiKey}`,
    "X-Runway-Version": API_VERSION,
    Accept: "application/json",
  };
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  const fetchOptions = {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  };

  let lastError;

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    if (attempt > 0) {
      const delay = Math.min(1000 * 2 ** (attempt - 1), 4000);
      await new Promise((r) => setTimeout(r, delay));
    }

    try {
      const response = await fetch(url, fetchOptions);

      if (RETRYABLE_STATUSES.has(response.status) && attempt < MAX_RETRIES) {
        lastError = { status: response.status, message: `HTTP ${response.status}` };
        continue;
      }

      if (!response.ok) {
        let errorBody;
        try {
          errorBody = await response.json();
        } catch {
          errorBody = { message: await response.text() };
        }
        const error = new Error(errorBody.message || errorBody.error || `HTTP ${response.status}`);
        error.status = response.status;
        if (errorBody.code) error.code = errorBody.code;
        throw error;
      }

      if (response.status === 204) return {};

      return await response.json();
    } catch (error) {
      if (error.status && !RETRYABLE_STATUSES.has(error.status)) throw error;
      lastError = error;
      if (attempt === MAX_RETRIES) throw lastError;
    }
  }
}

// ---------------------------------------------------------------------------
// Output helpers
// ---------------------------------------------------------------------------

function printJson(data) {
  console.log(JSON.stringify(data, null, 2));
}

function printError(message, details) {
  const payload = { error: message };
  if (details) payload.details = details;
  console.error(JSON.stringify(payload, null, 2));
}

function printApiError(error) {
  const payload = { error: error.message };
  if (error.status) payload.status = error.status;
  if (error.code) payload.code = error.code;
  console.error(JSON.stringify(payload, null, 2));
}

// ---------------------------------------------------------------------------
// Commands: auth
// ---------------------------------------------------------------------------

async function authLogin(args) {
  const apiKey = args[0];
  if (!apiKey) {
    printError("Usage: auth login <api-key> [--base-url <url>]");
    process.exit(1);
  }

  const baseUrlIdx = args.indexOf("--base-url");
  const baseUrl =
    baseUrlIdx !== -1 && args[baseUrlIdx + 1]
      ? args[baseUrlIdx + 1]
      : DEFAULT_BASE_URL;

  try {
    const org = await apiFetch("GET", "/v1/organization", {
      auth: { apiKey, baseUrl },
    });

    await writeCredentials({ apiKey, baseUrl });

    printJson({
      status: "authenticated",
      organization: org.name,
      credentialsFile: CREDENTIALS_FILE,
    });
  } catch (error) {
    printError("Authentication failed — check your API key.", error.message);
    process.exit(1);
  }
}

async function authStatus() {
  const auth = await resolveAuth();
  if (!auth) {
    printJson({ authenticated: false });
    return;
  }

  printJson({
    authenticated: true,
    source: auth.source,
    baseUrl: auth.baseUrl,
    keyPrefix: auth.apiKey.slice(0, 8) + "...",
  });
}

async function authLogout() {
  await deleteCredentials();
  printJson({ status: "logged_out" });
}

// ---------------------------------------------------------------------------
// Commands: request
// ---------------------------------------------------------------------------

async function request(args) {
  const method = args[0]?.toUpperCase();
  const path = args[1];

  if (!method || !path) {
    printError("Usage: request <METHOD> <path> [--body <json>]");
    process.exit(1);
  }

  const supportedMethods = new Set(["GET", "POST", "PATCH", "PUT", "DELETE"]);
  if (!supportedMethods.has(method)) {
    printError(`Unsupported HTTP method: ${method}`);
    process.exit(1);
  }

  const bodyIdx = args.indexOf("--body");
  let body;
  if (bodyIdx !== -1 && args[bodyIdx + 1]) {
    try {
      body = JSON.parse(args[bodyIdx + 1]);
    } catch {
      printError("Invalid JSON in --body argument.");
      process.exit(1);
    }
  }

  try {
    const result = await apiFetch(method, path, { body });
    printJson(result);
  } catch (error) {
    printApiError(error);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Commands: wait
// ---------------------------------------------------------------------------

const POLL_INTERVAL_MS = 5_000;
const TERMINAL_STATUSES = new Set(["SUCCEEDED", "FAILED", "CANCELLED"]);

async function waitForTask(args) {
  const taskId = args[0];
  if (!taskId) {
    printError("Usage: wait <task-id>");
    process.exit(1);
  }

  try {
    let task = await apiFetch("GET", `/v1/tasks/${taskId}`);

    while (!TERMINAL_STATUSES.has(task.status)) {
      await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
      task = await apiFetch("GET", `/v1/tasks/${taskId}`);
      process.stderr.write(`status: ${task.status}\n`);
    }

    printJson(task);

    if (task.status !== "SUCCEEDED") {
      process.exit(1);
    }
  } catch (error) {
    printApiError(error);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const [command, subcommand, ...rest] = process.argv.slice(2);

try {
  switch (command) {
    case "auth":
      switch (subcommand) {
        case "login":
          await authLogin(rest);
          break;
        case "status":
          await authStatus();
          break;
        case "logout":
          await authLogout();
          break;
        default:
          printError("Usage: auth <login|status|logout>");
          process.exit(1);
      }
      break;

    case "request":
      await request([subcommand, ...rest]);
      break;

    case "wait":
      await waitForTask([subcommand, ...rest]);
      break;

    default:
      printJson({
        name: "runway-api",
        commands: {
          "auth login <key>": "Store API key globally",
          "auth status": "Show current authentication",
          "auth logout": "Remove stored credentials",
          "request <METHOD> <path>": "Call any public API endpoint",
          "wait <task-id>": "Poll a task until completion",
        },
      });
      if (command) process.exit(1);
  }
} catch (error) {
  printApiError(error);
  process.exit(1);
}
