"""Registro ordenado das metricas.

Unica fonte de verdade sobre quais colunas derivadas existem e em que ordem aparecem no
CSV. Acrescentar uma RQ = criar o modulo dela e registrar uma entrada aqui; a
serializacao, o cabecalho do CSV e a analise seguem automaticamente.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from src.domain.metrics import (
    rq01_age,
    rq02_merged_pull_requests,
    rq03_releases,
    rq04_days_since_update,
    rq05_primary_language,
    rq06_closed_issues_ratio,
)
from src.domain.metrics.base import MetricValue
from src.domain.models import Repository


@dataclass(frozen=True)
class MetricEntry:
    rq: str
    column: str
    compute: Callable[[Repository], MetricValue]


METRICS: tuple[MetricEntry, ...] = (
    MetricEntry(rq01_age.RQ, rq01_age.COLUMN, rq01_age.age_in_years),
    MetricEntry(
        rq02_merged_pull_requests.RQ,
        rq02_merged_pull_requests.COLUMN,
        rq02_merged_pull_requests.merged_pull_requests,
    ),
    MetricEntry(rq03_releases.RQ, rq03_releases.COLUMN, rq03_releases.total_releases),
    MetricEntry(
        rq04_days_since_update.RQ,
        rq04_days_since_update.COLUMN,
        rq04_days_since_update.days_since_update,
    ),
    MetricEntry(
        rq05_primary_language.RQ,
        rq05_primary_language.COLUMN,
        rq05_primary_language.primary_language,
    ),
    MetricEntry(
        rq06_closed_issues_ratio.RQ,
        rq06_closed_issues_ratio.COLUMN,
        rq06_closed_issues_ratio.closed_issues_ratio,
    ),
)


def metric_columns() -> tuple[str, ...]:
    """Nomes das colunas derivadas, na ordem do registro."""
    return tuple(entry.column for entry in METRICS)
