"""Validacao da selecao de amostra e da comparacao entre fontes (Issue #2)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from src.domain.models import Repository
from src.domain.sampling import DERIVA, DIVERGENCIA, OK, compare, select_sample


def repo(nome, *, stars=1000, lang="Python", prs=10, releases=5, fechadas=5, total=10):
    return Repository(
        name_with_owner=nome,
        url=f"https://github.com/{nome}",
        stars=stars,
        created_at=datetime(2015, 1, 1, tzinfo=timezone.utc),
        pushed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        primary_language=lang,
        merged_pull_requests=prs,
        releases=releases,
        closed_issues=fechadas,
        total_issues=total,
    )


@dataclass(frozen=True)
class FakeSnapshot:
    stars: int
    created_at: datetime
    pushed_at: datetime
    primary_language: str | None


def test_amostra_cobre_os_casos_de_borda():
    repos = [
        repo("org/normal", stars=9000),
        repo("org/sem-linguagem", stars=8000, lang=None),
        repo("org/sem-release", stars=7000, releases=0),
        repo("org/sem-issue", stars=6000, fechadas=0, total=0),
        repo("org/tudo-fechado", stars=5000, fechadas=40, total=40),
        repo("org/muitos-prs", stars=4000, prs=99999),
        repo("org/muitas-releases", stars=3000, releases=888),
    ]

    motivos = {e.repository.name_with_owner: e.motivo for e in select_sample(repos, size=8)}

    assert motivos["org/sem-linguagem"] == "sem linguagem primaria"
    assert motivos["org/sem-release"] == "sem nenhuma release"
    assert motivos["org/sem-issue"] == "sem nenhuma issue"
    assert motivos["org/muitos-prs"] == "mais pull requests aceitas"
    assert motivos["org/muitas-releases"] == "mais releases"


def test_amostra_nao_repete_repositorio():
    repos = [repo(f"org/r{i}", stars=1000 - i) for i in range(20)]

    amostra = select_sample(repos, size=8)
    nomes = [e.repository.name_with_owner for e in amostra]

    assert len(nomes) == len(set(nomes))
    assert len(amostra) == 8


def test_amostra_e_deterministica():
    repos = [repo(f"org/r{i}", stars=1000 - i, releases=i) for i in range(20)]

    primeira = [e.repository.name_with_owner for e in select_sample(repos, 8)]
    segunda = [e.repository.name_with_owner for e in select_sample(repos, 8)]

    assert primeira == segunda


def test_amostra_menor_que_o_pedido_quando_faltam_repositorios():
    amostra = select_sample([repo("org/unico")], size=8)

    assert len(amostra) == 1


def _snapshot(r: Repository, **overrides):
    campos = {
        "stars": r.stars,
        "created_at": r.created_at,
        "pushed_at": r.pushed_at,
        "primary_language": r.primary_language,
    }
    return FakeSnapshot(**{**campos, **overrides})


def test_campos_identicos_conferem():
    r = repo("org/x")

    assert all(c.status == OK for c in compare(r, _snapshot(r)))


def test_estrelas_a_mais_sao_deriva_temporal_e_nao_erro():
    """A coleta e um retrato; a REST le o estado de agora."""
    r = repo("org/x", stars=100_000)

    stars = compare(r, _snapshot(r, stars=100_008))[0]

    assert stars.status == DERIVA
    assert stars.confere
    assert "+8" in stars.observacao


def test_estrelas_muito_diferentes_sao_divergencia():
    r = repo("org/x", stars=100_000)

    stars = compare(r, _snapshot(r, stars=42))[0]

    assert stars.status == DIVERGENCIA
    assert not stars.confere


def test_push_mais_recente_e_deriva_mas_retroceder_e_divergencia():
    r = repo("org/x")

    frente = compare(r, _snapshot(r, pushed_at=datetime(2026, 6, 1, tzinfo=timezone.utc)))[2]
    tras = compare(r, _snapshot(r, pushed_at=datetime(2020, 1, 1, tzinfo=timezone.utc)))[2]

    assert frente.status == DERIVA
    assert tras.status == DIVERGENCIA


def test_campo_estavel_diferente_e_sempre_divergencia():
    """created_at e primary_language nao mudam - diferenca ali e erro nosso."""
    r = repo("org/x", lang="Python")

    criado = compare(r, _snapshot(r, created_at=datetime(2001, 1, 1, tzinfo=timezone.utc)))[1]
    lingua = compare(r, _snapshot(r, primary_language="Rust"))[3]

    assert criado.status == DIVERGENCIA
    assert lingua.status == DIVERGENCIA
