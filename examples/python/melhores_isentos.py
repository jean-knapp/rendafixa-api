"""As LCIs, LCAs, CRIs e CRAs isentas de IR que mais rendem, pela Renda Fixa API.

Sem dependências: só a biblioteca padrão do Python 3.8+.

    python melhores_isentos.py                  # prévia, sem chave
    RENDAFIXA_KEY=rf_... python melhores_isentos.py
"""
import json
import os
import urllib.parse
import urllib.request

BASE = os.environ.get("RENDAFIXA_BASE", "https://rendafixa.api.br")
KEY = os.environ.get("RENDAFIXA_KEY")


def buscar(**filtros):
    url = BASE + "/api/?" + urllib.parse.urlencode(filtros)
    pedido = urllib.request.Request(url, headers={"Accept": "application/json"})
    if KEY:
        pedido.add_header("Authorization", "Bearer " + KEY)
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        return json.load(resposta)


def pct(valor):
    return "-" if valor is None else f"{valor * 100:.2f}%".replace(".", ",")


dados = buscar(tax_free=1)
status = dados["response"]["status"]
titulos = sorted(
    dados["bonds"],
    key=lambda t: t["net_annualized_return"] or 0,
    reverse=True,
)

print(f"status: {status} — {dados['response']['description']}\n")
print(f"{'título':42} {'banco':18} {'vence':10} {'líquido a.a.':>12} {'real a.a.':>10}")
for t in titulos[:15]:
    print(
        f"{t['name'][:42]:42} {t['bank_name'][:18]:18} {t['maturity_date']:10} "
        f"{pct(t['net_annualized_return']):>12} {pct(t['real_annualized_return']):>10}"
    )

if status == "preview":
    print(f"\nIsto é uma prévia. Todos os títulos: assine em {BASE}/pricing e defina RENDAFIXA_KEY.")
