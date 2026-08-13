"""Referencia de "linguagens mais populares" usada na RQ05 e na RQ07.

Fonte unica declarada em `docs/fontes.md` e mantida ao longo de todo o laboratorio,
como o enunciado exige. Ficar isolada aqui garante que trocar a fonte seja uma alteracao
de um arquivo so, e que RQ05 e RQ07 jamais usem listas divergentes.

Preencher `POPULAR_LANGUAGES` com o ranking da fonte escolhida antes de rodar a analise.
"""

from __future__ import annotations

import pandas as pd

#: Fonte da lista - registrar tambem em docs/fontes.md com link e data de consulta.
SOURCE = "GitHub Octoverse"
SOURCE_URL = "https://octoverse.github.com/"
SOURCE_ACCESSED = ""  # AAAA-MM-DD da consulta

#: Ranking da fonte, em ordem de popularidade. Nomes devem bater com os da API do
#: GitHub (ex.: "C#", "Jupyter Notebook", "Shell").
POPULAR_LANGUAGES: tuple[str, ...] = ()


def is_popular(language: str) -> bool:
    """Indica se a linguagem consta no ranking da fonte de referencia."""
    raise NotImplementedError


def add_popularity_flag(frame: pd.DataFrame) -> pd.DataFrame:
    """Devolve uma copia do DataFrame com a coluna booleana `is_popular_language`."""
    raise NotImplementedError
