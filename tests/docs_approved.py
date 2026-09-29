from affinity import Affinity, AffinityError
from types import SimpleNamespace

api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-practice-0")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
patients = api.patients.list(params={'limit': 20})
patient = api.patients.get(patient_id)
items = api.catalog.items.list(params={'limit': 20})


api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-1")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
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



api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-2")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
practice = api.for_practice(practice_id)

patients = practice.patients.list(params={'limit': 20})
items = practice.catalog.items.list(params={'limit': 20})


api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-3")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
patient = practice.patients.create(
    params={
        'name': {'first': 'Alex', 'last': 'Example'},
        'date_of_birth': '1990-01-01',
    },
)

saved = practice.patients.get(patient.id)
practice.patients.update(patient.id, params={'email': 'alex@example.com'})
practice.patients.update(patient.id, params={'status': 'archived'})


api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-4")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
practice.patients.delete(patient_id)


api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-5")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
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



api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-6")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
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



api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-7")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
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


api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-8")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
try:
    practice.patients.get(patient_id)
except AffinityError as error:
    print(error.status, error.code, error.request_id, error.retryable, error.retry_after)


api=Affinity("test",base_url="http://127.0.0.1:5199/python-docs-platform-9")
practice_id,patient_id,order_id="prac_a","pat_a","ord_a"
practice=api.for_practice(practice_id)
draft=SimpleNamespace(prescriptions=[])
job=SimpleNamespace(create_order_key="create",sign_order_key="sign",submit_order_key="submit")
review=SimpleNamespace(prescriber_id="prov_a",order_revision="rev_a",signature_attestation=True)
def sync_patient(patient): pass
practices = api.practices.list(params={'limit': 20})
selected = api.practices.get(practice_id)
endpoints = api.webhooks.endpoints.list(params={'limit': 20})

