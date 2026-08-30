# Validacao da amostra - Lab01S01

Gerado por `python -m src.cli.validate_sample` em 2026-08-13 22:47 UTC.
Fonte: `raw_repos_lab01s01.json` (10 repositorios coletados).

## Amostra selecionada

Selecao deterministica, priorizando os casos de borda onde o mapeamento pode
falhar - repositorio sem linguagem primaria, sem releases, sem issues. Uma amostra
sorteada tenderia a conter so repositorios comuns e nao validaria nada.

| # | Repositorio | Motivo da escolha | Estrelas | Criado em | Linguagem |
|---|---|---|---|---|---|
| 1 | [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | maior numero de estrelas | 539,443 | 2018-05-09 | Markdown |
| 2 | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | sem linguagem primaria | 495,376 | 2014-07-11 | Undefined |
| 3 | [public-apis/public-apis](https://github.com/public-apis/public-apis) | sem nenhuma release | 455,948 | 2016-03-20 | Python |
| 4 | [vinta/awesome-python](https://github.com/vinta/awesome-python) | sem nenhuma issue | 313,806 | 2014-06-27 | Python |
| 5 | [freeCodeCamp/freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp) | mais pull requests aceitas | 453,959 | 2014-12-24 | TypeScript |
| 6 | [openclaw/openclaw](https://github.com/openclaw/openclaw) | mais releases | 386,193 | 2025-11-24 | TypeScript |
| 7 | [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books) | entre os mais estrelados | 394,337 | 2013-10-11 | Python |

## Conferencia automatica: GraphQL vs REST

Os mesmos repositorios lidos pela API REST, que e uma fonte independente da
GraphQL usada na coleta. `pushed_at` e comparado ate o minuto, porque os dois
endpoints podem ser servidos por caches diferentes.

**Deriva temporal nao e erro.** O dataset e um retrato do instante da coleta; a
REST responde com o estado de agora. Entre um e outro, repositorios populares
ganham estrelas e recebem pushes. Por isso `stars` e `pushed_at` sao tratados como
campos vivos: diferenca pequena e esperada e vem anotada como deriva. Ja `created_at`
e `primary_language` sao estaveis - qualquer diferenca ali seria erro de verdade na
query ou no mapeamento.

| Repositorio | Campo | GraphQL (coletado) | REST (agora) | Resultado |
|---|---|---|---|---|
| codecrafters-io/build-your-own-x | stars | 539443 | 539443 | confere |
| codecrafters-io/build-your-own-x | created_at | 2018-05-09T12:03:18+00:00 | 2018-05-09T12:03:18+00:00 | confere |
| codecrafters-io/build-your-own-x | pushed_at | 2026-07-14 19:25 | 2026-07-14 19:25 | confere |
| codecrafters-io/build-your-own-x | primary_language | Markdown | Markdown | confere |
| sindresorhus/awesome | stars | 495376 | 495376 | confere |
| sindresorhus/awesome | created_at | 2014-07-11T13:42:37+00:00 | 2014-07-11T13:42:37+00:00 | confere |
| sindresorhus/awesome | pushed_at | 2026-06-30 18:21 | 2026-06-30 18:21 | confere |
| sindresorhus/awesome | primary_language | None | None | confere |
| public-apis/public-apis | stars | 455948 | 455948 | confere |
| public-apis/public-apis | created_at | 2016-03-20T23:49:42+00:00 | 2016-03-20T23:49:42+00:00 | confere |
| public-apis/public-apis | pushed_at | 2026-08-13 21:07 | 2026-08-13 21:07 | confere |
| public-apis/public-apis | primary_language | Python | Python | confere |
| vinta/awesome-python | stars | 313806 | 313806 | confere |
| vinta/awesome-python | created_at | 2014-06-27T21:00:06+00:00 | 2014-06-27T21:00:06+00:00 | confere |
| vinta/awesome-python | pushed_at | 2026-08-05 06:11 | 2026-08-05 06:11 | confere |
| vinta/awesome-python | primary_language | Python | Python | confere |
| freeCodeCamp/freeCodeCamp | stars | 453959 | 453959 | confere |
| freeCodeCamp/freeCodeCamp | created_at | 2014-12-24T17:49:19+00:00 | 2014-12-24T17:49:19+00:00 | confere |
| freeCodeCamp/freeCodeCamp | pushed_at | 2026-08-13 21:20 | 2026-08-13 21:20 | confere |
| freeCodeCamp/freeCodeCamp | primary_language | TypeScript | TypeScript | confere |
| openclaw/openclaw | stars | 386193 | 386194 | deriva temporal (+1) |
| openclaw/openclaw | created_at | 2025-11-24T10:16:47+00:00 | 2025-11-24T10:16:47+00:00 | confere |
| openclaw/openclaw | pushed_at | 2026-08-13 22:40 | 2026-08-13 22:46 | deriva temporal (2026-08-13 22:40 -> 2026-08-13 22:46) |
| openclaw/openclaw | primary_language | TypeScript | TypeScript | confere |
| EbookFoundation/free-programming-books | stars | 394337 | 394337 | confere |
| EbookFoundation/free-programming-books | created_at | 2013-10-11T06:50:37+00:00 | 2013-10-11T06:50:37+00:00 | confere |
| EbookFoundation/free-programming-books | pushed_at | 2026-08-11 12:11 | 2026-08-11 12:11 | confere |
| EbookFoundation/free-programming-books | primary_language | Python | Python | confere |

**Divergencias reais encontradas: 0**

## Teto de contagem

Nenhum repositorio com contagem exatamente igual a 1000.

## Conferencia manual

A REST nao entrega barato o total de PRs aceitas nem o de releases. Estes tres
repositorios foram conferidos a mao nas paginas do GitHub:

| Repositorio | PRs aceitas (coletado) | Releases (coletado) | Conferir em |
|---|---|---|---|
| freeCodeCamp/freeCodeCamp | 29,089 | 0 | [PRs](https://github.com/freeCodeCamp/freeCodeCamp/pulls?q=is%3Apr+is%3Amerged) / [releases](https://github.com/freeCodeCamp/freeCodeCamp/releases) |
| openclaw/openclaw | 24,601 | 233 | [PRs](https://github.com/openclaw/openclaw/pulls?q=is%3Apr+is%3Amerged) / [releases](https://github.com/openclaw/openclaw/releases) |
| codecrafters-io/build-your-own-x | 157 | 0 | [PRs](https://github.com/codecrafters-io/build-your-own-x/pulls?q=is%3Apr+is%3Amerged) / [releases](https://github.com/codecrafters-io/build-your-own-x/releases) |

| Repositorio | Conferido por | Data | Resultado |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

> Preencher a tabela acima ao conferir. O criterio de aceite da Issue #2 exige
> validacao manual de pelo menos 2 a 3 repositorios da amostra.
