# Affinity Python SDK

Typed client for the Affinity API, for Python 3.10 and later. It targets API version `2026-11-01` and sends it in `Affinity-Version` on every request. It has a sync client, `Affinity`, and an async client, `AsyncAffinity`, with the same methods.

Use it only on a server. Never put an API key in a browser, a mobile application or a public environment variable.

## Install

The package is not on PyPI. Install it from GitHub at the release tag:

```sh
pip install "affinity-health-sdk @ git+https://github.com/affinity-health/affinity-python@v0.9.0"
```

The distribution is `affinity-health-sdk`; the import package is `affinity`.

## Quickstart

Use a Test key (`sk_test_…`). Test orders go to a test pharmacy.

```python
import os

from affinity import Affinity

client = Affinity(token=os.environ["AFFINITY_API_KEY"])
account = client.account.get()
if account.mode != "test":
    raise SystemExit("Use a Test key for this example")

for medication in client.medications.list():
    print(medication.name, medication.pharmacy.name)
```

The key sets the organization and the Test or Live mode. The async client works the same way:

```python
from affinity import AsyncAffinity

client = AsyncAffinity(token=os.environ["AFFINITY_API_KEY"])
account = await client.account.get()
async for medication in await client.medications.list():
    print(medication.name)
```

## What to know

- **Writes need an `idempotency_key`.** `orders.create`, `orders.cancel`, `practices.create`, `practices.update`, `webhooks.create`, `webhooks.update`, `webhooks.resend_failed` and `feedback.create` require it as a keyword argument. Save the key with the reviewed order before the first request, and send the same key and body to retry. The client's automatic retries send the same key.
- **Lists iterate every page.** `for item in client.orders.list(limit=25)` reads each next page. `page.items` is one page, `page.has_next` says if there is another, and `page.iter_pages()` gives the pages.
- **Errors are typed.** Each API error is a subclass of `affinity.core.api_error.ApiError` with `status_code`, `headers` and `body`: `BadRequestError` (400), `UnauthorizedError` (401), `ForbiddenError` (403), `NotFoundError` (404), `ConflictError` (409), `UnprocessableEntityError` (422), `TooManyRequestsError` (429) and others, all importable from `affinity`. For most of them `body` is a `Problem` with `code`, `detail` and `request_id`. On a 422, `body.issues` names each refused field:

  ```python
  from affinity import UnprocessableEntityError

  try:
      order = client.orders.create(idempotency_key=saved_key, **saved_order)
  except UnprocessableEntityError as error:
      for issue in error.body.issues or []:
          print(issue.field, issue.message)  # for example prescriptions[0].quantity
  ```

- **Raw responses.** `client.orders.with_raw_response.get(order_id)` returns the response `headers` (with `x-request-id`) and `data`.
- **Timestamps.** `orders.list(updated_after=...)` takes a timezone-aware `datetime`, which holds microseconds at most. To send more digits, pass the string in `request_options={"additional_query_parameters": {"updatedAfter": "..."}}`.

### Defaults

| Setting | Default | Change it with |
| --- | --- | --- |
| Base URL | `https://api.affinityrx.com` | `Affinity(base_url=...)` |
| `Affinity-Version` | `2026-11-01` | `Affinity(affinity_version=...)` |
| Retries | 2, for 408, 409, 429 and 5xx responses and failed connections, waiting for `Retry-After` | `Affinity(max_retries=...)` or `request_options={"max_retries": ...}` |
| Timeout | 60 seconds | `Affinity(timeout=...)` or `request_options={"timeout_in_seconds": ...}` |

You can also pass your own `httpx_client` (`httpx.Client` or `httpx.AsyncClient`).

## Verify webhooks

Affinity signs each webhook request with the endpoint's secret (`whsec_…`, returned once by `webhooks.create`). The `Affinity-Signature` header is `t=<unix seconds>,v1=<hex>`. The signature is HMAC-SHA256, keyed with the secret, over `<t>.` followed by the exact raw body bytes, as lowercase hex. The SDK does not include a verifier. Use this function, which needs only the standard library:

<!-- webhook-example:start -->
```python
import hashlib
import hmac
import json
import time


def verify_affinity_webhook(body: bytes, signature: str, secret: str, tolerance: int = 300) -> dict:
    """Return the event if the Affinity-Signature header is valid; raise ValueError if not."""
    timestamp = None
    candidates = []
    for part in signature.split(","):
        name, _, value = part.strip().partition("=")
        if name == "t":
            timestamp = value
        elif name == "v1":
            candidates.append(value)
    if timestamp is None or not timestamp.isdigit() or not candidates:
        raise ValueError("malformed Affinity-Signature header")
    if abs(time.time() - int(timestamp)) > tolerance:
        raise ValueError("timestamp outside the tolerance")
    expected = hmac.new(secret.encode(), timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, candidate) for candidate in candidates):
        raise ValueError("signature does not match")
    return json.loads(body)
```
<!-- webhook-example:end -->

Pass the raw request body, before any JSON parsing, for example `await request.body()` in Starlette or `request.get_data()` in Flask. Answer 2xx after you save the event. Save each event once by its `id`, ignore event types you do not know, and read the current order when you process an event, so a late event cannot move your state back. To get a typed event, parse the result with `affinity.core.parse_obj_as(affinity.WebhookEvent, event)`.

## More

- [API reference for this SDK](docs/reference.md): every method and parameter.
- [Affinity API documentation](https://docs.affinityrx.com).

## Build and verify

[Fern](https://buildwithfern.com) generates `src/affinity` and `tests/generated` from `spec/affinity.openapi.json`, the Affinity API contract. It runs locally in Docker, with no Fern account. See [AGENTS.md](AGENTS.md) for the files written by hand.

```sh
# Regenerate after the contract changes (needs Docker, Node and jq).
scripts/generate.sh
# Fail if the committed code differs from a fresh generation.
scripts/generate-check.sh

# Build the wheel and run the unit tests (Python 3.12; also run with python:3.10).
docker run --rm -e PYTHONDONTWRITEBYTECODE=1 -v "$PWD":/src:ro python:3.12 bash -c '
  cp -R /src /tmp/sdk && cd /tmp/sdk && pip install -q build && python -m build &&
  pip install -q "$(ls dist/*.whl)[test]" && python -m pytest -q tests'

# Call every operation against a real API. Test keys only; it creates a Test practice and a
# Test order and cancels the order. The env file holds AFFINITY_API_KEY, AFFINITY_BASE_URL and
# AFFINITY_SMOKE_WEBHOOK_URL.
docker run --rm -e PYTHONDONTWRITEBYTECODE=1 --env-file smoke.env -v "$PWD":/src:ro python:3.12 bash -c '
  cp -R /src /tmp/sdk && cd /tmp/sdk && pip install -q . && python tests/smoke.py'
```
