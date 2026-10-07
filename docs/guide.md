# Python SDK guide

Synchronous and asynchronous Python applications. These examples use the synchronous client, with Stripe-style `params` and `options` dictionaries. [Source repository](https://github.com/affinity-health/affinity-python) · [All SDKs](https://docs.affinityrx.com/guides/reference/sdks/)

## Install

```sh
python -m pip install "git+https://github.com/affinity-health/affinity-python.git@v0.3.0"
```

Version 0.3.0 uses the same deployed API contract as TypeScript SDK 1.16.0.

## Connect

Set `AFFINITY_API_KEY` to a Test API key on your server. The key selects Test or Live mode. Keep it out of browser and mobile code.

```python
import os
from affinity import Affinity, AffinityError

api = Affinity(os.environ['AFFINITY_API_KEY'])
```

## With a practice key

The key identifies the practice. No practice ID or scoped client is needed.
The resource IDs below come from records in that practice.
Each section is a separate usage example, not one script to concatenate.

```python
patients = api.patients.list(params={'limit': 20})
patient = api.patients.get(patient_id)
items = api.catalog.items.list(params={'limit': 20})
```

## With a platform key

Pass the target practice with each practice-scoped request. Keep record data separate from request context and idempotency options.

```python
patients = api.patients.list(
    params={'limit': 20},
    options={'practice_id': practice_id},
)

patient = api.patients.get(patient_id, options={'practice_id': practice_id})

api.patients.update(
    patient_id,
    params={
        'email': 'alex@example.com',
    },
    options={
        'practice_id': practice_id,
    },
)

```

## Scope a workflow once

A scoped client remembers the practice for subsequent requests. It is immutable; the original client and other scoped clients stay independent.
A conflicting practice ID produces an error. Scoping never grants access to another practice.

```python
practice = api.for_practice(practice_id)

patients = practice.patients.list(params={'limit': 20})
items = practice.catalog.items.list(params={'limit': 20})
```

The following examples use this scoped client. A practice-key client supports the same calls without the scoping step.

## Create, get, and update a patient

Use synthetic Test data. Routine writes generate a fresh idempotency key per call and preserve it during internal retries.
Supply your own persisted key when retrying across calls or process restarts.

```python
patient = practice.patients.create(
    params={
        'name': {'first': 'Alex', 'last': 'Example'},
        'date_of_birth': '1990-01-01',
    },
)

saved = practice.patients.get(patient.id)
practice.patients.update(patient.id, params={'email': 'alex@example.com'})
practice.patients.update(patient.id, params={'status': 'archived'})
```

The SDK maps `archived` to the API’s `inactive` status. Returned records use `inactive`.

Archive patients whose records you need to retain. Permanent deletion is available only for patients without order history. No explicit idempotency key is needed.

```python
practice.patients.delete(patient_id)
```

## Create an order draft

`draft` is your application's prepared prescription data, using catalog and prescribing options from this practice.
An order contains 1–20 complete prescriptions for one patient. This example creates an unsigned draft.
It shows a platform call without a scoped client: practice context and the persisted key belong together in request options.

`job` is your persisted workflow record. Generate and save a unique key for each action before making its first request.

```python
order = api.orders.create(
    params={
        'patient_id': patient_id,
        'prescriptions': draft.prescriptions,
    },
    options={
        'practice_id': practice_id,
        'idempotency_key': job.create_order_key,
    },
)

```

## Sign and submit

`review` is your saved clinician review and signing consent for this exact order.
Store the reviewed revision, authorized prescriber ID, and explicit attestation together.
Your API key needs `orders:sign`. Never infer consent or automatically replace a stale revision.

```python
practice.orders.sign(
    order_id,
    params={
        'prescriber': {'id': review.prescriber_id},
        'expected_revision': review.order_revision,
        'signature_attestation': review.signature_attestation,
    },
    options={
        'idempotency_key': job.sign_order_key,
    },
)

submission = practice.orders.submit(
    order_id,
    options={
        'idempotency_key': job.submit_order_key,
    },
)

```

Use separate keys for creating, signing, and submitting. After an uncertain response, retry the same action with the same key and unchanged data.
A revision conflict requires renewed clinician review before another signing attempt.

Submission means queued, not accepted by the pharmacy. Inspect the result and track order events or webhooks.
After a reported partial submission failure, retry only the unconfirmed send with a new submission key.

## Read more than one page

The list method returns one page. Pass the last record's ID to request the next page.
The iterator fetches pages as you consume records; it does not load the full collection into memory.
`syncPatient` or its language equivalent represents your application's record handler.

```python
page = practice.patients.list(params={'limit': 20})

if page.has_more and page.data:
    next_page = practice.patients.list(
        params={
            'limit': 20,
            'starting_after': page.data[-1].id,
        },
    )

for patient in practice.patients.iterate(params={'limit': 100}):
    sync_patient(patient)
```

## Handle errors

API failures expose status, code, request ID, retryability, and an optional retry delay in seconds.
Log those fields without logging patient data or credentials. Transport failures remain distinguishable from API responses.

```python
try:
    practice.patients.get(patient_id)
except AffinityError as error:
    print(error.status, error.code, error.request_id, error.retryable, error.retry_after)
```

Retryability is a transport hint, not permission to repeat a clinical action with a new key.
Keep the same key and body for an uncertain write. Validation and authorization errors require a corrected request.
See [API errors](https://docs.affinityrx.com/errors/) for recovery guidance.

## Platform directory and webhooks

Use the root platform client to list its practices and webhook endpoints. These calls do not need a target practice or an idempotency key.
The webhook list belongs to the platform itself. Access to another organization's endpoints still requires an explicit grant.

```python
practices = api.practices.list(params={'limit': 20})
selected = api.practices.get(practice_id)
endpoints = api.webhooks.endpoints.list(params={'limit': 20})
```

## More resources

Use the same conventions for addresses, allergies, locations, team members, and nested order resources.
[API reference](https://docs.affinityrx.com/api/) · [Webhooks](https://docs.affinityrx.com/guides/webhooks/)
