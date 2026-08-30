"""Validacao da referencia de linguagens populares (Issue #4).

A lista vem do Octoverse 2025 e e a unica fonte usada por RQ05 e RQ07 - ver docs/fontes.md.
"""

from __future__ import annotations

import pandas as pd

from src.analysis.popular_languages import (
    POPULAR_LANGUAGES,
    POPULARITY_COLUMN,
    RANK_COLUMN,
    add_popularity_flag,
    is_popular,
    rank,
)
from src.domain.metrics.rq05_primary_language import UNDEFINED


def test_ranking_nao_esta_vazio_e_nao_tem_repetidos():
    assert len(POPULAR_LANGUAGES) == 10
    assert len(set(POPULAR_LANGUAGES)) == len(POPULAR_LANGUAGES)


def test_topo_do_ranking_segue_a_fonte():
    """Octoverse 2025: TypeScript assumiu o primeiro lugar, a frente de Python."""
    assert POPULAR_LANGUAGES[:3] == ("TypeScript", "Python", "JavaScript")


def test_linguagem_do_ranking_e_popular():
    assert is_popular("TypeScript")
    assert is_popular("Go")


def test_linguagem_fora_do_ranking_nao_e_popular():
    assert not is_popular("Rust")
    assert not is_popular("Haskell")


def test_sem_linguagem_primaria_nunca_e_popular():
    """Repositorio sem linguagem nao tem posicao possivel num ranking de linguagens."""
    assert not is_popular(None)
    assert not is_popular(UNDEFINED)
    assert not is_popular("")


def test_comparacao_ignora_caixa():
    assert is_popular("typescript")
    assert is_popular("PYTHON")


def test_rank_devolve_a_posicao_da_fonte():
    assert rank("TypeScript") == 1
    assert rank("Python") == 2
    assert rank("Go") == 10


def test_rank_de_fora_do_ranking_e_nulo():
    assert rank("Rust") is None
    assert rank(UNDEFINED) is None


def test_flag_de_popularidade_e_adicionada_ao_dataframe():
    frame = pd.DataFrame({"primary_language": ["Python", "Rust", UNDEFINED]})

    resultado = add_popularity_flag(frame)

    assert list(resultado[POPULARITY_COLUMN]) == [True, False, False]
    assert resultado[RANK_COLUMN][0] == 2
    assert resultado[RANK_COLUMN].isna().tolist() == [False, True, True]


def test_rank_e_inteiro_nulavel_e_nao_float():
    """Sem Int64, um unico None promoveria a coluna a float e o rank 2 viraria 2.0."""
    frame = pd.DataFrame({"primary_language": ["Python", "Rust"]})

    resultado = add_popularity_flag(frame)

    assert str(resultado[RANK_COLUMN].dtype) == "Int64"


def test_flag_nao_altera_o_dataframe_original():
    """A analise reusa o original; mutar tornaria o resultado dependente da ordem."""
    frame = pd.DataFrame({"primary_language": ["Python"]})

    add_popularity_flag(frame)

    assert POPULARITY_COLUMN not in frame.columns
