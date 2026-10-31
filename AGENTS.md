# Affinity Python SDK agent guide

This repository contains the official Python SDK for the Affinity public API: distribution
`affinity-health-sdk`, import package `affinity`, clients `Affinity` and `AsyncAffinity`.

## Source of truth

- `spec/affinity.openapi.json` is the Affinity API contract, copied unchanged from the matching
  committed snapshot in the private Affinity monorepo. Change the contract there, never here.
- Fern generates `src/affinity`, `tests/generated` and `docs/reference.md` from the spec, and
  `scripts/generate.sh` writes `generation.json`. Never hand-edit these files. Change
  `fern/generators.yml` or `scripts/generate.sh` and regenerate instead.
- `fern/openapi.json` and `.fern-output/` are build artifacts and are not committed.

## Hand-written files

- `pyproject.toml`: package metadata and version. Fern's local generation writes none.
  `scripts/generate.sh` reads the version from it.
- `fern/fern.config.json`, `fern/generators.yml`: pinned Fern CLI and generator versions and config.
- `scripts/generate.sh`, `scripts/generate-check.sh`, `scripts/prepare-spec.jq`.
- `tests/smoke.py` (staging smoke test) and `tests/test_webhook_example.py` (runs the README's
  webhook verification example).
- `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `AGENTS.md`, `LICENSE`,
  `.github/workflows/ci.yml`, `.gitignore`.

## Commands

```sh
scripts/generate.sh         # regenerate (Docker, Node, jq)
scripts/generate-check.sh   # fail if the committed code differs from a fresh generation
```

Build and unit-test in Docker with `python:3.12` and `python:3.10`; the README's "Build and
verify" section has the exact commands. `tests/smoke.py` calls a real API.

## Rules

- Use only Test keys (`sk_test_…`) for the smoke test, against staging or a development API.
  Never print, log or commit keys or webhook secrets.
- Do not publish to PyPI or any registry, and do not push tags, without explicit authorization.
- The SDK is for trusted server-side code. Never suggest API keys in browser or mobile code.
- A provider is an individual clinician or prescriber; a practice is the customer organization.
  Do not introduce a `clinic` resource.
