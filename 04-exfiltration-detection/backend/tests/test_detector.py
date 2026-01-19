from app.detector import ExfiltrationDetector
from app.generator import generate_flows


def test_detector_predicts() -> None:
    records = generate_flows(count=200, anomaly_ratio=0.15)
    detector = ExfiltrationDetector()
    detector.train(records)
    results = detector.predict(records)
    assert len(results) == len(records)
    assert any(result.prediction == "anomaly" for result in results)
