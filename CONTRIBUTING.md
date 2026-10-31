# Contributing

The SDK code is generated. Do not edit `src/affinity`, `tests/generated`, `docs/reference.md` or
`generation.json` by hand.

1. Copy the new contract to `spec/affinity.openapi.json`.
2. Run `scripts/generate.sh`. It needs Docker, Node and jq, and no Fern account.
3. Run `scripts/generate-check.sh`. It must pass with no diff.
4. Build and run the unit tests with the Docker commands in the README's "Build and verify"
   section, on `python:3.12` and `python:3.10`.
5. Run `tests/smoke.py` with a Test key against staging.
6. Update `CHANGELOG.md` and, for a release, the version in `pyproject.toml`; then regenerate.

To change generated code, change `fern/generators.yml` or `scripts/generate.sh`, regenerate and
explain the change in the changelog.
