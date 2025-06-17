"""Calcula variáveis adicionais e métricas ambientais para cada voo."""

import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from config import ANALYSIS_DIR

# Configuração do logging com mensagens detalhadas
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos de entrada e saída
input_csv = ANALYSIS_DIR / "FILTRADOS_DADOS.csv"
output_csv = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_V3.csv"

logging.info("Carregando o arquivo de dados filtrados...")
df = pd.read_csv(input_csv, delimiter=",", encoding="utf-8", low_memory=False)
logging.info(f"Arquivo carregado. Total de registros: {df.shape[0]}")

# Lista das colunas essenciais
required_cols = [
    "Modelo Equipamento", "Número de Assentos", "Partida Real", "Chegada Real", 
    "Partida Prevista", "Chegada Prevista", "Sigla ICAO Aeroporto Origem", "Sigla ICAO Aeroporto Destino"
]
for col in required_cols:
    if col not in df.columns:
        logging.error(f"Coluna necessária ausente: {col}")
        exit()

# Extração do ano a partir de "Partida Real", se necessário
if "Ano" not in df.columns:
    logging.info("Coluna 'Ano' não encontrada. Extraindo o ano a partir de 'Partida Real'...")
    df["Partida Real"] = pd.to_datetime(df["Partida Real"], errors="coerce")
    df["Ano"] = df["Partida Real"].dt.year

# Ajuste da coluna "Quantidade de Pousos"
if "Quantidade de Pousos" not in df.columns:
    logging.info("Coluna 'Quantidade de Pousos' não encontrada. Considerando cada linha como 1 pouso.")
    df["Quantidade de Pousos"] = 1
