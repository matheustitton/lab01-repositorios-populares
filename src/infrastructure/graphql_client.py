"""Cliente GraphQL generico da API do GitHub.

Sabe falar GraphQL - nao sabe o que e um "repositorio" nem um "item de Project".
E justamente esse desacoplamento que permite a Parte 2 (snapshot do GitHub Projects)
reaproveitar integralmente o codigo de consulta escrito para a Parte 1.
"""

from __future__ import annotations

from typing import Any

from src.infrastructure.http_client import post_json
from src.infrastructure.retry import with_retry

RATE_LIMIT_QUERY = """
query RateLimit {
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""


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

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "lab01-repositorios-populares",
        }

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Executa a query e devolve o conteudo de `data`.

        Levanta `GraphQLError` se a resposta trouxer `errors`, e `HttpError` para falhas
        de transporte que sobreviveram ao retry.
        """
        payload = {"query": query, "variables": variables or {}}

        response = with_retry(
            lambda: post_json(self._url, payload, self._headers, self._timeout)
        )

        body = response.body
        # A API responde 200 com `errors` para query invalida, campo inexistente ou
        # permissao faltando - por isso nao basta olhar o status HTTP.
        if body.get("errors"):
            raise GraphQLError(body["errors"])

        data = body.get("data")
        if data is None:
            raise GraphQLError([{"message": "resposta sem o campo 'data'"}])
        return data

    def rate_limit(self) -> dict[str, Any]:
        """Consulta `rateLimit` - util para logar custo/saldo durante a coleta longa."""
        return self.execute(RATE_LIMIT_QUERY)["rateLimit"]
