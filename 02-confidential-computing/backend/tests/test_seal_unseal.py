from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_seal_and_unseal_roundtrip() -> None:
    seal_resp = client.post("/api/records", json={"data": "secret-tee", "encoding": "utf-8"})
    assert seal_resp.status_code == 200
    payload = seal_resp.json()
    record_id = payload["record_id"]

    unseal_resp = client.get(f"/api/records/{record_id}?encoding=utf-8")
    assert unseal_resp.status_code == 200
    unsealed = unseal_resp.json()
    assert unsealed["plaintext"] == "secret-tee"


def test_list_records() -> None:
    client.post("/api/records", json={"data": "alpha", "encoding": "utf-8"})
    list_resp = client.get("/api/records")
    assert list_resp.status_code == 200
    assert len(list_resp.json()["record_ids"]) >= 1
