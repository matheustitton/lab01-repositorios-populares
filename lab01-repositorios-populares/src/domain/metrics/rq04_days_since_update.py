"""RQ04 - Sistemas populares sao atualizados com frequencia?

Metrica: tempo (em dias) desde a ultima atualizacao.

Usa `pushed_at` e nao `updated_at`: `updated_at` muda com eventos que nao sao alteracao
de codigo (estrela recebida, edicao da descricao), o que inflaria a atualidade aparente
dos repositorios mais populares - justamente a amostra deste estudo.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.domain.models import Repository

RQ = "rq04"
COLUMN = "days_since_update"


def days_since_update(repository: Repository, reference: datetime | None = None) -> float:
    """Dias decorridos desde o ultimo push ate `reference` (default: agora, em UTC)."""
    delta = (reference or datetime.now(timezone.utc)) - repository.pushed_at
    return round(delta.total_seconds() / 86400, 2)
