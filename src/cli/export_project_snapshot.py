"""Snapshot de fechamento de sprint do GitHub Projects (Parte 2, item 6).

    python -m src.cli.export_project_snapshot --sprint lab01s01

Gera `data/snapshots/project_snapshot_<sprint>.csv` com os cartoes e o Status vigente.
Rodar ao FIM de cada sprint: a API do Projects nao guarda historico de mudanca de coluna,
entao a serie acumulada de snapshots e a unica base para os Labs 04 e 05. Um snapshot
perdido nao pode ser reconstruido depois.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """--sprint, --owner, --number, --output."""
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Exporta o snapshot e devolve o codigo de saida do processo."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
