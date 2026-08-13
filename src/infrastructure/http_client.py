"""Cliente HTTP minimo sobre `urllib.request` (biblioteca padrao).

O enunciado proibe bibliotecas de terceiros que consultem a API do GitHub; este modulo
existe para que nem mesmo um cliente HTTP externo seja necessario.

Nao sabe nada sobre GraphQL nem sobre o GitHub: recebe URL, cabecalhos e um dicionario,
devolve a resposta decodificada. Trocar o transporte nao afeta nenhuma outra camada.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
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


def get_json(url: str, headers: dict[str, str], timeout: int) -> HttpResponse:
    """Faz um GET e devolve a resposta desserializada.

    Existe para a validacao cruzada da amostra (Issue #2), que confere os dados da
    GraphQL contra a API REST - uma fonte independente para os mesmos campos.
    """
    request = urllib.request.Request(url, method="GET")
    for key, value in headers.items():
        request.add_header(key, value)
    return _send(request, timeout)


def post_json(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    timeout: int,
) -> HttpResponse:
    """Envia `payload` como JSON via POST e devolve a resposta desserializada."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")
    for key, value in {"Content-Type": "application/json", **headers}.items():
        request.add_header(key, value)
    return _send(request, timeout)


def _send(request: urllib.request.Request, timeout: int) -> HttpResponse:
    """Executa a requisicao e traduz as falhas do urllib em `HttpError`."""
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return HttpResponse(status=response.status, body=json.loads(raw))
    except urllib.error.HTTPError as exc:
        # O corpo do erro costuma trazer a explicacao real (rate limit, escopo de token
        # faltando); sem le-lo, o diagnostico vira adivinhacao.
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HttpError(exc.code, detail) from exc
    except urllib.error.URLError as exc:
        # Falha de rede/DNS/timeout: status 0 sinaliza "nao chegou a haver resposta".
        raise HttpError(0, str(exc.reason)) from exc
    except json.JSONDecodeError as exc:
        raise HttpError(0, f"resposta nao e JSON valido: {exc}") from exc
