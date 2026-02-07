from fastapi import FastAPI, HTTPException
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
if not (BASE_DIR / "backend").exists():
    BASE_DIR = Path(__file__).resolve().parents[1]

import structlog
from prometheus_fastapi_instrumentator import Instrumentator

from app.models import InspectRequest, InspectResponse
from app.pii_detector import detect_pii, redact_pii

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

app = FastAPI(title="Privacy Proxy", version="1.0.0")

# Instrument FastAPI for Prometheus metrics
Instrumentator().instrument(app).expose(app)


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
