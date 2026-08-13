"""Validacao da traducao JSON -> dominio.

Sem rede: tudo sai de `tests/fixtures/search_response_sample.json`.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.collection.mappers import parse_datetime, to_repository


def test_parse_datetime_converte_sufixo_z_em_timezone():
    parsed = parse_datetime("2014-08-13T10:00:00Z")

    assert parsed == datetime(2014, 8, 13, 10, 0, tzinfo=timezone.utc)
    assert parsed.tzinfo is not None


def test_to_repository_mapeia_todos_os_campos(search_response):
    node = search_response["search"]["nodes"][0]

    repo = to_repository(node)

    assert repo.name_with_owner == "exemplo/projeto-maduro"
    assert repo.stars == 350000
    assert repo.primary_language == "TypeScript"
    assert repo.merged_pull_requests == 12500
    assert repo.releases == 430
    assert repo.closed_issues == 8000
    assert repo.total_issues == 10000
    assert repo.created_at.year == 2014
    assert repo.pushed_at.year == 2026


def test_to_repository_aceita_linguagem_primaria_nula(search_response):
    node = search_response["search"]["nodes"][1]

    repo = to_repository(node)

    assert repo.primary_language is None


def test_to_repository_aceita_contagens_zeradas(search_response):
    node = search_response["search"]["nodes"][1]

    repo = to_repository(node)

    assert repo.releases == 0
    assert repo.total_issues == 0
    assert repo.closed_issues == 0


def test_to_repository_usa_created_at_quando_pushed_at_e_nulo(search_response):
    node = dict(search_response["search"]["nodes"][0], pushedAt=None)

    repo = to_repository(node)

    assert repo.pushed_at == repo.created_at


def test_to_repository_trata_conexao_ausente(search_response):
    node = {k: v for k, v in search_response["search"]["nodes"][0].items() if k != "releases"}

    repo = to_repository(node)

    assert repo.releases == 0
