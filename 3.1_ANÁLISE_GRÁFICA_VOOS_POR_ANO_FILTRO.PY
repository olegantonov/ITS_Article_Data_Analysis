import matplotlib
matplotlib.use("Agg")  # Backend não interativo para evitar problemas com Tcl/Tk

import pandas as pd
import matplotlib.pyplot as plt
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos de entrada e saída
input_csv = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\FILTRADOS_DADOS.csv"
output_image_year = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\FILTRO_voos_por_ANO.png"
output_image_route = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\FILTRO_voos_por_ROTA.png"

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
    # Se o seu formato for diferente, adapte em "format=".
    df["DATA_PURA"] = pd.to_datetime(df["DATA_PURA"], format="%d/%m/%Y", errors="coerce")

    # 4) Cria "Ano do Voo" a partir do ano de "DATA_PURA"
    df["Ano do Voo"] = df["DATA_PURA"].dt.year
    coluna_ano_criada = True

# Verifica quantos valores ficaram sem data após o parsing
if "Ano do Voo" not in df.columns:
    logging.error("Não foi possível criar ou identificar a coluna de ano ('Ano do Voo'). Abortando.")
    exit()

nat_count = df["Ano do Voo"].isna().sum()
logging.info(f"Número de registros sem ano parseado (NaT): {nat_count}")

# --------------------
# GRÁFICO 1: Voos por Ano
# --------------------
voos_por_ano = df["Ano do Voo"].value_counts().sort_index()
if len(voos_por_ano) == 0:
    logging.warning("A série de voos por ano está vazia. O gráfico não será gerado.")
else:
    plt.figure(figsize=(10, 6))
    voos_por_ano.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Quantidade de Voos por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Número de Voos")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_image_year)
    plt.close()
    logging.info(f"Gráfico de voos por ano salvo em: {output_image_year}")

# --------------------
# GRÁFICO 2: Voos por Rota
# --------------------
if "Sigla ICAO Aeroporto Origem" in df.columns and "Sigla ICAO Aeroporto Destino" in df.columns:
    df["Rota"] = (
        df["Sigla ICAO Aeroporto Origem"].astype(str).str.strip()
        + " -> "
        + df["Sigla ICAO Aeroporto Destino"].astype(str).str.strip()
    )
    voos_por_rota = df["Rota"].value_counts().sort_values(ascending=False)

    if len(voos_por_rota) == 0:
        logging.warning("A série de voos por rota está vazia. O gráfico não será gerado.")
    else:
        plt.figure(figsize=(12, 8))
        voos_por_rota.plot(kind="bar", color="lightgreen", edgecolor="black")
        plt.title("Quantidade de Voos por Rota")
        plt.xlabel("Rota")
        plt.ylabel("Número de Voos")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_image_route)
        plt.close()
        logging.info(f"Gráfico de voos por rota salvo em: {output_image_route}")
else:
    logging.warning("Colunas de origem/destino não encontradas. Gráfico de voos por rota não será gerado.")

# --------------------
# Remove a coluna de ano criada, se necessário
# --------------------
if coluna_ano_criada:
    logging.info("Excluindo a coluna 'Ano do Voo' para manter os dados originais inalterados...")
    df.drop(columns=["Ano do Voo", "DATA_PURA"], inplace=True, errors="ignore")
    logging.info("Colunas 'Ano do Voo' e 'DATA_PURA' removidas.")
