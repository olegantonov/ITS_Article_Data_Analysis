"""Modelos de regressão para avaliar impacto do PBN em indicadores de voo."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from config import ANALYSIS_DIR

# Leitura dos dados filtrados com tempos diferentes
caminho_arquivo = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_v2_tempo_diferente.csv"
df = pd.read_csv(caminho_arquivo, low_memory=False)

# Colunas numéricas
cols_numericas = [
    'Ano', 'Distância_Rota_NM', 'Load_Factor_Utilizado', 'Número de Assentos',
    'Tempo_Voo_Real_min'
]
for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())

# Dados de implantação do PBN
implantation_years = {
    'SBCF': 2015, 'SBBR': 2015, 'SBCT': 2017, 'SBFZ': None,
    'SBPA': 2017, 'SBRF': 2010, 'SBRJ': 2011, 'SBGL': 2011,
    'SBSV': 2017, 'SBSP': 2015, 'SBGR': 2015
}

def ano_implantacao(row):
    icao = str(row['Sigla ICAO Aeroporto Origem']).upper()
    year = implantation_years.get(icao)
    return year

df['Ano_PBN'] = df.apply(ano_implantacao, axis=1)

df['PBN_implantado'] = (df['Ano'] >= df['Ano_PBN']).astype(int)

# Prepara variáveis independentes e dependente
X = df[['Ano', 'Distância_Rota_NM', 'Load_Factor_Utilizado', 'Número de Assentos', 'PBN_implantado']]
X = sm.add_constant(X)
y = df['Tempo_Voo_Real_min']

modelo = sm.OLS(y, X, missing='drop').fit()

# Salva sumário
summary_path = ANALYSIS_DIR / 'resultado_regressao.txt'
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(modelo.summary().as_text())

print(f"Resumo salvo em {summary_path}")
