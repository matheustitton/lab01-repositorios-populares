"""Coleta dos repositorios mais populares (Parte 1).

Orquestra query + paginacao + mapeamento. Nao escreve CSV e nao imprime nada: devolve
`Repository` e deixa apresentacao e persistencia para as camadas de cima.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

from src.collection.paginator import Page
from src.domain.models import Repository
from src.infrastructure.graphql_client import GraphQLClient


def extract_search_page(data: dict[str, Any]) -> Page:
    """Localiza `nodes`/`pageInfo` dentro de `data.search`."""
    raise NotImplementedError


def collect_repositories(
    client: GraphQLClient,
    limit: int,
    page_size: int,
    on_page: Callable[[int, Page], None] | None = None,
) -> Iterator[Repository]:
    """Coleta ate `limit` repositorios ordenados por numero de estrelas."""
    raise NotImplementedError
