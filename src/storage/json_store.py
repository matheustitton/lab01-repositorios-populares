"""Cache das respostas cruas em `data/raw/`.

Uma coleta de 1000 repositorios leva varios minutos e pode falhar no meio. Guardar cada
pagina crua permite reprocessar o CSV (corrigir uma metrica, por exemplo) sem gastar
rate limit de novo, e deixa o dado original disponivel para auditoria da metodologia.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any


def save_page(directory: Path, index: int, payload: dict[str, Any]) -> Path:
    """Grava uma pagina crua como `page_<index:03d>.json`."""
    raise NotImplementedError


def load_pages(directory: Path) -> Iterator[dict[str, Any]]:
    """Le as paginas cruas em ordem, para reprocessamento offline."""
    raise NotImplementedError
