from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List


@dataclass
class FlowRecord:
    timestamp: str
    src_ip: str
    dest_ip: str
    dest_port: int
    bytes_out: int
    label: str


def generate_flows(count: int = 500, anomaly_ratio: float = 0.1) -> List[FlowRecord]:
    random.seed(42)
    start_time = datetime.now(timezone.utc)
    records: List[FlowRecord] = []
    for i in range(count):
        ts = (start_time + timedelta(seconds=i * 15)).isoformat() + "Z"
        is_anomaly = random.random() < anomaly_ratio
        bytes_out = random.randint(300, 1800)
        dest_port = random.choice([80, 443, 8080, 53, 22])
        if is_anomaly:
            bytes_out = random.randint(8000, 20000)
            dest_port = random.choice([443, 8443, 9000])
        record = FlowRecord(
            timestamp=ts,
            src_ip="10.0.0.%d" % random.randint(2, 250),
            dest_ip="192.168.1.%d" % random.randint(2, 250),
            dest_port=dest_port,
            bytes_out=bytes_out,
            label="anomaly" if is_anomaly else "normal",
        )
        records.append(record)
    return records
