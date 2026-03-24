---
name: fetch-api-reference
description: "Retrieve the latest Runway API reference from docs.dev.runwayml.com and use it as the authoritative source before any integration work"
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# Fetch Latest API Reference

Before guiding or implementing **any** Runway API integration, retrieve the current API reference and use it as the source of truth.

## Why This Matters

The [Runway API](https://docs.dev.runwayml.com/api/) is the official reference. Models, endpoints, request/response shapes, and versioning can change. Using the live docs ensures integration guidance and code match the latest API.

## Steps

### 1. Fetch the API Reference

Retrieve the contents of:

**https://docs.dev.runwayml.com/api/**

Use your available fetch tool (e.g. `mcp_web_fetch` or equivalent) to load this URL. The page contains the full API reference: endpoints, request bodies, accepted values, and examples.

### 2. Use It Before Integrating

- **Before** writing or suggesting integration code for video, image, audio, uploads, characters, documents, or any other Runway API feature, use the fetched content as the authoritative reference.
- Prefer **exact** endpoint paths, model IDs, parameter names, and header values from the fetched reference over any cached or local documentation.
- If the fetched content conflicts with text in other skills (e.g. `+api-reference` or an integrate skill), **the fetched docs take precedence** for that session.

### 3. When to Re-Fetch

- Re-fetch when the user asks to integrate a **new** capability or when you are unsure about an endpoint or parameter.
- Re-fetch when the user reports errors that might be due to API changes (e.g. invalid model name, changed request shape).

## After Fetching

Proceed with the relevant integrate skill (`+integrate-video`, `+integrate-image`, `+integrate-audio`, `+integrate-uploads`, `+integrate-characters`, `+integrate-documents`, `+integrate-character-embed`) using the retrieved reference to guide implementation.

## Important Notes

- Base URL for the API is `https://api.dev.runwayml.com`.
- All requests require `Authorization: Bearer <RUNWAYML_API_SECRET>` and `X-Runway-Version: 2024-11-06` (or the version stated in the fetched docs).
- Do not rely solely on bundled or in-repo API summaries when the user is integrating; the live docs are the source of truth.
