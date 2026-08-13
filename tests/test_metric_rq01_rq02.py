"""Validacao das metricas RQ01 (idade) e RQ02 (PRs aceitas).

Responsavel: integrante A.

Cobrir, no minimo:
  - RQ01: idade correta para uma data de criacao conhecida (usar `reference` fixo);
          repositorio criado hoje -> idade proxima de zero, nunca negativa.
  - RQ02: valor lido corresponde a `pullRequests(states: MERGED)`, nao ao total de PRs.
  - Ambas: amostra de 5 a 10 repositorios da fixture, conferida contra o GitHub
    (validacao exigida pelo Lab01S01).
"""
