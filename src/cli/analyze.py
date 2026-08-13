"""Analise e visualizacao das sete RQs (Lab01S03).

    python -m src.cli.analyze
    python -m src.cli.analyze --no-charts

Le o CSV, executa as RQs e grava as figuras em `docs/assets/`. Nao acessa a rede.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """--input, --output-dir, --no-charts."""
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Roda a analise e devolve o codigo de saida do processo."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
