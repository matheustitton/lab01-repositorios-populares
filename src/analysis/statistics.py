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
    valores = pd.to_numeric(series, errors="coerce").dropna()

    if valores.empty:
        vazio = float("nan")
        return {
            "count": 0,
            "median": vazio,
            "mean": vazio,
            "std": vazio,
            "min": vazio,
            "q1": vazio,
            "q3": vazio,
            "max": vazio,
        }

    return {
        "count": int(valores.count()),
        "median": round(float(valores.median()), 4),
        "mean": round(float(valores.mean()), 4),
        # desvio padrao amostral (ddof=1) exige ao menos 2 observacoes.
        "std": round(float(valores.std(ddof=1)), 4) if valores.count() > 1 else 0.0,
        "min": round(float(valores.min()), 4),
        "q1": round(float(valores.quantile(0.25)), 4),
        "q3": round(float(valores.quantile(0.75)), 4),
        "max": round(float(valores.max()), 4),
    }


def count_by_category(series: pd.Series, top: int | None = None) -> pd.Series:
    """Contagem por categoria, em ordem decrescente (RQ05)."""
    contagem = series.fillna("Undefined").value_counts(sort=True)
    return contagem.head(top) if top is not None else contagem


def median_by_group(frame: pd.DataFrame, group_column: str, value_column: str) -> pd.Series:
    """Mediana de `value_column` por grupo - base da RQ07."""
    dados = frame[[group_column, value_column]].copy()
    dados[value_column] = pd.to_numeric(dados[value_column], errors="coerce")

    medianas = dados.groupby(group_column)[value_column].median()
    return medianas.sort_values(ascending=False)
