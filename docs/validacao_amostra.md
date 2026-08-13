# Validacao da amostra - Lab01S01

Gerado por `python -m src.cli.validate_sample` em 2026-08-13 15:05 UTC.
Fonte: `raw_repos_lab01s01.json` (100 repositorios coletados).

## Amostra selecionada

Selecao deterministica, priorizando os casos de borda onde o mapeamento pode
falhar - repositorio sem linguagem primaria, sem releases, sem issues. Uma amostra
sorteada tenderia a conter so repositorios comuns e nao validaria nada.

| # | Repositorio | Motivo da escolha | Estrelas | Criado em | Linguagem |
|---|---|---|---|---|---|
| 1 | [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | maior numero de estrelas | 539,335 | 2018-05-09 | Markdown |
| 2 | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | sem linguagem primaria | 495,251 | 2014-07-11 | Undefined |
| 3 | [public-apis/public-apis](https://github.com/public-apis/public-apis) | sem nenhuma release | 455,880 | 2016-03-20 | Python |
| 4 | [vinta/awesome-python](https://github.com/vinta/awesome-python) | sem nenhuma issue | 313,731 | 2014-06-27 | Python |
| 5 | [getify/You-Dont-Know-JS](https://github.com/getify/You-Dont-Know-JS) | todas as issues fechadas | 184,653 | 2013-11-16 | Undefined |
| 6 | [rust-lang/rust](https://github.com/rust-lang/rust) | mais pull requests aceitas | 115,489 | 2010-06-16 | Rust |
| 7 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | mais releases | 144,166 | 2022-10-17 | Python |
| 8 | [freeCodeCamp/freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp) | entre os mais estrelados | 453,944 | 2014-12-24 | TypeScript |

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
| codecrafters-io/build-your-own-x | stars | 539335 | 539343 | deriva temporal (+8) |
| codecrafters-io/build-your-own-x | created_at | 2018-05-09T12:03:18+00:00 | 2018-05-09T12:03:18+00:00 | confere |
| codecrafters-io/build-your-own-x | pushed_at | 2026-07-14 19:25 | 2026-07-14 19:25 | confere |
| codecrafters-io/build-your-own-x | primary_language | Markdown | Markdown | confere |
| sindresorhus/awesome | stars | 495251 | 495261 | deriva temporal (+10) |
| sindresorhus/awesome | created_at | 2014-07-11T13:42:37+00:00 | 2014-07-11T13:42:37+00:00 | confere |
| sindresorhus/awesome | pushed_at | 2026-06-30 18:21 | 2026-06-30 18:21 | confere |
| sindresorhus/awesome | primary_language | None | None | confere |
| public-apis/public-apis | stars | 455880 | 455885 | deriva temporal (+5) |
| public-apis/public-apis | created_at | 2016-03-20T23:49:42+00:00 | 2016-03-20T23:49:42+00:00 | confere |
| public-apis/public-apis | pushed_at | 2026-08-12 09:25 | 2026-08-12 09:25 | confere |
| public-apis/public-apis | primary_language | Python | Python | confere |
| vinta/awesome-python | stars | 313731 | 313734 | deriva temporal (+3) |
| vinta/awesome-python | created_at | 2014-06-27T21:00:06+00:00 | 2014-06-27T21:00:06+00:00 | confere |
| vinta/awesome-python | pushed_at | 2026-08-05 06:11 | 2026-08-05 06:11 | confere |
| vinta/awesome-python | primary_language | Python | Python | confere |
| getify/You-Dont-Know-JS | stars | 184653 | 184655 | deriva temporal (+2) |
| getify/You-Dont-Know-JS | created_at | 2013-11-16T02:37:24+00:00 | 2013-11-16T02:37:24+00:00 | confere |
| getify/You-Dont-Know-JS | pushed_at | 2026-02-15 04:36 | 2026-02-15 04:36 | confere |
| getify/You-Dont-Know-JS | primary_language | None | None | confere |
| rust-lang/rust | stars | 115489 | 115490 | deriva temporal (+1) |
| rust-lang/rust | created_at | 2010-06-16T20:39:03+00:00 | 2010-06-16T20:39:03+00:00 | confere |
| rust-lang/rust | pushed_at | 2026-08-13 14:01 | 2026-08-13 14:01 | confere |
| rust-lang/rust | primary_language | Rust | Rust | confere |
| langchain-ai/langchain | stars | 144166 | 144166 | confere |
| langchain-ai/langchain | created_at | 2022-10-17T02:58:36+00:00 | 2022-10-17T02:58:36+00:00 | confere |
| langchain-ai/langchain | pushed_at | 2026-08-13 14:17 | 2026-08-13 14:17 | confere |
| langchain-ai/langchain | primary_language | Python | Python | confere |
| freeCodeCamp/freeCodeCamp | stars | 453944 | 453946 | deriva temporal (+2) |
| freeCodeCamp/freeCodeCamp | created_at | 2014-12-24T17:49:19+00:00 | 2014-12-24T17:49:19+00:00 | confere |
| freeCodeCamp/freeCodeCamp | pushed_at | 2026-08-13 09:34 | 2026-08-13 14:51 | deriva temporal (2026-08-13 09:34 -> 2026-08-13 14:51) |
| freeCodeCamp/freeCodeCamp | primary_language | TypeScript | TypeScript | confere |

**Divergencias reais encontradas: 0**

## Teto de contagem detectado

A conexao `releases` da GraphQL para de contar em 1000. Os
repositorios abaixo reportaram exatamente esse valor: sao contagens **censuradas**,
nao contagens reais. O valor verdadeiro veio da paginacao da REST.

| Repositorio | GraphQL (censurado) | REST (real) |
|---|---|---|
| langchain-ai/langchain | 1,000 | 1,326 |
| vercel/next.js | 1,000 | 3,799 |
| ggml-org/llama.cpp | 1,000 | 6,844 |
| electron/electron | 1,000 | 1,979 |

**4 de 100 repositorios afetados (4%).**

Impacto na RQ03: a **mediana nao e afetada**, porque os censurados estao muito
acima dela. Ja media, maximo e o formato da cauda superior ficam incorretos e nao
devem ser reportados sem esta ressalva. Os demais campos foram verificados e nao
tem teto: PRs aceitas e issues aparecem na coleta com valores bem acima de
1000.

## Conferencia manual

A REST nao entrega barato o total de PRs aceitas nem o de releases. Estes tres
repositorios foram conferidos a mao nas paginas do GitHub:

| Repositorio | PRs aceitas (coletado) | Releases (coletado) | Conferir em |
|---|---|---|---|
| rust-lang/rust | 73,425 | 153 | [PRs](https://github.com/rust-lang/rust/pulls?q=is%3Apr+is%3Amerged) / [releases](https://github.com/rust-lang/rust/releases) |
| langchain-ai/langchain | 17,229 | 1,000 | [PRs](https://github.com/langchain-ai/langchain/pulls?q=is%3Apr+is%3Amerged) / [releases](https://github.com/langchain-ai/langchain/releases) |
| codecrafters-io/build-your-own-x | 157 | 0 | [PRs](https://github.com/codecrafters-io/build-your-own-x/pulls?q=is%3Apr+is%3Amerged) / [releases](https://github.com/codecrafters-io/build-your-own-x/releases) |

| Repositorio | Conferido por | Data | Resultado |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

> Preencher a tabela acima ao conferir. O criterio de aceite da Issue #2 exige
> validacao manual de pelo menos 2 a 3 repositorios da amostra.
