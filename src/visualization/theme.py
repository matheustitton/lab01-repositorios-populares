"""Estilo comum dos graficos.

Centralizar paleta, tamanho de figura e DPI faz com que as sete figuras do relatorio
tenham a mesma aparencia sem repetir configuracao em cada grafico.

"""

from __future__ import annotations

FIGURE_SIZE = (9, 5)
DPI = 150

PALETTE = {
    "primary": "#2563eb",
    "secondary": "#f59e0b",
    "muted": "#94a3b8",
    "grid": "#e2e8f0",
}


def apply_theme() -> None:
    """Aplica o estilo global do matplotlib. Chamar uma vez, antes de plotar."""
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.figsize": FIGURE_SIZE,
            "figure.dpi": DPI,
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "axes.edgecolor": PALETTE["muted"],
            "axes.labelcolor": "#1e293b",
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": PALETTE["grid"],
            "grid.linewidth": 0.8,
            "font.size": 11,
            "text.color": "#1e293b",
            "xtick.color": "#1e293b",
            "ytick.color": "#1e293b",
            "axes.prop_cycle": plt.cycler(
                color=[PALETTE["primary"], PALETTE["secondary"], PALETTE["muted"]]
            ),
        }
    )
