"""Resultados por questao de pesquisa (Lab01S03).

Cada funcao responde uma RQ e devolve dados prontos para o relatorio e para os graficos -
nenhuma formatacao de texto e nenhum `print` aqui, para que os mesmos numeros alimentem
tanto `docs/relatorio.md` quanto `src/visualization/charts.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class RQResult:
    """Resultado de uma questao de pesquisa."""

    rq: str
    question: str
    metric: str
    summary: dict[str, Any]
    table: pd.DataFrame | None = None


def rq01_age(frame: pd.DataFrame) -> RQResult:
    """Sistemas populares sao maduros/antigos? (mediana de idade em anos)"""
    raise NotImplementedError


def rq02_merged_pull_requests(frame: pd.DataFrame) -> RQResult:
    """Recebem muita contribuicao externa? (mediana de PRs aceitas)"""
    raise NotImplementedError


def rq03_releases(frame: pd.DataFrame) -> RQResult:
    """Lancam releases com frequencia? (mediana de releases)"""
    raise NotImplementedError


def rq04_days_since_update(frame: pd.DataFrame) -> RQResult:
    """Sao atualizados com frequencia? (mediana de dias desde o ultimo push)"""
    raise NotImplementedError


def rq05_primary_language(frame: pd.DataFrame) -> RQResult:
    """Sao escritos nas linguagens mais populares? (contagem por linguagem)"""
    raise NotImplementedError


def rq06_closed_issues_ratio(frame: pd.DataFrame) -> RQResult:
    """Possuem alto percentual de issues fechadas? (mediana da razao)"""
    raise NotImplementedError


def rq07_by_language(frame: pd.DataFrame) -> RQResult:
    """RQ02, RQ03 e RQ04 desdobradas por linguagem primaria.

    A tabela traz uma linha por linguagem e as medianas das tres metricas, alem da flag
    de popularidade vinda de `popular_languages`. Linguagens com poucos repositorios
    devem ser agrupadas em "Outras" para nao gerar mediana sobre 1 ou 2 observacoes.
    """
    raise NotImplementedError


def all_results(frame: pd.DataFrame) -> list[RQResult]:
    """Executa as sete RQs, na ordem do enunciado."""
    raise NotImplementedError
