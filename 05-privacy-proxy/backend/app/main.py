from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.models import InspectRequest, InspectResponse
from app.pii_detector import detect_pii, redact_pii

app = FastAPI(title="Privacy Proxy", version="1.0.0")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/inspect", response_model=InspectResponse)
def inspect_payload(request: InspectRequest) -> InspectResponse:
    if not request.payload.strip():
        raise HTTPException(status_code=400, detail="payload is empty")
    findings = detect_pii(request.payload)
    redacted = redact_pii(request.payload)
    return InspectResponse(
        findings=[{"pii_type": f.pii_type, "value": f.value} for f in findings],
        redacted=redacted,
    )
