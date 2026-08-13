"""Validacao das metricas RQ01 (idade) e RQ02 (PRs aceitas).

Responsavel: integrante A.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.collection.mappers import to_repository
from src.domain.metrics.rq01_age import age_in_days, age_in_years
from src.domain.metrics.rq02_merged_pull_requests import merged_pull_requests
from tests.test_sampling import repo

REFERENCIA = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _com_criacao(quando: datetime):
    base = repo("org/x")
    return type(base)(**{**base.__dict__, "created_at": quando})


def test_idade_em_anos_para_data_conhecida():
    criado = REFERENCIA - timedelta(days=3652)  # ~10 anos

    assert age_in_years(_com_criacao(criado), REFERENCIA) == 10.0


def test_idade_em_dias_para_data_conhecida():
    criado = REFERENCIA - timedelta(days=100)

    assert age_in_days(_com_criacao(criado), REFERENCIA) == 100.0


def test_repositorio_criado_agora_tem_idade_zero_e_nunca_negativa():
    r = _com_criacao(REFERENCIA)

    assert age_in_years(r, REFERENCIA) == 0.0
    assert age_in_days(r, REFERENCIA) >= 0


def test_idade_cresce_com_o_tempo():
    r = _com_criacao(REFERENCIA - timedelta(days=365))

    antes = age_in_years(r, REFERENCIA)
    depois = age_in_years(r, REFERENCIA + timedelta(days=365))

    assert depois > antes


def test_prs_aceitas_le_o_campo_de_merged_e_nao_o_total(search_response):
    """A query usa pullRequests(states: MERGED); o total geral seria outro numero."""
    node = search_response["search"]["nodes"][0]

    r = to_repository(node)

    assert merged_pull_requests(r) == node["mergedPullRequests"]["totalCount"]


def test_prs_aceitas_de_toda_a_amostra_sao_nao_negativas(search_response):
    repos = [to_repository(n) for n in search_response["search"]["nodes"]]

    assert all(merged_pull_requests(r) >= 0 for r in repos)


def test_amostra_real_tem_idades_plausiveis(search_response):
    """O GitHub existe desde 2008 - idade acima disso indicaria erro de parsing."""
    agora = datetime.now(timezone.utc)
    repos = [to_repository(n) for n in search_response["search"]["nodes"]]

    idades = [age_in_years(r, agora) for r in repos]

    assert all(0 < idade < 20 for idade in idades)
