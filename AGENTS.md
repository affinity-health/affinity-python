# Affinity Python SDK

API clients and models are generated from `spec/affinity.openapi.json` by the private Affinity
monorepo's `packages/sdk-generation` pipeline. Change the source contract or generator there,
then copy the regenerated output here. `generation.json` pins the generation inputs.
Preserve the curated README, license, smoke tests, and CI when refreshing generated code.

Validate changes with:

```sh
python -m pip install .
python tests/smoke.py
```

Use synthetic fixtures and Test API keys only. Registry publication is deferred; current consumers
install from GitHub or build locally as described in the README.
