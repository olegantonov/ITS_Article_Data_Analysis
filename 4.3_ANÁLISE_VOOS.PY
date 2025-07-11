"""Analisa tempos de voo e uso de aeronaves, gerando gráficos resumidos."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from config import ANALYSIS_DIR

caminho_arquivo = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_v2.csv"

# Carregar os dados
_dtype = {"Número Voo": str, "Justificativa": str}
df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8', dtype=_dtype, low_memory=False)

# Garante existência da coluna 'Ano'
if 'Ano' not in df.columns:
    raise ValueError("Coluna 'Ano' não encontrada no arquivo de análise.")

# Remove voos com tempos negativos
if 'Tempo_Voo_Real_min' in df.columns:
    df = df[df['Tempo_Voo_Real_min'] >= 0]

# Estatísticas anuais
cols = ['Tempo_Voo_Real_min']
df_analise = df.groupby('Ano')[cols].agg(['mean', 'min', 'max'])

plt.figure(figsize=(8,5))
plt.plot(df_analise.index, df_analise[('Tempo_Voo_Real_min','mean')], label='Tempo médio')
plt.plot(df_analise.index, df_analise[('Tempo_Voo_Real_min','min')], label='Tempo mínimo')
plt.plot(df_analise.index, df_analise[('Tempo_Voo_Real_min','max')], label='Tempo máximo')
plt.legend()
plt.xlabel('Ano')
plt.ylabel('Tempo de voo (min)')
plt.title('Resumo do tempo de voo ao longo dos anos')
plt.tight_layout()
plt.savefig(ANALYSIS_DIR / 'Tempo_voo_resumo.png')
plt.close()

# Ranking de aeronaves por ano
df_ranking = df.groupby(['Ano', 'Modelo Equipamento']).size().reset_index(name='Voos')
fig, ax = plt.subplots(figsize=(10,6))
for ano, grupo in df_ranking.groupby("Ano"):
    top = grupo.sort_values("Voos", ascending=False).head(5)
    ax.bar(top["Modelo Equipamento"] + f" ({ano})", top["Voos"])
ax.set_title('Aeronaves mais utilizadas por ano (top 5)')
ax.set_ylabel("Voos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(ANALYSIS_DIR / 'Ranking_aeronaves.png')
plt.close()
