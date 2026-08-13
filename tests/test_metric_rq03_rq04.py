"""Validacao das metricas RQ03 (releases) e RQ04 (dias desde a ultima atualizacao).

Responsavel: integrante B.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.collection.mappers import to_repository
from src.domain.metrics.rq03_releases import TETO_CONTAGEM, is_censored, total_releases
from src.domain.metrics.rq04_days_since_update import days_since_update
from tests.test_sampling import repo

REFERENCIA = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _com_push(quando: datetime):
    base = repo("org/x")
    return type(base)(**{**base.__dict__, "pushed_at": quando})


def test_repositorio_sem_release_devolve_zero():
    assert total_releases(repo("org/x", releases=0)) == 0


def test_contagem_no_teto_e_marcada_como_censurada():
    """A conexao releases da GraphQL para de contar em 1000."""
    assert is_censored(repo("org/x", releases=TETO_CONTAGEM))
    assert not is_censored(repo("org/x", releases=TETO_CONTAGEM - 1))


def test_dias_desde_atualizacao_para_data_conhecida():
    r = _com_push(REFERENCIA - timedelta(days=30))

    assert days_since_update(r, REFERENCIA) == 30.0


def test_push_de_hoje_da_proximo_de_zero():
    r = _com_push(REFERENCIA)

    assert days_since_update(r, REFERENCIA) == 0.0


def test_resultado_nunca_negativo_na_amostra_real(search_response):
    agora = datetime.now(timezone.utc)
    repos = [to_repository(n) for n in search_response["search"]["nodes"]]

    assert all(days_since_update(r, agora) >= 0 for r in repos)


def test_usa_pushed_at_e_nao_created_at():
    """updated_at/created_at dariam outro numero; a metrica e sobre atividade de codigo."""
    r = _com_push(REFERENCIA - timedelta(days=5))

    assert days_since_update(r, REFERENCIA) == 5.0


def test_releases_da_amostra_real_sao_nao_negativos(search_response):
    repos = [to_repository(n) for n in search_response["search"]["nodes"]]

    assert all(total_releases(r) >= 0 for r in repos)
