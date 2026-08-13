# Fixtures

Respostas reais da API, salvas para que os testes rodem sem rede e sem gastar rate limit.

Para gerar `search_response_sample.json`, rode a coleta com `--save-raw` e `--limit 10` e
copie uma página de `data/raw/`. Recorte para 5–10 repositórios e inclua propositalmente
os casos de borda: repositório sem `primaryLanguage`, sem releases e sem issues.

Para `project_items_sample.json`, use `--save-raw` no export do snapshot. Inclua um cartão
sem assignee e, se houver, um item que não seja Issue (draft).
