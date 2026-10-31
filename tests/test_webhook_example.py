"""Runs the webhook verification example from README.md against signatures made by openssl."""

import pathlib
import re
import shutil
import subprocess
import time

import pytest

README = pathlib.Path(__file__).resolve().parents[1] / "README.md"
SECRET = "whsec_test_only_not_a_real_secret"
BODY = b'{"id":"evt_test","type":"webhook_endpoint.test","createdAt":"2026-10-31T00:00:00Z","data":{}}'


def load_example():
    text = README.read_text()
    match = re.search(r"<!-- webhook-example:start -->\n```python\n(.*?)```\n<!-- webhook-example:end -->", text, re.S)
    assert match, "README.md has no webhook example block"
    namespace: dict = {}
    exec(match.group(1), namespace)  # noqa: S102 - the README's own code
    return namespace["verify_affinity_webhook"]


def openssl_signature(timestamp: int, body: bytes) -> str:
    if shutil.which("openssl") is None:
        pytest.skip("openssl is not installed")
    output = subprocess.run(
        ["openssl", "dgst", "-sha256", "-hmac", SECRET],
        input=f"{timestamp}.".encode() + body,
        capture_output=True,
        check=True,
    ).stdout.decode()
    return output.strip().split()[-1]


verify = load_example()


def test_accepts_a_valid_signature():
    t = int(time.time())
    header = f"t={t},v1=0000,v1={openssl_signature(t, BODY)}"
    assert verify(BODY, header, SECRET)["id"] == "evt_test"


def test_rejects_a_tampered_body():
    t = int(time.time())
    header = f"t={t},v1={openssl_signature(t, BODY)}"
    with pytest.raises(ValueError, match="does not match"):
        verify(BODY.replace(b"evt_test", b"evt_other"), header, SECRET)


def test_rejects_the_wrong_secret():
    t = int(time.time())
    header = f"t={t},v1={openssl_signature(t, BODY)}"
    with pytest.raises(ValueError, match="does not match"):
        verify(BODY, header, "whsec_other")


def test_rejects_an_old_timestamp():
    t = int(time.time()) - 301
    header = f"t={t},v1={openssl_signature(t, BODY)}"
    with pytest.raises(ValueError, match="tolerance"):
        verify(BODY, header, SECRET)


def test_rejects_a_malformed_header():
    with pytest.raises(ValueError, match="malformed"):
        verify(BODY, "v1=abc", SECRET)
