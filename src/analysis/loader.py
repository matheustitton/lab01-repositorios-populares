"""Leitura do CSV coletado para dentro do pandas.

Fronteira da camada de analise: daqui para baixo nao existe rede nem API do GitHub, so
o CSV. Isso permite que o integrante responsavel pelo Lab01S03 trabalhe com um dataset
parcial enquanto a coleta ainda esta sendo ajustada.

"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config.settings import REPOSITORIES_CSV

#: Colunas de data, convertidas para datetime UTC na leitura.
DATE_COLUMNS: tuple[str, ...] = ("created_at", "pushed_at")

#: Colunas numericas; forcar o tipo evita que uma mediana seja calculada sobre texto,
#: caso o CSV tenha sido reaberto e resalvo manualmente (ex.: no Excel).
NUMERIC_COLUMNS: tuple[str, ...] = (
    "stars",
    "closed_issues",
    "total_issues",
    "age_years",
    "age_days",
    "merged_pull_requests",
    "releases",
    "days_since_update",
    "closed_issues_ratio",
)


def load_repositories(path: Path | None = None) -> pd.DataFrame:
    """Le `data/processed/repositories.csv` com os tipos corretos.

    Converte colunas de data para datetime e as numericas para numero, para que uma
    mediana nunca seja calculada sobre texto.
    """
    csv_path = path or REPOSITORIES_CSV
    if not csv_path.exists():
        raise FileNotFoundError(
            f"{csv_path} nao encontrado. Rode a coleta e o processamento antes:\n"
            "  python -m src.cli.collect_repositories --limit 1000\n"
            "  python -m src.cli.process_data"
        )

    # utf-8-sig porque o csv_writer grava o BOM (para o arquivo abrir certo no Excel);
    # sem isso, o nome da primeira coluna viria com o caractere do BOM colado.
    frame = pd.read_csv(csv_path, encoding="utf-8-sig")

    for column in DATE_COLUMNS:
        if column in frame.columns:
            frame[column] = pd.to_datetime(frame[column], utc=True, errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    return frame
