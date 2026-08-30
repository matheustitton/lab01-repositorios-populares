"""Validacao da serializacao para CSV e do resumo agregado (Issue #3)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.domain.metrics.registry import METRICS, metrics_at
from src.domain.summary import SUMMARY_COLUMNS, build_summary
from src.storage.csv_writer import write_csv
from src.storage.serializers import BASE_COLUMNS, repository_header, repository_row, repository_rows
from tests.test_sampling import repo

REFERENCIA = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_cabecalho_e_base_seguida_das_metricas():
    header = repository_header()

    assert header[: len(BASE_COLUMNS)] == BASE_COLUMNS
    assert len(header) == len(BASE_COLUMNS) + len(METRICS)


def test_linha_tem_o_mesmo_comprimento_do_cabecalho():
    linha = repository_row(repo("org/x"), metrics_at(REFERENCIA))

    assert len(linha) == len(repository_header())


def test_registrar_metrica_nova_reflete_em_cabecalho_e_linha():
    """O registro e a unica fonte de verdade das colunas derivadas."""
    header_antes = len(repository_header())
    linha_antes = len(repository_row(repo("org/x"), metrics_at(REFERENCIA)))

    assert header_antes == linha_antes
    assert "age_years" in repository_header()
    assert "age_days" in repository_header()


def test_todas_as_linhas_usam_a_mesma_referencia():
    """Sem instante fixo, reprocessar o mesmo JSON daria numeros diferentes."""
    repos = [repo(f"org/r{i}") for i in range(5)]

    primeira = repository_rows(repos, REFERENCIA)
    segunda = repository_rows(repos, REFERENCIA)

    assert primeira == segunda


def test_referencias_diferentes_mudam_as_metricas_temporais():
    repos = [repo("org/x")]

    agora = repository_rows(repos, REFERENCIA)[0]
    depois = repository_rows(repos, REFERENCIA + timedelta(days=365))[0]

    assert agora != depois


def test_csv_e_escrito_com_cabecalho_e_linhas(tmp_path):
    destino = tmp_path / "sub" / "saida.csv"

    total = write_csv(destino, ("a", "b"), [[1, 2], [3, 4]])

    assert total == 2
    conteudo = destino.read_text(encoding="utf-8-sig").splitlines()
    assert conteudo[0] == "a,b"
    assert len(conteudo) == 3


def test_resumo_cobre_todas_as_rqs():
    repos = [
        repo("org/a", lang="Python", prs=10, releases=5, fechadas=8, total=10),
        repo("org/b", lang=None, prs=20, releases=0, fechadas=0, total=0),
        repo("org/c", lang="Python", prs=30, releases=15, fechadas=5, total=10),
    ]

    resumo = build_summary(repos, REFERENCIA)
    rqs = {linha.rq for linha in resumo}

    assert rqs == {"rq01", "rq02", "rq03", "rq04", "rq05", "rq06"}
    assert all(len(linha.as_row()) == len(SUMMARY_COLUMNS) for linha in resumo)


def test_resumo_separa_repositorios_sem_issues_na_rq06():
    """Incluir quem nao tem issue puxa a mediana para baixo sem significar nada."""
    repos = [
        repo("org/a", fechadas=9, total=10),
        repo("org/b", fechadas=0, total=0),
        repo("org/c", fechadas=8, total=10),
    ]

    resumo = {linha.metrica: linha for linha in build_summary(repos, REFERENCIA)}

    com_todos = resumo["mediana_razao_issues_fechadas"].valor
    sem_vazios = resumo["mediana_razao_issues_fechadas_excluindo_sem_issues"].valor

    assert resumo["repositorios_sem_issues"].valor == 1
    assert sem_vazios > com_todos


def test_resumo_conta_censurados_da_rq03():
    repos = [repo("org/a", releases=1000), repo("org/b", releases=12)]

    resumo = {linha.metrica: linha for linha in build_summary(repos, REFERENCIA)}

    assert resumo["contagem_censurada_no_teto"].valor == 1


def test_contagem_por_linguagem_e_ordenada_e_estavel():
    repos = [
        repo("org/a", lang="Python"),
        repo("org/b", lang="Rust"),
        repo("org/c", lang="Python"),
        repo("org/d", lang=None),
    ]

    linhas = [r for r in build_summary(repos, REFERENCIA) if r.metrica == "contagem_por_linguagem"]

    assert linhas[0].categoria == "Python"
    assert linhas[0].valor == 2
    assert {linha.categoria for linha in linhas} == {"Python", "Rust", "Undefined"}
