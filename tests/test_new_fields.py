"""API 2026-11-01 additions on the wire: `query` on medications.list and `patient.id` on orders.create."""

import json

import httpx

from affinity import Affinity, AddressInput, PatientInput, PrescriberInput, PrescriptionInput
from affinity.orders import OrderInputShipping


def ident(prefix: str, n: int = 1) -> str:
    return f"{prefix}_{str(n).zfill(26)}"


def recorded(*bodies: dict) -> tuple[Affinity, list[httpx.Request]]:
    replies = list(bodies)
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=replies.pop(0))

    client = Affinity(
        token="sk_test_synthetic",
        base_url="https://api.example.test",
        httpx_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    )
    return client, requests


def page(n: int, next_cursor: str | None) -> dict:
    return {
        "object": "list",
        "url": "/v1/medications",
        "data": [{"id": ident("med", n), "name": f"Semaglutide {n}"}],
        "hasMore": next_cursor is not None,
        "nextCursor": next_cursor,
    }


def test_medications_list_sends_query_and_the_next_page_keeps_it() -> None:
    client, requests = recorded(page(1, "cursor-1"), page(2, None))
    names = [m.name for m in client.medications.list(query="semaglutide inj", limit=1)]
    assert names == ["Semaglutide 1", "Semaglutide 2"]
    assert [dict(r.url.params) for r in requests] == [
        {"limit": "1", "query": "semaglutide inj"},
        {"limit": "1", "query": "semaglutide inj", "startingAfter": "cursor-1"},
    ]


def test_medications_list_without_query_sends_no_query() -> None:
    client, requests = recorded(page(1, None))
    list(client.medications.list())
    assert "query" not in requests[0].url.params


def test_orders_create_sends_patient_id() -> None:
    client, requests = recorded({"id": ident("ord"), "patientId": ident("pat")})
    client.orders.create(
        idempotency_key="order-key-1",
        practice_id=ident("prac"),
        patient=PatientInput(
            id=ident("pat"),
            first_name="Test",
            last_name="Patient",
            date_of_birth="1990-01-01",
            sex="female",
            email="test.patient@example.test",
            phone="+15125550101",
            allergies=[],
            address=AddressInput(line1="200 Example Ave", city="Austin", state="TX", postal_code="78701"),
        ),
        prescriber=PrescriberInput(npi="1234567893", first_name="Sam", last_name="Lee"),
        prescriptions=[PrescriptionInput(medication_id=ident("med"), quantity=1, refills=0, directions="Use as directed.")],
        shipping=OrderInputShipping(option_id=ident("shp")),
        signature_attestation=True,
    )
    patient = json.loads(requests[0].content)["patient"]
    assert patient["id"] == ident("pat")
    assert "externalId" not in patient
