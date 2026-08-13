"""Ponto de entrada da coleta (Lab01S01 com 100, Lab01S02 com 1000).

    python -m src.cli.collect_repositories --limit 100
    python -m src.cli.collect_repositories --limit 1000 --page-size 25

Camada fina: le argumentos, monta as dependencias, liga coleta -> serializacao -> CSV e
imprime progresso. Nenhuma regra de negocio mora aqui.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """--limit, --page-size, --output, --save-raw."""
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Executa a coleta e devolve o codigo de saida do processo."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
