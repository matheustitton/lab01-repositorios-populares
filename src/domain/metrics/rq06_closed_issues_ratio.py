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
    mediana puxa o resultado para baixo indevidamente.
    """
    raise NotImplementedError
