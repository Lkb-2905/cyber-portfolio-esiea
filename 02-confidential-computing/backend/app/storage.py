from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict

from app.crypto import Envelope


class EnvelopeStore:
    def __init__(self, storage_path: Path) -> None:
        self._storage_path = storage_path
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._storage_path.exists():
            self._storage_path.write_text("{}", encoding="utf-8")

    def _load(self) -> Dict[str, dict]:
        return json.loads(self._storage_path.read_text(encoding="utf-8"))

    def _save(self, data: Dict[str, dict]) -> None:
        self._storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def put(self, record_id: str, envelope: Envelope) -> None:
        data = self._load()
        data[record_id] = asdict(envelope)
        self._save(data)

    def get(self, record_id: str) -> Envelope | None:
        data = self._load()
        record = data.get(record_id)
        if not record:
            return None
        return Envelope(**record)

    def list_ids(self) -> list[str]:
        return sorted(self._load().keys())
