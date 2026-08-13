"""Politica de reenvio para falhas transitorias da API do GitHub.

Coletar 1000 repositorios significa dezenas de requisicoes pesadas; 502/504 e limites
secundarios de taxa sao rotina. Isolar a politica aqui mantem o cliente GraphQL legivel
e permite testar o backoff sem rede.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from src.infrastructure.http_client import HttpError

T = TypeVar("T")

#: 0 = falha de transporte (timeout, DNS). 403/429 = limite de taxa. 5xx = instabilidade.
RETRYABLE_STATUS = frozenset({0, 403, 429, 500, 502, 503, 504})


def with_retry(
    operation: Callable[[], T],
    attempts: int = 5,
    base_delay: float = 2.0,
    sleep: Callable[[float], None] | None = None,
) -> T:
    """Executa `operation`, repetindo com backoff exponencial em falhas transitorias.

    `sleep` e injetavel para que os testes nao precisem esperar de verdade.
    Erros nao transitorios (401 token invalido, 404, erro de sintaxe da query) sobem na
    hora: repeti-los so gastaria tempo e rate limit.
    """
    wait = sleep or time.sleep
    last_error: HttpError | None = None

    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except HttpError as exc:
            if exc.status not in RETRYABLE_STATUS:
                raise
            last_error = exc
            if attempt == attempts:
                break
            wait(base_delay * (2 ** (attempt - 1)))

    assert last_error is not None  # so se chega aqui apos um HttpError transitorio
    raise last_error
