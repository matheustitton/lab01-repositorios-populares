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
    raise NotImplementedError
