"""Validacao da traducao JSON -> dominio.

Cobrir, no minimo:
  - todos os campos da fixture chegam ao `Repository` com o tipo certo;
  - datas ISO-8601 com sufixo `Z` viram `datetime` com timezone;
  - `primaryLanguage: null` nao levanta excecao;
  - item de Project sem Issue associada (draft) vira `issue_number = None`;
  - cartao sem assignee vira tupla vazia, nunca `None`.
"""
