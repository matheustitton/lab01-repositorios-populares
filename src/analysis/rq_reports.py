from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.analysis.popular_languages import POPULARITY_COLUMN, add_popularity_flag
from src.domain.metrics.rq05_primary_language import UNDEFINED
from src.domain.metrics.rq06_closed_issues_ratio import COLUMN as RQ06_COLUMN

from src.analysis import statistics


@dataclass(frozen=True)
class RQResult:
    rq: str
    question: str
    metric: str
    summary: dict[str, Any]
    table: pd.DataFrame | None = None


def _value_table(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """Coluna unica com os valores validos, para os graficos de distribuicao lerem os
    dados brutos sem recalcular nada em `charts.py`."""
    return frame[[column]].rename(columns={column: "value"}).dropna()


def rq01_age(frame: pd.DataFrame) -> RQResult:
    """Sistemas populares sao maduros/antigos? (mediana de idade em anos)"""
    return RQResult(
        rq="RQ01",
        question="Sistemas populares sao maduros/antigos?",
        metric="Idade do repositorio, em anos (age_years)",
        summary=statistics.summarize(frame["age_years"]),
        table=_value_table(frame, "age_years"),
    )


def rq02_merged_pull_requests(frame: pd.DataFrame) -> RQResult:
    """Recebem muita contribuicao externa? (mediana de PRs aceitas)"""
    return RQResult(
        rq="RQ02",
        question="Sistemas populares recebem muita contribuicao externa?",
        metric="Total de pull requests aceitas (merged_pull_requests)",
        summary=statistics.summarize(frame["merged_pull_requests"]),
        table=_value_table(frame, "merged_pull_requests"),
    )


def rq03_releases(frame: pd.DataFrame) -> RQResult:
    """Lancam releases com frequencia? (mediana de releases)"""
    summary = statistics.summarize(frame["releases"])
    sem_release = int((frame["releases"] == 0).sum())
    total = len(frame)
    summary = {
        **summary,
        "sem_release": sem_release,
        "sem_release_pct": round(sem_release / total, 4) if total else 0.0,
    }
    return RQResult(
        rq="RQ03",
        question="Sistemas populares lancam releases com frequencia?",
        metric="Total de releases (releases)",
        summary=summary,
        table=_value_table(frame, "releases"),
    )


def rq04_days_since_update(frame: pd.DataFrame) -> RQResult:
    """Sao atualizados com frequencia? (mediana de dias desde o ultimo push)"""
    return RQResult(
        rq="RQ04",
        question="Sistemas populares sao atualizados com frequencia?",
        metric="Dias desde a ultima atualizacao (days_since_update)",
        summary=statistics.summarize(frame["days_since_update"]),
        table=_value_table(frame, "days_since_update"),
    )


def rq05_primary_language(frame: pd.DataFrame) -> RQResult:
    """Sao escritos nas linguagens mais populares? (contagem por linguagem)"""
    contagem = statistics.count_by_category(frame["primary_language"])
    tabela = contagem.rename_axis("primary_language").reset_index(name="count")

    total = len(frame)
    indefinidos = int((frame["primary_language"].fillna(UNDEFINED) == UNDEFINED).sum())
    top = tabela.iloc[0] if not tabela.empty else None

    summary = {
        "total_repositorios": total,
        "linguagens_distintas": int(contagem.shape[0]),
        "sem_linguagem": indefinidos,
        "sem_linguagem_pct": round(indefinidos / total, 4) if total else 0.0,
        "linguagem_mais_frequente": str(top["primary_language"]) if top is not None else None,
        "linguagem_mais_frequente_count": int(top["count"]) if top is not None else 0,
    }

    return RQResult(
        rq="RQ05",
        question="Sistemas populares sao escritos nas linguagens mais populares?",
        metric="Contagem de repositorios por linguagem primaria (primary_language)",
        summary=summary,
        table=tabela,
    )


def rq06_closed_issues_ratio(frame: pd.DataFrame) -> RQResult:
    """Possuem alto percentual de issues fechadas? (mediana da razao)

    Repositorios sem nenhuma issue sao excluidos do resultado principal (ver
    docs/hipoteses.md e src/domain/metrics/rq06_closed_issues_ratio.py) - "nao teve
    issue" nao e o mesmo que "nao resolveu issue", e inclui-los puxaria a mediana para
    baixo de forma artificial. A mediana com esses casos incluidos fica registrada em
    `summary["median_incluindo_sem_issues"]`, para referencia.
    """
    com_issues = frame[frame["total_issues"] > 0]
    summary_geral = statistics.summarize(frame[RQ06_COLUMN])
    summary_interpretavel = statistics.summarize(com_issues[RQ06_COLUMN])

    summary = {
        **summary_interpretavel,
        "median_incluindo_sem_issues": summary_geral["median"],
        "repositorios_sem_issues": int(len(frame) - len(com_issues)),
    }

    return RQResult(
        rq="RQ06",
        question="Sistemas populares possuem alto percentual de issues fechadas?",
        metric=(
            "Razao entre issues fechadas e total (closed_issues_ratio), "
            "excluindo repositorios sem nenhuma issue"
        ),
        summary=summary,
        table=_value_table(com_issues, RQ06_COLUMN),
    )


#: Linguagens com menos repositorios do que isto entram no grupo "Outras" na RQ07 - o
#: mesmo limiar (n >= 30) que docs/hipoteses.md ja usa para decidir quais linguagens
#: sustentam uma mediana estavel o suficiente para comparacao.
MIN_GROUP_SIZE = 30
OTHER_LABEL = "Outras"


def rq07_by_language(frame: pd.DataFrame) -> RQResult:
    """RQ02, RQ03 e RQ04 desdobradas por linguagem primaria.
    """
    dados = add_popularity_flag(frame)

    contagem = dados["primary_language"].value_counts()
    linguagens_grandes = set(contagem[contagem >= MIN_GROUP_SIZE].index) - {UNDEFINED}
    dados = dados.assign(
        grupo=dados["primary_language"].where(
            dados["primary_language"].isin(linguagens_grandes), OTHER_LABEL
        )
    )

    linhas = []
    for grupo, subframe in dados.groupby("grupo"):
        linhas.append(
            {
                "primary_language": grupo,
                "n": len(subframe),
                POPULARITY_COLUMN: bool(subframe[POPULARITY_COLUMN].any())
                if grupo != OTHER_LABEL
                else False,
                "median_merged_pull_requests": statistics.summarize(
                    subframe["merged_pull_requests"]
                )["median"],
                "median_releases": statistics.summarize(subframe["releases"])["median"],
                "median_days_since_update": statistics.summarize(
                    subframe["days_since_update"]
                )["median"],
            }
        )

    tabela = pd.DataFrame(linhas).sort_values("n", ascending=False).reset_index(drop=True)
    outras_n = int(tabela.loc[tabela["primary_language"] == OTHER_LABEL, "n"].sum()) if (
        (tabela["primary_language"] == OTHER_LABEL).any()
    ) else 0

    summary = {
        "linguagens_comparadas": int((tabela["primary_language"] != OTHER_LABEL).sum()),
        "min_group_size": MIN_GROUP_SIZE,
        "repositorios_em_outras": outras_n,
    }

    return RQResult(
        rq="RQ07",
        question=(
            "Linguagens populares recebem mais contribuicao, lancam mais releases e "
            "sao atualizadas com mais frequencia?"
        ),
        metric=(
            "Mediana de PRs aceitas, releases e dias desde atualizacao, por linguagem "
            f"primaria (n >= {MIN_GROUP_SIZE}; o restante agrupado em 'Outras')"
        ),
        summary=summary,
        table=tabela,
    )


def all_results(frame: pd.DataFrame) -> list[RQResult]:
    """Executa as sete RQs, na ordem do enunciado."""
    return [
        rq01_age(frame),
        rq02_merged_pull_requests(frame),
        rq03_releases(frame),
        rq04_days_since_update(frame),
        rq05_primary_language(frame),
        rq06_closed_issues_ratio(frame),
        rq07_by_language(frame),
    ]
