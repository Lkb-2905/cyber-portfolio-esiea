from __future__ import annotations

import hmac
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.crypto_utils import decode_secret, encode_secret, int_to_bytes, sha256_hex, bytes_to_int
from app.models import CombineRequest, CombineResponse, SignRequest, SignResponse, SplitRequest, SplitResponse
from app.shamir import PRIME, Share, combine_shares, split_secret

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="MPC Sandbox", version="1.0.0")

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/split", response_model=SplitResponse)
def split(request: SplitRequest) -> SplitResponse:
    try:
        secret_bytes = decode_secret(request.secret, request.encoding)
        secret_int = bytes_to_int(secret_bytes)
        shares = split_secret(secret_int, request.threshold, request.shares, PRIME)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    response_shares = [{"x": share.x, "y": hex(share.y)} for share in shares]
    return SplitResponse(
        prime=hex(PRIME),
        threshold=request.threshold,
        shares=request.shares,
        secret_hash=sha256_hex(secret_bytes),
        shares_data=response_shares,
    )


@app.post("/api/combine", response_model=CombineResponse)
def combine(request: CombineRequest) -> CombineResponse:
    try:
        shares = [Share(x=item.x, y=int(item.y, 16)) for item in request.shares]
        secret_int = combine_shares(shares, PRIME)
        secret_bytes = int_to_bytes(secret_int)
        encoded_secret, encoding_used = encode_secret(secret_bytes, request.encoding)
        secret_hash = sha256_hex(secret_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    matches_expected = None
    if request.expected_hash:
        matches_expected = request.expected_hash.lower() == secret_hash.lower()

    return CombineResponse(
        secret=encoded_secret,
        secret_hex=secret_bytes.hex(),
        secret_hash=secret_hash,
        encoding_used=encoding_used,
        matches_expected=matches_expected,
    )


@app.post("/api/sign", response_model=SignResponse)
def sign(request: SignRequest) -> SignResponse:
    try:
        shares = [Share(x=item.x, y=int(item.y, 16)) for item in request.shares]
        secret_int = combine_shares(shares, PRIME)
        secret_bytes = int_to_bytes(secret_int)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    signature = hmac.new(secret_bytes, request.message.encode("utf-8"), "sha256").hexdigest()
    return SignResponse(message=request.message, signature_hex=signature)
