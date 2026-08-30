"""Resumo agregado das RQ01 a RQ06 (Issue #3).

Funcoes puras sobre `Repository`, com `statistics` da biblioteca padrao. Nao usa pandas
de proposito: o caminho de coleta e processamento fica sem dependencia externa, e o
pandas entra so na analise mais rica do Lab01S03 (`src/analysis/`).

O enunciado pede valores medianos. As distribuicoes aqui sao fortemente assimetricas -
poucos repositorios gigantes dominariam qualquer media.
"""

from __future__ import annotations

import statistics
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from src.domain.metrics import (
    rq01_age,
    rq02_merged_pull_requests,
    rq03_releases,
    rq04_days_since_update,
    rq05_primary_language,
    rq06_closed_issues_ratio,
)
from src.domain.models import Repository

SUMMARY_COLUMNS: tuple[str, ...] = ("rq", "metrica", "categoria", "valor", "n")


@dataclass(frozen=True)
class SummaryRow:
    """Uma linha do resumo: um numero, com o que ele mede e sobre quantos casos."""

    rq: str
    metrica: str
    categoria: str
    valor: float | int
    n: int

    def as_row(self) -> list[object]:
        return [self.rq, self.metrica, self.categoria, self.valor, self.n]


def _mediana(valores: Sequence[float]) -> float:
    return round(statistics.median(valores), 4) if valores else 0.0


def build_summary(
    repositories: Sequence[Repository],
    reference: datetime,
) -> list[SummaryRow]:
    """Monta o resumo das RQ01 a RQ06.

    RQ03 e RQ06 ganham linhas extras porque o numero simples engana:
    - RQ03: repositorios com contagem no teto da API sao censurados, nao reais.
    - RQ06: repositorios sem nenhuma issue tem razao 0.0 por convencao, e inclui-los na
      mediana confunde "nao teve issue" com "nao resolveu issue".
    """
    total = len(repositories)
    linhas: list[SummaryRow] = []

    idades_anos = [rq01_age.age_in_years(r, reference) for r in repositories]
    idades_dias = [rq01_age.age_in_days(r, reference) for r in repositories]
    linhas.append(SummaryRow("rq01", "mediana_idade_anos", "", _mediana(idades_anos), total))
    linhas.append(SummaryRow("rq01", "mediana_idade_dias", "", _mediana(idades_dias), total))

    prs = [rq02_merged_pull_requests.merged_pull_requests(r) for r in repositories]
    linhas.append(SummaryRow("rq02", "mediana_prs_aceitas", "", _mediana(prs), total))

    releases = [rq03_releases.total_releases(r) for r in repositories]
    censurados = [r for r in repositories if rq03_releases.is_censored(r)]
    sem_release = [r for r in repositories if r.releases == 0]
    linhas.append(SummaryRow("rq03", "mediana_releases", "", _mediana(releases), total))
    linhas.append(
        SummaryRow("rq03", "repositorios_sem_release", "", len(sem_release), total)
    )
    linhas.append(
        SummaryRow("rq03", "contagem_censurada_no_teto", "", len(censurados), total)
    )

    dias = [rq04_days_since_update.days_since_update(r, reference) for r in repositories]
    linhas.append(SummaryRow("rq04", "mediana_dias_desde_atualizacao", "", _mediana(dias), total))

    contagem = Counter(rq05_primary_language.primary_language(r) for r in repositories)
    # Ordem: mais frequentes primeiro; empate resolvido por nome, para o CSV ser estavel.
    for linguagem, quantidade in sorted(contagem.items(), key=lambda kv: (-kv[1], kv[0])):
        linhas.append(SummaryRow("rq05", "contagem_por_linguagem", linguagem, quantidade, total))
    linhas.append(SummaryRow("rq05", "linguagens_distintas", "", len(contagem), total))

    razoes = [rq06_closed_issues_ratio.closed_issues_ratio(r) for r in repositories]
    com_issues = [r for r in repositories if rq06_closed_issues_ratio.has_issues(r)]
    razoes_com_issues = [rq06_closed_issues_ratio.closed_issues_ratio(r) for r in com_issues]
    linhas.append(
        SummaryRow("rq06", "mediana_razao_issues_fechadas", "", _mediana(razoes), total)
    )
    linhas.append(
        SummaryRow(
            "rq06",
            "mediana_razao_issues_fechadas_excluindo_sem_issues",
            "",
            _mediana(razoes_com_issues),
            len(com_issues),
        )
    )
    linhas.append(
        SummaryRow("rq06", "repositorios_sem_issues", "", total - len(com_issues), total)
    )

    return linhas
