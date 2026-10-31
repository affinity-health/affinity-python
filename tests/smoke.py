"""Calls every operation of the installed SDK against a real Affinity API in Test mode.

    AFFINITY_API_KEY=sk_test_... [AFFINITY_BASE_URL=https://...] \\
      [AFFINITY_SMOKE_WEBHOOK_URL=https://...] python tests/smoke.py

It refuses a key that is not a Test key. Use a platform Test key: it creates a practice and a Test
order (sent to the API's test pharmacy) and cancels the order. With AFFINITY_SMOKE_WEBHOOK_URL it
also creates, updates and removes a webhook endpoint. Feedback is sent only as an invalid request,
so no one is notified. The Test practice stays: the API has no way to remove a practice.
Exits 1 when any check fails. pytest does not collect this file.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import os
import sys
import traceback
import typing
import uuid

from affinity import (
    AddressInput,
    Affinity,
    AsyncAffinity,
    BadRequestError,
    NotFoundError,
    PatientInput,
    PrescriberInput,
    PrescriptionInput,
    UnauthorizedError,
    UnprocessableEntityError,
)
from affinity.core.api_error import ApiError
from affinity.orders import OrderInputShipping

KEY = os.environ.get("AFFINITY_API_KEY", "")
if not KEY.startswith("sk_test_"):
    sys.exit("Set AFFINITY_API_KEY to a Test key (sk_test_...).")
BASE_URL = os.environ.get("AFFINITY_BASE_URL") or None
WEBHOOK_URL = os.environ.get("AFFINITY_SMOKE_WEBHOOK_URL") or None
DIRECTIONS = "SDK smoke test. TEST ONLY. DO NOT FILL."

T = typing.TypeVar("T")
results: list[tuple[str, bool, str]] = []


def describe(error: BaseException) -> str:
    if isinstance(error, ApiError):
        body = error.body
        code = body.get("code", "") if isinstance(body, dict) else getattr(body, "code", "")
        return f"{type(error).__name__} {error.status_code} {code}"
    return f"{type(error).__name__}: {str(error)[:300]}"


def check(name: str, work: typing.Callable[[], T], note: typing.Callable[[T], str] | None = None) -> T | None:
    try:
        value = work()
    except Exception as error:  # noqa: BLE001 - every failure is a FAIL line
        results.append((name, False, describe(error)))
        if os.environ.get("SMOKE_TRACEBACK"):
            traceback.print_exc()
        return None
    results.append((name, True, note(value) if note else ""))
    return value


def refused(
    name: str,
    error_class: type[BaseException],
    work: typing.Callable[[], object],
    inspect: typing.Callable[[typing.Any], str | None] | None = None,
) -> None:
    try:
        work()
    except Exception as error:  # noqa: BLE001
        if not isinstance(error, error_class):
            results.append((name, False, f"got {describe(error)}"))
            return
        problem = inspect(error) if inspect else None
        results.append((name, problem is None, problem or describe(error)))
        return
    results.append((name, False, "succeeded"))


def key() -> str:
    return str(uuid.uuid4())


client = Affinity(token=KEY, base_url=BASE_URL, max_retries=0)
label = f"SDK smoke {dt.datetime.now(dt.timezone.utc).isoformat()}"
order_ids: list[str] = []
endpoint_ids: list[str] = []


def run() -> None:
    account = check("account.get", client.account.get, lambda a: f"{a.type} {a.mode}")
    if account is None or account.mode != "test":
        raise RuntimeError("This smoke test runs only with a Test key.")
    if account.type != "platform":
        raise RuntimeError("Use a platform Test key: it creates a practice.")

    refused(
        "a bad key raises UnauthorizedError",
        UnauthorizedError,
        lambda: Affinity(token="sk_test_not_a_key", base_url=BASE_URL, max_retries=0).account.get(),
    )
    refused(
        "feedback.create without a message raises BadRequestError",
        BadRequestError,
        lambda: client.feedback.create(idempotency_key=key(), message=""),
    )

    practice = check(
        "practices.create",
        lambda: client.practices.create(
            idempotency_key=key(),
            name=label,
            phone="+15125550100",
            address=AddressInput(line1="100 Congress Ave", city="Austin", state="TX", postal_code="78701"),
        ),
        lambda p: p.id,
    )
    if practice is None:
        raise RuntimeError("No practice; stopping.")
    check("practices.get", lambda: client.practices.get(practice.id), lambda p: p.name)
    check(
        "practices.update",
        lambda: client.practices.update(practice.id, idempotency_key=key(), name=f"{label} renamed"),
        lambda p: p.name,
    )

    def every_practice() -> int:
        ids = [p.id for p in client.practices.list(limit=1)]
        if practice.id not in ids:
            raise RuntimeError("the new practice is not listed")
        return len(ids)

    check("practices.list (every page, 1 per page)", every_practice, lambda n: f"{n} practices")

    check(
        "medications.list (one page)",
        lambda: client.medications.list(limit=5),
        lambda page: f"{len(page.items or [])}, more: {page.has_next}",
    )

    def every_medication() -> list[typing.Any]:
        medications = list(client.medications.list(limit=25))
        if len({m.id for m in medications}) != len(medications):
            raise RuntimeError("a medication repeats across pages")
        return medications

    medications = check("medications.list (every page, 25 per page)", every_medication, lambda m: f"{len(m)} medications")
    medications = medications or []
    medication = next(
        (m for m in medications if not m.cold_chain_required and m.shipping_options and not m.requirements),
        next((m for m in medications if m.shipping_options), None),
    )
    if medication is None:
        raise RuntimeError("No orderable medication in Test mode; stopping.")
    check(
        "medications.get",
        lambda: client.medications.get(medication.id),
        lambda m: f"{m.name} ({m.pharmacy.name})",
    )
    check(
        "medications.get expand=variants",
        lambda: client.medications.get(medication.id, expand="variants"),
        lambda m: f"{len(m.variants or [])} variants",
    )
    check(
        "medications.list for a practice",
        lambda: client.medications.list(limit=5, practice_id=practice.id),
        lambda page: f"{len(page.items or [])}",
    )

    def order_input(quantity: int) -> dict[str, typing.Any]:
        prescription = PrescriptionInput(
            medication_id=medication.id,
            quantity=quantity,
            refills=0,
            directions=DIRECTIONS,
            **(
                {"compounding_reason": medication.compounding_reasons[0]}
                if "compoundingReason" in medication.requirements and medication.compounding_reasons
                else {}
            ),
        )
        return dict(
            idempotency_key=key(),
            external_order_id=f"sdk-smoke-{key()[:8]}",
            patient=PatientInput(
                external_id=f"sdk-smoke-{key()}",
                first_name="Test",
                last_name="Smoke",
                date_of_birth="1988-04-02",
                sex="female",
                email=f"sdk-smoke-{key()[:8]}@example.test",
                phone="+15125550101",
                allergies=[],
                address=AddressInput(line1="200 Congress Ave", city="Austin", state="TX", postal_code="78701"),
            ),
            practice_id=practice.id,
            prescriber=PrescriberInput(npi="1234567893", first_name="Sam", last_name="Lee"),
            prescriptions=[prescription],
            shipping=OrderInputShipping(option_id=medication.shipping_options[0].id),
            signature_attestation=True,
        )

    def created(request: dict[str, typing.Any]) -> object:
        order = client.orders.create(**request)
        order_ids.append(order.id)
        return order

    quantity = medication.quantities[0] if medication.quantities else 1
    request = order_input(quantity)
    order = check("orders.create", lambda: client.orders.create(**request), lambda o: f"{o.id} {o.status}")
    if order is not None:
        order_ids.append(order.id)

    def create_again() -> str:
        again = client.orders.create(**request)
        if order is None or again.id != order.id:
            order_ids.append(again.id)
            raise RuntimeError(f"created a second order {again.id}")
        return again.id

    check("orders.create again with the same key returns the same order", create_again)

    def quantity_issue(error: UnprocessableEntityError) -> str | None:
        issues = error.body.issues or []
        if any(issue.field == "prescriptions[0].quantity" for issue in issues):
            return None
        return f"issues {[issue.field for issue in issues]}"

    refused(
        "an unaccepted quantity raises UnprocessableEntityError with the field",
        UnprocessableEntityError,
        lambda: created(order_input(max([0, *medication.quantities]) + 1)),
        quantity_issue,
    )
    refused(
        "orders.create without idempotency_key raises TypeError locally",
        TypeError,
        lambda: created({k: v for k, v in order_input(quantity).items() if k != "idempotency_key"}),
    )

    if order is not None:
        check(
            "orders.get",
            lambda: client.orders.get(order.id),
            lambda o: f"{o.status}, {len(o.prescriptions)} prescription",
        )

        def by_external_id() -> str:
            ids = [o.id for o in client.orders.list(external_order_id=request["external_order_id"]).items or []]
            if ids != [order.id]:
                raise RuntimeError(f"found {ids}")
            return ids[0]

        check("orders.list by external_order_id", by_external_id)
        hour_ago = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)
        check(
            "orders.list updated_after (milliseconds)",
            lambda: client.orders.list(updated_after=hour_ago.replace(microsecond=hour_ago.microsecond // 1000 * 1000), limit=5),
            lambda page: f"{len(page.items or [])}",
        )
        check(
            "orders.list updated_after (microseconds, a datetime)",
            lambda: client.orders.list(updated_after=dt.datetime(2026, 1, 1, 0, 0, 0, 123456, tzinfo=dt.timezone.utc), limit=5),
            lambda page: f"{len(page.items or [])}",
        )
        # A datetime holds microseconds at most; send nanoseconds as a raw query parameter.
        check(
            "orders.list updatedAfter (nanoseconds, raw query parameter)",
            lambda: client.orders.list(
                limit=5,
                request_options={"additional_query_parameters": {"updatedAfter": "2026-01-01T00:00:00.123456789Z"}},
            ),
            lambda page: f"{len(page.items or [])}",
        )

        def every_order() -> int:
            count = sum(1 for _ in client.orders.list(limit=1, practice_id=practice.id))
            if count != 1:
                raise RuntimeError(f"{count} orders for a practice with 1")
            return count

        check("orders.list (every page, 1 per page)", every_order)
        check(
            "orders.cancel",
            lambda: client.orders.cancel(order.id, idempotency_key=key()),
            lambda o: f"{o.status}{', waiting for the pharmacy' if o.cancel_requested_at else ''}",
        )

    refused(
        "orders.get for an unknown order raises NotFoundError",
        NotFoundError,
        lambda: client.orders.get("ord_01j2y8m6jcc9tt24af5pw9x1bc"),
    )

    if WEBHOOK_URL:
        endpoint = check(
            "webhooks.create",
            lambda: client.webhooks.create(idempotency_key=key(), url=f"{WEBHOOK_URL.rstrip('/')}/{uuid.uuid4()}"),
            lambda e: e.id,
        )
        if endpoint is not None:
            endpoint_ids.append(endpoint.id)

            def every_endpoint() -> int:
                ids = [e.id for e in client.webhooks.list()]
                if endpoint.id not in ids:
                    raise RuntimeError("the new endpoint is not listed")
                return len(ids)

            check("webhooks.list (every page)", every_endpoint, str)
            check(
                "webhooks.update",
                lambda: client.webhooks.update(
                    endpoint.id, idempotency_key=key(), url=f"{WEBHOOK_URL.rstrip('/')}/{uuid.uuid4()}"
                ),
                lambda e: e.id,
            )
            check(
                "webhooks.resend_failed",
                lambda: client.webhooks.resend_failed(endpoint.id, idempotency_key=key()),
                lambda r: repr(r)[:200],
            )

            def remove() -> str:
                client.webhooks.remove(endpoint.id)
                endpoint_ids.remove(endpoint.id)
                return "removed"

            check("webhooks.remove", remove)
    else:
        results.append(("webhooks (AFFINITY_SMOKE_WEBHOOK_URL is not set)", False, "skipped"))

    def request_id() -> str:
        response = client.account.with_raw_response.get()
        value = response.headers.get("x-request-id")
        if not value:
            raise RuntimeError("no X-Request-Id header")
        return value

    check("with_raw_response gives the request ID", request_id)

    async def async_reads() -> str:
        async_client = AsyncAffinity(token=KEY, base_url=BASE_URL, max_retries=0)
        account = await async_client.account.get()
        count = 0
        async for _ in await async_client.medications.list(limit=25):
            count += 1
        return f"{account.mode}, {count} medications"

    check("AsyncAffinity account.get and every medication", lambda: asyncio.run(async_reads()), str)


try:
    run()
except Exception as error:  # noqa: BLE001
    results.append(("stopped", False, describe(error)))
finally:
    for order_id in order_ids:
        try:
            client.orders.cancel(order_id, idempotency_key=key())
        except Exception:  # noqa: BLE001 - already cancelled
            pass
    for endpoint_id in endpoint_ids:
        try:
            client.webhooks.remove(endpoint_id)
        except Exception:  # noqa: BLE001
            pass

for name, ok, note in results:
    print(f"{'PASS' if ok else 'FAIL'} {name}{f' - {note}' if note else ''}")
failed = sum(1 for _, ok, _ in results if not ok)
print(f"{len(results) - failed} of {len(results)} checks passed.")
sys.exit(1 if failed else 0)
