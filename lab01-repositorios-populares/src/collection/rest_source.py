"""Leitura dos mesmos repositorios pela API REST do GitHub.

Fonte independente da GraphQL, usada apenas na validacao cruzada da amostra (Issue #2):
se os dois caminhos concordam, o erro teria que estar nos dois ao mesmo tempo, o que e
bem menos provavel do que um engano na nossa query ou no nosso mapeamento.

Como a REST nao entrega barato "PRs aceitas" nem "total de releases", ela cobre so os
campos diretos. Os agregados continuam dependendo da conferencia manual no GitHub, que
e o que o criterio de aceite da Issue pede.
"""

from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass
from datetime import datetime

from src.collection.mappers import parse_datetime
from src.infrastructure.http_client import get_json
from src.infrastructure.retry import with_retry

REST_BASE_URL = "https://api.github.com/repos"

#: A conexao `releases` da GraphQL para de contar em 1000. Um repositorio que reporta
#: exatamente esse valor tem contagem censurada, nao contagem real.
TETO_TOTALCOUNT = 1000


@dataclass(frozen=True)
class RestSnapshot:
    """Os campos que a REST devolve para um repositorio."""

    name_with_owner: str
    stars: int
    created_at: datetime
    pushed_at: datetime
    primary_language: str | None


def fetch_repository(
    name_with_owner: str,
    token: str | None = None,
    timeout: int = 30,
) -> RestSnapshot:
    """Busca um repositorio na REST.

    O token e opcional: os dados sao publicos. Sem ele o limite e de 60 requisicoes por
    hora, o que ja basta para uma amostra de 5 a 10 repositorios.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "lab01-repositorios-populares",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{REST_BASE_URL}/{name_with_owner}"
    response = with_retry(lambda: get_json(url, headers, timeout))
    body = response.body

    return RestSnapshot(
        name_with_owner=body["full_name"],
        stars=int(body["stargazers_count"]),
        created_at=parse_datetime(body["created_at"]),
        pushed_at=parse_datetime(body["pushed_at"]),
        primary_language=body.get("language"),
    )


def count_releases(name_with_owner: str, token: str | None = None, timeout: int = 30) -> int:
    """Conta as releases pela REST, usada quando a GraphQL bate no teto de 1000.

    Truque de paginacao: pedindo 1 item por pagina, o numero da ultima pagina do
    cabecalho `Link` e o total. Evita baixar milhares de releases so para conta-las.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "lab01-repositorios-populares",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{REST_BASE_URL}/{name_with_owner}/releases?per_page=1"
    request = urllib.request.Request(url, method="GET")
    for key, value in headers.items():
        request.add_header(key, value)

    with urllib.request.urlopen(request, timeout=timeout) as response:
        link = response.headers.get("Link", "")
        corpo_vazio = response.read().strip() in (b"[]", b"")

    ultima = re.search(r"[?&]page=(\d+)>;\s*rel=\"last\"", link)
    if ultima:
        return int(ultima.group(1))
    # Sem cabecalho Link: cabe em uma pagina, ou seja, 0 ou 1 release.
    return 0 if corpo_vazio else 1
