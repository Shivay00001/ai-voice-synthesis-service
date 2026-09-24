import os
from fastapi.testclient import TestClient

# sandbox quirk: NO_PROXY contains patterns httpx cannot parse
os.environ.pop("no_proxy", None)
os.environ.pop("NO_PROXY", None)

from main import app  # noqa: E402

client = TestClient(app)


def test_health_reports_key_status():
    os.environ.pop("ELEVENLABS_API_KEY", None)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["key_configured"] is False


def test_synthesize_without_key_is_honest_error():
    os.environ.pop("ELEVENLABS_API_KEY", None)
    r = client.post("/synthesize", json={"text": "Hello world"})
    assert r.status_code == 503
    assert "ELEVENLABS_API_KEY" in r.json()["detail"]


def test_synthesize_with_dummy_key_gets_real_401():
    os.environ["ELEVENLABS_API_KEY"] = "dummy-key-for-testing"
    try:
        r = client.post("/synthesize", json={"text": "Hello world"})
    finally:
        os.environ.pop("ELEVENLABS_API_KEY", None)
    # real HTTP client -> real provider -> honest 401 (proves plumbing is real)
    assert r.status_code == 401, (r.status_code, r.text[:200])


def test_voices_with_dummy_key_gets_real_401():
    os.environ["ELEVENLABS_API_KEY"] = "dummy-key-for-testing"
    try:
        r = client.get("/voices")
    finally:
        os.environ.pop("ELEVENLABS_API_KEY", None)
    assert r.status_code == 401, (r.status_code, r.text[:200])


def test_empty_text_rejected():
    os.environ["ELEVENLABS_API_KEY"] = "dummy-key-for-testing"
    try:
        r = client.post("/synthesize", json={"text": "   "})
    finally:
        os.environ.pop("ELEVENLABS_API_KEY", None)
    assert r.status_code == 400
