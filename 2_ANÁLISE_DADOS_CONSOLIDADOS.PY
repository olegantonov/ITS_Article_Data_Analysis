import pandas as pd

# Caminho do arquivo unificado
file_path = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\DADOS_CONSOLIDADOS_2010_2024.csv"

# Primeiro, leia somente o cabeçalho para verificar as colunas disponíveis
df_header = pd.read_csv(file_path, sep=",", encoding='utf-8', nrows=0, low_memory=False)
# Remove espaços extras nos nomes das colunas
df_header.columns = df_header.columns.str.strip()

print("Colunas disponíveis no DataFrame:")
print(df_header.columns.tolist())
print("-" * 50)

# Lista de colunas de interesse
columns_of_interest = ['Modelo Equipamento', 'Situação Voo', 'Código DI', 'Código Tipo Linha']

# Inicializa um dicionário para armazenar os valores únicos de cada coluna (utilizando conjuntos)
unique_values = {col: set() for col in columns_of_interest}

# Tamanho do chunk (ajuste conforme necessário)
chunk_size = 500000
chunks_processed = 0

# Processa o arquivo em chunks utilizando o separador correto
for chunk in pd.read_csv(file_path, sep=",", encoding='utf-8', low_memory=False, chunksize=chunk_size):
    # Remove espaços extras nos nomes das colunas
    chunk.columns = chunk.columns.str.strip()
    
    # Verifica cada coluna de interesse e atualiza os conjuntos de valores únicos
    for col in columns_of_interest:
        if col in chunk.columns:
            unique_values[col].update(chunk[col].dropna().unique())
        else:
            print(f"A coluna '{col}' não foi encontrada no chunk atual.")
    
    chunks_processed += 1
    print(f"Processado chunk {chunks_processed} com {chunk.shape[0]} linhas.")

# Relatório final: exibe os valores únicos de cada coluna de interesse
print("\n--- Relatório Final dos Valores Únicos ---")
for col in columns_of_interest:
    print(f"Valores únicos para a coluna '{col}':")
    print(unique_values[col])
    print("-" * 50)
