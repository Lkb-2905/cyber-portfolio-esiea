from __future__ import annotations

import base64
import hashlib


def bytes_to_int(value: bytes) -> int:
    return int.from_bytes(value, byteorder="big", signed=False)


def int_to_bytes(value: int) -> bytes:
    if value == 0:
        return b"\x00"
    length = (value.bit_length() + 7) // 8
    return value.to_bytes(length, byteorder="big", signed=False)


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_secret(secret: str, encoding: str) -> bytes:
    normalized = encoding.lower()
    if normalized in ("utf-8", "utf8"):
        return secret.encode("utf-8")
    if normalized == "hex":
        return bytes.fromhex(secret)
    if normalized == "base64":
        return base64.b64decode(secret.encode("utf-8"))
    raise ValueError(f"unsupported encoding: {encoding}")


def encode_secret(secret_bytes: bytes, encoding: str) -> tuple[str, str]:
    normalized = encoding.lower()
    if normalized in ("utf-8", "utf8"):
        try:
            return secret_bytes.decode("utf-8"), "utf-8"
        except UnicodeDecodeError:
            return base64.b64encode(secret_bytes).decode("utf-8"), "base64"
    if normalized == "hex":
        return secret_bytes.hex(), "hex"
    if normalized == "base64":
        return base64.b64encode(secret_bytes).decode("utf-8"), "base64"
    raise ValueError(f"unsupported encoding: {encoding}")
