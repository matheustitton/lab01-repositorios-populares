"""Paginacao por cursor, generica.

Nao conhece repositorios nem itens de Project: recebe a query, as variaveis e uma funcao
que sabe onde estao `nodes` e `pageInfo` dentro da resposta. E por isso que a coleta dos
1000 repositorios (Parte 1) e o snapshot do board (Parte 2) compartilham este codigo.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any, Protocol

from src.infrastructure.http_client import HttpError
from src.infrastructure.retry import RETRYABLE_STATUS


@dataclass(frozen=True)
class Page:
    """Uma pagina ja localizada dentro da resposta GraphQL."""

    nodes: list[dict[str, Any]]
    has_next_page: bool
    end_cursor: str | None


#: Extrai a pagina de dentro do `data` retornado. Ex.: data -> data["search"].
PageExtractor = Callable[[dict[str, Any]], Page]

#: Menor pagina aceitavel antes de desistir e propagar o erro.
MIN_PAGE_SIZE = 5


class SupportsExecute(Protocol):
    """Minimo que o paginador exige de um cliente - permite injetar um fake nos testes."""

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]: ...


def paginate(
    client: SupportsExecute,
    query: str,
    variables: dict[str, Any],
    extract: PageExtractor,
    limit: int,
    on_page: Callable[[int, Page], None] | None = None,
    page_size_key: str | None = None,
    on_degrade: Callable[[int, int], None] | None = None,
) -> Iterator[dict[str, Any]]:
    """Percorre as paginas ate juntar `limit` nos, entregando um no por vez.

    `on_page` e um gancho opcional para logar progresso e persistir a pagina crua, sem
    que este modulo precise conhecer disco ou terminal.

    **Degradacao adaptativa:** quando `page_size_key` e informado, uma falha transitoria
    que sobreviveu ao retry (tipicamente 502) faz a pagina ser repetida com metade dos
    itens, ate `MIN_PAGE_SIZE`. Isso e necessario porque o custo da query cresce com o
    tamanho da pagina: pedir 25 repositorios com quatro `totalCount` agregados cada
    estoura o tempo de resposta do GitHub em trechos com repositorios muito grandes, e o
    erro e deterministico - repetir a mesma requisicao falha de novo, so pedir menos
    resolve. `on_degrade(anterior, novo)` avisa a camada de cima para logar.

    Nota de limite da API: `search` devolve no maximo 1000 resultados por consulta.
    Para ir alem disso, fatie por faixa de estrelas ("stars:100..500") e concatene -
    a assinatura ja suporta, bastando variar `variables`.
    """
    cursor: str | None = None
    delivered = 0
    index = 0
    page_size = variables.get(page_size_key) if page_size_key else None

    while delivered < limit:
        request = {**variables, "cursor": cursor}
        if page_size_key and page_size is not None:
            request[page_size_key] = page_size

        try:
            data = client.execute(query, request)
        except HttpError as exc:
            degradavel = (
                page_size_key is not None
                and page_size is not None
                and page_size > MIN_PAGE_SIZE
                and exc.status in RETRYABLE_STATUS
            )
            if not degradavel:
                raise
            anterior, page_size = page_size, max(MIN_PAGE_SIZE, page_size // 2)
            if on_degrade is not None:
                on_degrade(anterior, page_size)
            continue  # mesma posicao do cursor, pedindo menos itens

        page = extract(data)

        index += 1
        if on_page is not None:
            on_page(index, page)

        for node in page.nodes:
            if delivered >= limit:
                break
            # A busca pode devolver nos vazios quando o fragmento nao casa com o tipo.
            if not node:
                continue
            yield node
            delivered += 1

        # Para tambem quando o cursor nao avanca, o que evita laco infinito caso a API
        # repita a mesma pagina.
        if not page.has_next_page or page.end_cursor == cursor or page.end_cursor is None:
            break
        cursor = page.end_cursor
