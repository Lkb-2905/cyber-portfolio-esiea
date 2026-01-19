from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from app.crypto import Envelope, b64decode, b64encode, generate_data_key, unwrap_key, wrap_key, xor_decrypt, xor_encrypt


@dataclass
class TeeConfig:
    master_key_path: Path


class TeeSimulator:
    def __init__(self, config: TeeConfig) -> None:
        self._config = config
        self._master_key = self._load_or_create_master_key()

    def _load_or_create_master_key(self) -> bytes:
        if self._config.master_key_path.exists():
            return self._config.master_key_path.read_bytes()
        self._config.master_key_path.parent.mkdir(parents=True, exist_ok=True)
        key = os.urandom(32)
        self._config.master_key_path.write_bytes(key)
        return key

    def seal(self, plaintext: bytes) -> Envelope:
        data_key = generate_data_key()
        nonce = os.urandom(16)
        ciphertext = xor_encrypt(plaintext, data_key)
        wrapped_key = wrap_key(data_key, self._master_key, nonce)
        return Envelope(
            ciphertext_b64=b64encode(ciphertext),
            wrapped_key_b64=b64encode(wrapped_key),
            nonce_b64=b64encode(nonce),
        )

    def unseal(self, envelope: Envelope) -> bytes:
        ciphertext = b64decode(envelope.ciphertext_b64)
        wrapped_key = b64decode(envelope.wrapped_key_b64)
        nonce = b64decode(envelope.nonce_b64)
        data_key = unwrap_key(wrapped_key, self._master_key, nonce)
        return xor_decrypt(ciphertext, data_key)
