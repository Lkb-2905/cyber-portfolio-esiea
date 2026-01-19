from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    count: int = Field(default=500, ge=50, le=5000)
    anomaly_ratio: float = Field(default=0.1, ge=0.01, le=0.5)


class DetectionSummary(BaseModel):
    total: int
    anomalies: int
    anomaly_ratio: float


class DetectionItem(BaseModel):
    timestamp: str
    src_ip: str
    dest_ip: str
    dest_port: int
    bytes_out: int
    label: str
    prediction: str
    score: float


class DetectionResponse(BaseModel):
    summary: DetectionSummary
    items: list[DetectionItem]
