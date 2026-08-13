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


def load_settings() -> Settings:
    """Le o `.env` (se existir) e as variaveis de ambiente.

    Levanta `MissingTokenError` quando `GITHUB_TOKEN` nao esta definido - falhar cedo
    e mais util do que receber 401 no meio de uma coleta de 1000 repositorios.
    """
    raise NotImplementedError


def load_dotenv(path: Path | None = None) -> None:
    """Carrega pares `CHAVE=valor` de um arquivo `.env` para `os.environ`.

    Implementacao propria e trivial (5 linhas) para evitar mais uma dependencia.
    Nao sobrescreve variaveis ja definidas no ambiente.
    """
    raise NotImplementedError


class MissingTokenError(RuntimeError):
    """`GITHUB_TOKEN` ausente ou vazio."""
