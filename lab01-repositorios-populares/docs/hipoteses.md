# Hipóteses informais

Expectativas do grupo sobre cada questão de pesquisa, com o raciocínio subjacente que as sustenta.

## Nota de procedimento

Estas hipóteses foram registradas **depois** da coleta do Lab01S01 (100 repositórios) e
**antes** da coleta completa do Lab01S02 (1000 repositórios). Não são, portanto,
previsões cegas: o grupo já tinha visto os números da amostra menor quando as escreveu.

Registrar isso importa porque muda o que a confirmação de uma hipótese significa. O teste
real é a coleta de 1000 repositórios: se o comportamento observado em 100 se mantiver em
uma amostra dez vezes maior, a hipótese ganha força. Se não se mantiver, o que os 100
mostraram era particularidade do topo da lista, não padrão.

---

## RQ01 — Sistemas populares são maduros/antigos?

**Métrica:** idade do repositório, a partir de `createdAt`.

**Hipótese: sim, com mediana bem acima de cinco anos.**

Estrela é um contador que só cresce: dificilmente um usuário retira estrelas de um projeto,
o que reduz a probabilidade de um efeito manada de redução do número de estrelas. 
Acumular centenas de milhares de estrelas exige tempo de exposição, então a
amostra dos mais estrelados deve ser enviesada em favor de projetos antigos por
construção da própria métrica de popularidade.

A força contrária é o ciclo recente de IA: projetos surgidos nos últimos dois anos
acumularam estrelas em velocidade sem precedente. Esperamos que isso apareça como uma
cauda de repositórios novos, sem deslocar a mediana.

## RQ02 — Sistemas populares recebem muita contribuição externa?

**Métrica:** total de pull requests aceitas (`MERGED`).

**Hipótese: sim em volume absoluto, mas com distribuição muito assimétrica.**

Esperamos mediana na casa do milhar, com dispersão enorme. A intuição é que o número de
PRs aceitas mede menos "popularidade" e mais **modelo de governança**: projetos de
infraestrutura com processo formal de contribuição (compiladores, runtimes, frameworks)
devem ter dezenas de milhares, enquanto listas curadas e materiais de estudo recebem
contribuições pequenas e pontuais.

Se isso valer, a média será várias vezes a mediana. Motivo pelo qual o enunciado pede
mediana.

## RQ03 — Sistemas populares lançam releases com frequência?

**Métrica:** total de releases.

**Hipótese: não. Esperamos mediana baixa e uma fração grande com zero releases.**

É a hipótese em que mais esperamos contrariar o senso comum. Boa parte dos repositórios
mais estrelados **não é software instalável**: são listas de links, roteiros de estudo,
coletâneas de exercícios. Esses projetos não têm o que versionar e nunca publicam
release.

Soma-se a isso que muitos projetos que *são* software versionam apenas por tag Git, sem criar a
release no GitHub. Portanto, a métrica conta releases publicadas, não tags.

## RQ04 — Sistemas populares são atualizados com frequência?

**Métrica:** tempo até a última atualização (`pushedAt`).

**Hipótese: sim, fortemente — mediana de poucos dias.**

Popularidade atrai contribuição, e contribuição gera push. Um repositório com centenas de
milhares de estrelas recebe correções de documentação, traduções e dependências
atualizadas continuamente, mesmo quando o núcleo do código está estável.

Esperamos que esta seja a hipótese mais bem confirmada das sete, e que o mesmo se
mantenha nos 1000: abandono é raro no topo da lista, porque um projeto abandonado perde
relevância antes de acumular estrelas suficientes para entrar nela.

## RQ05 — Sistemas populares são escritos nas linguagens mais populares?

**Métrica:** linguagem primária, comparada ao ranking do Octoverse 2025
(ver [fontes.md](fontes.md)).

**Hipótese: parcialmente, com concordância no topo e divergência na ordem.**

Esperamos que as linguagens do topo do Octoverse — TypeScript, Python, JavaScript —
apareçam bastante, mas **não na mesma ordem**, porque as duas medidas contam coisas
diferentes: o Octoverse ordena por número de contribuidores e este estudo por estrelas.

Esperamos também uma fração relevante de repositórios **sem linguagem primária**, que o
ranking não consegue classificar. Se essa fração for grande, ela é a resposta mais
interessante da RQ05: parte do que é popular no GitHub não é código.

## RQ06 — Sistemas populares possuem alto percentual de issues fechadas?

**Métrica:** razão entre issues fechadas e total de issues.

**Hipótese: sim, com mediana acima de 0,8.**

Projetos populares têm triagem ativa, e issues antigas acabam fechadas: por resolução,
por duplicidade ou por bot de inatividade. Uma razão baixa indicaria backlog abandonado, o
que é incompatível com a atividade que esperamos ver na RQ04.

Duas ressalvas que podem inflar o número artificialmente: no GitHub **todo pull request
também é uma issue**, e PRs têm taxa de fechamento muito alta; e repositórios sem nenhuma
issue produzem razão 0,0 por convenção, o que puxa a mediana no sentido oposto. Por isso
o resumo reporta a mediana com e sem esses casos.

## RQ07 — Linguagens populares recebem mais contribuição, lançam mais releases e são atualizadas com mais frequência?

**Métrica:** RQ02, RQ03 e RQ04 agrupadas por linguagem primária.

**Hipótese: não. A linguagem explica pouco, e o tipo de projeto explica muito.**

Esperamos que a diferença entre linguagens seja menor do que a diferença entre categorias
de projeto. Um repositório de infraestrutura em Rust e um em Go devem se parecer mais
entre si do que um projeto em Python e uma lista curada sem linguagem, mesmo que a lista
"seja" Python pela contagem de arquivos.

Se houver padrão por linguagem, esperamos que ele apareça mais em **releases** do que em
PRs ou atualidade: linguagens de sistema e compilados têm cultura de versionamento
formal, enquanto ecossistemas web tendem a publicação contínua.

Esta é a hipótese que menos confiança temos, e a que mais depende da amostra de 1000 —
com 100 repositórios, várias linguagens terão poucos casos, e mediana sobre dois ou três
repositórios não sustenta conclusão.

---


## Consistência dos dados nos 1000 repositórios (Lab01S02)

Cada integrante valida, para as suas RQs: distribuição, outliers e valores ausentes.
Coleta de 1000 repositórios em 2026-08-18 (ver [metodologia.md](metodologia.md) para
data, contagem e custo em rate limit). Apenas consistência dos dados — a resposta de
cada RQ fica para o relatório final.

| RQ | Valores ausentes | Outliers observados | Observações |
|---|---|---|---|
| RQ01 | 0/1000 | 28 repositórios com idade < 0,5 ano (o mais novo, deepseek-ai/deepseek-harness, 0,01 ano); o mais antigo é rails/rails, 18,35 anos (criado em 2008-04-11) | Q1=3,52 · mediana=7,75 · Q3=11,35 · P95=14,95 anos. Nenhum valor negativo ou anterior à fundação do GitHub (2008) |
| RQ02 | 0/1000 | Máximo 103.316 PRs (firstcontributions/first-contributions), seguido de 96.977 (llvm/llvm-project) e 95.483 (elastic/elasticsearch); 129 repositórios (12,9%) acima de 10× a mediana | 20 repositórios (2%) com zero PRs aceitas. Q1=175 · mediana=768 · Q3=3.413,5 · P95=19.839,5. Distribuição fortemente assimétrica: média (4.234) é 5,5× a mediana |
| RQ03 | 0/1000 | 21 repositórios (2,1%) com contagem censurada no teto de 1000 da API (ver [validacao_amostra.md](validacao_amostra.md)) — valor real é maior, não confiável para média/máximo | 286 repositórios (28,6%) com zero releases. Q1=0 · mediana=39 · Q3=146,25 · P95=611,35 — quartil inferior inteiro em zero |
| RQ04 | 0/1000 | 115 repositórios (11,5%) sem push há mais de 1 ano; o mais parado é exacity/deeplearningbook-chinese, 2.450,77 dias (~6,7 anos) sem push | Q1=0,19 · mediana=1,81 · Q3=49,41 · P95=748,06 dias — cauda longa puxada por poucos repositórios abandonados |
| RQ05 | 87/1000 (8,7%) sem linguagem primária, rotulados `Undefined` | 12 das 44 linguagens distintas aparecem em apenas 1 repositório cada | Top 5 concentram 620/1000 (62%) da amostra: Python (228), TypeScript (174), JavaScript (111), Undefined (87), Go (76) |
| RQ06 | 43/1000 (4,3%) sem nenhuma issue — denominador zero, razão não interpretável. A métrica devolve `0.0` nesses casos, mas `has_issues()` os separa; a base interpretável é de **957 repositórios** | Cauda inferior curta: menor razão 0,077 (ComposioHQ/awesome-claude-skills, 11/143), seguida de 0,086 (floodsung/Deep-Learning-Papers-Reading-Roadmap) e 0,095 (anthropics/prompt-eng-interactive-tutorial) — todos repositórios de conteúdo/lista, não de software. 28 repositórios (2,9%) com razão exatamente 1,0. Apenas 1 repositório tem denominador frágil (≤ 5 issues) | Q1=0,704 · mediana=0,876 · Q3=0,969 · P5=0,317 · P95=0,998; média (0,802) abaixo da mediana — distribuição assimétrica à esquerda, concentrada no alto. Integridade: nenhum caso de `closed > total` e nenhuma razão fora de [0, 1]. Maior volume absoluto: microsoft/vscode, 233.639/251.153 = 0,930 |

**Nota sobre a RQ07.** Ela não tem linha própria na tabela porque não é uma métrica por
repositório: é a RQ02, a RQ03 e a RQ04 agrupadas por linguagem primária, e só será
calculada no Lab01S03. O que cabe verificar agora é se o **tamanho de amostra por
linguagem** sustenta esse tipo de comparação com n=1000 — e sustenta apenas parcialmente:

- São **44 rótulos distintos**, mas a distribuição é muito desigual: **30 deles têm n < 10**
  e somam apenas 86 repositórios; **12 aparecem em um único repositório**.
- Apenas **8 rótulos têm n ≥ 30**, e um deles é `Undefined` (ausência de linguagem, não uma
  linguagem). Restam **7 linguagens comparáveis**: Python (228), TypeScript (174),
  JavaScript (111), Go (76), Rust (57), C++ (41) e Java (41) — **728 repositórios (72,8%)**
  da amostra.
- **Consequência para o Lab01S03:** a comparação entre linguagens deve se restringir a essas
  7; a cauda de 30 linguagens com n < 10 não sustenta mediana estável e será agregada como
  "Outras" ou omitida, com o critério declarado no relatório. Comparar medianas de RQ02/RQ03/RQ04
  para linguagens com n = 1 produziria diferenças sem qualquer significado estatístico.
