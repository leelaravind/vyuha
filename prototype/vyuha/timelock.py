"""Time-lock puzzle (Rivest, Shamir & Wagner, 1996).

A time-lock puzzle asks a client to compute

    y = base ** (2 ** t) mod n

The only known way to do this without the factorisation of n is t modular
squarings performed one after another. Extra machines cannot shorten a single
chain of squarings, so the work takes a predictable amount of wall-clock time.

The party that created n knows its factors, and therefore knows phi(n). It can
reduce the exponent  2**t mod phi(n)  and get the same answer with one fast
pow() call. So the issuer creates and checks puzzles almost for free, while a
solver without the secret must spend the full sequential time.

This module is a plain, self-contained implementation of that published
construction. It performs no network, file, or system actions.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import secrets
from dataclasses import dataclass

# Small primes for cheap trial division before the (slower) primality test.
_SMALL_PRIMES = [
    p for p in range(3, 2000, 2)
    if all(p % d for d in range(3, math.isqrt(p) + 1, 2))
]


def _is_probable_prime(n: int, rounds: int = 40) -> bool:
    """Miller-Rabin primality test, after trial division by small primes."""
    if n < 2 or n % 2 == 0:
        return n == 2
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _random_prime(bits: int) -> int:
    """Return a random prime with the top and bottom bits set."""
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if _is_probable_prime(candidate):
            return candidate


@dataclass(frozen=True)
class Puzzle:
    """A puzzle handed to a solver. Contains nothing that helps skip the work."""

    n: int      # the modulus (product of two secret primes)
    base: int   # the starting value
    t: int      # number of sequential squarings required


class PuzzleMaker:
    """Holds the secret factors of n, which make issuing and checking cheap.

    A single PuzzleMaker can issue many puzzles from one modulus. Rotate the
    modulus periodically by creating a new PuzzleMaker.
    """

    def __init__(self, bits: int = 2048):
        half = bits // 2
        p = _random_prime(half)
        q = _random_prime(half)
        while q == p:
            q = _random_prime(half)
        self.n = p * q
        self._phi = (p - 1) * (q - 1)

    def make(self, t: int, base: int | None = None) -> tuple[Puzzle, int]:
        """Create a puzzle needing t squarings and return (puzzle, answer).

        The answer is computed instantly using the secret phi(n). If base is
        omitted a fresh random base is chosen (it must be coprime to n so the
        phi(n) shortcut is valid).
        """
        if base is None:
            while True:
                base = secrets.randbelow(self.n - 3) + 2
                if math.gcd(base, self.n) == 1:
                    break
        reduced_exponent = pow(2, t, self._phi)
        answer = pow(base, reduced_exponent, self.n)
        return Puzzle(self.n, base, t), answer

    def verify(self, puzzle: Puzzle, candidate: int) -> bool:
        """Check a solver's answer cheaply, using the secret phi(n)."""
        reduced_exponent = pow(2, puzzle.t, self._phi)
        expected = pow(puzzle.base, reduced_exponent, self.n)
        return hmac.compare_digest(str(expected), str(candidate))


def solve(puzzle: Puzzle) -> int:
    """Solve a puzzle the slow way: t squarings, one after another.

    This is what a solver without the secret must do. It is intentionally
    sequential; adding machines does not make a single call faster.
    """
    x = puzzle.base
    for _ in range(puzzle.t):
        x = x * x % puzzle.n
    return x


def derive_base(secret_key: bytes, puzzle_id: str, n: int) -> int:
    """Derive a puzzle's base deterministically from a server secret.

    This lets the issuer stay stateless: it can recompute the base for a given
    puzzle_id without storing it, and a solver still cannot choose the base.
    """
    material = hmac.new(secret_key, puzzle_id.encode(), hashlib.sha256).digest()
    return (int.from_bytes(material, "big") % (n - 3)) + 2
