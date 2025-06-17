import os
import glob
import pandas as pd
import logging

# Configuração do logging com mensagens detalhadas
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define o caminho base e o diretório de saída
base_path = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\docs"
output_dir = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL"
output_file = os.path.join(output_dir, 'DADOS_CONSOLIDADOS_2010_2024.csv')

# Verifica se o caminho base existe
if not os.path.exists(base_path):
    raise FileNotFoundError(f"O caminho {base_path} não foi encontrado. Verifique se o diretório está correto.")

# Cria o diretório de saída, se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Lista para registrar inconsistências de colunas entre os arquivos
inconsistencies = []

# Identifica as subpastas cujo nome é um ano (ex: 2010, 2011, etc.)
year_folders = [os.path.join(base_path, folder) for folder in os.listdir(base_path)
                if os.path.isdir(os.path.join(base_path, folder)) and folder.isdigit()]

if not year_folders:
    raise FileNotFoundError("Nenhuma subpasta com nome numérico (ano) encontrada em " + base_path)

# Coleta os caminhos de todos os arquivos CSV presentes nas subpastas dos anos
csv_files = []
for folder in year_folders:
    folder_files = glob.glob(os.path.join(folder, '*.csv'))
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

# Define o tamanho dos chunks para processamento (ajuste conforme a memória disponível)
chunk_size = 200000
header_flag = True  # Escreve o cabeçalho apenas na primeira vez

# Contadores para o relatório final
total_files_processed = 0
total_chunks_processed = 0
total_rows_processed = 0

# Processa cada arquivo CSV encontrado e escreve os dados unificados no arquivo de saída
for file_path in csv_files:
    total_files_processed += 1
    logging.info(f"Processando arquivo: {file_path}")
    try:
        chunk_number = 0
        for chunk in pd.read_csv(file_path, delimiter=';', encoding='utf-8', chunksize=chunk_size, low_memory=False):
            chunk_number += 1
            total_chunks_processed += 1
            total_rows_processed += chunk.shape[0]
            
            # Remove espaços extras nos nomes das colunas
            chunk.columns = chunk.columns.str.strip()
            
            # Adiciona as colunas ausentes com valor NA
            for col in final_columns_order:
                if col not in chunk.columns:
                    chunk[col] = pd.NA
            # Reordena as colunas de acordo com o padrão unificado
            chunk = chunk[final_columns_order]
            
            # Escreve o chunk no arquivo de saída
            chunk.to_csv(output_file, mode="a", index=False, header=header_flag, encoding='utf-8', errors='replace')
            header_flag = False
            
            logging.info(f"Arquivo: {file_path} - Processado chunk {chunk_number} com {chunk.shape[0]} linhas.")
    except Exception as e:
        inconsistencies.append(f"Erro ao processar {file_path}: {str(e)}")
        continue

logging.info(f"\nDados unificados salvos em: {output_file}")

# Relatório final
print("\n--- Relatório Final ---")
print(f"Total de arquivos processados: {total_files_processed}")
print(f"Total de chunks processados: {total_chunks_processed}")
print(f"Total de linhas processadas: {total_rows_processed}")

if inconsistencies:
    print("\nInconsistências encontradas durante o processamento:")
    for inc in inconsistencies:
        print(inc)
else:
    print("\nNenhuma inconsistência encontrada.")
