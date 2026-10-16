import json
import requests
from datetime import date, timedelta
from pathlib import Path

DIAS = 30
hoje = date.today()
data_inicial = hoje - timedelta(days=DIAS)

# Query string montada à mão: o Olinda exige '@' e '$' literais nos nomes
# dos parâmetros, e o requests os codifica (%40, %24) quando usamos params=.
url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
    "?@dataInicial='01-02-2025'"
    "&@dataFinalCotacao='01-31-2025'"
    "&$select=dataHoraCotacao,cotacaoCompra"
    "&$format=json"
)

resp = requests.get(url, timeout=60)
print("URL enviada:", resp.url)
if resp.status_code != 200:
    print("Status:", resp.status_code)
    print("Corpo da resposta:", resp.text[:500])   # o Olinda explica o erro aqui
resp.raise_for_status()

dados = resp.json()["value"]
if not dados:
    raise SystemExit("A API não retornou cotações. Tente ampliar o período.")

saida = Path(__file__).resolve().parent.parent / "data" / "cotacao_dolar.json"
saida.parent.mkdir(exist_ok=True)
with open(saida, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"{len(dados)} cotações salvas em {saida}")
print("Primeira:", dados[0])
print("Última:  ", dados[-1])