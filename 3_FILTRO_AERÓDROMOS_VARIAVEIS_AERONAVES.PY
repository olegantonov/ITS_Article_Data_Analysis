import pandas as pd
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos de entrada e saída
input_file = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\DADOS_CONSOLIDADOS_2010_2024.csv"
output_file = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\FILTRADOS_DADOS.csv"

# Conjuntos permitidos (todos em caixa alta)
allowed_models = {"B738", "A320", "A319", "B737", "A321"}
allowed_codigo_tipo_linha = {"N", "C"}
allowed_codigo_di = {"0", "4", "C"}
# Note que, para rotas, usamos o formato ordenado (isto é, sorted([origem, destino]) juntado com '-'):
allowed_routes = {
    "SBRJ-SBSP",  # SBSP e SBRJ => sorted: ["SBRJ", "SBSP"]
    "SBBR-SBSP",  # SBSP e SBBR => ["SBBR", "SBSP"]
    "SBCF-SBSP",  # SBSP e SBCF => ["SBCF", "SBSP"]
    "SBPA-SBGR",  # SBPA e SBGR => ["SBPA", "SBGR"]
    "SBGR-SBSV",  # SBSV e SBGR => ["SBGR", "SBSV"]
    "SBGR-SBRF",  # SBRF e SBGR => ["SBGR", "SBRF"]
    "SBPA-SBSP",  # SBSP e SBPA => ["SBPA", "SBSP"]
    "SBCT-SBSP",  # SBSP e SBCT => ["SBCT", "SBSP"]
    "SBCT-SBGR",  # SBGR e SBCT => ["SBCT", "SBGR"]
    "SBCF-SBGR",  # SBGR e SBCF => ["SBCF", "SBGR"]
    "SBBR-SBGR",  # SBGR e SBBR => ["SBBR", "SBGR"]
    "SBBR-SBRJ",  # SBRJ e SBBR => ["SBBR", "SBRJ"]
    "SBGL-SBGR",  # SBGR e SBGL => ["SBGL", "SBGR"]
    "SBFZ-SBGR"   # SBGR e SBFZ => ["SBFZ", "SBGR"]
}

# Tamanho do chunk para processamento (ajuste conforme necessário)
chunk_size = 100000
header_flag = True  # Cabeçalho é escrito somente no primeiro chunk
chunks_processed = 0
total_rows_filtered = 0

logging.info("Iniciando processamento e filtragem dos dados...")

# Processa o arquivo em chunks
for chunk in pd.read_csv(input_file, sep=",", encoding="utf-8", low_memory=False, chunksize=chunk_size):
    chunks_processed += 1
    
    # Remove espaços extras nos nomes das colunas
    chunk.columns = chunk.columns.str.strip()
    
    # Garante que "Partida Real" e "Chegada Real" estejam preenchidos
    chunk = chunk[chunk["Partida Real"].notna() & chunk["Chegada Real"].notna()]
    
    # Normaliza os valores para os filtros
    situacao = chunk["Situação Voo"].astype(str).str.strip().str.upper()
    codigo_tipo = chunk["Código Tipo Linha"].astype(str).str.strip().str.upper()
    codigo_di = chunk["Código DI"].astype(str).str.strip().str.upper()
    modelo = chunk["Modelo Equipamento"].astype(str).str.strip().str.upper()
    
    origem = chunk["Sigla ICAO Aeroporto Origem"].astype(str).str.strip().str.upper()
    destino = chunk["Sigla ICAO Aeroporto Destino"].astype(str).str.strip().str.upper()
    # Cria a rota ordenada para que ida e volta sejam equivalentes
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
    
    # Grava o chunk filtrado no arquivo de saída (modo append)
    filtered_chunk.to_csv(output_file, mode="a", index=False, header=header_flag, encoding="utf-8", errors="replace")
    header_flag = False

logging.info(f"Processamento concluído. Total de chunks processados: {chunks_processed}")
logging.info(f"Total de linhas filtradas: {total_rows_filtered}")
logging.info(f"Novo arquivo filtrado salvo em: {output_file}")
