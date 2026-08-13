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

Raciocínio completo em [hipoteses.md](hipoteses.md). As hipóteses foram registradas após
a coleta do Lab01S01 (100 repositórios) e antes da coleta de 1000 — a amostra maior é o
teste real de cada uma.

| RQ | Hipótese |
|---|---|
| RQ01 | **Sim.** Estrela é contador que só cresce, então acumular muitas exige tempo. Mediana bem acima de 5 anos, com cauda de projetos recentes de IA. |
| RQ02 | **Sim em volume, com assimetria forte.** O número reflete modelo de governança mais que popularidade: infraestrutura formal tem dezenas de milhares, listas curadas têm poucas. |
| RQ03 | **Não.** Boa parte dos mais estrelados não é software instalável (listas, roteiros de estudo) e nunca publica release. Mediana baixa e fração grande com zero. |
| RQ04 | **Sim, fortemente.** Popularidade atrai contribuição contínua. Mediana de poucos dias; deve ser a hipótese mais bem confirmada. |
| RQ05 | **Parcialmente.** Concordância no topo (TypeScript, Python, JavaScript), mas ordem diferente — o Octoverse conta contribuidores e este estudo conta estrelas. Fração relevante sem linguagem primária. |
| RQ06 | **Sim, mediana acima de 0,8.** Triagem ativa e fechamento por inatividade. Ressalva: PRs contam como issues e inflam a razão. |
| RQ07 | **Não.** A linguagem explica pouco; o tipo de projeto explica muito. Se houver efeito, deve aparecer em releases, não em PRs ou atualidade. |

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
