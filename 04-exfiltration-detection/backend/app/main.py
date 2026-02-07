from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import structlog
from prometheus_fastapi_instrumentator import Instrumentator

from app.detector import ExfiltrationDetector
from app.generator import generate_flows
from app.models import DetectionItem, DetectionResponse, DetectionSummary, GenerateRequest
from app.storage import DetectionStore, FlowStore

BASE_DIR = Path(__file__).resolve().parents[2]
if not (BASE_DIR / "backend").exists():
    BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

flow_store = FlowStore(DATA_DIR / "flows.json")
detection_store = DetectionStore(DATA_DIR / "detections.json")
detector = ExfiltrationDetector()

app = FastAPI(title="Exfiltration Detection", version="1.0.0")

# Instrument FastAPI for Prometheus metrics
Instrumentator().instrument(app).expose(app)

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


@app.post("/api/generate", response_model=DetectionResponse)
def generate_and_detect(request: GenerateRequest) -> DetectionResponse:
    records = generate_flows(count=request.count, anomaly_ratio=request.anomaly_ratio)
    detector.train(records)
    results = detector.predict(records)
    flow_store.save(records)
    detection_store.save(results)

    items = []
    anomalies = 0
    for result in results:
        if result.prediction == "anomaly":
            anomalies += 1
        items.append(
            DetectionItem(
                timestamp=result.record.timestamp,
                src_ip=result.record.src_ip,
                dest_ip=result.record.dest_ip,
                dest_port=result.record.dest_port,
                bytes_out=result.record.bytes_out,
                label=result.record.label,
                prediction=result.prediction,
                score=result.score,
            )
        )

    total = len(items)
    summary = DetectionSummary(
        total=total,
        anomalies=anomalies,
        anomaly_ratio=round(anomalies / total if total else 0, 3),
    )
    return DetectionResponse(summary=summary, items=items)


@app.get("/api/detections", response_model=DetectionResponse)
def get_last_detection() -> DetectionResponse:
    results = detection_store.load()
    if not results:
        raise HTTPException(status_code=404, detail="No detections yet")

    items = []
    anomalies = 0
    for result in results:
        if result.prediction == "anomaly":
            anomalies += 1
        items.append(
            DetectionItem(
                timestamp=result.record.timestamp,
                src_ip=result.record.src_ip,
                dest_ip=result.record.dest_ip,
                dest_port=result.record.dest_port,
                bytes_out=result.record.bytes_out,
                label=result.record.label,
                prediction=result.prediction,
                score=result.score,
            )
        )

    total = len(items)
    summary = DetectionSummary(
        total=total,
        anomalies=anomalies,
        anomaly_ratio=round(anomalies / total if total else 0, 3),
    )
    return DetectionResponse(summary=summary, items=items)
