from app.crypto_utils import bytes_to_int, int_to_bytes
from app.shamir import PRIME, Share, combine_shares, split_secret


def test_split_combine_roundtrip() -> None:
    secret = b"esiea-mpc-sandbox"
    secret_int = bytes_to_int(secret)
    shares = split_secret(secret_int, threshold=3, shares=5, prime=PRIME)
    recovered = combine_shares(shares[:3], prime=PRIME)
    assert int_to_bytes(recovered) == secret


def test_requires_two_shares() -> None:
    share = Share(x=1, y=1234)
    try:
        combine_shares([share], prime=PRIME)
    except ValueError as exc:
        assert "at least two shares" in str(exc)
    else:
        assert False, "Expected ValueError"


def test_secret_too_large() -> None:
    secret_int = PRIME
    try:
        split_secret(secret_int, threshold=2, shares=2, prime=PRIME)
    except ValueError as exc:
        assert "too large" in str(exc)
    else:
        assert False, "Expected ValueError"
