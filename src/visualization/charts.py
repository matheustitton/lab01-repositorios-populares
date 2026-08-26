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

def plot_language_counts(result: RQResult, top: int = 15, output_dir: Path | None = None) -> Path:
    """Barras horizontais com as linguagens mais frequentes (RQ05)."""
    apply_theme()
    tabela = result.table.head(top).iloc[::-1]

    fig, ax = plt.subplots()
    ax.barh(tabela["primary_language"], tabela["count"], color=PALETTE["primary"])
    ax.set_xlabel("Numero de repositorios")
    ax.set_title(f"{result.rq} - {result.question}")

    path = _output_path(result, output_dir)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path

def plot_metrics_by_language(result: RQResult, output_dir: Path | None = None) -> Path:
    """Barras agrupadas: PRs aceitas, releases e atualidade por linguagem (RQ07)."""
    apply_theme()
    tabela = result.table[result.table["primary_language"] != "Outras"].sort_values(
        "n", ascending=False
    )

    metricas = ["median_merged_pull_requests", "median_releases", "median_days_since_update"]
    rotulos = ["PRs aceitas (mediana)", "Releases (mediana)", "Dias desde atualizacao (mediana)"]
    cores = [PALETTE["primary"], PALETTE["secondary"], PALETTE["muted"]]

    x = np.arange(len(tabela))
    largura = 0.25

    fig, ax = plt.subplots()
    for indice, (metrica, rotulo, cor) in enumerate(zip(metricas, rotulos, cores)):
        ax.bar(x + indice * largura, tabela[metrica], width=largura, label=rotulo, color=cor)

    ax.set_xticks(x + largura)
    ax.set_xticklabels(tabela["primary_language"], rotation=30, ha="right")
    ax.set_yscale("log")
    ax.set_ylabel("Mediana (escala log)")
    ax.set_title(f"{result.rq} - {result.question}")
    ax.legend()

    path = _output_path(result, output_dir)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path

def render_all(results: list[RQResult], output_dir: Path | None = None) -> list[Path]:
    """Gera todas as figuras do relatorio e devolve os caminhos criados."""
    caminhos = []
    for result in results:
        if result.rq == "RQ05":
            caminhos.append(plot_language_counts(result, output_dir=output_dir))
        elif result.rq == "RQ07":
            caminhos.append(plot_metrics_by_language(result, output_dir=output_dir))
        else:
            caminhos.append(plot_distribution(result, output_dir=output_dir))
    return caminhos
