"""Validacao da paginacao por cursor, usando `FakeGraphQLClient` (sem rede)."""

from __future__ import annotations

import pytest

from src.collection.paginator import MIN_PAGE_SIZE, Page, paginate
from src.collection.repository_collector import extract_search_page
from src.infrastructure.http_client import HttpError
from tests.conftest import FakeGraphQLClient


def _data(ids, *, has_next, cursor):
    return {
        "search": {
            "nodes": [{"nameWithOwner": f"org/repo{i}"} for i in ids],
            "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
        }
    }


def _paginate(client, limit, on_page=None):
    return list(paginate(client, "query {}", {}, extract_search_page, limit, on_page))


def test_extract_search_page_localiza_nodes_e_pageinfo():
    page = extract_search_page(_data([1, 2], has_next=True, cursor="abc"))

    assert isinstance(page, Page)
    assert len(page.nodes) == 2
    assert page.has_next_page is True
    assert page.end_cursor == "abc"


def test_envia_o_cursor_da_pagina_anterior_na_chamada_seguinte():
    client = FakeGraphQLClient(
        [
            _data([1, 2], has_next=True, cursor="cursor-1"),
            _data([3, 4], has_next=False, cursor="cursor-2"),
        ]
    )

    _paginate(client, limit=10)

    assert client.calls[0]["cursor"] is None
    assert client.calls[1]["cursor"] == "cursor-1"


def test_para_quando_nao_ha_proxima_pagina_mesmo_sem_atingir_o_limite():
    client = FakeGraphQLClient([_data([1, 2], has_next=False, cursor=None)])

    nodes = _paginate(client, limit=100)

    assert len(nodes) == 2
    assert len(client.calls) == 1


def test_para_exatamente_no_limite_sem_pedir_pagina_desnecessaria():
    client = FakeGraphQLClient(
        [
            _data([1, 2, 3], has_next=True, cursor="cursor-1"),
            _data([4, 5, 6], has_next=True, cursor="cursor-2"),
        ]
    )

    nodes = _paginate(client, limit=4)

    assert len(nodes) == 4
    assert len(client.calls) == 2


def test_on_page_e_chamado_uma_vez_por_pagina():
    client = FakeGraphQLClient(
        [
            _data([1], has_next=True, cursor="cursor-1"),
            _data([2], has_next=False, cursor="cursor-2"),
        ]
    )
    seen: list[int] = []

    _paginate(client, limit=10, on_page=lambda index, page: seen.append(index))

    assert seen == [1, 2]


def test_para_quando_o_cursor_nao_avanca():
    """Protege contra laco infinito caso a API repita a mesma pagina."""
    client = FakeGraphQLClient([_data([1], has_next=True, cursor=None)] * 5)

    nodes = _paginate(client, limit=50)

    assert len(nodes) == 1
    assert len(client.calls) == 1


class FailingThenOkClient:
    """Responde 502 nas primeiras `falhas` chamadas, depois devolve uma pagina."""

    def __init__(self, falhas: int, status: int = 502):
        self._restantes = falhas
        self._status = status
        self.calls: list[dict] = []

    def execute(self, query, variables=None):
        self.calls.append(variables or {})
        if self._restantes > 0:
            self._restantes -= 1
            raise HttpError(self._status, "Bad Gateway")
        return _data([1, 2], has_next=False, cursor=None)


def _paginate_degradavel(client, limit, page_size, on_degrade=None):
    return list(
        paginate(
            client,
            "query {}",
            {"pageSize": page_size},
            extract_search_page,
            limit,
            page_size_key="pageSize",
            on_degrade=on_degrade,
        )
    )


def test_reduz_pela_metade_o_tamanho_da_pagina_apos_502():
    """Reproduz o 502 deterministico observado na coleta real com 25 por pagina."""
    client = FailingThenOkClient(falhas=1)
    degradacoes: list[tuple[int, int]] = []

    nodes = _paginate_degradavel(
        client, limit=10, page_size=20, on_degrade=lambda a, n: degradacoes.append((a, n))
    )

    assert degradacoes == [(20, 10)]
    assert client.calls[0]["pageSize"] == 20
    assert client.calls[1]["pageSize"] == 10
    assert len(nodes) == 2


def test_repete_a_mesma_posicao_do_cursor_ao_degradar():
    client = FailingThenOkClient(falhas=1)

    _paginate_degradavel(client, limit=10, page_size=20)

    assert client.calls[0]["cursor"] is None
    assert client.calls[1]["cursor"] is None


def test_degrada_ate_o_minimo_e_entao_propaga_o_erro():
    client = FailingThenOkClient(falhas=99)

    with pytest.raises(HttpError):
        _paginate_degradavel(client, limit=10, page_size=40)

    tamanhos = [c["pageSize"] for c in client.calls]
    assert tamanhos == [40, 20, 10, MIN_PAGE_SIZE]


def test_nao_degrada_erro_permanente():
    """401 nao adianta repetir com menos itens - tem que subir na hora."""
    client = FailingThenOkClient(falhas=1, status=401)

    with pytest.raises(HttpError):
        _paginate_degradavel(client, limit=10, page_size=20)

    assert len(client.calls) == 1


def test_sem_page_size_key_o_erro_sobe_direto():
    client = FailingThenOkClient(falhas=1)

    with pytest.raises(HttpError):
        _paginate(client, limit=10)

    assert len(client.calls) == 1
