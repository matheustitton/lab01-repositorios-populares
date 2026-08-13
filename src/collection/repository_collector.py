"""Coleta dos repositorios mais populares (Parte 1).

Orquestra query + paginacao + mapeamento. Nao escreve CSV e nao imprime nada: devolve
`Repository` e deixa apresentacao e persistencia para as camadas de cima.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

from src.collection.mappers import to_repository
from src.collection.paginator import Page, SupportsExecute, paginate
from src.domain.models import Repository
from src.infrastructure.query_loader import load_query

QUERY_NAME = "search_repositories"

#: Teto da busca do GitHub: uma consulta nunca devolve mais que 1000 resultados.
SEARCH_RESULT_CAP = 1000


def extract_search_page(data: dict[str, Any]) -> Page:
    """Localiza `nodes`/`pageInfo` dentro de `data.search`."""
    search = data["search"]
    page_info = search.get("pageInfo") or {}
    return Page(
        nodes=search.get("nodes") or [],
        has_next_page=bool(page_info.get("hasNextPage")),
        end_cursor=page_info.get("endCursor"),
    )


def collect_repository_nodes(
    client: SupportsExecute,
    limit: int,
    page_size: int,
    on_page: Callable[[int, Page], None] | None = None,
    on_degrade: Callable[[int, int], None] | None = None,
) -> Iterator[dict[str, Any]]:
    """Coleta os nos crus, sem mapear - e o que alimenta o JSON bruto da Issue #1."""
    query = load_query(QUERY_NAME)
    variables = {"pageSize": min(page_size, limit)}
    return paginate(
        client,
        query,
        variables,
        extract_search_page,
        limit,
        on_page,
        page_size_key="pageSize",
        on_degrade=on_degrade,
    )


def collect_repositories(
    client: SupportsExecute,
    limit: int,
    page_size: int,
    on_page: Callable[[int, Page], None] | None = None,
    on_degrade: Callable[[int, int], None] | None = None,
) -> Iterator[Repository]:
    """Coleta ate `limit` repositorios ordenados por numero de estrelas."""
    for node in collect_repository_nodes(client, limit, page_size, on_page, on_degrade):
        yield to_repository(node)
