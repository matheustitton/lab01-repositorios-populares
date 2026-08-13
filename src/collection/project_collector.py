"""Coleta dos itens do GitHub Projects (Parte 2, item 6).

Mesma infraestrutura da Parte 1 - so mudam a query e o extrator de pagina. E a prova
pratica de que a camada de infraestrutura ficou desacoplada do dominio.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from typing import Any

from src.collection.paginator import Page
from src.domain.models import ProjectItem
from src.infrastructure.graphql_client import GraphQLClient


def extract_project_page(data: dict[str, Any]) -> Page:
    """Localiza `nodes`/`pageInfo` dentro de `data.user.projectV2.items`."""
    raise NotImplementedError


def collect_project_items(
    client: GraphQLClient,
    owner: str,
    number: int,
    sprint: str,
    captured_at: datetime | None = None,
) -> Iterator[ProjectItem]:
    """Coleta todos os cartoes do Project, com o Status vigente no momento da captura."""
    raise NotImplementedError
