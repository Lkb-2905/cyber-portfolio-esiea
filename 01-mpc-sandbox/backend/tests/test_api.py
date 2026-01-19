from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_split_and_combine_api() -> None:
    split_resp = client.post(
        "/api/split",
        json={"secret": "katvio-demo", "threshold": 3, "shares": 5, "encoding": "utf-8"},
    )
    assert split_resp.status_code == 200
    payload = split_resp.json()
    shares = payload["shares_data"][:3]

    combine_resp = client.post(
        "/api/combine",
        json={"shares": shares, "encoding": "utf-8", "expected_hash": payload["secret_hash"]},
    )
    assert combine_resp.status_code == 200
    combined = combine_resp.json()
    assert combined["secret"] == "katvio-demo"
    assert combined["matches_expected"] is True


def test_sign_api() -> None:
    split_resp = client.post(
        "/api/split",
        json={"secret": "sign-key", "threshold": 2, "shares": 3, "encoding": "utf-8"},
    )
    shares = split_resp.json()["shares_data"][:2]

    sign_resp = client.post(
        "/api/sign",
        json={"message": "hello", "shares": shares, "encoding": "utf-8"},
    )
    assert sign_resp.status_code == 200
    signature = sign_resp.json()["signature_hex"]
    assert isinstance(signature, str)
    assert len(signature) == 64
