"""Referencia de "linguagens mais populares" usada na RQ05 e na RQ07.

Fonte unica declarada em `docs/fontes.md` e mantida ao longo de todo o laboratorio,
como o enunciado exige. Ficar isolada aqui garante que trocar a fonte seja uma alteracao
de um arquivo so, e que RQ05 e RQ07 jamais usem listas divergentes.

Ressalva metodologica: o Octoverse ordena por numero de contribuidores, enquanto este
estudo ordena por estrelas. Sao medidas diferentes de popularidade - a divergencia entre
as duas ordenacoes e o resultado que a RQ05 investiga, nao um defeito da referencia.
"""

from __future__ import annotations

import pandas as pd

from src.domain.metrics.rq05_primary_language import UNDEFINED

#: Fonte da lista - registrada tambem em docs/fontes.md.
SOURCE = "GitHub Octoverse 2025"
SOURCE_URL = "https://octoverse.github.com/"
SOURCE_PERIOD = "2024-09-01 a 2025-08-31"
SOURCE_ACCESSED = "2026-08-13"

#: Ranking da fonte, em ordem de popularidade. Os nomes seguem a grafia do GitHub
#: Linguist, que e a mesma devolvida por `primaryLanguage.name` na API.
POPULAR_LANGUAGES: tuple[str, ...] = (
    "TypeScript",
    "Python",
    "JavaScript",
    "Java",
    "C#",
    "PHP",
    "Shell",
    "C++",
    "HCL",
    "Go",
)

#: Busca sem depender de caixa, para o caso de a API mudar a grafia.
_INDICE = {nome.casefold(): posicao for posicao, nome in enumerate(POPULAR_LANGUAGES, 1)}

POPULARITY_COLUMN = "is_popular_language"
RANK_COLUMN = "language_rank"


def is_popular(language: str | None) -> bool:
    """Indica se a linguagem consta no ranking da fonte de referencia.

    `None` e `Undefined` sao falsos por definicao: repositorio sem linguagem primaria nao
    tem posicao possivel num ranking de linguagens.
    """
    if not language or language == UNDEFINED:
        return False
    return language.casefold() in _INDICE


def rank(language: str | None) -> int | None:
    """Posicao da linguagem no ranking (1 e a mais popular), ou `None` se fora dele."""
    if not language or language == UNDEFINED:
        return None
    return _INDICE.get(language.casefold())


def add_popularity_flag(frame: pd.DataFrame, column: str = "primary_language") -> pd.DataFrame:
    """Devolve uma copia do DataFrame com as colunas de popularidade da linguagem.

    Nao altera o DataFrame recebido: a analise costuma reutilizar o original, e mutar o
    argumento faria o resultado depender da ordem em que as RQs sao executadas.
    """
    resultado = frame.copy()
    resultado[POPULARITY_COLUMN] = resultado[column].apply(is_popular)
    # "Int64" (maiusculo) e o inteiro nulavel do pandas. Com o int comum, a presenca de
    # um unico None promoveria a coluna a float e a posicao 2 viraria "2.0".
    resultado[RANK_COLUMN] = pd.array(
        [rank(valor) for valor in resultado[column]], dtype="Int64"
    )
    return resultado
