import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# ⚠️ SOLUÇÃO DO PROBLEMA COM TKINTER: Muda o backend do Matplotlib para não usar interface gráfica
matplotlib.use('Agg')  # Define o backend sem GUI para evitar erro do Tcl/Tk

# Caminho do arquivo CSV
caminho_arquivo = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\ANALISE_VOO_DETALHADA_v2.csv"

# ⚠️ SOLUÇÃO DO DTYPEWARNING: Especifica `dtype` para colunas problemáticas e usa `low_memory=False`
dtype_especifico = {
    "Número Voo": str,  # Número do voo pode ter valores misturados, força como string
    "Justificativa": str  # Justificativa pode conter texto ou valores nulos, forçamos como string
}

# Carregar os dados corrigindo os problemas de dtype
df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8', dtype=dtype_especifico, low_memory=False)

# Certificar-se de que a coluna "Ano do Voo" existe e está no formato correto
df['Ano'] = pd.to_numeric(df['Ano do Voo'], errors='coerce')

# Remover voos com tempos negativos (caso existam)
df = df[df['Tempo_Voo_Real_min'] >= 0]

# Criar DataFrame com estatísticas anuais
df_analise = df.groupby('Ano').agg(
    Tempo_Medio=('Tempo_Voo_Real_min', 'mean'),
    Tempo_Minimo=('Tempo_Voo_Real_min', 'min'),
    Tempo_Maximo=('Tempo_Voo_Real_min', 'max')
).reset_index()

# Criar ranking de aeronaves mais utilizadas por ano
df_ranking = df.groupby(['Ano', 'Modelo Equipamento']).size().reset_index(name='Voos')
df_ranking = df_ranking.sort_values(by=['Ano', 'Voos'], ascending=[True, False])

# Criar gráfico de linha para mostrar a evolução do tempo médio de voo ao longo dos anos
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_analise, x='Ano', y='Tempo_Medio', marker='o')
plt.title('Evolução do Tempo Médio de Voo (Ano a Ano)')
plt.xlabel('Ano')
plt.ylabel('Tempo Médio de Voo (min)')
plt.grid(True)

# ⚠️ Salvar o gráfico ao invés de exibir (evita erro com interface gráfica)
plt.savefig("evolucao_tempo_voo.png")
plt.close()

# Criar gráfico de barras para visualizar o ranking das aeronaves mais utilizadas por ano
plt.figure(figsize=(12, 6))
sns.barplot(data=df_ranking, x='Ano', y='Voos', hue='Modelo Equipamento', dodge=False)
plt.title('Aeronaves Mais Utilizadas por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Voos')
plt.legend(title="Modelo de Aeronave", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(axis='y')

# ⚠️ Salvar o gráfico ao invés de exibir
plt.savefig("ranking_aeronaves.png")
plt.close()

# Exibir os resultados detalhados no terminal
print("\n📊 Análise Estatística de Voos (Tempo Médio, Mínimo e Máximo):")
print(df_analise)

print("\n🏆 Ranking de Aeronaves Mais Utilizadas por Ano:")
print(df_ranking)

print("\n✅ Gráficos salvos como 'evolucao_tempo_voo.png' e 'ranking_aeronaves.png'")
