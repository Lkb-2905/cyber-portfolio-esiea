from __future__ import annotations

from pydantic import BaseModel, Field


class InspectRequest(BaseModel):
    payload: str = Field(..., min_length=1)


class FindingModel(BaseModel):
    pii_type: str
    value: str


class InspectResponse(BaseModel):
    findings: list[FindingModel]
    redacted: str
