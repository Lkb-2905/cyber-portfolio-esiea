from __future__ import annotations

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    owner: str = Field(..., min_length=1, max_length=80)


class Item(BaseModel):
    id: str
    name: str
    owner: str


class ItemList(BaseModel):
    items: list[Item]
