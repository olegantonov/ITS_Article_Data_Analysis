"""Analisa tempos de voo e uso de aeronaves, gerando gráficos resumidos."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from config import ANALYSIS_DIR

# ⚠️ SOLUÇÃO DO PROBLEMA COM TKINTER: Muda o backend do Matplotlib para não usar interface gráfica
matplotlib.use('Agg')  # Define o backend sem GUI para evitar erro do Tcl/Tk␊
␊
# Caminho do arquivo CSV␊
caminho_arquivo = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_v2.csv"

# ⚠️ SOLUÇÃO DO DTYPEWARNING: Especifica `dtype` para colunas problemáticas e usa `low_memory=False`
dtype_especifico = {
    "Número Voo": str,  # Número do voo pode ter valores misturados, força como string
    "Justificativa": str  # Justificativa pode conter texto ou valores nulos, forçamos como string
}

# Carregar os dados corrigindo os problemas de dtype
df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8', dtype=dtype_especifico, low_memory=False)

# Certificar-se de que a coluna "Ano do Voo" existe e está no formato correto
df['Ano'] = pd.to_numeric(df['Ano do Voo'], errors='coerce')

# Remover voos com tempos negativos (caso existam)
df = df[df['Tempo_Voo_Real_min'] >= 0]

# Criar DataFrame com estatísticas anuais
df_analise = df.groupby('Ano').agg(
    Tempo_Medio=('Tempo_Voo_Real_min', 'mean'),
    Tempo_Minimo=('Tempo_Voo_Real_min', 'min'),
    Tempo_Maximo=('Tempo_Voo_Real_min', 'max')
).reset_index()

# Criar ranking de aeronaves mais utilizadas por ano
df_ranking = df.groupby(['Ano', 'Modelo Equipamento']).size().reset_index(name='Voos')
