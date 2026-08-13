"""Validacao das metricas RQ05 (linguagem primaria) e RQ06 (razao de issues fechadas).

Responsavel: integrante C.

Cobrir, no minimo:
  - RQ05: `primaryLanguage` nulo vira o rotulo "Undefined", nao string vazia.
  - RQ06: razao correta em caso comum; resultado sempre dentro de [0, 1].
  - RQ06: repositorio com zero issues -> 0.0, sem divisao por zero.
  - Ambas: amostra de 5 a 10 repositorios da fixture, conferida contra o GitHub.
"""
