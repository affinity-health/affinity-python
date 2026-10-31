#!/usr/bin/env bash
# Generates src/affinity and tests/generated with Fern from spec/affinity.openapi.json, the
# committed Affinity contract. Fern runs locally in Docker; no Fern account or token is used.
# Needs Docker, Node (npx) and jq. The package version comes from pyproject.toml.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

spec="spec/affinity.openapi.json"
output="$root/.fern-output"
fern_version="$(jq -r .version fern/fern.config.json)"
generator_version="$(sed -n 's/^ *version: *\([^ ]*\)$/\1/p' fern/generators.yml | head -1)"
package_version="$(sed -n 's/^version = "\(.*\)"$/\1/p' pyproject.toml | head -1)"
[ -n "$generator_version" ] && [ -n "$package_version" ] || { echo "versions not found" >&2; exit 1; }

jq -f scripts/prepare-spec.jq "$spec" > fern/openapi.json
rm -rf "$output"
env -u FERN_TOKEN npx --yes "fern-api@$fern_version" generate --group python --local \
  --no-prompt --force --version "$package_version"
# Fern can exit 0 after its container fails; require the client it writes.
[ -f "$output/client.py" ] || { echo "Fern wrote no client.py" >&2; exit 1; }

mkdir -p docs tests
# Fern links source files from the repository root; the reference lives in docs/.
sed 's#href="src/#href="../src/#g' "$output/reference.md" > docs/reference.md
rm "$output/reference.md"
# Fern's README and CONTRIBUTING describe a published package; ours are written by hand.
# .fern/metadata.json records the local git commit, which would change on every commit.
rm -rf "$output/README.md" "$output/CONTRIBUTING.md" "$output/.fern"
rm -rf tests/generated
mv "$output/tests" tests/generated
rm -rf src/affinity
mkdir -p src
mv "$output" src/affinity
# PEP 561 marker: the package ships type hints. Fern writes it only for a full project.
: > src/affinity/py.typed
rm -f fern/openapi.json

jq --arg sha "$(sha256sum "$spec" | cut -d' ' -f1)" \
  --arg fern "$fern_version" --arg generatorVersion "$generator_version" '
  {
    contractVersion: .info.version,
    contractSha256: $sha,
    fernVersion: $fern,
    generator: "fernapi/fern-python-sdk",
    generatorVersion: $generatorVersion,
    operations: ([.paths | to_entries[] | .key as $path | .value | to_entries[]
      | select((.value | type) == "object" and .value.operationId != null)
      | {key: .value.operationId, value: "\(.key | ascii_upcase) \($path)"}] | from_entries)
  }' "$spec" > generation.json

echo "Generated src/affinity from API $(jq -r .contractVersion generation.json): $(jq '.operations | length' generation.json) operations."
