"""RQ01 - Sistemas populares sao maduros/antigos?

Metrica: idade do repositorio em anos, calculada a partir de `created_at`.
"""

from __future__ import annotations

from datetime import datetime

from src.domain.models import Repository

RQ = "rq01"
COLUMN = "age_years"

DAYS_IN_YEAR = 365.25


def age_in_years(repository: Repository, reference: datetime | None = None) -> float:
    """Idade em anos ate `reference` (default: agora, em UTC).

    `reference` e injetavel para que o teste seja deterministico.
    """
    raise NotImplementedError
