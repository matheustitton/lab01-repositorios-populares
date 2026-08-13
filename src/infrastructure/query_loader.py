"""Carrega queries `.graphql` do disco.

As queries ficam em arquivos proprios, e nao em strings dentro do Python, para que
possam ser coladas no GraphQL Explorer do GitHub e validadas antes de rodar o script.
"""

from __future__ import annotations

from functools import lru_cache

from src.config.settings import QUERIES_DIR


class QueryNotFoundError(FileNotFoundError):
    """Arquivo `.graphql` inexistente."""


@lru_cache(maxsize=None)
def load_query(name: str) -> str:
    """Devolve o conteudo de `src/queries/<name>.graphql`.

    O cache evita reler o arquivo a cada pagina da coleta.
    """
    path = QUERIES_DIR / f"{name}.graphql"
    if not path.exists():
        raise QueryNotFoundError(f"query nao encontrada: {path}")
    return path.read_text(encoding="utf-8")
