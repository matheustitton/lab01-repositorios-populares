"""Traducao de JSON da API para modelos de dominio.

Fronteira anti-corrupcao: e o unico lugar do projeto que conhece os nomes de campo da
API do GitHub. Se a query mudar, muda so este arquivo.

Tolerante a `null`: campos opcionais (`primaryLanguage`, `assignees`, itens de Project
que nao sao Issue) aparecem como `None` na resposta real e nao podem derrubar a coleta.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.domain.models import ProjectItem, Repository


def parse_datetime(value: str) -> datetime:
    """Converte timestamp ISO-8601 da API (sufixo `Z`) em `datetime` com timezone."""
    raise NotImplementedError


def to_repository(node: dict[str, Any]) -> Repository:
    """Mapeia um no de `search.nodes` para `Repository`."""
    raise NotImplementedError


def to_project_item(node: dict[str, Any], sprint: str, captured_at: datetime) -> ProjectItem:
    """Mapeia um no de `projectV2.items.nodes` para `ProjectItem`.

    Itens sem Issue associada (draft issues) sao mapeados com `issue_number = None`,
    para que a auditoria do board consiga apontar que existem cartoes fora da regra do
    enunciado (que exige Issue de verdade, rastreavel pela API).
    """
    raise NotImplementedError
