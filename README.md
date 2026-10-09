# Renda Fixa API

**Títulos de renda fixa do Brasil em uma chamada** — CDB, LCI, LCA, CRI, CRA, debêntures e Tesouro Direto de vários bancos e corretoras, com **retorno líquido após IR** e **ganho real acima do IPCA** já calculados a partir das projeções do Boletim Focus (Banco Central). Atualizado diariamente.

- **REST/JSON** — `GET https://rendafixa.api.br/api/`
- **CSV para planilhas** — Google Sheets e Excel, sem programar
- **Servidor MCP** — use no Claude, ChatGPT, Cursor e outros assistentes de IA
- **OpenAPI 3.1** — [`openapi.json`](https://rendafixa.api.br/openapi.json)

📖 Documentação: **https://rendafixa.api.br/docs/api** · 💳 Planos: https://rendafixa.api.br/pricing

## Experimente agora (sem chave)

Sem chave, a API responde com uma prévia de 5 títulos:

```bash
curl "https://rendafixa.api.br/api/"
```

```json
{
  "response": { "status": "preview", "description": "No API key provided. Showing up to 5 bonds as a preview." },
  "bonds": [
    {
      "name": "CDB 360 DIAS",
      "bank": 77,
      "bank_name": "Banco Inter",
      "product": "cdb",
      "index": "cdi*",
      "rate": 1.05,
      "fgc_protection": true,
      "tax_free": false,
      "min_investment": 100,
      "maturity_date": "2027-05-08",
      "rating": "AA+",
      "net_annualized_return": 0.1165,
      "real_annualized_return": 0.0676
    }
  ]
}
```

Com uma chave de uma conta com assinatura ativa, a resposta traz **todos** os títulos. Gere a sua em [rendafixa.api.br/user/api-keys](https://rendafixa.api.br/user/api-keys).

```bash
curl -H "Authorization: Bearer rf_SUA_CHAVE" \
     "https://rendafixa.api.br/api/?product=lci,lca&tax_free=1&fgc=1"
```

## Filtros

| Parâmetro | Valores | |
|---|---|---|
| `product` | `cdb`, `lci`, `lca`, `cri`, `cra`, `deb`, `tpf`, `td`, `lf`, `misc` | lista separada por vírgula |
| `index` | `cdi*`, `cdi+`, `ipca*`, `ipca+`, `selic*`, `selic+`, `pre` | codifique `+` como `%2B` |
| `bank` | códigos numéricos | ex.: `341` Itaú, `77` Inter, `208` BTG |
| `tax_free` | `0` / `1` | só tributados / só isentos de IR |
| `fgc` | `0` / `1` | sem / com cobertura do FGC |
| `format` | `json` / `csv` | |

Taxas e retornos são decimais: `0.1165` = 11,65% a.a. Detalhes de cada campo e de como os retornos são calculados estão na [documentação](https://rendafixa.api.br/docs/api).

## Exemplos

Os títulos isentos de IR que mais rendem, sem nenhuma dependência:

- Python: [`examples/python/melhores_isentos.py`](examples/python/melhores_isentos.py)
- JavaScript (Node 18+): [`examples/javascript/melhores-isentos.mjs`](examples/javascript/melhores-isentos.mjs)

```bash
RENDAFIXA_KEY=rf_SUA_CHAVE python examples/python/melhores_isentos.py
```

## Planilhas

**Google Sheets** (planilha em português):

```
=IMPORTDATA("https://rendafixa.api.br/api/?format=csv&locale=pt-BR&key=rf_SUA_CHAVE")
```

Em uma planilha em inglês, tire o `&locale=pt-BR`. Os filtros funcionam na mesma URL: `&product=lci,lca&tax_free=1`.

**Excel**: Dados → Da Web → cole a URL acima.

## Assistentes de IA (MCP)

A API também é um servidor [MCP](https://modelcontextprotocol.io) remoto: **`https://rendafixa.api.br/mcp`**. Depois de adicionado, é só perguntar — *"qual LCI com FGC rende mais em até 2 anos?"*.

**Claude Code**

```bash
claude mcp add --transport http rendafixa https://rendafixa.api.br/mcp \
  --header "Authorization: Bearer rf_SUA_CHAVE"
```

**Cursor** (`.cursor/mcp.json`) e outros clientes com configuração em JSON

```json
{
  "mcpServers": {
    "rendafixa": {
      "url": "https://rendafixa.api.br/mcp",
      "headers": { "Authorization": "Bearer rf_SUA_CHAVE" }
    }
  }
}
```

**Claude.ai e ChatGPT** (conectores personalizados, que aceitam só uma URL): `https://rendafixa.api.br/mcp?key=rf_SUA_CHAVE`

Ferramentas: `search_bonds` (filtra e ordena por retorno líquido, ganho real, vencimento ou aplicação mínima) e `list_issuers` (bancos e códigos). Sem chave, a prévia.

## Licença

Os exemplos deste repositório são MIT. O uso da API está sujeito aos [planos e termos](https://rendafixa.api.br/pricing) do Renda Fixa.
