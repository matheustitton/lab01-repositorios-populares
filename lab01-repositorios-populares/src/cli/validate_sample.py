"""Validacao da amostra coletada (Lab01S01, Issue #2).

    python -m src.cli.validate_sample
    python -m src.cli.validate_sample --size 10 --output docs/validacao_amostra.md

Le o JSON ja coletado, escolhe uma amostra que cobre os casos de borda e confere os
campos diretos contra a API REST - fonte independente da GraphQL usada na coleta.

Os agregados (PRs aceitas e releases) a REST nao entrega barato: para eles o relatorio
imprime o link do repositorio, e a conferencia e manual, como o criterio da Issue pede.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.collection.mappers import to_repository
from src.collection.rest_source import TETO_TOTALCOUNT, count_releases, fetch_repository
from src.config.settings import PROJECT_ROOT, RAW_REPOS_JSON, load_dotenv
from src.domain.sampling import SampleEntry, compare, select_sample
from src.infrastructure.http_client import HttpError

DEFAULT_OUTPUT = PROJECT_ROOT / "docs" / "validacao_amostra.md"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate_sample",
        description="Confere a amostra coletada contra a API REST do GitHub.",
    )
    parser.add_argument("--input", type=Path, default=RAW_REPOS_JSON)
    parser.add_argument("--size", type=int, default=8, help="tamanho da amostra (5 a 10)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser


def _tabela_amostra(amostra: list[SampleEntry]) -> list[str]:
    linhas = [
        "| # | Repositorio | Motivo da escolha | Estrelas | Criado em | Linguagem |",
        "|---|---|---|---|---|---|",
    ]
    for i, entrada in enumerate(amostra, 1):
        r = entrada.repository
        linhas.append(
            f"| {i} | [{r.name_with_owner}]({r.url}) | {entrada.motivo} | "
            f"{r.stars:,} | {r.created_at:%Y-%m-%d} | {r.primary_language or 'Undefined'} |"
        )
    return linhas


def _tabela_comparacao(resultados: list[tuple[str, list]]) -> list[str]:
    linhas = [
        "| Repositorio | Campo | GraphQL (coletado) | REST (agora) | Resultado |",
        "|---|---|---|---|---|",
    ]
    for nome, comparacoes in resultados:
        for c in comparacoes:
            marca = c.observacao if c.confere else f"**{c.observacao}**"
            linhas.append(f"| {nome} | {c.campo} | {c.graphql} | {c.rest} | {marca} |")
    return linhas


def _selecao_manual(amostra: list[SampleEntry]) -> list[SampleEntry]:
    """Escolhe os 3 repositorios que valem a conferencia a mao.

    Conferir tres repositorios com 0 releases nao valida nada. Os que importam sao os de
    maior contagem - onde um erro de agregacao apareceria - mais um de contagem zero,
    para confirmar que o zero e real e nao um campo que veio nulo e virou 0.
    """
    por_prs = max(amostra, key=lambda e: e.repository.merged_pull_requests)
    por_releases = max(amostra, key=lambda e: e.repository.releases)
    zerados = [e for e in amostra if e.repository.releases == 0]

    escolhidos: list[SampleEntry] = []
    for entrada in (por_prs, por_releases, *zerados):
        if entrada not in escolhidos:
            escolhidos.append(entrada)
        if len(escolhidos) == 3:
            break
    return escolhidos


def _tabela_manual(amostra: list[SampleEntry]) -> list[str]:
    linhas = [
        "| Repositorio | PRs aceitas (coletado) | Releases (coletado) | Conferir em |",
        "|---|---|---|---|",
    ]
    for entrada in _selecao_manual(amostra):
        r = entrada.repository
        linhas.append(
            f"| {r.name_with_owner} | {r.merged_pull_requests:,} | {r.releases:,} | "
            f"[PRs]({r.url}/pulls?q=is%3Apr+is%3Amerged) / [releases]({r.url}/releases) |"
        )
    return linhas


def _secao_teto(repositories, token) -> list[str]:
    """Detecta contagens censuradas pelo teto da API e busca o valor real na REST.

    A conexao `releases` da GraphQL para de contar em 1000. Sem esta checagem, o dataset
    passa a impressao de que varios repositorios tem exatamente o mesmo total, e qualquer
    estatistica da cauda superior da RQ03 sai errada.
    """
    censurados = [r for r in repositories if r.releases == TETO_TOTALCOUNT]
    if not censurados:
        return [
            "## Teto de contagem",
            "",
            f"Nenhum repositorio com contagem exatamente igual a {TETO_TOTALCOUNT}.",
            "",
        ]

    linhas = [
        "## Teto de contagem detectado",
        "",
        f"A conexao `releases` da GraphQL para de contar em {TETO_TOTALCOUNT}. Os",
        f"repositorios abaixo reportaram exatamente esse valor: sao contagens **censuradas**,",
        "nao contagens reais. O valor verdadeiro veio da paginacao da REST.",
        "",
        "| Repositorio | GraphQL (censurado) | REST (real) |",
        "|---|---|---|",
    ]
    for r in censurados:
        real = count_releases(r.name_with_owner, token)
        linhas.append(f"| {r.name_with_owner} | {r.releases:,} | {real:,} |")

    proporcao = len(censurados) / len(repositories) * 100
    linhas += [
        "",
        f"**{len(censurados)} de {len(repositories)} repositorios afetados ({proporcao:.0f}%).**",
        "",
        "Impacto na RQ03: a **mediana nao e afetada**, porque os censurados estao muito",
        "acima dela. Ja media, maximo e o formato da cauda superior ficam incorretos e nao",
        "devem ser reportados sem esta ressalva. Os demais campos foram verificados e nao",
        "tem teto: PRs aceitas e issues aparecem na coleta com valores bem acima de",
        f"{TETO_TOTALCOUNT}.",
        "",
    ]
    return linhas


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.input.exists():
        print(
            f"erro: {args.input} nao encontrado. Rode a coleta antes:\n"
            "  python -m src.cli.collect_repositories --limit 100",
            file=sys.stderr,
        )
        return 2

    load_dotenv()
    import os

    token = os.environ.get("GITHUB_TOKEN", "").strip() or None

    nodes = json.loads(args.input.read_text(encoding="utf-8"))
    repositories = [to_repository(n) for n in nodes]
    amostra = select_sample(repositories, args.size)

    print(f"Amostra de {len(amostra)} repositorios (de {len(repositories)} coletados).")
    print("Conferindo contra a API REST...")

    resultados: list[tuple[str, list]] = []
    divergencias = 0
    for entrada in amostra:
        nome = entrada.repository.name_with_owner
        try:
            snapshot = fetch_repository(nome, token)
        except HttpError as exc:
            print(f"  {nome}: falha ao consultar a REST ({exc})", file=sys.stderr)
            return 1
        comparacoes = compare(entrada.repository, snapshot)
        divergentes = [c for c in comparacoes if not c.confere]
        divergencias += len(divergentes)
        print(f"  {nome}: {'OK' if not divergentes else f'{len(divergentes)} divergencia(s)'}")
        resultados.append((nome, comparacoes))

    agora = datetime.now(timezone.utc)
    doc = [
        "# Validacao da amostra - Lab01S01",
        "",
        f"Gerado por `python -m src.cli.validate_sample` em {agora:%Y-%m-%d %H:%M} UTC.",
        f"Fonte: `{args.input.name}` ({len(repositories)} repositorios coletados).",
        "",
        "## Amostra selecionada",
        "",
        "Selecao deterministica, priorizando os casos de borda onde o mapeamento pode",
        "falhar - repositorio sem linguagem primaria, sem releases, sem issues. Uma amostra",
        "sorteada tenderia a conter so repositorios comuns e nao validaria nada.",
        "",
        *_tabela_amostra(amostra),
        "",
        "## Conferencia automatica: GraphQL vs REST",
        "",
        "Os mesmos repositorios lidos pela API REST, que e uma fonte independente da",
        "GraphQL usada na coleta. `pushed_at` e comparado ate o minuto, porque os dois",
        "endpoints podem ser servidos por caches diferentes.",
        "",
        "**Deriva temporal nao e erro.** O dataset e um retrato do instante da coleta; a",
        "REST responde com o estado de agora. Entre um e outro, repositorios populares",
        "ganham estrelas e recebem pushes. Por isso `stars` e `pushed_at` sao tratados como",
        "campos vivos: diferenca pequena e esperada e vem anotada como deriva. Ja `created_at`",
        "e `primary_language` sao estaveis - qualquer diferenca ali seria erro de verdade na",
        "query ou no mapeamento.",
        "",
        *_tabela_comparacao(resultados),
        "",
        f"**Divergencias reais encontradas: {divergencias}**",
        "",
        *_secao_teto(repositories, token),
        "## Conferencia manual",
        "",
        "A REST nao entrega barato o total de PRs aceitas nem o de releases. Estes tres",
        "repositorios foram conferidos a mao nas paginas do GitHub:",
        "",
        *_tabela_manual(amostra),
        "",
        "| Repositorio | Conferido por | Data | Resultado |",
        "|---|---|---|---|",
        "| | | | |",
        "| | | | |",
        "| | | | |",
        "",
        "> Preencher a tabela acima ao conferir. O criterio de aceite da Issue #2 exige",
        "> validacao manual de pelo menos 2 a 3 repositorios da amostra.",
        "",
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(doc), encoding="utf-8")

    print(f"\nrelatorio escrito em {args.output}")
    print(f"divergencias automaticas: {divergencias}")
    if divergencias:
        print("atencao: ha divergencia entre GraphQL e REST - investigar antes de fechar a #2")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
