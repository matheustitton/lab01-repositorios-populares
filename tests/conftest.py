"""Fixtures compartilhadas.

Nenhum teste deste projeto acessa a rede: as respostas da API vem de `tests/fixtures/` e
o cliente GraphQL e substituido por um fake. Isso torna a suite rapida, deterministica e
independente de rate limit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any]:
    """Le um JSON de `tests/fixtures/`."""
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


@pytest.fixture
def search_response() -> dict[str, Any]:
    """Resposta de `search` com a amostra de repositorios usada nas validacoes do S01."""
    return load_fixture("search_response_sample.json")


@pytest.fixture
def project_items_response() -> dict[str, Any]:
    """Resposta de `projectV2.items` com alguns cartoes de exemplo."""
    return load_fixture("project_items_sample.json")


class FakeGraphQLClient:
    """Devolve respostas pre-programadas, em ordem, sem tocar na rede.

    Usado para testar paginacao e coletores: cada chamada a `execute` consome a proxima
    resposta da lista e registra as variaveis recebidas em `self.calls`.
    """

    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self._responses = list(responses)
        self.calls: list[dict[str, Any]] = []

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        self.calls.append(variables or {})
        return self._responses.pop(0)
