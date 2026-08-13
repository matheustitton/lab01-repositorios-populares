"""Cliente HTTP minimo sobre `urllib.request` (biblioteca padrao).

O enunciado proibe bibliotecas de terceiros que consultem a API do GitHub; este modulo
existe para que nem mesmo um cliente HTTP externo seja necessario.

Nao sabe nada sobre GraphQL nem sobre o GitHub: recebe URL, cabecalhos e um dicionario,
devolve a resposta decodificada. Trocar o transporte nao afeta nenhuma outra camada.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HttpResponse:
    status: int
    body: dict[str, Any]


class HttpError(RuntimeError):
    """Falha de transporte ou status HTTP != 200."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"HTTP {status}: {message}")
        self.status = status


def post_json(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    timeout: int,
) -> HttpResponse:
    """Envia `payload` como JSON via POST e devolve a resposta desserializada."""
    raise NotImplementedError
