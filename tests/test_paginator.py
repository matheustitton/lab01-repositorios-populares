"""Validacao da paginacao por cursor, usando `FakeGraphQLClient` (sem rede).

Cobrir, no minimo:
  - o cursor da pagina anterior e enviado como variavel na chamada seguinte;
  - a iteracao para quando `hasNextPage` e falso, mesmo sem atingir o limite;
  - a iteracao para exatamente em `limit` nos, sem pedir pagina desnecessaria;
  - o gancho `on_page` e chamado uma vez por pagina.
"""
