"""Calcula variáveis adicionais e métricas ambientais para cada voo."""

import logging
import pandas as pd
from config import ANALYSIS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

input_csv = ANALYSIS_DIR / "FILTRADOS_DADOS.csv"
output_csv = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_v2.csv"

logging.info("Carregando o arquivo de dados filtrados...")
df = pd.read_csv(input_csv, delimiter=",", encoding="utf-8", low_memory=False)
logging.info(f"Arquivo carregado. Total de registros: {df.shape[0]}")

required_cols = ["Número de Assentos", "Partida Real", "Chegada Real", "Partida Prevista", "Chegada Prevista"]
for col in required_cols:
    if col not in df.columns:
        logging.error(f"Coluna necessária ausente: {col}")
        exit()

# Converte colunas de data/hora
for col in ["Partida Real", "Chegada Real", "Partida Prevista", "Chegada Prevista"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Extrai o ano
if "Ano" not in df.columns:
    df["Ano"] = df["Partida Real"].dt.year

# Calcula tempos de voo
df["Tempo_Voo_Real_min"] = (df["Chegada Real"] - df["Partida Real"]).dt.total_seconds() / 60
df["Tempo_Voo_Estimado_min"] = (df["Chegada Prevista"] - df["Partida Prevista"]).dt.total_seconds() / 60

df["Diferenca_Tempo_Real_Estimado_min"] = df["Tempo_Voo_Real_min"] - df["Tempo_Voo_Estimado_min"]

# Load factor simples, se disponível
if "Quantidade de Passageiros" in df.columns:
    df["Load_Factor_Utilizado"] = (df["Quantidade de Passageiros"] / df["Número de Assentos"]) * 100

# Arredonda valores numéricos relevantes
df["Tempo_Voo_Real_min"] = df["Tempo_Voo_Real_min"].round(2)
df["Tempo_Voo_Estimado_min"] = df["Tempo_Voo_Estimado_min"].round(2)
df["Diferenca_Tempo_Real_Estimado_min"] = df["Diferenca_Tempo_Real_Estimado_min"].round(2)

# Salva resultado
df.to_csv(output_csv, index=False, encoding="utf-8")
logging.info(f"Arquivo gerado: {output_csv}")
