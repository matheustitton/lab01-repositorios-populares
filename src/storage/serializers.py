"""Conversao de modelos de dominio em linhas de CSV.

Ponte entre `domain` e `storage`: o cabecalho e montado a partir do registro de metricas,
de modo que registrar uma nova RQ ja a faz aparecer no CSV sem alterar este arquivo.
"""

from __future__ import annotations

from collections.abc import Sequence

from src.domain.models import ProjectItem, Repository

#: Campos brutos que precedem as colunas derivadas do registro de metricas.
BASE_COLUMNS: tuple[str, ...] = (
    "name_with_owner",
    "url",
    "stars",
    "created_at",
    "pushed_at",
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
    raise NotImplementedError


def repository_row(repository: Repository) -> Sequence[object]:
    """Linha de CSV correspondente a um repositorio, alinhada ao cabecalho."""
    raise NotImplementedError


def project_item_row(item: ProjectItem) -> Sequence[object]:
    """Linha de CSV de um cartao do board; listas viram texto separado por `;`."""
    raise NotImplementedError
