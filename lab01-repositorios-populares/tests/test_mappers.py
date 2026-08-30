"""Validacao da traducao JSON -> dominio.

A fixture e uma fatia real da coleta do Lab01S01, escolhida para conter os casos de
borda: repositorio sem linguagem primaria, sem releases e sem issues. Os testes
localizam cada caso por predicado, e nao por indice, para continuarem validos se a
fixture for regerada com outra amostra.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.collection.mappers import parse_datetime, to_repository


@pytest.fixture
def nodes(search_response):
    return search_response["search"]["nodes"]


def _primeiro(nodes, criterio, descricao):
    for node in nodes:
        if criterio(node):
            return node
    pytest.fail(f"a fixture nao contem nenhum repositorio {descricao}")


def test_parse_datetime_converte_sufixo_z_em_timezone():
    parsed = parse_datetime("2014-08-13T10:00:00Z")

    assert parsed == datetime(2014, 8, 13, 10, 0, tzinfo=timezone.utc)
    assert parsed.tzinfo is not None


def test_to_repository_mapeia_todos_os_campos_com_os_tipos_certos(nodes):
    repo = to_repository(nodes[0])

    assert repo.name_with_owner == nodes[0]["nameWithOwner"]
    assert repo.url.startswith("https://github.com/")
    assert isinstance(repo.stars, int) and repo.stars > 0
    assert isinstance(repo.merged_pull_requests, int)
    assert isinstance(repo.releases, int)
    assert isinstance(repo.closed_issues, int)
    assert isinstance(repo.total_issues, int)
    assert repo.created_at.tzinfo is not None
    assert repo.pushed_at.tzinfo is not None
    assert repo.pushed_at >= repo.created_at


def test_valores_batem_com_o_json_de_origem(nodes):
    node = nodes[0]

    repo = to_repository(node)

    assert repo.stars == node["stargazerCount"]
    assert repo.merged_pull_requests == node["mergedPullRequests"]["totalCount"]
    assert repo.releases == node["releases"]["totalCount"]
    assert repo.closed_issues == node["closedIssues"]["totalCount"]
    assert repo.total_issues == node["totalIssues"]["totalCount"]


def test_todos_os_repositorios_da_amostra_mapeiam_sem_erro(nodes):
    repos = [to_repository(n) for n in nodes]

    assert len(repos) == len(nodes)
    assert all(r.closed_issues <= r.total_issues for r in repos)


def test_aceita_linguagem_primaria_nula(nodes):
    node = _primeiro(nodes, lambda n: n["primaryLanguage"] is None, "sem linguagem primaria")

    assert to_repository(node).primary_language is None


def test_aceita_repositorio_sem_releases(nodes):
    node = _primeiro(nodes, lambda n: n["releases"]["totalCount"] == 0, "sem releases")

    assert to_repository(node).releases == 0


def test_aceita_repositorio_sem_issues(nodes):
    node = _primeiro(nodes, lambda n: n["totalIssues"]["totalCount"] == 0, "sem issues")

    repo = to_repository(node)

    assert repo.total_issues == 0
    assert repo.closed_issues == 0


def test_usa_created_at_quando_pushed_at_e_nulo(nodes):
    node = dict(nodes[0], pushedAt=None)

    repo = to_repository(node)

    assert repo.pushed_at == repo.created_at


def test_trata_conexao_ausente(nodes):
    node = {k: v for k, v in nodes[0].items() if k != "releases"}

    assert to_repository(node).releases == 0
