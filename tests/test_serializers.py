"""Validacao da serializacao para CSV.

Cobrir, no minimo:
  - `repository_header()` traz `BASE_COLUMNS` seguidas das colunas do registro;
  - a linha gerada tem exatamente o mesmo comprimento do cabecalho;
  - registrar uma metrica nova acrescenta coluna no cabecalho e valor na linha;
  - listas (assignees, labels) viram texto separado por `;`.
"""
