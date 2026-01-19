from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from app.detector import DetectionResult
from app.generator import FlowRecord


class FlowStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("[]", encoding="utf-8")

    def save(self, records: List[FlowRecord]) -> None:
        self._path.write_text(json.dumps([asdict(r) for r in records], indent=2), encoding="utf-8")

    def load(self) -> List[FlowRecord]:
        data = json.loads(self._path.read_text(encoding="utf-8"))
        return [FlowRecord(**item) for item in data]


class DetectionStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("[]", encoding="utf-8")

    def save(self, results: List[DetectionResult]) -> None:
        payload = []
        for result in results:
            record_dict = asdict(result.record)
            payload.append(
                {
                    "record": record_dict,
                    "score": result.score,
                    "prediction": result.prediction,
                }
            )
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> List[DetectionResult]:
        data = json.loads(self._path.read_text(encoding="utf-8"))
        results = []
        for item in data:
            record = FlowRecord(**item["record"])
            results.append(DetectionResult(record=record, score=item["score"], prediction=item["prediction"]))
        return results
