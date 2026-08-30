"""Coleta dos itens do GitHub Projects (Parte 2, item 6).

Mesma infraestrutura da Parte 1 - so mudam a query e o extrator de pagina. E a prova
pratica de que a camada de infraestrutura ficou desacoplada do dominio.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any

from src.collection.mappers import to_project_item
from src.collection.paginator import Page, SupportsExecute, paginate
from src.domain.models import ProjectItem
from src.infrastructure.query_loader import load_query

QUERY_NAME = "project_items"

#: Teto generoso: o board de uma disciplina nao passa disso, e o limite evita laco
#: infinito caso a API devolva paginacao inconsistente.
MAX_ITEMS = 500


class ProjectNotFoundError(RuntimeError):
    """Project inexistente, ou invisivel para o token usado.

    O GitHub nao distingue os dois casos: um Project privado ao qual o token nao tem
    acesso simplesmente vem nulo, igual a um que nao existe.
    """


def extract_project_page(data: dict[str, Any]) -> Page:
    """Localiza `nodes`/`pageInfo` dentro de `data.user.projectV2.items`."""
    user = data.get("user")
    if not user:
        raise ProjectNotFoundError("usuario nao encontrado")

    project = user.get("projectV2")
    if not project:
        raise ProjectNotFoundError(
            "Project nao encontrado ou sem permissao de leitura. "
            "Confira o numero e se o token tem escopo read:project."
        )

    items = project.get("items") or {}
    page_info = items.get("pageInfo") or {}
    return Page(
        nodes=items.get("nodes") or [],
        has_next_page=bool(page_info.get("hasNextPage")),
        end_cursor=page_info.get("endCursor"),
    )


def collect_project_items(
    client: SupportsExecute,
    owner: str,
    number: int,
    sprint: str,
    captured_at: datetime | None = None,
) -> Iterator[ProjectItem]:
    """Coleta todos os cartoes do Project, com o Status vigente no momento da captura."""
    momento = captured_at or datetime.now(timezone.utc)
    query = load_query(QUERY_NAME)
    variables = {"owner": owner, "number": number}

    for node in paginate(client, query, variables, extract_project_page, MAX_ITEMS):
        yield to_project_item(node, sprint, momento)
