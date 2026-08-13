"""Carrega queries `.graphql` do disco.

As queries ficam em arquivos proprios, e nao em strings dentro do Python, para que
possam ser coladas no GraphQL Explorer do GitHub e validadas antes de rodar o script.
"""

from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=None)
def load_query(name: str) -> str:
    """Devolve o conteudo de `src/queries/<name>.graphql`.

    Levanta `QueryNotFoundError` se o arquivo nao existir.
    """
    raise NotImplementedError


class QueryNotFoundError(FileNotFoundError):
    """Arquivo `.graphql` inexistente."""
