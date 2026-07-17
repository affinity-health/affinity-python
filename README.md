# Affinity Python SDK

The official Python SDK for the Affinity API.

> **Status:** This repository is being prepared for its first release. The package is not yet
> published and its public API may change before `0.1.0`.

The SDK will provide a small, resource-oriented interface for Python services connecting
healthcare practices to Affinity's compounder network. It is intended for trusted server-side
applications, workers, and data workflows.

## Planned package

```sh
pip install affinity-health-sdk
```

The distribution uses an Affinity Health-specific name because the unrelated `affinity-sdk` name
is already occupied on PyPI.

## Intended usage

```python
import os

from affinity_health import Affinity

with Affinity(
    os.environ["AFFINITY_API_KEY"],
    api_version="2026-07-09",
) as affinity:
    catalog = affinity.catalog.list(query="semaglutide")
    practices = affinity.practices.list()
    orders = affinity.orders.list()
```

## Resource model

The initial client surface is planned around these resources:

- `account` — inspect the authenticated organization and API access
- `catalog` — search products available through the Affinity network
- `practices` — create and manage customer practices
- `orders` — create, submit, inspect, update, and cancel orders
- `webhooks` — manage endpoints and inspect or replay events

Generated transport classes will remain available as an escape hatch, while `Affinity` will be the
recommended entry point.

## Safety

Affinity API keys are service-account credentials. Use this SDK only in a trusted backend and load
keys from server-side secret storage. Do not include a key in notebooks, public repositories,
browser code, mobile applications, or client-visible logs.

Requests involving patient, prescription, or fulfillment data may contain protected health
information. Integrators are responsible for their own authorization, logging, retention,
infrastructure, and compliance controls.

## Generation and releases

This SDK will be generated from the versioned contract in
[`affinity-openapi`](https://github.com/affinity-health/affinity-openapi), with a maintained
resource facade layered over the generated transport. Releases will be validated against the same
contract before publication to PyPI.

## Related projects

- [OpenAPI specification](https://github.com/affinity-health/affinity-openapi)
- [TypeScript SDK](https://github.com/affinity-health/affinity-typescript)

