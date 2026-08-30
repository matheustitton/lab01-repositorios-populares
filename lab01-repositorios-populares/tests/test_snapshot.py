"""Validacao da coleta do board e da acumulacao dos snapshots (Issue #6)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.collection.project_collector import (
    ProjectNotFoundError,
    collect_project_items,
    extract_project_page,
)
from src.storage.serializers import PROJECT_COLUMNS, project_item_row
from src.storage.snapshot_store import merge_snapshot, read_rows
from tests.conftest import FakeGraphQLClient

CAPTURA = datetime(2026, 8, 13, 21, 0, tzinfo=timezone.utc)


def _item(numero, titulo, status, state="OPEN", assignees=("pedroMontandon",)):
    return {
        "id": f"item{numero}",
        "type": "ISSUE",
        "fieldValueByName": {"name": status},
        "content": {
            "number": numero,
            "title": titulo,
            "state": state,
            "url": f"https://github.com/org/repo/issues/{numero}",
            "createdAt": "2026-08-11T23:48:04Z",
            "closedAt": "2026-08-13T14:54:17Z" if state == "CLOSED" else None,
            "assignees": {"nodes": [{"login": a} for a in assignees]},
            "labels": {"nodes": []},
        },
    }


def _resposta(nodes, has_next=False, cursor=None):
    return {
        "user": {
            "projectV2": {
                "items": {
                    "nodes": nodes,
                    "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
                }
            }
        }
    }


def test_extract_localiza_nodes_e_pageinfo():
    page = extract_project_page(_resposta([_item(1, "a", "Done")], has_next=True, cursor="c1"))

    assert len(page.nodes) == 1
    assert page.has_next_page is True
    assert page.end_cursor == "c1"


def test_project_invisivel_levanta_erro_explicativo():
    """Project privado sem acesso vem nulo, igual a um que nao existe."""
    with pytest.raises(ProjectNotFoundError, match="read:project"):
        extract_project_page({"user": {"projectV2": None}})


def test_usuario_inexistente_levanta_erro():
    with pytest.raises(ProjectNotFoundError):
        extract_project_page({"user": None})


def test_coleta_mapeia_cartoes_com_sprint_e_captura():
    client = FakeGraphQLClient([_resposta([_item(1, "Coleta", "Done", "CLOSED")])])

    itens = list(collect_project_items(client, "org", 2, "lab01s01", CAPTURA))

    assert len(itens) == 1
    assert itens[0].issue_number == 1
    assert itens[0].status == "Done"
    assert itens[0].state == "CLOSED"
    assert itens[0].sprint == "lab01s01"
    assert itens[0].captured_at == CAPTURA
    assert itens[0].assignees == ("pedroMontandon",)


def test_cartao_sem_assignee_vira_tupla_vazia():
    client = FakeGraphQLClient([_resposta([_item(1, "x", "Doing", assignees=())])])

    itens = list(collect_project_items(client, "org", 2, "lab01s01", CAPTURA))

    assert itens[0].assignees == ()


def test_reexecutar_na_mesma_sprint_substitui_em_vez_de_duplicar(tmp_path):
    """Regra central: a serie acumulada e a base dos Labs 04 e 05."""
    destino = tmp_path / "snapshots_board.csv"
    linhas = [project_item_row(_criar_item("Done"))]

    merge_snapshot(destino, PROJECT_COLUMNS, "lab01s01", linhas)
    substituidas, total = merge_snapshot(destino, PROJECT_COLUMNS, "lab01s01", linhas)

    assert substituidas == 1
    assert total == 1


def test_sprint_nova_acumula_sem_apagar_a_anterior(tmp_path):
    destino = tmp_path / "snapshots_board.csv"

    merge_snapshot(
        destino, PROJECT_COLUMNS, "lab01s01", [project_item_row(_criar_item("Doing"))]
    )
    substituidas, total = merge_snapshot(
        destino,
        PROJECT_COLUMNS,
        "lab01s02",
        [project_item_row(_criar_item("Done", sprint="lab01s02"))],
    )

    assert substituidas == 0
    assert total == 2

    _, gravadas = read_rows(destino)
    assert [linha[0] for linha in gravadas] == ["lab01s01", "lab01s02"]


def test_linhas_de_sprint_divergente_sao_recusadas(tmp_path):
    """Evita apagar as linhas de uma sprint e gravar no lugar as de outra."""
    destino = tmp_path / "snapshots_board.csv"
    linhas = [project_item_row(_criar_item("Done", sprint="lab01s01"))]

    with pytest.raises(ValueError, match="sprint divergente"):
        merge_snapshot(destino, PROJECT_COLUMNS, "lab01s02", linhas)


def test_cabecalho_divergente_falha_alto(tmp_path):
    """Concatenar colunas diferentes produziria serie historica inutilizavel."""
    destino = tmp_path / "snapshots_board.csv"
    merge_snapshot(destino, ("sprint", "outra"), "lab01s01", [["lab01s01", "x"]])

    with pytest.raises(ValueError, match="cabecalho"):
        merge_snapshot(destino, PROJECT_COLUMNS, "lab01s02", [])


def test_arquivo_inexistente_comeca_vazio(tmp_path):
    header, linhas = read_rows(tmp_path / "nao_existe.csv")

    assert header == []
    assert linhas == []


def _criar_item(status, sprint="lab01s01"):
    from src.collection.mappers import to_project_item

    return to_project_item(_item(1, "Titulo", status), sprint, CAPTURA)
