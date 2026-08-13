# Relatório Final — Características de repositórios populares

**Disciplina:** Laboratório de Experimentação de Software
**Professor:** Danilo Maia
**Integrantes:** `<preencher>`
**Repositório:** `<preencher>`
**GitHub Projects:** `<preencher>`

---

## 1. Introdução

`<contexto do estudo e o que se pretende responder>`

### Hipóteses informais

Detalhadas em [hipoteses.md](hipoteses.md).

| RQ | Hipótese |
|---|---|
| RQ01 | `<preencher>` |
| RQ02 | `<preencher>` |
| RQ03 | `<preencher>` |
| RQ04 | `<preencher>` |
| RQ05 | `<preencher>` |
| RQ06 | `<preencher>` |
| RQ07 | `<preencher>` |

## 2. Metodologia

Resumo — detalhamento em [metodologia.md](metodologia.md).

## 3. Resultados

### RQ01 — Sistemas populares são maduros/antigos?
**Métrica:** idade do repositório (anos) · **Mediana:** `<preencher>`

### RQ02 — Sistemas populares recebem muita contribuição externa?
**Métrica:** total de pull requests aceitas · **Mediana:** `<preencher>`

### RQ03 — Sistemas populares lançam releases com frequência?
**Métrica:** total de releases · **Mediana:** `<preencher>`

### RQ04 — Sistemas populares são atualizados com frequência?
**Métrica:** dias desde a última atualização · **Mediana:** `<preencher>`

### RQ05 — Sistemas populares são escritos nas linguagens mais populares?
**Métrica:** linguagem primária · **Contagem por linguagem:** `<preencher>`
Fonte de referência de popularidade: ver [fontes.md](fontes.md).

### RQ06 — Sistemas populares possuem alto percentual de issues fechadas?
**Métrica:** razão issues fechadas / total · **Mediana:** `<preencher>`

### RQ07 — Linguagens populares recebem mais contribuição, releases e atualizações?
**RQ02, RQ03 e RQ04 desdobradas por linguagem:** `<preencher tabela>`

## 4. Discussão — hipótese vs. resultado

| RQ | Hipótese | Resultado | Confirmada? | Interpretação |
|---|---|---|---|---|
| RQ01 | | | | |
| RQ02 | | | | |
| RQ03 | | | | |
| RQ04 | | | | |
| RQ05 | | | | |
| RQ06 | | | | |
| RQ07 | | | | |

## 5. Configuração do processo

Estrutura do GitHub Projects, colunas e política de WIP: ver [processo.md](processo.md).

- **Colunas:** Backlog → Sprint Backlog → Doing → Review → Done
- **Limite de WIP em Doing:** 3 (um por integrante) — justificativa em [processo.md](processo.md)
- **Print do board:** `<inserir docs/assets/board-lab01.png>`

## 6. Ameaças à validade

**Confirmadas na validação da amostra** (ver [validacao_amostra.md](validacao_amostra.md)):

- **Teto de 1000 no `totalCount` de releases (RQ03).** A GraphQL para de contar em 1000:
  `ggml-org/llama.cpp` reporta 1000 tendo 6844. Afeta 4% da coleta de 100. A mediana da
  RQ03 permanece válida, mas média, máximo e cauda superior não. Os demais campos foram
  verificados e não têm teto.
- **Corte temporal único.** O dataset é um retrato do instante da coleta. Estrelas e
  `pushedAt` mudam continuamente — a validação mediu deriva de poucas unidades por hora
  nos repositórios mais populares.

**Limitações de desenho:**

- **Teto de 1000 resultados da busca.** A amostra é exatamente o limite que uma consulta
  `search` devolve; ir além exigiria fatiar por faixa de estrelas.
- **Estrelas como proxy de popularidade.** Estrela mede visibilidade e favoritismo, não
  uso em produção nem qualidade.
- **`totalCount` de issues inclui pull requests.** No GitHub, todo PR também é uma issue,
  o que infla o denominador da RQ06 em repositórios com muitos PRs.
- **Repositórios sem issues na RQ06.** 11% da coleta não tem nenhuma issue; incluí-los com
  razão 0.0 puxaria a mediana para baixo sem significar baixa taxa de resolução.
- **`releases` conta apenas releases publicadas**, não tags. Projetos que versionam só por
  tag aparecem com 0 — 41% da coleta está nessa situação.
