"""Resumos estatisticos reutilizaveis.

Funcoes genericas sobre DataFrame, sem nocao de RQ. A leitura de cada numero e feita em
`rq_reports.py`; aqui so se calcula.

O enunciado pede valores medianos: as distribuicoes de estrelas, PRs e releases sao
fortemente assimetricas, e a media seria dominada por poucos outliers gigantes.
"""

from __future__ import annotations

import pandas as pd


def summarize(series: pd.Series) -> dict[str, float]:
    """Contagem, mediana, media, desvio, minimo, quartis e maximo de uma serie."""
    raise NotImplementedError


def count_by_category(series: pd.Series, top: int | None = None) -> pd.Series:
    """Contagem por categoria, em ordem decrescente (RQ05)."""
    raise NotImplementedError


def median_by_group(frame: pd.DataFrame, group_column: str, value_column: str) -> pd.Series:
    """Mediana de `value_column` por grupo - base da RQ07."""
    raise NotImplementedError
