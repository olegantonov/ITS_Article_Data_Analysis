"""Gera um arquivo contendo apenas os voos com tempos real e estimado diferentes."""

import pandas as pd
from config import ANALYSIS_DIR

# Caminho para o arquivo CSV original
caminho_arquivo = ANALYSIS_DIR / "ANALISE_VOO_DETALHADA_v2.csv"

# Lê o arquivo CSV em um DataFrame (ajuste delimitador e encoding se necessário)
df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8')

# Filtra apenas as linhas em que Tempo_Voo_Real_min ≠ Tempo_Voo_Estimado_min
df_diferentes = df[df['Tempo_Voo_Real_min'] != df['Tempo_Voo_Estimado_min']]

# Remove valores negativos na coluna Tempo_Voo_Real_min
df_diferentes_sem_negativos = df_diferentes[df_diferentes['Tempo_Voo_Real_min'] >= 0]

# Exibe relatório da filtragem
total_inicial = len(df)
total_diferentes = len(df_diferentes)
total_sem_negativos = len(df_diferentes_sem_negativos)

print(f"Total de voos no arquivo: {total_inicial}")
print(f"Total de voos onde Tempo_Voo_Real_min ≠ Tempo_Voo_Estimado_min: {total_diferentes}")
print(f"Total de voos (sem negativos) onde Tempo_Voo_Real_min ≠ Tempo_Voo_Estimado_min: {total_sem_negativos}")

# Caminho para o arquivo de saída (versão apenas com as linhas filtradas)
caminho_arquivo_saida = caminho_arquivo.replace(".csv", "_tempo_diferente.csv")

# Salva o DataFrame filtrado em um novo CSV
df_diferentes_sem_negativos.to_csv(caminho_arquivo_saida, index=False, sep=',', encoding='utf-8')
print(f"Arquivo gerado: {caminho_arquivo_saida}")
