"""Consolida os arquivos CSV anuais em um único conjunto de dados."""

import glob
import logging
import os
from pathlib import Path

import pandas as pd
from config import RAW_DIR, ANALYSIS_DIR

# Configuração do logging com mensagens detalhadas
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define o caminho base e o diretório de saída
base_path = RAW_DIR
output_dir = ANALYSIS_DIR
output_file = output_dir / "DADOS_CONSOLIDADOS_2010_2024.csv"

# Verifica se o caminho base existe
if not base_path.exists():
    raise FileNotFoundError(
        f"O caminho {base_path} não foi encontrado. Verifique se o diretório está correto."
    )

# Cria o diretório de saída, se não existir
output_dir.mkdir(parents=True, exist_ok=True)

# Lista para registrar inconsistências de colunas entre os arquivos
inconsistencies = []

# Identifica as subpastas cujo nome é um ano (ex: 2010, 2011, etc.)
year_folders = [
    base_path / folder
    for folder in os.listdir(base_path)
    if (base_path / folder).is_dir() and folder.isdigit()
]

if not year_folders:
    raise FileNotFoundError("Nenhuma subpasta com nome numérico (ano) encontrada em " + base_path)

# Coleta os caminhos de todos os arquivos CSV presentes nas subpastas dos anos
csv_files = []
for folder in year_folders:
    folder_files = glob.glob(str(Path(folder) / '*.csv'))
    csv_files.extend(folder_files)

if not csv_files:
    raise FileNotFoundError("Nenhum arquivo CSV encontrado nas subpastas em " + base_path)

# Primeira passagem: calcule a união de todas as colunas (lendo apenas os cabeçalhos)
union_columns = set()
for file_path in csv_files:
    try:
        temp_df = pd.read_csv(file_path, delimiter=';', encoding='utf-8', nrows=0, low_memory=False)
        temp_df.columns = temp_df.columns.str.strip()  # Remove espaços extras
        union_columns = union_columns.union(set(temp_df.columns))
    except Exception as e:
        inconsistencies.append(f"Erro ao ler cabeçalho de {file_path}: {str(e)}")

# Define uma ordem final para as colunas:
# Mantém a ordem do primeiro arquivo e, em seguida, acrescenta as colunas extras (em ordem alfabética)
first_file = csv_files[0]
first_df = pd.read_csv(first_file, delimiter=';', encoding='utf-8', nrows=0, low_memory=False)
first_df.columns = first_df.columns.str.strip()
baseline_cols = list(first_df.columns)
extra_cols = sorted(list(union_columns.difference(baseline_cols)))
final_columns_order = baseline_cols + extra_cols

print("Colunas unificadas definidas:")
print(final_columns_order)

# Inicializa variáveis de controle
header_flag = True
total_files_processed = 0
total_chunks_processed = 0
total_rows_processed = 0

# Processa os arquivos em chunks
for file_path in csv_files:
    try:
        for chunk_number, chunk in enumerate(pd.read_csv(file_path, delimiter=';', encoding='utf-8',
                                                         chunksize=100_000, low_memory=False)):
            chunk.columns = chunk.columns.str.strip()

            # Adiciona colunas ausentes com valores nulos
            for col in final_columns_order:
                if col not in chunk.columns:
                    chunk[col] = None

            # Reordena as colunas
            chunk = chunk[final_columns_order]

            # Escreve o chunk no CSV consolidado
            chunk.to_csv(output_file, mode="a", index=False, header=header_flag, encoding='utf-8', errors='replace')
            header_flag = False

            total_chunks_processed += 1
            total_rows_processed += len(chunk)

            logging.info(f"Arquivo: {file_path} - Processado chunk {chunk_number} com {chunk.shape[0]} linhas.")

        total_files_processed += 1

    except Exception as e:
        inconsistencies.append(f"Erro ao processar {file_path}: {str(e)}")
        continue

# Relatório final
logging.info(f"\nDados unificados salvos em: {output_file}")
print("\n--- Relatório Final ---")
print(f"Total de arquivos processados: {total_files_processed
