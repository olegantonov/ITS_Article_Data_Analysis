import pandas as pd

# Caminho do arquivo unificado
file_path = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\DADOS_CONSOLIDADOS_2010_2024.csv"

# Carrega um chunk para investigação (ajuste nrows conforme necessário)
df = pd.read_csv(file_path, sep=",", encoding="utf-8", low_memory=False, nrows=100000)

# Normaliza os valores removendo espaços e convertendo para caixa alta
df["Situação Voo_norm"] = df["Situação Voo"].astype(str).str.strip().str.upper()
df["Código Tipo Linha_norm"] = df["Código Tipo Linha"].astype(str).str.strip().str.upper()
df["Código DI_norm"] = df["Código DI"].astype(str).str.strip().str.upper()
df["Modelo Equipamento_norm"] = df["Modelo Equipamento"].astype(str).str.strip().str.upper()
df["Sigla ICAO Aeroporto Origem_norm"] = df["Sigla ICAO Aeroporto Origem"].astype(str).str.strip().str.upper()
df["Sigla ICAO Aeroporto Destino_norm"] = df["Sigla ICAO Aeroporto Destino"].astype(str).str.strip().str.upper()

# Exibe os valores únicos e suas contagens para as colunas de interesse
print("Valores únicos e contagens para 'Situação Voo':")
print(df["Situação Voo_norm"].value_counts())
print("\nValores únicos e contagens para 'Código Tipo Linha':")
print(df["Código Tipo Linha_norm"].value_counts())
print("\nValores únicos e contagens para 'Código DI':")
print(df["Código DI_norm"].value_counts())
print("\nValores únicos e contagens para 'Modelo Equipamento':")
print(df["Modelo Equipamento_norm"].value_counts())

# Para investigar as rotas: cria uma coluna com a rota ordenada (para considerar ida e volta como a mesma)
df["Rota_norm"] = df["Sigla ICAO Aeroporto Origem_norm"].combine(
    df["Sigla ICAO Aeroporto Destino_norm"],
    lambda o, d: "-".join(sorted([o, d]))
)

print("\nRotas (ordenadas) e contagens:")
print(df["Rota_norm"].value_counts())
