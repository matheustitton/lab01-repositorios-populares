from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.analysis import statistics


@dataclass(frozen=True)
class RQResult:
    rq: str
    question: str
    metric: str
    summary: dict[str, Any]
    table: pd.DataFrame | None = None


def _value_table(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """Coluna unica com os valores validos, para os graficos de distribuicao lerem os
    dados brutos sem recalcular nada em `charts.py`."""
    return frame[[column]].rename(columns={column: "value"}).dropna()


def rq01_age(frame: pd.DataFrame) -> RQResult:
    """Sistemas populares sao maduros/antigos? (mediana de idade em anos)"""
    return RQResult(
        rq="RQ01",
        question="Sistemas populares sao maduros/antigos?",
        metric="Idade do repositorio, em anos (age_years)",
        summary=statistics.summarize(frame["age_years"]),
        table=_value_table(frame, "age_years"),
    )


def rq02_merged_pull_requests(frame: pd.DataFrame) -> RQResult:
    """Recebem muita contribuicao externa? (mediana de PRs aceitas)"""
    return RQResult(
        rq="RQ02",
        question="Sistemas populares recebem muita contribuicao externa?",
        metric="Total de pull requests aceitas (merged_pull_requests)",
        summary=statistics.summarize(frame["merged_pull_requests"]),
        table=_value_table(frame, "merged_pull_requests"),
    )
