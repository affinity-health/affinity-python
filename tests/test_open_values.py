"""A response with a value or field this SDK does not know decodes without an error.

The contract keeps response objects and value lists open: a later API version can add a status, a
category or a field. The fixture has an unknown order, prescription and history status, an unknown
allergy category and an added field at the root and in nested objects.
"""

import json
import pathlib
import typing

import httpx

from affinity import Affinity
from affinity.types.allergy_category import AllergyCategory
from affinity.types.order_status import OrderStatus

FIXTURE = json.loads((pathlib.Path(__file__).parent / "fixtures" / "order-unknown-values.json").read_text())


def client(*bodies: dict) -> Affinity:
    replies = list(bodies)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=replies.pop(0))

    return Affinity(
        token="sk_test_synthetic",
        base_url="https://api.example.test",
        httpx_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    )


def test_orders_get_keeps_unknown_values_and_added_fields() -> None:
    order = client(FIXTURE).orders.get(FIXTURE["id"])
    assert order.status == "on_hold"
    assert order.prescriptions[0].status == "on_hold"
    assert [entry.status for entry in order.status_history] == ["submitted", "on_hold"]
    assert [allergy.category for allergy in order.patient.allergies] == ["drug", "dust"]
    assert order.model_extra["addedField"] == {"nested": True}
    assert order.patient.model_extra["addedField"] == "patient"
    assert order.prescriptions[0].medication.model_extra["addedField"] == "medication"


def test_orders_list_iterates_unknown_values() -> None:
    page = lambda cursor: {  # noqa: E731
        "object": "list",
        "url": "/v1/orders",
        "data": [FIXTURE],
        "hasMore": cursor is not None,
        "nextCursor": cursor,
        "addedField": "list",
    }
    statuses = [order.status for order in client(page("cursor-a"), page(None)).orders.list()]
    assert statuses == ["on_hold", "on_hold"]


def test_known_values_stay_typed() -> None:
    known, _ = typing.get_args(OrderStatus)
    assert "awaiting_approval" in typing.get_args(known)
    known, _ = typing.get_args(AllergyCategory)
    assert typing.get_args(known) == ("drug", "food", "insect", "latex", "mold", "pet", "pollen")
