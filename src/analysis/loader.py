"""Leitura do CSV coletado para dentro do pandas.

Fronteira da camada de analise: daqui para baixo nao existe rede nem API do GitHub, so
o CSV. Isso permite que o integrante responsavel pelo Lab01S03 trabalhe com um dataset
parcial enquanto a coleta ainda esta sendo ajustada.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_repositories(path: Path | None = None) -> pd.DataFrame:
    """Le `data/processed/repositories.csv` com os tipos corretos.

    Converte colunas de data para datetime e as numericas para numero, para que uma
    mediana nunca seja calculada sobre texto.
    """
    raise NotImplementedError
