from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np
from sklearn.ensemble import IsolationForest

from app.generator import FlowRecord


@dataclass
class DetectionResult:
    record: FlowRecord
    score: float
    prediction: str


class ExfiltrationDetector:
    def __init__(self) -> None:
        self._model = IsolationForest(
            n_estimators=200,
            contamination=0.1,
            random_state=42,
        )
        self._trained = False

    def _features(self, record: FlowRecord) -> List[float]:
        return [record.bytes_out, record.dest_port]

    def train(self, records: Iterable[FlowRecord]) -> None:
        features = np.array([self._features(r) for r in records])
        self._model.fit(features)
        self._trained = True

    def predict(self, records: Iterable[FlowRecord]) -> List[DetectionResult]:
        if not self._trained:
            raise ValueError("Detector not trained")
        features = np.array([self._features(r) for r in records])
        scores = self._model.decision_function(features)
        preds = self._model.predict(features)
        results: List[DetectionResult] = []
        for record, score, pred in zip(records, scores, preds):
            results.append(
                DetectionResult(
                    record=record,
                    score=float(score),
                    prediction="anomaly" if pred == -1 else "normal",
                )
            )
        return results
