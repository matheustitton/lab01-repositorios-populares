"""RQ03 - Sistemas populares lancam releases com frequencia?

Metrica: total de releases publicadas.

Atencao ao teto: a conexao `releases` da GraphQL para de contar em 1000, entao um valor
exatamente igual a `TETO_CONTAGEM` e censurado a direita, nao o total real. A mediana
nao e afetada (os censurados estao muito acima dela), mas media e maximo sao.
Ver docs/validacao_amostra.md.
"""

from __future__ import annotations

from src.domain.models import Repository

RQ = "rq03"
COLUMN = "releases"

TETO_CONTAGEM = 1000


def total_releases(repository: Repository) -> int:
    """Total de releases do repositorio."""
    return repository.releases


def is_censored(repository: Repository) -> bool:
    """Indica que o total bateu no teto da API e o valor real e maior."""
    return repository.releases == TETO_CONTAGEM
