"""RQ03 - Sistemas populares lancam releases com frequencia?

Metrica: total de releases publicadas.
"""

from __future__ import annotations

from src.domain.models import Repository

RQ = "rq03"
COLUMN = "releases"


def total_releases(repository: Repository) -> int:
    """Total de releases do repositorio."""
    raise NotImplementedError
