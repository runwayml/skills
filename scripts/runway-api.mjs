#!/usr/bin/env node

const VERSION = "1.0.1";
const DEFAULT_BASE_URL = "https://api.dev.runwayml.com";
const STAGE_BASE_URL = "https://api.dev-stage.runwayml.com";
const API_VERSION = "2024-11-06";
const BIN = "runway-api.mjs";

const useStage = process.argv.includes("--stage");

function hasFlag(args, ...flags) {
  return flags.some((f) => args.includes(f));
}

function stripFlag(args, flag) {
  return args.filter((a) => a !== flag);
}

// ---------------------------------------------------------------------------
// Auth resolution
// ---------------------------------------------------------------------------

async function resolveAuth() {
  const envKey = useStage
    ? process.env.RUNWAY_SKILLS_API_SECRET_STAGE ?? process.env.RUNWAY_SKILLS_API_SECRET
    : process.env.RUNWAY_SKILLS_API_SECRET;
  const envUrl = useStage
    ? process.env.RUNWAY_SKILLS_BASE_URL ?? STAGE_BASE_URL
    : process.env.RUNWAY_SKILLS_BASE_URL;

  if (!envKey) return null;

  return {
    apiKey: envKey,
    baseUrl: envUrl || DEFAULT_BASE_URL,
    source: useStage ? "environment (stage)" : "environment",
  };
}

async function requireAuth() {
  const auth = await resolveAuth();
  if (!auth) {
    printError(
      "Not authenticated. Set RUNWAY_SKILLS_API_SECRET in the environment that launches your editor or shell.",
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
        if (errorBody.issues) error.issues = errorBody.issues;
        if (errorBody.docUrl) error.docUrl = errorBody.docUrl;
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

function printError(message, { example, details } = {}) {
  const payload = { error: message };
  if (example) payload.example = example;
  if (details) payload.details = details;
  console.error(JSON.stringify(payload, null, 2));
}

function printHelp(text) {
  console.log(text.trimStart());
}

function printApiError(error) {
  const payload = { error: error.message };
  if (error.status) payload.status = error.status;
  if (error.code) payload.code = error.code;
  if (error.issues) payload.issues = summarizeIssues(error.issues);
  if (error.docUrl) payload.docUrl = error.docUrl;
  console.error(JSON.stringify(payload, null, 2));
}

function summarizeIssues(issues) {
  return issues.map((issue) => {
    const field = Array.isArray(issue.path) ? issue.path.join(".") : undefined;
    const messages = [];
    if (issue.message && issue.message !== "Invalid input") messages.push(issue.message);
    if (Array.isArray(issue.errors)) {
      for (const branch of issue.errors) {
        const branchMsgs = (Array.isArray(branch) ? branch : [branch])
          .map((e) => e.message)
          .filter(Boolean);
        if (branchMsgs.length) messages.push(...branchMsgs);
      }
    }
    const unique = [...new Set(messages)];
    return { field, messages: unique.length ? unique : [issue.message ?? issue.code] };
  });
}

function compactIsoDate(value) {
  if (!value) return null;
  const parsedDate = new Date(value);
  if (Number.isNaN(parsedDate.getTime())) return value;
  return parsedDate.toISOString();
}

function describeVoice(voice) {
  if (!voice) return null;
  if (typeof voice === "string") return voice;

  const voiceName = voice.name ?? voice.id ?? "Unknown";
  if (voice.type === "custom") return `${voiceName} (custom)`;
  if (voice.type === "preset") return `${voiceName} (preset)`;
  return voiceName;
}

function pickArray(result) {
  if (Array.isArray(result)) return result;
  if (Array.isArray(result.data)) return result.data;
  return [];
}

async function readStdin() {
  if (process.stdin.isTTY) {
    printError("--stdin requires piped input, but stdin is a terminal.", {
      example: `echo '{"name":"test"}' | ${BIN} request POST /v1/avatars --stdin`,
    });
    process.exit(1);
  }
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf-8");
}

// ---------------------------------------------------------------------------
// Commands: auth
// ---------------------------------------------------------------------------

async function authLogin(args) {
  void args;
  printError(
    "Persisted auth is disabled. Set RUNWAY_SKILLS_API_SECRET in your environment instead.",
  );
  process.exit(1);
}

async function authStatus() {
  const auth = await resolveAuth();
  if (!auth) {
    printJson({
      authenticated: false,
      source: "environment",
      baseUrl: process.env.RUNWAY_SKILLS_BASE_URL || DEFAULT_BASE_URL,
    });
    return;
  }

  try {
    const organization = await apiFetch("GET", "/v1/organization", { auth });
    printJson({
      authenticated: true,
      source: auth.source,
      baseUrl: auth.baseUrl,
      keyPrefix: auth.apiKey.slice(0, 8) + "...",
      organization: organization.name ?? null,
    });
  } catch (primaryError) {
    try {
      await apiFetch("GET", "/v1/avatars", { auth });
      printJson({
        authenticated: true,
        source: auth.source,
        baseUrl: auth.baseUrl,
        keyPrefix: auth.apiKey.slice(0, 8) + "...",
        organization: null,
        note: "/v1/organization unavailable; verified via /v1/avatars",
      });
    } catch {
      printJson({
        authenticated: false,
        source: auth.source,
        baseUrl: auth.baseUrl,
        keyPrefix: auth.apiKey.slice(0, 8) + "...",
        error: primaryError.message,
      });
      process.exit(1);
    }
  }
}

async function authLogout() {
  printError(
    "Persisted auth is disabled. Unset RUNWAY_SKILLS_API_SECRET in your shell or editor environment to log out.",
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Commands: request
// ---------------------------------------------------------------------------

async function request(args) {
  if (hasFlag(args, "--help", "-h")) {
    printHelp(`
Usage: ${BIN} request <METHOD> <path> [options]

Options:
  --body <json>   JSON request body
  --stdin         Read JSON body from stdin
  --dry-run       Print request details without executing
  --help          Show this help

Examples:
  ${BIN} request GET /v1/avatars
  ${BIN} request POST /v1/documents --body '{"avatarId":"abc","name":"FAQ","content":"..."}'
  ${BIN} request DELETE /v1/avatars/abc123 --dry-run
  echo '{"name":"test"}' | ${BIN} request POST /v1/avatars --stdin
`);
    return;
  }

  const method = args[0]?.toUpperCase();
  const path = args[1];

  if (!method || !path) {
    printError("Missing required arguments: METHOD and path.", {
      example: `${BIN} request GET /v1/avatars`,
    });
    process.exit(1);
  }

  const supportedMethods = new Set(["GET", "POST", "PATCH", "PUT", "DELETE"]);
  if (!supportedMethods.has(method)) {
    printError(`Unsupported HTTP method: ${method}. Use one of: GET, POST, PATCH, PUT, DELETE.`, {
      example: `${BIN} request GET /v1/avatars`,
    });
    process.exit(1);
  }

  let body;

  if (hasFlag(args, "--stdin")) {
    const raw = await readStdin();
    try {
      body = JSON.parse(raw);
    } catch {
      printError("Invalid JSON from stdin.", {
        example: `echo '{"name":"test"}' | ${BIN} request POST /v1/avatars --stdin`,
      });
      process.exit(1);
    }
  } else {
    const bodyIdx = args.indexOf("--body");
    if (bodyIdx !== -1 && args[bodyIdx + 1]) {
      try {
        body = JSON.parse(args[bodyIdx + 1]);
      } catch {
        printError("Invalid JSON in --body argument.", {
          example: `${BIN} request POST /v1/documents --body '{"avatarId":"abc","name":"FAQ"}'`,
        });
        process.exit(1);
      }
    }
  }

  if (hasFlag(args, "--dry-run")) {
    const auth = await requireAuth();
    printJson({
      dry_run: true,
      method,
      url: `${auth.baseUrl}${path}`,
      headers: {
        Authorization: "Bearer ***",
        "X-Runway-Version": API_VERSION,
        Accept: "application/json",
        ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      },
      body: body ?? null,
    });
    return;
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
// Commands: compact lists
// ---------------------------------------------------------------------------

async function listAvatars() {
  try {
    const result = await apiFetch("GET", "/v1/avatars");
    const items = pickArray(result).map((avatar) => ({
      id: avatar.id,
      name: avatar.name ?? null,
      status: avatar.status ?? null,
      voice: describeVoice(avatar.voice),
      documents: Array.isArray(avatar.documentIds) ? avatar.documentIds.length : 0,
      createdAt: compactIsoDate(avatar.createdAt),
    }));

    printJson({ data: items });
  } catch (error) {
    printApiError(error);
    process.exit(1);
  }
}

async function listVoices() {
  try {
    const result = await apiFetch("GET", "/v1/voices");
    const items = pickArray(result).map((voice) => ({
      id: voice.id,
      name: voice.name ?? null,
      provider: voice.provider ?? voice.type ?? null,
      preview: voice.previewAudioUri ?? voice.previewUri ?? null,
    }));

    printJson({ data: items });
  } catch (error) {
    printApiError(error);
    process.exit(1);
  }
}

async function listDocuments(args) {
  if (hasFlag(args, "--help", "-h")) {
    printHelp(`
Usage: ${BIN} documents list [options]

Options:
  --avatar-id <id>   Filter documents by avatar
  --help             Show this help

Examples:
  ${BIN} documents list
  ${BIN} documents list --avatar-id abc123
`);
    return;
  }

  const avatarIdIndex = args.indexOf("--avatar-id");
  const avatarId =
    avatarIdIndex !== -1 && args[avatarIdIndex + 1]
      ? args[avatarIdIndex + 1]
      : null;

  const queryString = avatarId ? `?avatarId=${encodeURIComponent(avatarId)}` : "";

  try {
    const result = await apiFetch("GET", `/v1/documents${queryString}`);
    const items = pickArray(result).map((document) => ({
      id: document.id,
      name: document.name ?? null,
      avatarId: document.avatarId ?? null,
      createdAt: compactIsoDate(document.createdAt),
    }));

    printJson({ data: items });
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
  if (hasFlag(args, "--help", "-h")) {
    printHelp(`
Usage: ${BIN} wait <task-id>

Poll a generation task until it reaches a terminal status.
Prints status updates to stderr during polling.

Examples:
  ${BIN} wait task_abc123
`);
    return;
  }

  const taskId = args[0];
  if (!taskId) {
    printError("Missing required argument: task-id.", {
      example: `${BIN} wait task_abc123`,
    });
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
// Help text
// ---------------------------------------------------------------------------

function printRootHelp() {
  printHelp(`
Usage: ${BIN} <command> [options]

Commands:
  auth            Manage authentication
  request         Call any public API endpoint
  avatars list    List avatars (compact)
  voices list     List voices (compact)
  documents list  List documents (compact)
  wait            Poll a task until completion

Options:
  --stage         Target the staging API (uses RUNWAY_SKILLS_API_SECRET_STAGE)
  --help          Show help for a command
  --version       Show version

Examples:
  ${BIN} auth status
  ${BIN} request GET /v1/avatars
  ${BIN} request POST /v1/documents --body '{"avatarId":"abc","name":"FAQ","content":"..."}'
  ${BIN} avatars list
  ${BIN} documents list --avatar-id abc123
  ${BIN} wait task_abc123
`);
}

function printAuthHelp() {
  printHelp(`
Usage: ${BIN} auth <subcommand>

Subcommands:
  status    Verify current environment auth
  login     Show env-based auth guidance
  logout    Show env-based logout guidance

Examples:
  ${BIN} auth status
`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const allArgs = stripFlag(process.argv.slice(2), "--stage");

if (hasFlag(allArgs, "--version", "-v") && !allArgs.some((a) => !a.startsWith("-"))) {
  console.log(VERSION);
  process.exit(0);
}

if (allArgs.length === 0 || (hasFlag(allArgs, "--help", "-h") && !allArgs.some((a) => !a.startsWith("-")))) {
  printRootHelp();
  process.exit(0);
}

const [command, subcommand, ...rest] = allArgs;

try {
  switch (command) {
    case "auth":
      if (hasFlag([subcommand, ...rest], "--help", "-h") || !subcommand) {
        printAuthHelp();
        break;
      }
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
          printError(`Unknown auth subcommand: ${subcommand}.`, {
            example: `${BIN} auth status`,
          });
          process.exit(1);
      }
      break;

    case "request":
      await request([subcommand, ...rest].filter(Boolean));
      break;

    case "avatars":
      if (hasFlag([subcommand, ...rest], "--help", "-h")) {
        printHelp(`
Usage: ${BIN} avatars list

List all avatars with compact fields (id, name, status, voice, documents, createdAt).

Examples:
  ${BIN} avatars list
`);
        break;
      }
      if (subcommand === "list") {
        await listAvatars();
        break;
      }
      printError(`Unknown avatars subcommand: ${subcommand ?? "(none)"}.`, {
        example: `${BIN} avatars list`,
      });
      process.exit(1);
      break;

    case "voices":
      if (hasFlag([subcommand, ...rest], "--help", "-h")) {
        printHelp(`
Usage: ${BIN} voices list

List all voices with compact fields (id, name, provider, preview).

Examples:
  ${BIN} voices list
`);
        break;
      }
      if (subcommand === "list") {
        await listVoices();
        break;
      }
      printError(`Unknown voices subcommand: ${subcommand ?? "(none)"}.`, {
        example: `${BIN} voices list`,
      });
      process.exit(1);
      break;

    case "documents":
      if (hasFlag([subcommand, ...rest], "--help", "-h")) {
        await listDocuments(["--help"]);
        break;
      }
      if (subcommand === "list") {
        await listDocuments(rest);
        break;
      }
      printError(`Unknown documents subcommand: ${subcommand ?? "(none)"}.`, {
        example: `${BIN} documents list`,
      });
      process.exit(1);
      break;

    case "wait":
      await waitForTask([subcommand, ...rest].filter(Boolean));
      break;

    default:
      printError(`Unknown command: ${command}.`, {
        example: `${BIN} --help`,
      });
      process.exit(1);
  }
} catch (error) {
  printApiError(error);
  process.exit(1);
}
