"""Cache das respostas cruas em `data/raw/`.

Uma coleta de 1000 repositorios leva varios minutos e pode falhar no meio. Guardar cada
pagina crua permite reprocessar o CSV (corrigir uma metrica, por exemplo) sem gastar
rate limit de novo, e deixa o dado original disponivel para auditoria da metodologia.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any


def save_page(directory: Path, index: int, payload: dict[str, Any]) -> Path:
    """Grava uma pagina crua como `page_<index:03d>.json`."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"page_{index:03d}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_pages(directory: Path) -> Iterator[dict[str, Any]]:
    """Le as paginas cruas em ordem, para reprocessamento offline."""
    for path in sorted(directory.glob("page_*.json")):
        yield json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> Path:
    """Grava um JSON consolidado, criando os diretorios necessarios."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_repository_nodes(path: Path, nodes: Iterable[dict[str, Any]]) -> int:
    """Grava os nos crus dos repositorios e devolve quantos foram gravados.

    Formato pedido pela Issue #1: lista de repositorios, na ordem da coleta (estrelas
    decrescentes), com os campos originais da API preservados.
    """
    materialized = list(nodes)
    save_json(path, materialized)
    return len(materialized)
