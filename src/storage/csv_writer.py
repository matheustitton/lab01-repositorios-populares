"""Escrita de CSV com o modulo `csv` da biblioteca padrao.

Recebe cabecalho e linhas ja prontas - nao conhece `Repository` nem `ProjectItem`.
Sempre grava em UTF-8 com BOM e `newline=""`, para o arquivo abrir corretamente no Excel
em portugues sem quebrar acentos nem duplicar linhas em branco no Windows.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path


def write_csv(
    path: Path,
    header: Sequence[str],
    rows: Iterable[Sequence[object]],
) -> int:
    """Grava o CSV, criando os diretorios necessarios. Devolve o numero de linhas."""
    raise NotImplementedError
