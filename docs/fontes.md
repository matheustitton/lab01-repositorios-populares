# Fontes de referência

## Linguagens mais populares (RQ05 e RQ07)

O enunciado exige definir e referenciar explicitamente uma fonte para as "linguagens mais
populares", mantendo **a mesma referência ao longo de todo o laboratório**.

- **Fonte escolhida:** GitHub Octoverse
- **Edição:** Octoverse 2025
- **Período dos dados:** 1 de setembro de 2024 a 31 de agosto de 2025
- **Link:** https://octoverse.github.com/
- **Anúncio com o ranking:** https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- **Data de consulta:** 2026-08-13

### Ranking utilizado

| # | Linguagem |
|---|---|
| 1 | TypeScript |
| 2 | Python |
| 3 | JavaScript |
| 4 | Java |
| 5 | C# |
| 6 | PHP |
| 7 | Shell |
| 8 | C++ |
| 9 | HCL |
| 10 | Go |

A lista está codificada em [`src/analysis/popular_languages.py`](../src/analysis/popular_languages.py)
e é a única usada tanto na RQ05 quanto na RQ07 — nenhuma outra parte do código mantém
lista paralela de linguagens.

### Por que Octoverse

O ranqueamento do TIOBE, um dos mais usados para essas pesquisas, mede volume de buscas na web.
Porém, nos parece mais adequado um ranqueamento que leve em consideração o volume de atividades
dentro do github.

### Ressalva importante

**O Octoverse ordena por número de contribuidores; este estudo ordena por estrelas.** São
medidas diferentes de "popularidade": contribuidores medem quem *escreve* código,
estrelas medem quem *marca* o projeto. Uma linguagem pode liderar o Octoverse por ser
usada em muitos projetos corporativos pequenos e ainda assim aparecer pouco entre os
repositórios mais estrelados, e vice-versa. A RQ05 compara justamente essas duas ordenações e essa divergência é um dos diferenciais do nosso requisito 5.

Em um segundo limite o ranking cobre apenas linguagens: Repositórios sem linguagem primária
(listas curadas, materiais de estudo) não têm posição possível nele e são tratados como
categoria `Undefined` à parte.

## Dados coletados

- **API:** GitHub GraphQL API v4 — https://docs.github.com/en/graphql
- **Consulta:** `search(type: REPOSITORY, query: "stars:>1 sort:stars-desc")`
- **Data da coleta (Lab01S01):** 2026-08-13
- **Total de repositórios:** 100 (Lab01S01); 1000 previsto para o Lab01S02
