"""RQ05 - Sistemas populares sao escritos nas linguagens mais populares?

Metrica: linguagem primaria de cada repositorio.

Aqui apenas a linguagem bruta e extraida. A comparacao com a lista de "linguagens mais
populares" acontece em `src/analysis/popular_languages.py`, cuja fonte esta declarada em
`docs/fontes.md` e vale para todo o laboratorio.
"""

from __future__ import annotations

from src.domain.models import Repository

RQ = "rq05"
COLUMN = "primary_language"

UNDEFINED = "Undefined"


def primary_language(repository: Repository) -> str:
    """Linguagem primaria; `UNDEFINED` quando a API nao informa nenhuma.

    Repositorios sem linguagem primaria existem e sao comuns entre os mais estrelados
    (listas de links, colecoes de material de estudo). Sao categoria propria, nao dado
    faltante - por isso viram um rotulo explicito em vez de vazio.
    """
    return repository.primary_language or UNDEFINED
