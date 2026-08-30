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
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _total_count(node: dict[str, Any], key: str) -> int:
    """Le `node[key].totalCount`, devolvendo 0 quando a conexao vem nula."""
    connection = node.get(key) or {}
    return int(connection.get("totalCount") or 0)


def to_repository(node: dict[str, Any]) -> Repository:
    """Mapeia um no de `search.nodes` para `Repository`."""
    language = node.get("primaryLanguage") or {}

    return Repository(
        name_with_owner=node["nameWithOwner"],
        url=node["url"],
        stars=int(node.get("stargazerCount") or 0),
        created_at=parse_datetime(node["createdAt"]),
        pushed_at=parse_datetime(node["pushedAt"] or node["createdAt"]),
        primary_language=language.get("name"),
        merged_pull_requests=_total_count(node, "mergedPullRequests"),
        releases=_total_count(node, "releases"),
        closed_issues=_total_count(node, "closedIssues"),
        total_issues=_total_count(node, "totalIssues"),
    )


def _names(node: dict[str, Any], key: str) -> tuple[str, ...]:
    """Extrai `node[key].nodes[].login|name` como tupla, tolerando nulos."""
    connection = node.get(key) or {}
    entries = connection.get("nodes") or []
    return tuple(e.get("login") or e.get("name") for e in entries if e)


def to_project_item(node: dict[str, Any], sprint: str, captured_at: datetime) -> ProjectItem:
    """Mapeia um no de `projectV2.items.nodes` para `ProjectItem`.

    Itens sem Issue associada (draft issues) sao mapeados com `issue_number = None`,
    para que a auditoria do board consiga apontar que existem cartoes fora da regra do
    enunciado (que exige Issue de verdade, rastreavel pela API).
    """
    content = node.get("content") or {}
    status_field = node.get("fieldValueByName") or {}
    closed_at = content.get("closedAt")

    return ProjectItem(
        issue_number=content.get("number"),
        title=content.get("title") or "(sem titulo)",
        status=status_field.get("name"),
        state=content.get("state"),
        assignees=_names(content, "assignees"),
        labels=_names(content, "labels"),
        url=content.get("url"),
        created_at=parse_datetime(content["createdAt"]) if content.get("createdAt") else None,
        closed_at=parse_datetime(closed_at) if closed_at else None,
        captured_at=captured_at,
        sprint=sprint,
    )
