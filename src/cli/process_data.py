"""Processamento dos dados coletados (Lab01S01, Issue #3).

    python -m src.cli.process_data

Le `data/raw_repos_lab01s01.json`, calcula as metricas de RQ01 a RQ06 e exporta:

- `data/repos_lab01s01.csv`  - uma linha por repositorio
- `data/resumo_lab01s01.csv` - medianas das RQ01 a RQ04 e RQ06, e contagem por
                               linguagem da RQ05

Nao acessa a rede: opera apenas sobre o JSON ja coletado, o que permite reprocessar
quantas vezes for preciso sem gastar rate limit.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.collection.mappers import to_repository
from src.config.settings import RAW_REPOS_JSON, REPOS_CSV, RESUMO_CSV
from src.domain.summary import SUMMARY_COLUMNS, build_summary
from src.storage.csv_writer import write_csv
from src.storage.serializers import repository_header, repository_rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="process_data",
        description="Calcula as metricas das RQ01 a RQ06 e exporta os CSVs do Lab01S01.",
    )
    parser.add_argument("--input", type=Path, default=RAW_REPOS_JSON)
    parser.add_argument("--repos-csv", type=Path, default=REPOS_CSV)
    parser.add_argument("--resumo-csv", type=Path, default=RESUMO_CSV)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.input.exists():
        print(
            f"erro: {args.input} nao encontrado. Rode a coleta antes:\n"
            "  python -m src.cli.collect_repositories --limit 100",
            file=sys.stderr,
        )
        return 2

    nodes = json.loads(args.input.read_text(encoding="utf-8"))
    if not nodes:
        print(f"erro: {args.input} esta vazio.", file=sys.stderr)
        return 2

    repositories = [to_repository(n) for n in nodes]

    # Um unico instante de referencia para todas as metricas temporais: sem isso, cada
    # linha seria medida contra um "agora" diferente e o reprocessamento nao bateria.
    reference = datetime.now(timezone.utc)
    print(f"Processando {len(repositories)} repositorios (referencia: {reference:%Y-%m-%d %H:%M} UTC)")

    linhas = repository_rows(repositories, reference)
    total = write_csv(args.repos_csv, repository_header(), linhas)
    print(f"  {args.repos_csv.name}: {total} linhas, {len(repository_header())} colunas")

    resumo = build_summary(repositories, reference)
    write_csv(args.resumo_csv, SUMMARY_COLUMNS, [linha.as_row() for linha in resumo])
    print(f"  {args.resumo_csv.name}: {len(resumo)} linhas")

    print("\nResumo por questao de pesquisa:")
    por_linguagem = [linha for linha in resumo if linha.metrica == "contagem_por_linguagem"]
    for linha in resumo:
        # As linhas por linguagem sao dezenas; vao resumidas logo abaixo.
        if linha.metrica != "contagem_por_linguagem":
            print(f"  {linha.rq} {linha.metrica:<52} {linha.valor:>10}")

    print("\n  rq05 linguagens mais frequentes:")
    for linha in por_linguagem[:5]:
        print(f"    {linha.categoria:<20} {linha.valor:>4}")

    censuradas = next(
        (linha.valor for linha in resumo if linha.metrica == "contagem_censurada_no_teto"), 0
    )
    if censuradas:
        print(
            f"\naviso: {censuradas} repositorio(s) com releases no teto de contagem da API."
            "\n       A mediana da RQ03 nao e afetada, mas media e maximo sao."
            "\n       Ver docs/validacao_amostra.md.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
