"""Selecao da amostra de validacao e comparacao entre fontes (Issue #2).

Funcoes puras: nao acessam rede nem disco, o que permite testa-las com repositorios
montados a mao.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from src.domain.models import Repository

#: Cada criterio garante que a amostra cubra um caso onde o mapeamento pode falhar.
#: Amostra sorteada tende a pegar so repositorios "normais" e nao validar nada.
CRITERIOS: tuple[tuple[str, Callable[[Repository], bool]], ...] = (
    ("maior numero de estrelas", lambda r: True),
    ("sem linguagem primaria", lambda r: r.primary_language is None),
    ("sem nenhuma release", lambda r: r.releases == 0),
    ("sem nenhuma issue", lambda r: r.total_issues == 0),
    ("todas as issues fechadas", lambda r: r.total_issues > 0 and r.closed_issues == r.total_issues),
    ("mais pull requests aceitas", lambda r: r.merged_pull_requests > 0),
    ("mais releases", lambda r: r.releases > 0),
)


@dataclass(frozen=True)
class SampleEntry:
    """Um repositorio da amostra e o motivo pelo qual foi escolhido."""

    repository: Repository
    motivo: str


def select_sample(repositories: Iterable[Repository], size: int = 8) -> list[SampleEntry]:
    """Escolhe uma amostra deterministica que cobre os casos de borda.

    Deterministica de proposito: rodar de novo tem que produzir a mesma amostra, senao a
    evidencia colada na Issue nao pode ser reconferida depois.
    """
    repos = list(repositories)
    escolhidos: list[SampleEntry] = []
    usados: set[str] = set()

    ordenacoes: dict[str, Callable[[Repository], object]] = {
        "mais pull requests aceitas": lambda r: -r.merged_pull_requests,
        "mais releases": lambda r: -r.releases,
    }

    for motivo, criterio in CRITERIOS:
        if len(escolhidos) >= size:
            break
        candidatos = [r for r in repos if criterio(r) and r.name_with_owner not in usados]
        if not candidatos:
            continue
        chave = ordenacoes.get(motivo)
        escolhido = min(candidatos, key=chave) if chave else candidatos[0]
        escolhidos.append(SampleEntry(escolhido, motivo))
        usados.add(escolhido.name_with_owner)

    # Completa com os mais estrelados ainda de fora, para chegar ao tamanho pedido.
    for repo in repos:
        if len(escolhidos) >= size:
            break
        if repo.name_with_owner not in usados:
            escolhidos.append(SampleEntry(repo, "entre os mais estrelados"))
            usados.add(repo.name_with_owner)

    return escolhidos


#: Diferenca relativa aceita em contadores vivos antes de virar suspeita. Um erro de
#: mapeamento (campo trocado) erra por ordens de grandeza, nao por 0,001%.
TOLERANCIA_RELATIVA = 0.01

OK = "ok"
DERIVA = "deriva"
DIVERGENCIA = "divergencia"


@dataclass(frozen=True)
class FieldComparison:
    """Resultado da comparacao de um campo entre GraphQL e REST.

    Distingue **deriva temporal** de **divergencia**. A coleta e um retrato de um
    instante; a REST responde com o estado de agora. Estrelas sobem e pushes acontecem
    entre um e outro, e tratar isso como erro geraria alarme falso a cada execucao.
    Ja um campo imutavel que nao bate significa erro de verdade na query ou no mapeamento.
    """

    campo: str
    graphql: object
    rest: object
    volatil: bool = False

    @property
    def status(self) -> str:
        if self.graphql == self.rest:
            return OK
        if not self.volatil:
            return DIVERGENCIA
        return DERIVA if self._dentro_da_tolerancia() else DIVERGENCIA

    @property
    def confere(self) -> bool:
        """Verdadeiro quando nao ha erro - inclui deriva temporal esperada."""
        return self.status in (OK, DERIVA)

    @property
    def observacao(self) -> str:
        if self.status == OK:
            return "confere"
        if self.status == DERIVA:
            return f"deriva temporal ({self._delta()})"
        return "DIVERGENCIA"

    def _delta(self) -> str:
        if isinstance(self.graphql, int) and isinstance(self.rest, int):
            return f"{self.rest - self.graphql:+}"
        return f"{self.graphql} -> {self.rest}"

    def _dentro_da_tolerancia(self) -> bool:
        if isinstance(self.graphql, int) and isinstance(self.rest, int):
            if self.graphql <= 0:
                return False
            # Contador vivo que *cai* muito tambem e suspeito, nao so o que sobe demais.
            return abs(self.rest - self.graphql) / self.graphql <= TOLERANCIA_RELATIVA
        # Datas: avancar e normal (houve push novo); retroceder nao deveria acontecer.
        return str(self.rest) >= str(self.graphql)


def compare(repository: Repository, snapshot) -> list[FieldComparison]:
    """Compara os campos que as duas APIs entregam para o mesmo repositorio.

    `pushed_at` e comparado ate o minuto: os dois endpoints podem ser servidos por
    caches diferentes, e segundos de diferenca nao indicam erro nosso.
    """
    return [
        FieldComparison("stars", repository.stars, snapshot.stars, volatil=True),
        FieldComparison(
            "created_at",
            repository.created_at.isoformat(),
            snapshot.created_at.isoformat(),
        ),
        FieldComparison(
            "pushed_at",
            repository.pushed_at.strftime("%Y-%m-%d %H:%M"),
            snapshot.pushed_at.strftime("%Y-%m-%d %H:%M"),
            volatil=True,
        ),
        FieldComparison("primary_language", repository.primary_language, snapshot.primary_language),
    ]
