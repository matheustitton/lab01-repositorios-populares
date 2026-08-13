# Metodologia de coleta

## Amostra

Os 1.000 repositórios com maior número de estrelas do GitHub, obtidos via
`search(type: REPOSITORY, query: "stars:>1 sort:stars-desc")`.

> A busca do GitHub devolve no máximo 1.000 resultados por consulta, com até 100 por
> página. Os 1.000 repositórios cabem exatamente nesse teto.

## Ferramenta

Script próprio do grupo, escrito em Python, consumindo diretamente a GraphQL API v4.
Conforme a restrição do enunciado, **nenhuma biblioteca de terceiros que consulte a API
do GitHub foi utilizada** — as requisições usam apenas `urllib.request`, da biblioteca
padrão. `pandas` e `matplotlib` aparecem somente na etapa de análise, que lê o CSV já
coletado e não acessa a rede.

## Métricas extraídas

| RQ | Métrica | Campo GraphQL | Módulo |
|---|---|---|---|
| RQ01 | Idade em anos | `createdAt` | `src/domain/metrics/rq01_age.py` |
| RQ02 | PRs aceitas | `pullRequests(states: MERGED).totalCount` | `rq02_merged_pull_requests.py` |
| RQ03 | Total de releases | `releases.totalCount` | `rq03_releases.py` |
| RQ04 | Dias desde a última atualização | `pushedAt` | `rq04_days_since_update.py` |
| RQ05 | Linguagem primária | `primaryLanguage.name` | `rq05_primary_language.py` |
| RQ06 | Razão de issues fechadas | `issues(states: CLOSED)` / `issues` | `rq06_closed_issues_ratio.py` |

## Decisões metodológicas

- **`pushedAt` em vez de `updatedAt` (RQ04):** `updatedAt` muda com eventos que não são
  alteração de código (estrela recebida, edição de descrição), o que inflaria a atualidade
  aparente justamente dos repositórios mais populares.
- **PRs `MERGED`, não `CLOSED` (RQ02):** contribuição *aceita* é PR incorporada.
- **Mediana, não média:** as distribuições são fortemente assimétricas; poucos outliers
  dominariam a média.
- **Repositórios sem linguagem primária (RQ05):** rotulados como `Undefined`. São
  categoria própria (listas de links, material de estudo), não dado faltante.
- **Repositórios sem issues (RQ06):** razão 0.0, analisados à parte — "nenhuma issue" é
  diferente de "nenhuma issue resolvida".

## Reprodutibilidade

```bash
python -m src.cli.collect_repositories --limit 1000 --save-raw
```

As páginas brutas ficam em `data/raw/`, permitindo reprocessar o CSV sem nova coleta.

- **Data da coleta:** `<preencher>`
- **Total de repositórios obtidos:** `<preencher>`
- **Custo em rate limit:** `<preencher>`
