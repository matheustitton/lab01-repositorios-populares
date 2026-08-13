"""Politica de reenvio para falhas transitorias da API do GitHub.

Coletar 1000 repositorios significa dezenas de requisicoes pesadas; 502/504 e limites
secundarios de taxa sao rotina. Isolar a politica aqui mantem o cliente GraphQL legivel
e permite testar o backoff sem rede.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

RETRYABLE_STATUS = frozenset({403, 429, 500, 502, 503, 504})


def with_retry(
    operation: Callable[[], T],
    attempts: int = 5,
    base_delay: float = 2.0,
    sleep: Callable[[float], None] | None = None,
) -> T:
    """Executa `operation`, repetindo com backoff exponencial em falhas transitorias.

    `sleep` e injetavel para que os testes nao precisem esperar de verdade.
    Erros nao transitorios (401, 404, erro de sintaxe da query) sobem na hora.
    """
    raise NotImplementedError
