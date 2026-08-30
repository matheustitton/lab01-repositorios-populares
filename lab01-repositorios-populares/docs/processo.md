# Configuração do processo — GitHub Projects (v2)

- **Repositório:** `<preencher>`
- **GitHub Projects:** `<preencher>`
- **Integrantes:** `<preencher>`

## Colunas do board (campo Status)

`Backlog → Sprint Backlog → Doing → Review → Done`

| Coluna | Significado | Critério de saída |
|---|---|---|
| `Backlog` | Tarefa identificada, ainda não priorizada para a sprint | Entrou no escopo da sprint |
| `Sprint Backlog` | Priorizada para a sprint, com Assignee definido | Alguém começou a trabalhar |
| `Doing` | Em desenvolvimento | Código pronto e enviado |
| `Review` | Aguardando revisão de outro integrante | Revisão aprovada |
| `Done` | Integrada à `main` e validada | — |

> Atende ao mínimo exigido pelo enunciado (`Backlog → To Do → Doing → Review → Done`);
> o grupo nomeou a segunda coluna como `Sprint Backlog`, que cumpre o mesmo papel de "To Do".

## Limite de WIP na coluna Doing

- **Limite adotado:** **3**
- **Justificativa:** o grupo é um trio e cada integrante é responsável por 2–3 RQs, o que
  dá **uma tarefa em andamento por pessoa**. Um limite maior permitiria que alguém abrisse
  frentes paralelas e acumulasse trabalho pela metade no fim da sprint, já um limite menor
  bloquearia integrantes ociosos. O limite força terminar antes de começar. Quando `Doing`
  está cheio, quem ficou livre revisa o que está em `Review` em vez de puxar tarefa nova,
  o que também evita o gargalo de revisão no último dia.

Registrado na Issue [#5](https://github.com/matheustitton/lab01-repositorios-populares/issues/5).

## Regras acordadas pelo grupo

1. Todo cartão é uma **Issue de verdade** do repositório (sem draft issues).
2. Toda Issue tem **Assignee** antes de sair de `Backlog`.
3. Todo commit **referencia o número da Issue** (`#12 implementa consulta GraphQL`);
   commits sem referência não são considerados na avaliação.
4. Os cartões são movidos **conforme o progresso real**, nunca retroativamente.
5. Ao fim de cada sprint, exportar o snapshot:
   `python -m src.cli.export_project_snapshot --sprint lab01s01`

## Snapshots exportados

Todos acumulam no **mesmo arquivo**, `data/snapshots_board.csv`, uma linha por cartão por
sprint. Reexecutar na mesma sprint substitui as linhas daquela sprint — nunca duplica.

- **Project:** #2 — "@matheustitton's Kanbam de Acompanhamento", vinculado ao repositório
- **Comando:** `python -m src.cli.export_project_snapshot --sprint lab01s01 --owner matheustitton --number 2`

| Sprint | Data da captura | Itens | Distribuição |
|---|---|---|---|
| Lab01S01 | 2026-08-13 | 7 | Done 5 · Doing 1 · Sprint Backlog 1 |
| Lab01S02 | 2026-08-20 | 12 | Done 10 · Sprint Backlog 2 |
| Lab01S03 | | | |

Como a API do Projects não expõe histórico de mudança de coluna, esta série acumulada é a
base de dados dos Labs 04 e 05. **Um snapshot não tirado não pode ser reconstruído depois.**

O script também audita o board a cada execução e avisa sobre cartões sem Assignee, cartões
sem Issue real (draft) e cartões cujo Status contradiz o estado da Issue: os três pontos
que o enunciado penaliza.

## Print do board

`<inserir docs/assets/board-lab01.png ao final do laboratório>`
