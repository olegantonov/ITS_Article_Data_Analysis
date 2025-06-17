import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Configuração do logging com mensagens detalhadas
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Caminhos dos arquivos de entrada e saída
input_csv = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\FILTRADOS_DADOS.csv"
output_csv = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\ANALISE_VOO_DETALHADA_V3.csv"

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
else:
    df["Quantidade de Pousos"] = pd.to_numeric(df["Quantidade de Pousos"], errors="coerce")

# Dicionário de mapeamento de rotas e distâncias (incluindo ida e volta)
dist_dict = {
    ("SBSP", "SBRJ"): 197.3, ("SBRJ", "SBSP"): 197.3,
    ("SBSP", "SBBR"): 471.0, ("SBBR", "SBSP"): 471.0,
    ("SBSP", "SBCF"): 282.7, ("SBCF", "SBSP"): 282.7,
    ("SBPA", "SBGR"): 467.0, ("SBGR", "SBPA"): 467.0,
    ("SBSV", "SBGR"): 783.6, ("SBGR", "SBSV"): 783.6,
    ("SBRF", "SBGR"): 1133.9, ("SBGR", "SBRF"): 1133.9,
    ("SBSP", "SBPA"): 452.3, ("SBPA", "SBSP"): 452.3,
    ("SBSP", "SBCT"): 178.7, ("SBCT", "SBSP"): 178.7,
    ("SBGR", "SBCT"): 193.7, ("SBCT", "SBGR"): 193.7,
    ("SBGR", "SBCF"): 267.5, ("SBCF", "SBGR"): 267.5,
    ("SBGR", "SBBR"): 460.9, ("SBBR", "SBGR"): 460.9,
    ("SBRJ", "SBBR"): 501.5, ("SBBR", "SBRJ"): 501.5,
    ("SBGR", "SBGL"): 183.4, ("SBGL", "SBGR"): 183.4,
    ("SBGR", "SBFZ"): 1261.9, ("SBFZ", "SBGR"): 1261.9
}

logging.info("Criando a coluna 'Distância (NM)' a partir dos aeroportos de origem e destino...")
df["Distância (NM)"] = df.apply(
    lambda row: dist_dict.get(
        (row["Sigla ICAO Aeroporto Origem"].strip(), row["Sigla ICAO Aeroporto Destino"].strip()),
        np.nan
    ),
    axis=1
)

# Converter colunas numéricas para os tipos corretos
df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce")
df["Número de Assentos"] = pd.to_numeric(df["Número de Assentos"], errors="coerce")
df["Distância (NM)"] = pd.to_numeric(df["Distância (NM)"], errors="coerce")

# Converter colunas de data/hora para datetime
df["Partida Real"] = pd.to_datetime(df["Partida Real"], errors="coerce")
df["Chegada Real"] = pd.to_datetime(df["Chegada Real"], errors="coerce")
df["Partida Prevista"] = pd.to_datetime(df["Partida Prevista"], errors="coerce")
df["Chegada Prevista"] = pd.to_datetime(df["Chegada Prevista"], errors="coerce")

# Remover registros com dados essenciais faltantes
df = df.dropna(subset=required_cols + ["Ano", "Quantidade de Pousos", "Distância (NM)"])
logging.info(f"Registros após limpeza: {df.shape[0]}")

# Tabela de consumo de combustível (kg) para pontos específicos (distâncias em NM)
consumo_tables = {
    "A320": {125: 1672, 250: 3430, 500: 4585, 750: 6212, 1000: 7772, 1500: 10766},
    "A319": {125: 1596, 250: 3259, 500: 4323, 750: 5830, 1000: 7271, 1500: 10026},
    "B738": {125: 1715, 250: 3494, 500: 4621, 750: 6221, 1000: 7749, 1500: 10666},
    "B737": {125: 1695, 250: 3439, 500: 4515, 750: 6053, 1000: 7517, 1500: 10304},
    "A321": {125: 1909, 250: 3925, 500: 5270, 750: 7157, 1000: 8970, 1500: 12456}
}

# Fator de conversão para emissão de CO₂: 3.16 kg CO₂ por kg de combustível
CO2_factor = 3.16

# Dicionário de load factor com valores convertidos para fração (de 2010 a 2024)
load_factor_dict = {
    2010: 0.787,
    2011: 0.785,
    2012: 0.794,
    2013: 0.797,
    2014: 0.799,
    2015: 0.804,
    2016: 0.802,
    2017: 0.815,
    2018: 0.819,
    2019: 0.826,
    2020: 0.652,
    2021: 0.669,
    2022: 0.787,
    2023: 0.822,
    2024: 0.83
}

def interpolate_consumo(modelo, distancia):
    """
    Interpola o consumo de combustível (kg) para um dado modelo e uma distância (NM).
    Retorna NaN se o modelo não estiver na tabela ou se não houver dado para a distância.
    """
    if modelo not in consumo_tables:
        logging.warning(f"Sem dados de consumo para a aeronave '{modelo}'.")
        return np.nan
    
    table = consumo_tables[modelo]
    distancias = np.array(sorted(table.keys()))
    consumos = np.array([table[d] for d in distancias])
    consumo_estimado = np.interp(distancia, distancias, consumos)
    
    if np.isnan(consumo_estimado):
        logging.warning(f"Sem dados de consumo interpolado para a aeronave '{modelo}' na distância {distancia} NM.")
    
    return consumo_estimado

def calcular_valores(row):
    """
    Calcula os indicadores para cada voo:
      - Consumo de Combustível (kg) via interpolação.
      - Emissão de CO₂ (kg) do voo.
      - Passageiros estimados (Número de Assentos * load factor do ano).
      - Tempo de Voo Real (min).
      - Tempo de Voo Estimado (min).
      - Load Factor Utilizado.
      - Ano do Voo.

    Observações:
      - Qualquer valor negativo de Tempo_Voo_Real_min será removido posteriormente.
    """
    modelo = row["Modelo Equipamento"].strip()
    distancia = row["Distância (NM)"]
    consumo_flight = interpolate_consumo(modelo, distancia)
    
    co2_flight = consumo_flight * CO2_factor if not np.isnan(consumo_flight) else np.nan
    ano = row["Ano"]
    lf = load_factor_dict.get(ano, 0.82)  # Valor padrão caso o ano não esteja especificado
    passageiros_flight = row["Número de Assentos"] * lf

    # Cálculo do tempo de voo real (min)
    tempo_real = np.nan
    if pd.notna(row["Chegada Real"]) and pd.notna(row["Partida Real"]):
        diff = (row["Chegada Real"] - row["Partida Real"]).total_seconds() / 60
        tempo_real = diff

    # Cálculo do tempo de voo estimado (min)
    tempo_estimado = np.nan
    if pd.notna(row["Chegada Prevista"]) and pd.notna(row["Partida Prevista"]):
        diff_est = (row["Chegada Prevista"] - row["Partida Prevista"]).total_seconds() / 60
        tempo_estimado = diff_est

    return pd.Series({
        "Ano do Voo": ano,
        "Consumo_CO2_do_Voo_kg": co2_flight,
        "Consumo_Combustível_kg": consumo_flight,
        "Distância_Rota_NM": distancia,
        "Load_Factor_Utilizado": lf,
        "Passageiros_Estimados": passageiros_flight,
        "Tempo_Voo_Real_min": tempo_real,
        "Tempo_Voo_Estimado_min": tempo_estimado
    })

logging.info("Calculando indicadores para cada voo...")
valores = df.apply(calcular_valores, axis=1)
df_final = pd.concat([df, valores], axis=1)

# Evitar divisão por zero no cálculo de emissão de CO₂ por passageiro
df_final["Consumo_CO2_por_Passageiro_kg"] = np.where(
    df_final["Passageiros_Estimados"] > 0,
    df_final["Consumo_CO2_do_Voo_kg"] / df_final["Passageiros_Estimados"],
    np.nan
)

# Excluir voos com tempo de voo negativo
logging.info("Excluindo voos com tempo de voo real negativo (erro de registro)...")
registros_iniciais = df_final.shape[0]
df_final = df_final[df_final["Tempo_Voo_Real_min"] >= 0]
registros_negativos_excluidos = registros_iniciais - df_final.shape[0]
logging.info(f"{registros_negativos_excluidos} voos excluídos por tempo de voo negativo.")

# Remover voos cujo tempo de voo seja nulo (NaN) após conversão
df_final = df_final.dropna(subset=["Tempo_Voo_Real_min"])
logging.info(f"Após remover tempos nulos, total de registros: {df_final.shape[0]}")

# Salvar o DataFrame final
df_final.to_csv(output_csv, index=False, encoding="utf-8")
logging.info(f"Arquivo salvo: {output_csv}")

# -------------------
# Relatório Resumido
# -------------------
relatorio = f"""
RELATÓRIO FINAL
------------------------
Registros iniciais após limpeza:  {registros_iniciais}
Voos excluídos por tempo negativo: {registros_negativos_excluidos}
Registros finais (voos válidos):   {df_final.shape[0]}

Observações:
 - Divisão por zero evitada no cálculo de CO₂ por passageiro (atribui-se NaN se passageiros estimados <= 0).
 - Caso a aeronave ou distância não existam na tabela de consumo, logamos um aviso e consumo fica como NaN.
 - Voos com Tempo_Voo_Real_min < 0 foram excluídos como erro de registro.
 - Registros sem Tempo_Voo_Real_min (NaN) também foram removidos.
"""

logging.info(relatorio)
print(relatorio)
