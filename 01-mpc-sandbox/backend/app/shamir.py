from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Iterable, List, Tuple

PRIME = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F


@dataclass(frozen=True)
class Share:
    x: int
    y: int


def _eval_polynomial(coeffs: List[int], x: int, prime: int) -> int:
    result = 0
    power = 1
    for coeff in coeffs:
        result = (result + coeff * power) % prime
        power = (power * x) % prime
    return result


def split_secret(secret_int: int, threshold: int, shares: int, prime: int = PRIME) -> List[Share]:
    if threshold < 2:
        raise ValueError("threshold must be >= 2")
    if shares < threshold:
        raise ValueError("shares must be >= threshold")
    if secret_int <= 0:
        raise ValueError("secret must be a positive integer")
    if secret_int >= prime:
        raise ValueError("secret is too large for the field")

    coeffs = [secret_int] + [secrets.randbelow(prime) for _ in range(threshold - 1)]
    result: List[Share] = []
    for x in range(1, shares + 1):
        y = _eval_polynomial(coeffs, x, prime)
        result.append(Share(x=x, y=y))
    return result


def _lagrange_interpolate_zero(points: Iterable[Share], prime: int) -> int:
    points_list = list(points)
    if len(points_list) < 2:
        raise ValueError("at least two shares are required")

    x_values = [p.x for p in points_list]
    if len(set(x_values)) != len(x_values):
        raise ValueError("duplicate share x values are not allowed")

    secret = 0
    for j, share_j in enumerate(points_list):
        numerator = 1
        denominator = 1
        for m, share_m in enumerate(points_list):
            if m == j:
                continue
            numerator = (numerator * (-share_m.x)) % prime
            denominator = (denominator * (share_j.x - share_m.x)) % prime
        inv_denominator = pow(denominator, prime - 2, prime)
        lagrange_coeff = (numerator * inv_denominator) % prime
        secret = (secret + share_j.y * lagrange_coeff) % prime
    return secret


def combine_shares(shares: Iterable[Share], prime: int = PRIME) -> int:
    return _lagrange_interpolate_zero(shares, prime)
