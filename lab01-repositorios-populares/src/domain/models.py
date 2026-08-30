"""Modelos de dominio.

Estruturas imutaveis que representam o que foi coletado, ja normalizado e sem tracos do
formato JSON da API. Nao possuem dependencia de rede, de disco nem de pandas: sao o
contrato entre a coleta (que as produz) e as metricas/serializacao (que as consomem).

Guardam apenas dados **brutos**; toda grandeza derivada (idade, dias sem atualizacao,
razao de issues) e responsabilidade de `src/domain/metrics`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Repository:
    """Um repositorio popular, com os campos brutos das RQ01 a RQ06."""

    name_with_owner: str
    url: str
    stars: int
    created_at: datetime
    pushed_at: datetime
    primary_language: str | None
    merged_pull_requests: int
    releases: int
    closed_issues: int
    total_issues: int


@dataclass(frozen=True)
class ProjectItem:
    """Um cartao do GitHub Projects no momento do snapshot."""

    issue_number: int | None
    title: str
    status: str | None
    state: str | None
    assignees: tuple[str, ...]
    labels: tuple[str, ...]
    url: str | None
    created_at: datetime | None
    closed_at: datetime | None
    captured_at: datetime
    sprint: str
