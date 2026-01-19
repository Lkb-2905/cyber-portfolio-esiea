from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_and_fetch() -> None:
    gen_resp = client.post("/api/generate", json={"count": 120, "anomaly_ratio": 0.2})
    assert gen_resp.status_code == 200
    summary = gen_resp.json()["summary"]
    assert summary["total"] == 120

    get_resp = client.get("/api/detections")
    assert get_resp.status_code == 200
