"""Validacao das metricas RQ03 (releases) e RQ04 (dias desde a ultima atualizacao).

Responsavel: integrante B.

Cobrir, no minimo:
  - RQ03: repositorio sem nenhuma release -> 0, e nao erro nem valor ausente.
  - RQ04: calculo a partir de `pushed_at` com `reference` fixo; resultado nunca negativo.
  - RQ04: repositorio com push de hoje -> proximo de zero.
  - Ambas: amostra de 5 a 10 repositorios da fixture, conferida contra o GitHub.
"""
