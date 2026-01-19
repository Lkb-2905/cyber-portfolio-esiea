from __future__ import annotations

import base64
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.models import RecordListResponse, SealRequest, SealResponse, UnsealResponse
from app.storage import EnvelopeStore
from app.tee_simulator import TeeConfig, TeeSimulator

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

store = EnvelopeStore(DATA_DIR / "sealed_records.json")
tee = TeeSimulator(TeeConfig(master_key_path=DATA_DIR / "tee_master_key.bin"))

app = FastAPI(title="Confidential Computing Sandbox", version="1.0.0")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/records", response_model=RecordListResponse)
def list_records() -> RecordListResponse:
    return RecordListResponse(record_ids=store.list_ids())


@app.post("/api/records", response_model=SealResponse)
def seal_record(request: SealRequest) -> SealResponse:
    try:
        if request.encoding.lower() in ("utf-8", "utf8"):
            plaintext = request.data.encode("utf-8")
        elif request.encoding.lower() == "base64":
            plaintext = base64.b64decode(request.data.encode("utf-8"))
        else:
            raise ValueError("unsupported encoding")
    except (ValueError, base64.binascii.Error) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    envelope = tee.seal(plaintext)
    record_id = str(uuid.uuid4())
    store.put(record_id, envelope)

    return SealResponse(record_id=record_id, **envelope.__dict__)


@app.get("/api/records/{record_id}", response_model=UnsealResponse)
def unseal_record(record_id: str, encoding: str = "utf-8") -> UnsealResponse:
    envelope = store.get(record_id)
    if not envelope:
        raise HTTPException(status_code=404, detail="record not found")

    plaintext = tee.unseal(envelope)
    plaintext_b64 = base64.b64encode(plaintext).decode("utf-8")

    encoding_used = encoding.lower()
    if encoding_used in ("utf-8", "utf8"):
        plaintext_out = plaintext.decode("utf-8", errors="replace")
        encoding_used = "utf-8"
    elif encoding_used == "base64":
        plaintext_out = plaintext_b64
        encoding_used = "base64"
    else:
        raise HTTPException(status_code=400, detail="unsupported encoding")

    return UnsealResponse(
        record_id=record_id,
        plaintext=plaintext_out,
        plaintext_b64=plaintext_b64,
        encoding_used=encoding_used,
    )
