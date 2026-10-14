# Archived skills

These generation and utility skills are retired from the active Runway Dev plugin. Their source and helper scripts are preserved here; they have not been refreshed for v4. Check the [current API documentation](https://docs.dev.runwayml.com/) before using older model examples.

The root plugin loads only `skills/`. Standalone installation of the active Dev skills still uses `npx skills add runwayml/skills`.

To explicitly install a self-contained archived skill:

```sh
npx skills add https://github.com/runwayml/skills/tree/main/legacy --skill use-runway-api
```

`use-runway-api` includes its Node.js runtime and auth instructions within its own directory. Resolve the runtime relative to the installed `SKILL.md`.

The older `rw-generate-*` instructions reference shared Python helpers. To run them, clone this repository and use `legacy/` as the working directory so `scripts/generate_*.py` resolves. A standalone skill copy does not include those shared helpers. `rw-check-org-details` contains its own API examples.

Existing installations pinned to an older commit remain on that version until their marketplace or installer updates. Updating to v4 removes these skills from the active plugin; choose an explicit archived skill installation if still needed, and avoid duplicate skill copies.
