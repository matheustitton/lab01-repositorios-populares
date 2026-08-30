"""Validacao das metricas RQ05 (linguagem primaria) e RQ06 (razao de issues fechadas).

Responsavel: integrante C.
"""

from __future__ import annotations

from src.collection.mappers import to_repository
from src.domain.metrics.rq05_primary_language import UNDEFINED, primary_language
from src.domain.metrics.rq06_closed_issues_ratio import closed_issues_ratio, has_issues
from tests.test_sampling import repo


def test_linguagem_nula_vira_rotulo_explicito():
    """Categoria propria (listas de links, material de estudo), nao dado faltante."""
    assert primary_language(repo("org/x", lang=None)) == UNDEFINED


def test_linguagem_definida_e_preservada():
    assert primary_language(repo("org/x", lang="Rust")) == "Rust"


def test_nenhum_valor_vazio_na_amostra_real(search_response):
    repos = [to_repository(n) for n in search_response["search"]["nodes"]]

    assert all(primary_language(r) for r in repos)


def test_razao_em_caso_comum():
    assert closed_issues_ratio(repo("org/x", fechadas=75, total=100)) == 0.75


def test_razao_sempre_dentro_do_intervalo_na_amostra_real(search_response):
    repos = [to_repository(n) for n in search_response["search"]["nodes"]]

    assert all(0.0 <= closed_issues_ratio(r) <= 1.0 for r in repos)


def test_repositorio_sem_issues_nao_divide_por_zero():
    r = repo("org/x", fechadas=0, total=0)

    assert closed_issues_ratio(r) == 0.0
    assert not has_issues(r)


def test_has_issues_separa_quem_tem_denominador():
    assert has_issues(repo("org/x", fechadas=1, total=10))
    assert not has_issues(repo("org/x", fechadas=0, total=0))


def test_todas_fechadas_da_um():
    assert closed_issues_ratio(repo("org/x", fechadas=40, total=40)) == 1.0
