"""Geracao dos graficos das RQs (Lab01S03).

Recebe `RQResult` ja calculado - nao refaz estatistica. Cada funcao salva um PNG em
`docs/assets/` e devolve o caminho, para ser referenciado no relatorio.
"""

from __future__ import annotations

from pathlib import Path

from src.analysis.rq_reports import RQResult


def plot_distribution(result: RQResult, output_dir: Path | None = None) -> Path:
    """Histograma da metrica (RQ01, RQ02, RQ03, RQ04, RQ06).

    Metricas de cauda longa (PRs, releases) devem usar escala logaritmica no eixo x,
    caso contrario o histograma vira uma unica barra colada no zero.
    """
    raise NotImplementedError


def plot_language_counts(result: RQResult, top: int = 15, output_dir: Path | None = None) -> Path:
    """Barras horizontais com as linguagens mais frequentes (RQ05)."""
    raise NotImplementedError


def plot_metrics_by_language(result: RQResult, output_dir: Path | None = None) -> Path:
    """Barras agrupadas: PRs aceitas, releases e atualidade por linguagem (RQ07)."""
    raise NotImplementedError


def render_all(results: list[RQResult], output_dir: Path | None = None) -> list[Path]:
    """Gera todas as figuras do relatorio e devolve os caminhos criados."""
    raise NotImplementedError
