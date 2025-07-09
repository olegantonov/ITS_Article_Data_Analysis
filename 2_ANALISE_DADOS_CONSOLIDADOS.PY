"""Explora as colunas disponíveis no arquivo consolidado e seus valores únicos."""

import pandas as pd
import unicodedata
from config import ANALYSIS_DIR

# Função para normalizar os nomes das colunas
def normalize_columns(cols):
    return [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8').strip() for col in cols]

# Caminho do arquivo unificado
file_path = ANALYSIS_DIR / "DADOS_CONSOLIDADOS_2010_2024.csv"

# Leitura do cabeçalho
df_header = pd.read_csv(file_path, sep=",", encoding='utf-8', nrows=0, low_memory=False)
df_header.columns = normalize_columns(df_header.columns)

print("Colunas disponíveis no DataFrame:")
print(df_header.columns.tolist())
print("-" * 50)

# Lista de colunas de interesse (já normalizadas)
columns_of_interest = ['Modelo Equipamento', 'Situacao Voo', 'Codigo DI', 'Codigo Tipo Linha']

# Inicializa dicionário para armazenar os valores únicos
unique_values = {col: set() for col in columns_of_interest}

# Tamanho do chunk
chunk_size = 500000
chunks_processed = 0

# Processa o arquivo em chunks
for chunk in pd.read_csv(file_path, sep=",", encoding='utf-8', low_memory=False,
                         chunksize=chunk_size, on_bad_lines='skip'):
    chunk.columns = normalize_columns(chunk.columns)
    
    for col in columns_of_interest:
        if col in chunk.columns:
            unique_values[col].update(chunk[col].dropna().unique())
        else:
            print(f"A coluna '{col}' não foi encontrada no chunk atual.")
    
    chunks_processed += 1
    print(f"Processado chunk {chunks_processed} com {chunk.shape[0]} linhas.")

# Relatório final
print("\n--- Relatório Final dos Valores Únicos ---")
for col in columns_of_interest:
    print(f"Valores únicos para a coluna '{col}':")
    print(unique_values[col])
    print("-" * 50)
