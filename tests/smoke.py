"""Exercise the installed wheel through its public clients, without live credentials."""

import asyncio
import importlib
import json
import pkgutil
import unittest

import affinity
import httpx
from affinity.client import Affinity, AsyncAffinity
from affinity.core.api_error import ApiError
from affinity.orders import PreviewOrderRequestPrescriptionsItem

PAGE = {"object": "list", "data": [], "hasMore": False, "url": "/v1/orders"}
PROBLEM = {"type": "about:blank", "title": "Invalid request", "status": 422,
           "detail": "Synthetic validation failure", "requestId": "req_sdk_test", "code": "VALIDATION_ERROR", "instance": "/v1/orders"}


class SdkTests(unittest.TestCase):
    def client(self, handler):
        transport = httpx.Client(transport=httpx.MockTransport(handler))
        self.addCleanup(transport.close)
        return Affinity(api_key="synthetic-key",
                        base_url="https://sdk-test.invalid", httpx_client=transport)

    def test_automatic_keys_are_per_call_and_stable_on_retry(self):
        keys = []
        def handle(request):
            keys.append(request.headers["Idempotency-Key"])
            return httpx.Response(503, json={**PROBLEM, "status": 503}, headers={"Retry-After": "0"})
        client = self.client(handle)
        for _ in range(2):
            with self.assertRaises(ApiError):
                client.patients.create(practice_id="prac_synthetic", name={"first": "Alex", "last": "Example"}, date_of_birth="1990-01-01", request_options={"max_retries": 1})
        self.assertEqual(len(keys), 4)
        self.assertTrue(keys[0])
        self.assertEqual(keys[0], keys[1])
        self.assertEqual(keys[2], keys[3])
        self.assertNotEqual(keys[0], keys[2])

    def test_all_modules_import(self):
        for module in pkgutil.walk_packages(affinity.__path__, affinity.__name__ + "."):
            importlib.import_module(module.name)

    def test_auth_version_query_and_page(self):
        def handle(request):
            self.assertEqual(request.method, "GET")
            self.assertEqual(request.url.path, "/v1/orders")
            self.assertEqual(request.headers["x-affinity-api-key"], "synthetic-key")
            self.assertEqual(request.headers["Affinity-Version"], "2026-09-28")
            self.assertEqual(request.headers["Affinity-Actor-Id"], "user-synthetic")
            self.assertEqual(request.headers["Affinity-Actor-Type"], "user")
            self.assertEqual(request.url.params["startingAfter"], "ord_cursor")
            self.assertEqual(request.url.params["limit"], "2")
            self.assertNotIn("patientId", request.url.params)
            return httpx.Response(200, json=PAGE)
        result = self.client(handle).orders.list(
            starting_after="ord_cursor", limit=2,
            affinity_actor_id="user-synthetic", affinity_actor_type="user")
        self.assertEqual(result.data, [])
        self.assertFalse(result.has_more)

    def test_preview_serialization_and_typed_error(self):
        def handle(request):
            self.assertEqual(request.url.path, "/v1/order-previews")
            self.assertEqual(json.loads(request.content), {
                "practiceId": "prac_synthetic", "patientId": "pat_synthetic",
                "prescriptions": [{"medicationId": "cat_synthetic"}]})
            return httpx.Response(422, json=PROBLEM)
        with self.assertRaises(ApiError) as caught:
            self.client(handle).orders.preview(
                practice_id="prac_synthetic", patient_id="pat_synthetic",
                prescriptions=[PreviewOrderRequestPrescriptionsItem(medication_id="cat_synthetic")])
        self.assertEqual(caught.exception.status_code, 422)
        self.assertIn("Synthetic validation failure", str(caught.exception))

    def test_keyed_write_retry_preserves_key_and_body(self):
        requests = []
        def handle(request):
            requests.append(request)
            return httpx.Response(503 if len(requests) == 1 else 422, json=PROBLEM)
        with self.assertRaises(ApiError):
            self.client(handle).orders.create(
                practice_id="prac_synthetic", patient_id="pat_synthetic", prescriptions=[],
                idempotency_key="stable-synthetic-key", request_options={"max_retries": 1})
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0].headers["Idempotency-Key"], "stable-synthetic-key")
        self.assertEqual(requests[0].headers["Idempotency-Key"], requests[1].headers["Idempotency-Key"])
        self.assertEqual(requests[0].content, requests[1].content)

    def test_retries_disabled_by_default(self):
        calls = []
        def handle(request):
            calls.append(request)
            return httpx.Response(503, json={**PROBLEM, "status": 503})
        with self.assertRaises(ApiError):
            self.client(handle).orders.list()
        self.assertEqual(len(calls), 1)

    def test_async_client(self):
        async def check():
            async with httpx.AsyncClient(transport=httpx.MockTransport(
                lambda request: httpx.Response(200, json=PAGE))) as transport:
                client = AsyncAffinity(api_key="synthetic-key",
                                       base_url="https://sdk-test.invalid", httpx_client=transport)
                result = await client.orders.list()
                self.assertEqual(result.data, [])
        asyncio.run(check())


if __name__ == "__main__":
    unittest.main(verbosity=2)
