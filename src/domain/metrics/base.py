"""Contrato de uma metrica de pesquisa.

Uma metrica e uma funcao pura `Repository -> valor`: sem rede, sem disco, sem estado.
E o que permite validar cada RQ sobre uma amostra de 5 a 10 repositorios montada a mao,
como o Lab01S01 exige, e o que mantem os tres integrantes trabalhando em arquivos
diferentes sem conflito de merge.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.models import Repository

MetricValue = int | float | str | None


@runtime_checkable
class Metric(Protocol):
    """Uma metrica registravel no CSV."""

    #: identificador curto, ex.: "rq01"
    rq: str
    #: nome da coluna no CSV, ex.: "age_years"
    column: str

    def __call__(self, repository: Repository) -> MetricValue:
        """Calcula o valor da metrica para um repositorio."""
        ...
