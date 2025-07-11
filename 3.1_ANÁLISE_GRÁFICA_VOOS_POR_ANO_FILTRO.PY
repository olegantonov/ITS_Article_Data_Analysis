"""Gera gráficos de voos por ano e por rota usando o dataset filtrado."""

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from config import ANALYSIS_DIR

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos de entrada e saída
input_csv = ANALYSIS_DIR / "FILTRADOS_DADOS.csv"
output_image_year = ANALYSIS_DIR / "FILTRO_voos_por_ANO.png"
output_image_route = ANALYSIS_DIR / "FILTRO_voos_por_ROTA.png"

logging.info("Carregando a planilha final...")
df = pd.read_csv(input_csv, delimiter=",", encoding="utf-8", low_memory=False)
logging.info(f"Planilha carregada. Total de registros: {df.shape[0]}")

# Extrai o ano do voo
def obter_ano(col):
    if col in df.columns:
        data = pd.to_datetime(df[col], errors="coerce")
        return data.dt.year
    return None

if "Ano" in df.columns:
    anos = df["Ano"]
else:
    anos = obter_ano("Partida Real")
    if anos is None:
        anos = obter_ano("Chegada Real")
    df["Ano"] = anos

# Remove registros sem ano
df = df.dropna(subset=["Ano"])

# Gráfico de voos por ano
voos_por_ano = df.groupby("Ano").size().sort_index()
plt.figure(figsize=(10,5))
voos_por_ano.plot(kind="bar")
plt.title("Quantidade de voos por ano (dados filtrados)")
plt.xlabel("Ano")
plt.ylabel("Voos")
plt.tight_layout()
plt.savefig(output_image_year)
plt.close()
logging.info(f"Gráfico salvo em {output_image_year}")

# Gráfico de voos por rota (origem-destino ordenada)
df["Rota"] = df["Sigla ICAO Aeroporto Origem"].str.upper().str.strip() + "-" + df["Sigla ICAO Aeroporto Destino"].str.upper().str.strip()
# Ordena origem e destino para contar ida e volta juntos
rotas_ordenadas = df["Rota"].apply(lambda r: "-".join(sorted(r.split("-"))))
voos_por_rota = rotas_ordenadas.value_counts().sort_values(ascending=False)
plt.figure(figsize=(12,6))
voos_por_rota.plot(kind="bar")
plt.title("Quantidade de voos por rota (dados filtrados)")
plt.xlabel("Rota")
plt.ylabel("Voos")
plt.tight_layout()
plt.savefig(output_image_route)
plt.close()
logging.info(f"Gráfico salvo em {output_image_route}")
