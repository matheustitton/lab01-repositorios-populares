# Configuração do processo — GitHub Projects (v2)

- **Repositório:** `<preencher>`
- **GitHub Projects:** `<preencher>`
- **Integrantes:** `<preencher>`

## Colunas do board (campo Status)

| Coluna | Significado | Critério de saída |
|---|---|---|
| `Backlog` | Tarefa identificada, ainda não priorizada para a sprint | Entrou no escopo da sprint |
| `To Do` | Priorizada para a sprint, com Assignee definido | Alguém começou a trabalhar |
| `Doing` | Em desenvolvimento | Código pronto e enviado |
| `Review` | Aguardando revisão de outro integrante | Revisão aprovada |
| `Done` | Integrada à `main` e validada | — |

## Limite de WIP na coluna Doing

- **Limite adotado:** `<preencher — sugerido: 3>`
- **Justificativa:** `<preencher>`

Justificativa sugerida: o grupo é um trio e cada integrante é responsável por 2–3 RQs, o
que dá **uma tarefa em andamento por pessoa**. Um limite maior permitiria que alguém
abrisse frentes paralelas e acumulasse trabalho pela metade no fim da sprint; um limite
menor bloquearia integrantes ociosos. O limite força terminar antes de começar — quando
`Doing` está cheio, quem ficou livre revisa o que está em `Review` em vez de puxar tarefa
nova, o que também evita o gargalo de revisão no último dia.

## Regras acordadas pelo grupo

1. Todo cartão é uma **Issue de verdade** do repositório — sem draft issues.
2. Toda Issue tem **Assignee** antes de sair de `Backlog`.
3. Todo commit **referencia o número da Issue** (`#12 implementa consulta GraphQL`);
   commits sem referência não são considerados na avaliação.
4. Os cartões são movidos **conforme o progresso real**, nunca retroativamente.
5. Ao fim de cada sprint, exportar o snapshot:
   `python -m src.cli.export_project_snapshot --sprint lab01s01`

## Snapshots exportados

| Sprint | Arquivo | Data | Itens |
|---|---|---|---|
| Lab01S01 | `data/snapshots/project_snapshot_lab01s01.csv` | | |
| Lab01S02 | `data/snapshots/project_snapshot_lab01s02.csv` | | |
| Lab01S03 | `data/snapshots/project_snapshot_lab01s03.csv` | | |

Como a API do Projects não expõe histórico de mudança de coluna, esta série acumulada é a
base de dados dos Labs 04 e 05. **Um snapshot não tirado não pode ser reconstruído depois.**

## Print do board

`<inserir docs/assets/board-lab01.png ao final do laboratório>`
