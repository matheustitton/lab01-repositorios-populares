"""Paginacao por cursor, generica.

Nao conhece repositorios nem itens de Project: recebe a query, as variaveis e uma funcao
que sabe onde estao `nodes` e `pageInfo` dentro da resposta. E por isso que a coleta dos
1000 repositorios (Parte 1) e o snapshot do board (Parte 2) compartilham este codigo.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

from src.infrastructure.graphql_client import GraphQLClient


@dataclass(frozen=True)
class Page:
    """Uma pagina ja localizada dentro da resposta GraphQL."""

    nodes: list[dict[str, Any]]
    has_next_page: bool
    end_cursor: str | None


#: Extrai a pagina de dentro do `data` retornado. Ex.: data -> data["search"].
PageExtractor = Callable[[dict[str, Any]], Page]


def paginate(
    client: GraphQLClient,
    query: str,
    variables: dict[str, Any],
    extract: PageExtractor,
    limit: int,
    on_page: Callable[[int, Page], None] | None = None,
) -> Iterator[dict[str, Any]]:
    """Percorre as paginas ate juntar `limit` nos, entregando um no por vez.

    `on_page` e um gancho opcional para logar progresso e persistir a pagina crua, sem
    que este modulo precise conhecer disco ou terminal.

    Nota de limite da API: `search` devolve no maximo 1000 resultados por consulta.
    Para ir alem disso, fatie por faixa de estrelas ("stars:100..500") e concatene -
    a assinatura ja suporta, bastando variar `variables`.
    """
    raise NotImplementedError
