"""Configuracao central do laboratorio.

Unico ponto do projeto que le variaveis de ambiente e conhece caminhos de disco.
Todo o restante do codigo recebe a configuracao por parametro, nunca le `os.environ`
diretamente - isso mantem as demais camadas testaveis sem mexer no ambiente.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
QUERIES_DIR = PROJECT_ROOT / "src" / "queries"
ASSETS_DIR = PROJECT_ROOT / "docs" / "assets"

REPOSITORIES_CSV = PROCESSED_DIR / "repositories.csv"

#: Saida consolidada da coleta do Lab01S01, no caminho pedido pela Issue #1.
RAW_REPOS_JSON = DATA_DIR / "raw_repos_lab01s01.json"

#: Saidas do processamento do Lab01S01, nos caminhos pedidos pela Issue #3.
REPOS_CSV = DATA_DIR / "repos_lab01s01.csv"
RESUMO_CSV = DATA_DIR / "resumo_lab01s01.csv"

DEFAULT_GRAPHQL_URL = "https://api.github.com/graphql"

#: 10 e o maior valor que se mostrou estavel na pratica. Com 25, a API respondeu 502 de
#: forma deterministica ao chegar nos repositorios de rank ~76-100: cada repositorio pede
#: quatro `totalCount` agregados, e o custo por requisicao estoura o tempo de resposta.
DEFAULT_PAGE_SIZE = 10
DEFAULT_TARGET_COUNT = 1000
DEFAULT_REQUEST_TIMEOUT = 60


@dataclass(frozen=True)
class Settings:
    """Parametros de execucao resolvidos a partir do ambiente."""

    github_token: str
    graphql_url: str
    page_size: int
    target_count: int
    request_timeout: int
    project_owner: str | None
    project_number: int | None


class MissingTokenError(RuntimeError):
    """`GITHUB_TOKEN` ausente ou vazio."""


def load_dotenv(path: Path | None = None) -> None:
    """Carrega pares `CHAVE=valor` de um arquivo `.env` para `os.environ`.

    Implementacao propria e trivial para evitar mais uma dependencia. Ignora linhas
    vazias e comentarios, e **nao sobrescreve** variaveis ja definidas no ambiente -
    quem exporta a variavel no terminal manda mais do que o arquivo.
    """
    env_path = path or (PROJECT_ROOT / ".env")
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    return int(raw) if raw else default


def load_settings() -> Settings:
    """Le o `.env` (se existir) e as variaveis de ambiente.

    Levanta `MissingTokenError` quando `GITHUB_TOKEN` nao esta definido - falhar cedo
    e mais util do que receber 401 no meio de uma coleta de 1000 repositorios.
    """
    load_dotenv()

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        raise MissingTokenError(
            "GITHUB_TOKEN nao definido. Copie .env.example para .env e preencha o token."
        )

    project_number = os.environ.get("PROJECT_NUMBER", "").strip()

    return Settings(
        github_token=token,
        graphql_url=os.environ.get("GITHUB_GRAPHQL_URL", "").strip() or DEFAULT_GRAPHQL_URL,
        page_size=_int_env("PAGE_SIZE", DEFAULT_PAGE_SIZE),
        target_count=_int_env("TARGET_COUNT", DEFAULT_TARGET_COUNT),
        request_timeout=_int_env("REQUEST_TIMEOUT", DEFAULT_REQUEST_TIMEOUT),
        project_owner=os.environ.get("PROJECT_OWNER", "").strip() or None,
        project_number=int(project_number) if project_number else None,
    )
