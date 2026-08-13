"""Ponto de entrada da coleta (Lab01S01 com 100, Lab01S02 com 1000).

    python -m src.cli.collect_repositories --limit 100
    python -m src.cli.collect_repositories --limit 1000 --page-size 25

Camada fina: le argumentos, monta as dependencias, liga coleta -> persistencia e imprime
progresso. Nenhuma regra de negocio mora aqui.

A saida e o JSON bruto (`data/raw_repos_lab01s01.json`). O calculo das metricas e a
exportacao em CSV sao responsabilidade do processamento (Issue #3).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.collection.paginator import Page
from src.collection.repository_collector import SEARCH_RESULT_CAP, collect_repository_nodes
from src.config.settings import RAW_DIR, RAW_REPOS_JSON, MissingTokenError, load_settings
from src.infrastructure.graphql_client import GraphQLClient, GraphQLError
from src.infrastructure.http_client import HttpError
from src.storage.json_store import save_page, save_repository_nodes


def build_parser() -> argparse.ArgumentParser:
    """--limit, --page-size, --output, --save-raw."""
    parser = argparse.ArgumentParser(
        prog="collect_repositories",
        description="Coleta os repositorios mais estrelados do GitHub via GraphQL.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="quantidade de repositorios a coletar (default: 100)",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=None,
        help="repositorios por pagina (default: PAGE_SIZE do .env, ou 25)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=RAW_REPOS_JSON,
        help=f"arquivo JSON de saida (default: {RAW_REPOS_JSON.name})",
    )
    parser.add_argument(
        "--save-raw",
        action="store_true",
        help="salva tambem cada pagina crua em data/raw/, para reprocessamento offline",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Executa a coleta e devolve o codigo de saida do processo."""
    args = build_parser().parse_args(argv)

    if args.limit < 1:
        print("erro: --limit deve ser >= 1", file=sys.stderr)
        return 2
    if args.limit > SEARCH_RESULT_CAP:
        print(
            f"erro: a busca do GitHub devolve no maximo {SEARCH_RESULT_CAP} resultados por "
            "consulta; para ir alem, fatie por faixa de estrelas.",
            file=sys.stderr,
        )
        return 2

    try:
        settings = load_settings()
    except MissingTokenError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    page_size = args.page_size or settings.page_size
    client = GraphQLClient(settings.graphql_url, settings.github_token, settings.request_timeout)

    collected = 0

    def report(index: int, page: Page) -> None:
        nonlocal collected
        # O acumulado e limitado a `--limit`: a ultima pagina costuma trazer mais nos do
        # que os que faltam, e exibir "111 de 100" so confunde.
        collected = min(collected + len(page.nodes), args.limit)
        print(
            f"  pagina {index:>3}: {len(page.nodes):>3} repos (acumulado: {collected})",
            flush=True,
        )
        if args.save_raw:
            # O pageInfo vai junto para permitir retomar a coleta do cursor exato.
            save_page(
                RAW_DIR,
                index,
                {
                    "nodes": page.nodes,
                    "pageInfo": {
                        "hasNextPage": page.has_next_page,
                        "endCursor": page.end_cursor,
                    },
                },
            )

    def report_degrade(anterior: int, novo: int) -> None:
        # Em stdout junto com o resto do progresso: em stderr, o buffer separado fazia o
        # aviso aparecer fora de ordem em relacao as paginas.
        print(
            f"  aviso: a API falhou com {anterior} itens por pagina (query cara demais); "
            f"repetindo a mesma pagina com {novo}.",
            flush=True,
        )

    print(f"Coletando {args.limit} repositorios ({page_size} por pagina)...", flush=True)
    try:
        nodes = collect_repository_nodes(
            client, args.limit, page_size, on_page=report, on_degrade=report_degrade
        )
        total = save_repository_nodes(args.output, nodes)
    except GraphQLError as exc:
        print(f"erro na query GraphQL: {exc}", file=sys.stderr)
        return 1
    except HttpError as exc:
        print(f"erro de rede: {exc}", file=sys.stderr)
        return 1

    print(f"\n{total} repositorios gravados em {args.output}")
    if total < args.limit:
        print(
            f"aviso: esperados {args.limit}, obtidos {total} - a busca esgotou os resultados.",
            file=sys.stderr,
        )

    try:
        limit_info = client.rate_limit()
        print(f"rate limit restante: {limit_info['remaining']}/{limit_info['limit']}")
    except (GraphQLError, HttpError):
        pass  # informativo apenas; nao invalida a coleta

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
