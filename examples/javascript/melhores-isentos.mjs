// As LCIs, LCAs, CRIs e CRAs isentas de IR que mais rendem, pela Renda Fixa API.
// Node 18+ (fetch nativo), sem dependências.
//
//   node melhores-isentos.mjs                  # prévia, sem chave
//   RENDAFIXA_KEY=rf_... node melhores-isentos.mjs

const BASE = process.env.RENDAFIXA_BASE ?? "https://rendafixa.api.br";
const KEY = process.env.RENDAFIXA_KEY;

const resposta = await fetch(`${BASE}/api/?tax_free=1`, {
  headers: KEY ? { Authorization: `Bearer ${KEY}` } : {},
});
const { response, bonds } = await resposta.json();

const pct = (v) => (v == null ? "-" : `${(v * 100).toFixed(2).replace(".", ",")}%`);

console.log(`status: ${response.status} — ${response.description}\n`);

bonds
  .sort((a, b) => (b.net_annualized_return ?? 0) - (a.net_annualized_return ?? 0))
  .slice(0, 15)
  .forEach((t) => {
    console.log(
      `${t.name.slice(0, 42).padEnd(42)} ${t.bank_name.slice(0, 18).padEnd(18)} ${t.maturity_date} ` +
        `${pct(t.net_annualized_return).padStart(12)} ${pct(t.real_annualized_return).padStart(10)}`,
    );
  });

if (response.status === "preview") {
  console.log(`\nIsto é uma prévia. Todos os títulos: assine em ${BASE}/pricing e defina RENDAFIXA_KEY.`);
}
