"""Modelos de regressão para avaliar impacto do PBN em indicadores de voo."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import seaborn as sns
import statsmodels.api as sm
from datetime import datetime
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from config import ANALYSIS_DIR

# 1. Leitura dos dados
caminho_arquivo = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_v2_tempo_diferente.csv"
df = pd.read_csv(caminho_arquivo, low_memory=False)␊

# 2. Conversão das colunas numéricas e imputação de valores faltantes com a mediana
colunas_numericas = ['Ano', 'Distância_Rota_NM', 'Load_Factor_Utilizado', 'Número de Assentos',
                     'Tempo_Voo_Real_min', 'Consumo_Combustível_kg', 'Consumo_CO2_do_Voo_kg']
for col in colunas_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

# 3. Dados de implantação do PBN
implantation_dates = {
    'SBCF': '12/11/2015',
    'SBBR': '12/11/2015',
    'SBCT': '12/10/2017',
    'SBFZ': None,   # Dados não disponíveis
    'SBPA': '12/10/2017',
    'SBRF': '08/04/2010',
    'SBRJ': '28/07/2011',
    'SBGL': '28/07/2011',
    'SBSV': '27/04/2017',
    'SBSP': '12/11/2015',
    'SBGR': '12/11/2015'
}
implantation_years = {}
for icao, date_str in implantation_dates.items():
    if date_str is None or str(date_str).strip() == '':
