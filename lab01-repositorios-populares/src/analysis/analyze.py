"""Analise e visualizacao das sete RQs

    python -m src.cli.analyze
    python -m src.cli.analyze --no-charts

Le o CSV, executa as RQs e grava as figuras em `docs/assets/`. Nao acessa a rede.

"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.analysis.loader import load_repositories
from src.analysis.rq_reports import all_results
from src.config.settings import ASSETS_DIR, DATA_DIR
from src.visualization.charts import render_all

#: Dataset mais recente (1000 repositorios, Lab01S02). Passe --input para outro CSV.
DEFAULT_INPUT = DATA_DIR / "repos_lab01s02.csv"


def build_parser() -> argparse.ArgumentParser:
    """--input, --output-dir, --no-charts."""
    parser = argparse.ArgumentParser(
        prog="analyze",
        description="Analise e visualizacao das 7 RQs sobre o CSV coletado",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=ASSETS_DIR)
    parser.add_argument("--no-charts", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Roda a analise e devolve o codigo de saida do processo."""
    args = build_parser().parse_args(argv)

    frame = load_repositories(args.input)
    resultados = all_results(frame)

    for resultado in resultados:
        print(f"{resultado.rq}: {resultado.summary}")

    if not args.no_charts:
        for caminho in render_all(resultados, output_dir=args.output_dir):
            print(f"grafico salvo em {caminho}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
