from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/api/health")
    assert resp.status_code == 200


def test_items_crud() -> None:
    create_resp = client.post("/api/items", json={"name": "demo", "owner": "esiea"})
    assert create_resp.status_code == 200
    item = create_resp.json()

    list_resp = client.get("/api/items")
    assert list_resp.status_code == 200
    assert any(it["id"] == item["id"] for it in list_resp.json()["items"])

    delete_resp = client.delete(f"/api/items/{item['id']}")
    assert delete_resp.status_code == 200
