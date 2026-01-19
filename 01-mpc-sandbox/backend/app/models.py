from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ShareModel(BaseModel):
    x: int = Field(..., ge=1)
    y: str = Field(..., min_length=1, description="Hex-encoded share value")


class SplitRequest(BaseModel):
    secret: str = Field(..., min_length=1)
    threshold: int = Field(..., ge=2)
    shares: int = Field(..., ge=2)
    encoding: str = Field(default="utf-8")


class SplitResponse(BaseModel):
    prime: str
    threshold: int
    shares: int
    secret_hash: str
    shares_data: List[ShareModel]


class CombineRequest(BaseModel):
    shares: List[ShareModel]
    encoding: str = Field(default="utf-8")
    expected_hash: Optional[str] = None


class CombineResponse(BaseModel):
    secret: str
    secret_hex: str
    secret_hash: str
    encoding_used: str
    matches_expected: Optional[bool] = None


class SignRequest(BaseModel):
    message: str = Field(..., min_length=1)
    shares: List[ShareModel]
    encoding: str = Field(default="utf-8")


class SignResponse(BaseModel):
    message: str
    signature_hex: str
