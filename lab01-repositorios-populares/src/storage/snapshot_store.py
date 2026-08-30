"""Acumulacao dos snapshots do board em um unico CSV.

O enunciado pede uma serie acumulada, sprint a sprint: como a API do Projects nao expoe
o historico de mudanca de coluna, essa serie e a unica base de dados dos Labs 04 e 05.

Dai a regra central deste modulo: rodar o snapshot duas vezes na mesma sprint **substitui**
as linhas daquela sprint em vez de duplicar. Sem isso, uma reexecucao corriqueira
(corrigir um cartao e exportar de novo) contaminaria a serie historica com registros
repetidos, e o dado dos labs seguintes viria errado.
"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path

SPRINT_COLUMN = "sprint"


def read_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    """Le um CSV existente. Devolve `([], [])` quando o arquivo ainda nao existe."""
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = list(csv.reader(arquivo))
    if not leitor:
        return [], []
    return leitor[0], leitor[1:]


def merge_snapshot(
    path: Path,
    header: Sequence[str],
    sprint: str,
    rows: Sequence[Sequence[object]],
) -> tuple[int, int]:
    """Grava `rows` no CSV acumulado, substituindo as linhas da mesma sprint.

    Devolve `(substituidas, total_no_arquivo)`.

    Levanta `ValueError` se o cabecalho do arquivo existente for diferente do informado:
    concatenar colunas divergentes silenciosamente produziria uma serie historica
    inutilizavel, e e melhor falhar alto.
    """
    cabecalho_existente, linhas_existentes = read_rows(path)

    if cabecalho_existente and list(cabecalho_existente) != list(header):
        raise ValueError(
            f"cabecalho de {path.name} difere do esperado.\n"
            f"  no arquivo: {cabecalho_existente}\n"
            f"  esperado  : {list(header)}"
        )

    indice_sprint = list(header).index(SPRINT_COLUMN)

    # As linhas novas tem que pertencer a sprint que esta sendo gravada. Sem esta
    # checagem, um chamador distraido apagaria as linhas de uma sprint e gravaria no
    # lugar as de outra - e o estrago so apareceria no Lab 04, sem como reconstruir.
    divergentes = {
        str(linha[indice_sprint]) for linha in rows if str(linha[indice_sprint]) != sprint
    }
    if divergentes:
        raise ValueError(
            f"linhas de sprint divergente para gravacao em {sprint!r}: {sorted(divergentes)}"
        )

    preservadas = [
        linha for linha in linhas_existentes if linha[indice_sprint] != sprint
    ]
    substituidas = len(linhas_existentes) - len(preservadas)

    # Novas linhas por ultimo: a serie fica em ordem cronologica de exportacao.
    finais = preservadas + [list(linha) for linha in rows]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(header)
        escritor.writerows(finais)

    return substituidas, len(finais)
