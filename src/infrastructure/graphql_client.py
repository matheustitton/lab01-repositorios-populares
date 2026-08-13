"""Cliente GraphQL generico da API do GitHub.

Sabe falar GraphQL - nao sabe o que e um "repositorio" nem um "item de Project".
E justamente esse desacoplamento que permite a Parte 2 (snapshot do GitHub Projects)
reaproveitar integralmente o codigo de consulta escrito para a Parte 1.
"""

from __future__ import annotations

from typing import Any


class GraphQLError(RuntimeError):
    """A resposta veio com status 200 mas com o campo `errors` preenchido."""

    def __init__(self, errors: list[dict[str, Any]]) -> None:
        super().__init__("; ".join(e.get("message", "erro desconhecido") for e in errors))
        self.errors = errors


class GraphQLClient:
    """Executa queries GraphQL autenticadas, com retry e cabecalhos corretos."""

    def __init__(self, url: str, token: str, timeout: int) -> None:
        self._url = url
        self._token = token
        self._timeout = timeout

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Executa a query e devolve o conteudo de `data`.

        Levanta `GraphQLError` se a resposta trouxer `errors`, e `HttpError` para falhas
        de transporte que sobreviveram ao retry.
        """
        raise NotImplementedError

    def rate_limit(self) -> dict[str, Any]:
        """Consulta `rateLimit` - util para logar custo/saldo durante a coleta longa."""
        raise NotImplementedError
