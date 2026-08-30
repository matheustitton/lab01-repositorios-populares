"""RQ02 - Sistemas populares recebem muita contribuicao externa?

Metrica: total de pull requests aceitas, ou seja, com estado MERGED.
PRs apenas fechadas (CLOSED sem merge) nao contam como contribuicao aceita.
"""

from __future__ import annotations

from src.domain.models import Repository

RQ = "rq02"
COLUMN = "merged_pull_requests"


def merged_pull_requests(repository: Repository) -> int:
    """Total de pull requests aceitas."""
    return repository.merged_pull_requests
