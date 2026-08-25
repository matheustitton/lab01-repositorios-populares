from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.analysis.rq_reports import RQResult
from src.config.settings import ASSETS_DIR
from src.visualization.theme import PALETTE, apply_theme

LOG_SCALE_RQS = {"RQ02", "RQ03"}


def _output_path(result: RQResult, output_dir: Path | None) -> Path:
    directory = output_dir or ASSETS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{result.rq.lower()}.png"

def plot_distribution(result: RQResult, output_dir: Path | None = None) -> Path:
    """Histograma da metrica (RQ01, RQ02, RQ03, RQ04, RQ06).
    """
    if result.table is None or result.table.empty:
        raise ValueError(f"{result.rq}: sem tabela de valores para plotar distribuicao.")

    apply_theme()
    valores = result.table["value"]

    fig, ax = plt.subplots()
    if result.rq in LOG_SCALE_RQS:
        positivos = valores[valores > 0]
        bins = np.logspace(np.log10(max(positivos.min(), 1)), np.log10(positivos.max()), 30)
        ax.set_xscale("log")
        ax.hist(positivos, bins=bins, color=PALETTE["primary"], edgecolor="white")
    else:
        ax.hist(valores, bins=30, color=PALETTE["primary"], edgecolor="white")

    mediana = result.summary.get("median")
    if mediana is not None:
        ax.axvline(
            mediana, color=PALETTE["secondary"], linestyle="--", linewidth=2,
            label=f"mediana = {mediana:g}",
        )
        ax.legend()

    ax.set_title(f"{result.rq} - {result.question}")
    ax.set_xlabel(result.metric)
    ax.set_ylabel("Numero de repositorios")

    path = _output_path(result, output_dir)
    fig.savefig(path)
    plt.close(fig)
    return path
