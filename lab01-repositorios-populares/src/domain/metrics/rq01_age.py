"""RQ01 - Sistemas populares sao maduros/antigos?

Metrica: idade do repositorio, calculada a partir de `created_at`.

Exposta em anos (para o relatorio) e em dias (para nao perder precisao em cruzamentos),
como pede a descricao da Issue #3.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.domain.models import Repository

RQ = "rq01"
COLUMN = "age_years"
COLUMN_DAYS = "age_days"

#: Media do calendario gregoriano, contando os anos bissextos.
DAYS_IN_YEAR = 365.25


def _reference(reference: datetime | None) -> datetime:
    return reference or datetime.now(timezone.utc)


def age_in_days(repository: Repository, reference: datetime | None = None) -> float:
    """Idade em dias ate `reference` (default: agora, em UTC)."""
    delta = _reference(reference) - repository.created_at
    return round(delta.total_seconds() / 86400, 2)


def age_in_years(repository: Repository, reference: datetime | None = None) -> float:
    """Idade em anos ate `reference` (default: agora, em UTC).

    `reference` e injetavel para que o teste seja deterministico e para que todos os
    repositorios de uma mesma execucao sejam medidos contra o mesmo instante.
    """
    return round(age_in_days(repository, reference) / DAYS_IN_YEAR, 2)
