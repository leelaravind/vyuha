"""Decoy content: fake resources that look plausible but hold nothing real.

Each decoy path returns generated content that resembles the kind of file an
intruder hopes to find (an env file, a config, a key list). The content is:

  * Fake. It is derived from a seed and never contains real secrets or data.
  * Consistent. The same path returns internally consistent content, so it does
    not look randomly assembled.
  * Rotating. Any credential-shaped value embedded in it comes from the rotating
    vault, so it expires quickly and is stale by the time anyone could use it.

This module only generates strings. It does no I/O.
"""

from __future__ import annotations

import hashlib

from .vault import RotatingVault


def _fake_hex(seed: str, n: int) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[:n]


def _seeded(path: str, deployment_seed: bytes, salt: str, n: int) -> str:
    """Per-deployment fake hex, so content differs across deployments (FR-9)."""
    material = deployment_seed + f"{path}:{salt}".encode()
    return hashlib.sha256(material).hexdigest()[:n]


def render(path: str, vault: RotatingVault, deployment_seed: bytes = b"") -> str:
    """Return plausible fake content for a decoy path.

    The embedded secret-shaped value is a current vault value, so if it is ever
    used it is already being rotated out.
    """
    token = vault.value()  # fake, expiring
    if path == "/.env":
        return (
            "APP_ENV=production\n"
            f"SECRET_KEY={token}\n"
            f"DB_PASSWORD={_seeded(path, deployment_seed, 'db', 24)}\n"
            "DB_HOST=10.0.0.14\n"
            "DEBUG=false\n"
        )
    if path == "/.git/config":
        return (
            "[core]\n\trepositoryformatversion = 0\n"
            "[remote \"origin\"]\n"
            "\turl = https://git.internal.example/app.git\n"
            f"\ttoken = {token}\n"
        )
    if path == "/backup/db.sql":
        return (
            "-- MySQL dump (partial)\n"
            "CREATE TABLE users (id INT, email VARCHAR(120), api_key CHAR(32));\n"
            f"INSERT INTO users VALUES (1,'ops@example.internal','{_fake_hex(path,32)}');\n"
            f"INSERT INTO users VALUES (2,'svc@example.internal','{token[:32]}');\n"
        )
    if path == "/admin/api-keys":
        return (
            "{\n"
            f'  "primary": "{token}",\n'
            f'  "secondary": "svc_{_fake_hex(path, 32)}",\n'
            '  "rotated_at": "recently"\n'
            "}\n"
        )
    if path == "/internal/credentials.json":
        return (
            "{\n"
            '  "service_account": "backup-runner",\n'
            f'  "key": "{token}",\n'
            '  "scope": "read-only"\n'
            "}\n"
        )
    # default plausible-looking response
    return f"# resource\ntoken={token}\n"
