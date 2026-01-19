from fastapi.testclient import TestClient

from app.main import app
from app.pii_detector import detect_pii, redact_pii

client = TestClient(app)


def test_detect_pii() -> None:
    text = "Email: jean.dupont@example.com, tel 0612345678, iban FR7630006000011234567890189"
    findings = detect_pii(text)
    assert any(f.pii_type == "email" for f in findings)
    assert any(f.pii_type == "phone" for f in findings)
    assert any(f.pii_type == "iban" for f in findings)


def test_redact() -> None:
    text = "Contact: jean.dupont@example.com"
    redacted = redact_pii(text)
    assert "[REDACTED_EMAIL]" in redacted


def test_api_inspect() -> None:
    payload = "Email: jean.dupont@example.com"
    resp = client.post("/api/inspect", json={"payload": payload})
    assert resp.status_code == 200
    data = resp.json()
    assert data["findings"][0]["pii_type"] == "email"
