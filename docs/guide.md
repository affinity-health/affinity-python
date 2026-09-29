# Python SDK proposal

> **Proposed interface.**
  These examples describe the SDK we plan to build. They are for review and do not run against the
  current release. Package versions and migration steps will follow approval.


Synchronous and asynchronous Python applications. These examples use the synchronous client. [Source repository](https://github.com/affinity-health/affinity-python) · [All SDKs](https://docs.joinaffinityai.com/guides/reference/sdks/) · [Shared conventions](https://docs.joinaffinityai.com/guides/reference/sdks/methods/)

## Connect

Set `AFFINITY_API_KEY` to a Test API key on your server. The key selects Test or Live mode. Keep it out of browser and mobile code.

```python
import os
from affinity import Affinity, AffinityError

api = Affinity(api_key=os.environ["AFFINITY_API_KEY"])
```

## With a practice key

The key identifies the practice. No practice ID or scoped client is needed.
The resource IDs below come from records in that practice.
Each section is a separate usage example, not one script to concatenate.

```python
patients = api.patients.list(limit=20)
patient = api.patients.get(patient_id)
items = api.catalog.items.list(limit=20)
```

For a recoverable update, pass your persisted key without a practice ID. `job` is your application's saved workflow record.

```python
api.patients.update(
    patient_id,
    email="alex@example.com",
    idempotency_key=job.update_patient_key,
)
```

## With a platform key

Pass the target practice with each practice-scoped request. Keep record data separate from request context and idempotency options.
The update key below comes from your persisted workflow job.

```python
patients = api.patients.list(limit=20, practice_id=practice_id)
patient = api.patients.get(patient_id, practice_id=practice_id)

api.patients.update(
    patient_id,
    email="alex@example.com",
    practice_id=practice_id,
    idempotency_key=job.update_patient_key,
)
```

## Scope a workflow once

A scoped client remembers the practice for subsequent requests. It is immutable; the original client and other scoped clients stay independent.
A conflicting practice ID produces an error. Scoping never grants access to another practice.

```python
practice = api.for_practice(practice_id)
patients = practice.patients.list(limit=20)
items = practice.catalog.items.list(limit=20)
```

The following examples use this scoped client. A practice-key client supports the same calls without the scoping step.

## Create, get, and update a patient

Use synthetic Test data. Routine writes generate a fresh idempotency key per call and preserve it during internal retries.
Supply your own persisted key when retrying across calls or process restarts.

```python
patient = practice.patients.create(
    name={"first": "Alex", "last": "Example"},
    date_of_birth="1990-01-01",
)
saved = practice.patients.get(patient.id)
practice.patients.update(patient.id, email="alex@example.com")
practice.patients.update(patient.id, status="archived")
```

Archive patients whose records you need to retain. Permanent deletion is available only for patients without order history and requires an explicit key.

```python
practice.patients.delete(patient_id, idempotency_key=job.delete_patient_key)
```

## Create an order draft

`draft` is your application's prepared prescription data, using catalog and prescribing options from this practice.
An order contains 1–20 complete prescriptions for one patient. This example creates an unsigned draft.

`job` is your persisted workflow record. Generate and save a unique key for each action before making its first request.

```python
order = practice.orders.create(
    patient_id=patient_id,
    prescriptions=draft.prescriptions,
    idempotency_key=job.create_order_key,
)
```

## Sign and submit

`review` is your saved clinician review and signing consent for this exact order.
Store the reviewed revision, authorized prescriber ID, and explicit attestation together.
Your API key needs `orders:sign`. Never infer consent or automatically replace a stale revision.

```python
practice.orders.sign(
    order_id,
    prescriber={"id": review.prescriber_id},
    expected_revision=review.order_revision,
    signature_attestation=review.signature_attestation,
    idempotency_key=job.sign_order_key,
)
submission = practice.orders.submit(
    order_id,
    idempotency_key=job.submit_order_key,
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
page = practice.patients.list(limit=20)
if page.has_more and page.data:
    next_page = practice.patients.list(limit=20, starting_after=page.data[-1].id)

for patient in practice.patients.iterate(limit=100):
    sync_patient(patient)
```

## Handle errors

API failures expose status, code, request ID, retryability, and an optional retry delay in seconds.
Log those fields without logging patient data or credentials. Transport failures remain distinguishable from API responses.

```python
try:
    practice.patients.get(patient_id)
except AffinityError as error:
    print(error.status, error.code, error.request_id,
          error.retryable, error.retry_after)
```

Retryability is a transport hint, not permission to repeat a clinical action with a new key.
Keep the same key and body for an uncertain write. Validation and authorization errors require a corrected request.
See [API errors](https://docs.joinaffinityai.com/errors/) for recovery guidance.

## Platform directory and webhooks

Use the root platform client to list its practices and webhook endpoints. These calls do not need a target practice or an idempotency key.
The webhook list belongs to the platform itself. Access to another organization's endpoints still requires an explicit grant.

```python
practices = api.practices.list(limit=20)
selected = api.practices.get(practice_id)
endpoints = api.webhooks.endpoints.list(limit=20)
```

## More resources

Use the same conventions for addresses, allergies, locations, team members, and nested order resources.
[Resource directory](https://docs.joinaffinityai.com/guides/reference/sdks/methods/) · [API reference](https://docs.joinaffinityai.com/api/) · [Webhooks](https://docs.joinaffinityai.com/guides/webhooks/)
