from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass


def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def derive_key(master_key: bytes, context: str) -> bytes:
    return hmac.new(master_key, context.encode("utf-8"), hashlib.sha256).digest()


def xor_encrypt(plaintext: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(plaintext)])


def xor_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return xor_encrypt(ciphertext, key)


@dataclass(frozen=True)
class Envelope:
    ciphertext_b64: str
    wrapped_key_b64: str
    nonce_b64: str


def generate_data_key() -> bytes:
    return secrets.token_bytes(32)


def wrap_key(data_key: bytes, master_key: bytes, nonce: bytes) -> bytes:
    mask = derive_key(master_key, b64encode(nonce))
    return xor_encrypt(data_key, mask)


def unwrap_key(wrapped_key: bytes, master_key: bytes, nonce: bytes) -> bytes:
    mask = derive_key(master_key, b64encode(nonce))
    return xor_decrypt(wrapped_key, mask)
