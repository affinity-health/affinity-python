# Affinity Python SDK

Server-side client for the Affinity API. Requires Python 3.10+.

The new interface is implemented in this source update and has not been published to a registry yet.

## Install from source

```sh
python -m pip install "git+https://github.com/affinity-health/affinity-python.git@main"
```

## Use

Set `AFFINITY_API_KEY` to a Test practice key on your server. Keep API keys out of browser and mobile code.

```python
import os
from affinity import Affinity

api = Affinity(os.environ["AFFINITY_API_KEY"])
patients = api.patients.list(params={"limit": 20})
```

`AsyncAffinity` provides the same interface with awaitable requests and async iterators.

Practice keys identify their practice automatically. Platform keys pass a practice ID in request options or use a scoped client.

See the [SDK guide](docs/guide.md) for platform requests, patient updates, signing, submission, pagination, and errors.
Routine patient writes generate an idempotency key. Persist your own keys for order creation, signing, and submission.

Defaults: API `2026-09-28`, a 60-second timeout, and no automatic retries.

## Verify

```sh
python -m pip install .
./tests/with-fixtures.sh sh -c 'python tests/smoke.py && python tests/approved.py && python tests/docs_approved.py'
```

The tests use synthetic fixtures on loopback. The fixture runner requires Python 3; Docker runs the language toolchain for the `scripts/check.sh` commands.

Generated with Cloudflare Forge, Fern, and Affinity's facade generator. [generation.json](generation.json) records the pinned inputs. Fix the generator in the Affinity monorepo before regenerating client code.
