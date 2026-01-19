from __future__ import annotations

from pydantic import BaseModel, Field


class SealRequest(BaseModel):
    data: str = Field(..., min_length=1)
    encoding: str = Field(default="utf-8")


class SealResponse(BaseModel):
    record_id: str
    ciphertext_b64: str
    wrapped_key_b64: str
    nonce_b64: str


class UnsealResponse(BaseModel):
    record_id: str
    plaintext: str
    plaintext_b64: str
    encoding_used: str


class RecordListResponse(BaseModel):
    record_ids: list[str]
