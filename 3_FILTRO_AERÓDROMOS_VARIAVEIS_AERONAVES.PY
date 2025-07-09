"""Filtra o conjunto consolidado para rotas e aeronaves de interesse."""

import logging
from pathlib import Path

import pandas as pd
from config import ANALYSIS_DIR

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos de entrada e saída
input_file = ANALYSIS_DIR / "DADOS_CONSOLIDADOS_2010_2024.csv"
output_file = ANALYSIS_DIR / "FILTRADOS_DADOS.csv"

# Conjuntos permitidos (todos em caixa alta)
allowed_models = {"B738", "A320", "A319", "B737", "A321"}
allowed_codigo_tipo_linha = {"N", "C"}
allowed_codigo_di = {"0", "4", "C"}
allowed_routes = {
    "SBRJ-SBSP", "SBBR-SBSP", "SBCF-SBSP", "SBPA-SBGR", "SBGR-SBSV", "SBGR-SBRF",
    "SBPA-SBSP", "SBCT-SBSP", "SBCT-SBGR", "SBCF-SBGR", "SBBR-SBGR", "SBBR-SBRJ",
    "SBGL-SBGR", "SBFZ-SBGR"
}

# Tamanho do chunk para processamento
chunk_size = 100000

# Inicializa variáveis de controle
chunks_processed = 0
total_rows_filtered = 0
header_flag = True

# Leitura e filtragem em chunks
for chunk in pd.read_csv(input_file, sep=",", encoding="utf-8", low_memory=False, chunksize=chunk_size):
    chunks_processed += 1

    situacao = chunk["Situação Voo"].astype(str).str.strip().str.upper()
    codigo_tipo = chunk["Código Tipo Linha"].astype(str).str.strip().str.upper()
    codigo_di = chunk["Código DI"].astype(str).str.strip().str.upper()
    modelo = chunk["Modelo Equipamento"].astype(str).str.strip().str.upper()

    origem = chunk["Sigla ICAO Aeroporto Origem"].astype(str).str.strip().str.upper()
    destino = chunk["Sigla ICAO Aeroporto Destino"].astype(str).str.strip().str.upper()
    sorted_route = origem.combine(destino, lambda o, d: "-".join(sorted([o, d])))

    # Aplica os filtros
    mask = (
        (situacao == "REALIZADO") &
        (codigo_tipo.isin(allowed_codigo_tipo_linha)) &
        (codigo_di.isin(allowed_codigo_di)) &
        (modelo.isin(allowed_models)) &
        (sorted_route.isin(allowed_routes))
    )
    filtered_chunk = chunk[mask]
    total_rows_filtered += filtered_chunk.shape[0]

    logging.info(f"Chunk {chunks_processed}: {chunk.shape[0]} linhas lidas; {filtered_chunk.shape[0]} linhas filtradas.")

    # Grava o resultado no arquivo
    filtered_chunk.to_csv(output_file, mode="a", index=False, header=header_flag, encoding="utf-8", errors="replace")
    header_flag = False

# Finalização
logging.info(f"Processamento concluído. Total de chunks processados: {chunks_processed}")
logging.info(f"Total de linhas filtradas: {total_rows_filtered}")
logging.info(f"Novo arquivo filtrado salvo em: {output_file}")
