# Fontes de referência

## Linguagens mais populares (RQ05 e RQ07)

O enunciado exige definir e referenciar explicitamente uma fonte para "linguagens mais
populares", mantendo **a mesma referência ao longo de todo o laboratório**.

- **Fonte escolhida:** GitHub Octoverse
- **Link:** https://octoverse.github.com/
- **Edição/ano:** `<preencher>`
- **Data de consulta:** `<preencher — AAAA-MM-DD>`
- **Ranking utilizado (em ordem):** `<preencher>`

A lista está codificada em [`src/analysis/popular_languages.py`](../src/analysis/popular_languages.py)
e é a única usada tanto na RQ05 quanto na RQ07 — nenhuma outra parte do código mantém
lista paralela de linguagens.

**Por que Octoverse:** o estudo analisa repositórios do próprio GitHub, então um ranking
derivado da atividade no GitHub é mais coerente com a amostra do que o TIOBE, que mede
volume de buscas na web.

## Dados coletados

- **API:** GitHub GraphQL API v4 — https://docs.github.com/en/graphql
- **Consulta:** `search(type: REPOSITORY, query: "stars:>1 sort:stars-desc")`
- **Data da coleta:** `<preencher>`
- **Total de repositórios:** `<preencher>`
