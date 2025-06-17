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
df = pd.read_csv(input_csv, delimiter=",", encoding="utf-8")
logging.info(f"Planilha carregada. Total de registros: {df.shape[0]}")

# Verifica se a coluna 'Ano do Voo' já existe
coluna_ano_criada = False
if "Ano do Voo" not in df.columns:
    # Se não existir "Ano do Voo", iremos tentar criar a partir de "Chegada Real"
    if "Chegada Real" not in df.columns:
        logging.error("Coluna 'Chegada Real' não encontrada. Não é possível extrair o ano automaticamente.")
        exit()

    logging.info("Tentando criar a coluna 'Ano do Voo' a partir de 'Chegada Real'...")
    # 1) Converte para string e remove espaços
    df["Chegada Real"] = df["Chegada Real"].astype(str).str.strip()

    # 2) Quebra em hora e data, assumindo que o formato seja "HH:MM,DD/MM/AAAA"
    # Caso o seu arquivo tenha outro padrão (ex: "DD/MM/AAAA HH:MM"), ajuste a separação:
    df["DATA_PURA"] = df["Chegada Real"].apply(
        lambda x: x.split(",")[1].strip() if "," in x else None
    )
    # Agora "DATA_PURA" deve ficar no padrão "DD/MM/AAAA" (sem a parte da hora)

    # 3) Converte "DATA_PURA" para datetime
