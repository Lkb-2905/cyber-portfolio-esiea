from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import Item, ItemCreate, ItemList

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="DevSecOps Demo API", version="1.0.0")

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

ITEMS: dict[str, Item] = {}


@app.get("/")
def index() -> FileResponse:
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/items", response_model=ItemList)
def list_items() -> ItemList:
    return ItemList(items=list(ITEMS.values()))


@app.post("/api/items", response_model=Item)
def create_item(payload: ItemCreate) -> Item:
    item_id = str(uuid.uuid4())
    item = Item(id=item_id, name=payload.name, owner=payload.owner)
    ITEMS[item_id] = item
    return item


@app.delete("/api/items/{item_id}")
def delete_item(item_id: str) -> dict:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="item not found")
    ITEMS.pop(item_id)
    return {"deleted": item_id}
