# lab01-repositorios-populares

Repositório referente ao primeiro roteiro para a matéria de Laboratório de Experimentação
de Software — estudo das características dos 1.000 repositórios open-source mais
estrelados do GitHub.

## Requisitos

- Python 3.11+
- Um Personal Access Token do GitHub (escopo `public_repo`; para o snapshot do board,
  também `read:project`)

## Setup

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha o `GITHUB_TOKEN`.

> A coleta em si roda **apenas com a biblioteca padrão** do Python. As dependências do
> `requirements.txt` (pandas, matplotlib, pytest) são usadas só na análise e nos testes —
> nenhuma delas consulta a API do GitHub, conforme a restrição do enunciado.

## Uso

Coleta dos repositórios (Lab01S01 com 100, Lab01S02 com 1000):

```bash
python -m src.cli.collect_repositories --limit 1000
```

Validação da amostra coletada, conferindo contra a API REST (Lab01S01):

```bash
python -m src.cli.validate_sample --size 8
```

Análise e gráficos das 7 RQs (Lab01S03):

```bash
python -m src.cli.analyze
```

Snapshot do board ao fim de cada sprint:

```bash
python -m src.cli.export_project_snapshot --sprint lab01s01
```

Testes:

```bash
pytest
```

## Estrutura

```
docs/      relatório, hipóteses, metodologia, processo do board, fontes
data/      raw/ (páginas brutas)  processed/ (CSV)  snapshots/ (board por sprint)
src/
  config/          configuração via variáveis de ambiente
  infrastructure/  HTTP + GraphQL + retry (não conhece o domínio)
  queries/         arquivos .graphql
  domain/          modelos e métricas — uma RQ por arquivo
  collection/      mapeamento, paginação e coletores
  storage/         CSV e cache de respostas
  analysis/        estatísticas por RQ (lê CSV, não acessa a rede)
  visualization/   gráficos
  cli/             pontos de entrada
tests/     testes sem rede, sobre fixtures
```

O fluxo é unidirecional: `cli → collection → infrastructure` para coletar,
`domain → storage → CSV` para persistir, `analysis → visualization` para reportar.
A infraestrutura não conhece o domínio, e é por isso que o snapshot do GitHub Projects
reaproveita integralmente o código de consulta da Parte 1.

## Documentação

| Documento | Conteúdo |
|---|---|
| [docs/relatorio.md](docs/relatorio.md) | Relatório final |
| [docs/validacao_amostra.md](docs/validacao_amostra.md) | Conferência da amostra contra a REST |
| [docs/hipoteses.md](docs/hipoteses.md) | Hipóteses informais por RQ |
| [docs/metodologia.md](docs/metodologia.md) | Como os dados foram coletados |
| [docs/processo.md](docs/processo.md) | Colunas do board e política de WIP |
| [docs/fontes.md](docs/fontes.md) | Fonte de "linguagens mais populares" |

## Convenções do grupo

- Cada cartão do board é uma **Issue** real, com **Assignee**.
- **Todo commit referencia o número da Issue**: `#12 implementa consulta GraphQL`.
- Limite de WIP na coluna `Doing` — ver [docs/processo.md](docs/processo.md).
