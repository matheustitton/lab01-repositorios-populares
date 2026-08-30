"""Escrita de CSV com o modulo `csv` da biblioteca padrao.

Recebe cabecalho e linhas ja prontas - nao conhece `Repository` nem `ProjectItem`.
Sempre grava em UTF-8 com BOM e `newline=""`, para o arquivo abrir corretamente no Excel
em portugues sem quebrar acentos nem duplicar linhas em branco no Windows.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from pathlib import Path


def write_csv(
    path: Path,
    header: Sequence[str],
    rows: Iterable[Sequence[object]],
) -> int:
    """Grava o CSV, criando os diretorios necessarios. Devolve o numero de linhas."""
    path.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    # utf-8-sig escreve o BOM que o Excel usa para detectar UTF-8; newline="" evita a
    # linha em branco extra que o Windows insere entre registros.
    with path.open("w", encoding="utf-8-sig", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
            total += 1
    return total
