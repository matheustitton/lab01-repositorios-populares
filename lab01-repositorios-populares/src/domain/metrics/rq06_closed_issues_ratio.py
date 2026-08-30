"""RQ06 - Sistemas populares possuem alto percentual de issues fechadas?

Metrica: razao entre issues fechadas e total de issues.
"""

from __future__ import annotations

from src.domain.models import Repository

RQ = "rq06"
COLUMN = "closed_issues_ratio"


def closed_issues_ratio(repository: Repository) -> float:
    """Razao fechadas/total, no intervalo [0, 1].

    Repositorios sem nenhuma issue devolvem 0.0 e devem ser tratados a parte na analise:
    "nenhuma issue" nao e o mesmo que "nenhuma issue resolvida", e incluir esses casos na
    mediana puxa o resultado para baixo indevidamente. Use `has_issues` para separa-los.
    """
    if repository.total_issues <= 0:
        return 0.0
    return round(repository.closed_issues / repository.total_issues, 4)


def has_issues(repository: Repository) -> bool:
    """Indica que a razao e interpretavel - ou seja, que existe denominador."""
    return repository.total_issues > 0
