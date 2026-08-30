"""Conversao de modelos de dominio em linhas de CSV.

Ponte entre `domain` e `storage`: o cabecalho e montado a partir do registro de metricas,
de modo que registrar uma nova RQ ja a faz aparecer no CSV sem alterar este arquivo.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from src.domain.metrics.registry import METRICS, MetricEntry, metric_columns, metrics_at
from src.domain.models import ProjectItem, Repository

#: Campos brutos que precedem as colunas derivadas do registro de metricas.
BASE_COLUMNS: tuple[str, ...] = (
    "name_with_owner",
    "url",
    "stars",
    "created_at",
    "pushed_at",
    "closed_issues",
    "total_issues",
)

PROJECT_COLUMNS: tuple[str, ...] = (
    "sprint",
    "captured_at",
    "issue_number",
    "title",
    "status",
    "state",
    "assignees",
    "labels",
    "url",
    "created_at",
    "closed_at",
)


def repository_header() -> tuple[str, ...]:
    """`BASE_COLUMNS` + colunas do registro de metricas, nessa ordem."""
    return BASE_COLUMNS + metric_columns()


def repository_row(
    repository: Repository,
    metrics: Sequence[MetricEntry] | None = None,
) -> list[object]:
    """Linha de CSV correspondente a um repositorio, alinhada ao cabecalho.

    `metrics` permite passar as metricas com o instante de referencia ja fixado
    (`metrics_at`), garantindo que todas as linhas usem o mesmo "agora".
    """
    entries = metrics if metrics is not None else METRICS
    return [
        repository.name_with_owner,
        repository.url,
        repository.stars,
        repository.created_at.isoformat(),
        repository.pushed_at.isoformat(),
        repository.closed_issues,
        repository.total_issues,
        *(entry.compute(repository) for entry in entries),
    ]


def repository_rows(
    repositories: Sequence[Repository],
    reference: datetime,
) -> list[list[object]]:
    """Serializa varios repositorios contra o mesmo instante de referencia."""
    metrics = metrics_at(reference)
    return [repository_row(r, metrics) for r in repositories]


def project_item_row(item: ProjectItem) -> list[object]:
    """Linha de CSV de um cartao do board; listas viram texto separado por `;`."""
    return [
        item.sprint,
        item.captured_at.isoformat(),
        item.issue_number if item.issue_number is not None else "",
        item.title,
        item.status or "",
        item.state or "",
        ";".join(item.assignees),
        ";".join(item.labels),
        item.url or "",
        item.created_at.isoformat() if item.created_at else "",
        item.closed_at.isoformat() if item.closed_at else "",
    ]
