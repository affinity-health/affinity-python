#!/usr/bin/env bash
# Regenerates the SDK from spec/affinity.openapi.json and fails if anything differs from the
# committed files: generated code is never edited by hand. Needs Docker, Node and jq.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
snapshot="$(mktemp -d)"
trap 'rm -rf "$snapshot"' EXIT
cp -R "$root/src/affinity" "$snapshot/affinity"
cp -R "$root/tests/generated" "$snapshot/generated"
cp "$root/generation.json" "$root/docs/reference.md" "$snapshot/"
"$root/scripts/generate.sh" >/dev/null
diff -ru "$snapshot/affinity" "$root/src/affinity"
diff -ru "$snapshot/generated" "$root/tests/generated"
diff -u "$snapshot/generation.json" "$root/generation.json"
diff -u "$snapshot/reference.md" "$root/docs/reference.md"
