from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?33|0)\s?[1-9](?:[\s.-]?\d{2}){4}\b")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")


@dataclass
class Finding:
    pii_type: str
    value: str


def detect_pii(text: str) -> List[Finding]:
    findings: List[Finding] = []
    for match in EMAIL_RE.findall(text):
        findings.append(Finding(pii_type="email", value=match))
    for match in PHONE_RE.findall(text):
        findings.append(Finding(pii_type="phone", value=match))
    for match in IBAN_RE.findall(text):
        findings.append(Finding(pii_type="iban", value=match))
    return findings


def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    text = IBAN_RE.sub("[REDACTED_IBAN]", text)
    return text
