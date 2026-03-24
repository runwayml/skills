---
name: recipe-full-setup
description: "Complete Runway API setup: check compatibility, configure API key, and integrate generation endpoints"
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(node --version), Bash(python3 --version), Bash(npm install *), Bash(pip install *), Bash(pip3 install *)
---

# Full Runway API Setup

> **PREREQUISITE:** Run `+check-compatibility` first to ensure the project has server-side capability.

This recipe guides a user through the complete process of integrating Runway's public API into their project. It chains together the compatibility check, API key setup, and API integration skills.

## Workflow

### Phase 1: Compatibility Check

Use `+check-compatibility` to analyze the user's project.

1. Identify the project type (Node.js, Python, etc.)
2. Verify server-side capability
3. Check runtime version compatibility
4. Look for existing Runway SDK installation

**If the project is INCOMPATIBLE**, stop and explain the options:

- Add a backend (Express, FastAPI, etc.)
- Use a fullstack framework (Next.js, SvelteKit, Nuxt, Remix)
- Add serverless functions (Vercel Functions, AWS Lambda)
- Create a separate backend service

**If NEEDS CHANGES**, help the user make the required changes before proceeding.

**If COMPATIBLE**, proceed to Phase 2.

### Phase 2: API Key Setup

Use `+setup-api-key` to configure credentials.

1. Direct the user to https://dev.runwayml.com/ to create an account and API key
2. Install the appropriate SDK (`@runwayml/sdk` for Node.js, `runwayml` for Python)
3. Configure the `RUNWAYML_API_SECRET` environment variable
4. Update `.gitignore` to exclude `.env`
5. Remind about credit purchase requirement ($10 minimum)

**Wait for the user to confirm** they have their API key before proceeding.

### Phase 3: Determine What to Integrate

Ask the user what they want to build. Based on their response, use the appropriate integration skill:

| User wants...                   | Skill to use                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------- |
| Generate videos from text       | `+integrate-video` (text-to-video)                                              |
| Animate images into video       | `+integrate-video` (image-to-video) + `+integrate-uploads` if local files       |
| Edit/transform existing videos  | `+integrate-video` (video-to-video) + `+integrate-uploads`                      |
| Generate images from text       | `+integrate-image`                                                              |
| Generate images with references | `+integrate-image` + `+integrate-uploads` if local refs                         |
| Text-to-speech                  | `+integrate-audio`                                                              |
| Sound effects                   | `+integrate-audio`                                                              |
| Voice isolation/dubbing         | `+integrate-audio` + `+integrate-uploads`                                       |
| Real-time conversational avatar | `+integrate-characters` + `+integrate-character-embed` (React UI)               |
| Avatar with domain knowledge    | `+integrate-characters` + `+integrate-documents` + `+integrate-character-embed` |
| Multiple capabilities           | Integrate each one, sharing the same client instance                            |

### Phase 4: Write the Integration Code

Based on the user's framework and needs:

1. **Create the API route/handler** — server-side endpoint that calls Runway
2. **Add upload handling** if the user needs to accept files from their users
3. **Add error handling** — catch and handle task failures
4. **Handle output storage** — remind user that output URLs expire in 24-48 hours

### Phase 5: Test and Verify

Help the user:

1. Run a test generation to verify everything works
2. Check for common issues (missing env var, insufficient credits, wrong model)
3. Confirm output is accessible

## Decision Tree for Upload Requirements

When the user's workflow involves images or videos as input:

```
Does the input come from a public HTTPS URL?
├── YES → Pass the URL directly to the API
└── NO → Is it a local file or user-uploaded file?
    ├── YES → Use +integrate-uploads to upload first, then pass runway:// URI
    └── NO → Is it small enough for a data URI? (< 5MB image, < 16MB video)
        ├── YES → Convert to base64 data URI
        └── NO → Use +integrate-uploads
```

## Important Reminders

- **Never expose the API key in client-side code.** All API calls must happen server-side.
- **Output URLs expire.** Always download and store generated content.
- **Credits are required.** The API won't work without prepaid credits.
- **Rate limits exist.** Rate limits exist. You should always check what is the rate limit before attempting concurrent generations.
- **Content moderation applies** to both inputs and outputs. Safety-flagged inputs are non-refundable.
- **Be cost-conscious.** Help users pick the right model for their budget. Credit cost can be found on https://docs.dev.runwayml.com/guides/pricing/
