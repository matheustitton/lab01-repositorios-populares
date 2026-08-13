"""Snapshot de fechamento de sprint do GitHub Projects (Parte 2, item 6).

    python -m src.cli.export_project_snapshot --sprint lab01s01

Gera/atualiza `data/snapshots_board.csv` com os cartoes e o Status vigente. Cada linha
traz sprint, data da captura, numero da Issue, responsavel e status, alem de titulo,
labels e datas - campos extras que os Labs 04 e 05 vao querer.

Rodar ao FIM de cada sprint: a API do Projects nao guarda historico de mudanca de coluna,
entao a serie acumulada de snapshots e a unica base para os Labs 04 e 05. Um snapshot
perdido nao pode ser reconstruido depois.

Reexecutar na mesma sprint substitui as linhas daquela sprint, nunca duplica.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from src.collection.project_collector import ProjectNotFoundError, collect_project_items
from src.config.settings import DATA_DIR, MissingTokenError, load_settings
from src.infrastructure.graphql_client import GraphQLClient, GraphQLError
from src.infrastructure.http_client import HttpError
from src.storage.serializers import PROJECT_COLUMNS, project_item_row
from src.storage.snapshot_store import merge_snapshot

DEFAULT_OUTPUT = DATA_DIR / "snapshots_board.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="export_project_snapshot",
        description="Exporta os itens do GitHub Projects para o CSV acumulado de snapshots.",
    )
    parser.add_argument(
        "--sprint",
        required=True,
        help="identificador da sprint, ex.: lab01s01",
    )
    parser.add_argument("--owner", default=None, help="dono do Project (default: PROJECT_OWNER)")
    parser.add_argument(
        "--number", type=int, default=None, help="numero do Project (default: PROJECT_NUMBER)"
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        settings = load_settings()
    except MissingTokenError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    owner = args.owner or settings.project_owner
    number = args.number if args.number is not None else settings.project_number

    if not owner or number is None:
        print(
            "erro: dono e numero do Project nao definidos.\n"
            "  Passe --owner e --number, ou defina PROJECT_OWNER e PROJECT_NUMBER no .env.\n"
            "  O numero esta na URL do board: github.com/users/<owner>/projects/<numero>",
            file=sys.stderr,
        )
        return 2

    client = GraphQLClient(settings.graphql_url, settings.github_token, settings.request_timeout)
    captured_at = datetime.now(timezone.utc)

    print(f"Exportando o Project #{number} de {owner} (sprint {args.sprint})...")
    try:
        itens = list(collect_project_items(client, owner, number, args.sprint, captured_at))
    except ProjectNotFoundError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    except GraphQLError as exc:
        print(f"erro na query GraphQL: {exc}", file=sys.stderr)
        return 1
    except HttpError as exc:
        print(f"erro de rede: {exc}", file=sys.stderr)
        return 1

    if not itens:
        print("erro: o Project nao devolveu nenhum item.", file=sys.stderr)
        return 1

    linhas = [project_item_row(item) for item in itens]
    substituidas, total = merge_snapshot(args.output, PROJECT_COLUMNS, args.sprint, linhas)

    print(f"  {len(itens)} cartoes capturados em {captured_at:%Y-%m-%d %H:%M} UTC")
    if substituidas:
        print(f"  {substituidas} linha(s) da sprint {args.sprint} substituida(s)")
    print(f"  {args.output.name}: {total} linhas acumuladas no total")

    por_status = Counter(item.status or "(sem status)" for item in itens)
    print("\nDistribuicao no board:")
    for status, quantidade in por_status.most_common():
        print(f"  {status:<20} {quantidade:>3}")

    sem_assignee = [i for i in itens if not i.assignees]
    sem_issue = [i for i in itens if i.issue_number is None]
    # Issue fechada com cartao fora de Done (ou o contrario) e cartao desatualizado -
    # exatamente o que o enunciado penaliza, e o que so o snapshot consegue flagrar.
    incoerentes = [
        i
        for i in itens
        if i.state == "CLOSED"
        and i.status not in (None, "Done")
        or i.state == "OPEN"
        and i.status == "Done"
    ]

    if incoerentes:
        print(
            f"\naviso: {len(incoerentes)} cartao(oes) com status incoerente com o estado da"
            " Issue:",
            file=sys.stderr,
        )
        for item in incoerentes:
            print(
                f"  #{item.issue_number} Issue {item.state} mas cartao em '{item.status}'"
                f" - {item.title[:45]}",
                file=sys.stderr,
            )

    if sem_assignee:
        print(
            f"\naviso: {len(sem_assignee)} cartao(oes) sem Assignee - o enunciado preve"
            " desconto por isso:",
            file=sys.stderr,
        )
        for item in sem_assignee:
            numero = f"#{item.issue_number}" if item.issue_number else "(draft)"
            print(f"  {numero} {item.title}", file=sys.stderr)

    if sem_issue:
        print(
            f"\naviso: {len(sem_issue)} cartao(oes) sem Issue associada (draft). O enunciado"
            " exige Issues reais, rastreaveis pela API.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
