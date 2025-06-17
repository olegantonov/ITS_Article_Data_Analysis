import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan

# 1. Leitura dos dados
caminho_arquivo = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\ANÁLISE_FINAL\ANALISE_VOO_DETALHADA_v2_tempo_diferente.csv"
df = pd.read_csv(caminho_arquivo, low_memory=False)

# 2. Conversão das colunas numéricas e imputação de valores faltantes com a mediana
colunas_numericas = ['Ano', 'Distância_Rota_NM', 'Load_Factor_Utilizado', 'Número de Assentos',
                     'Tempo_Voo_Real_min', 'Consumo_Combustível_kg', 'Consumo_CO2_do_Voo_kg']
for col in colunas_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

# 3. Dados de implantação do PBN
implantation_dates = {
    'SBCF': '12/11/2015',
    'SBBR': '12/11/2015',
    'SBCT': '12/10/2017',
    'SBFZ': None,   # Dados não disponíveis
    'SBPA': '12/10/2017',
    'SBRF': '08/04/2010',
    'SBRJ': '28/07/2011',
    'SBGL': '28/07/2011',
    'SBSV': '27/04/2017',
    'SBSP': '12/11/2015',
    'SBGR': '12/11/2015'
}
implantation_years = {}
for icao, date_str in implantation_dates.items():
    if date_str is None or str(date_str).strip() == '':
        implantation_years[icao] = 0
    else:
        dt = datetime.strptime(date_str, '%d/%m/%Y')
        implantation_years[icao] = dt.year

df['Ano'] = df['Ano'].astype(int)

# 4. Cálculo dos valores de PBN para cada voo
def compute_PBNTMA(ano_voo, ano_implantacao):
    if ano_implantacao == 0:
        return 0
    if ano_voo >= ano_implantacao:
        return min(ano_voo - ano_implantacao, 2024 - ano_implantacao)
    return 0

df['PBN_orig'] = df.apply(lambda row: compute_PBNTMA(row['Ano'], implantation_years.get(row['Sigla ICAO Aeroporto Origem'], 0)), axis=1)
df['PBN_dest'] = df.apply(lambda row: compute_PBNTMA(row['Ano'], implantation_years.get(row['Sigla ICAO Aeroporto Destino'], 0)), axis=1)
df['PBN'] = (df['PBN_orig'] + df['PBN_dest']) / 2

# 5. Tratamento da variável categórica "Modelo Equipamento"
df = pd.get_dummies(df, columns=['Modelo Equipamento'], drop_first=True)

# 6. Definição das variáveis independentes
indep_vars = ['PBN', 'Distância_Rota_NM']
dummy_cols = [col for col in df.columns if col.startswith('Modelo Equipamento_')]
X_base = df[indep_vars + dummy_cols].copy()

# Converte X_base para numérico e preenche valores faltantes
X_base = X_base.apply(pd.to_numeric, errors='coerce')
for col in X_base.columns:
    X_base[col] = X_base[col].fillna(X_base[col].median())

# Função para ajustar o modelo e realizar diagnósticos
def ajustar_modelo(y, X, outcome_label):
    # Adiciona o intercepto
    X_model = sm.add_constant(X)
    
    # Converte todas as colunas para float para evitar problemas de dtype
    X_model = X_model.astype(float)
    y = y.astype(float)
    
    # Ajusta o modelo usando OLS com erros robustos (HC3)
    modelo = sm.OLS(y, X_model).fit(cov_type='HC3')
    
    print(f"\n=== Modelo para {outcome_label} ===")
    print(modelo.summary())
    
    # Teste de Breusch-Pagan para heterocedasticidade
    bp_test = het_breuschpagan(modelo.resid, X_model)
    bp_labels = ['Lagrange multiplier statistic', 'p-value', 'f-value', 'f p-value']
    print("\nTeste de Breusch-Pagan:")
    for label, value in zip(bp_labels, bp_test):
        print(f"{label}: {value:.4f}")
    
    # Identificação de observações influentes via Cook's Distance
    influence = modelo.get_influence()
    cooks = influence.cooks_distance[0]
    high_influence = np.where(cooks > 4 / len(X_model))[0]
    if len(high_influence) > 0:
        print("\nObservações com alta influência (Cook's distance > 4/n):")
        print(high_influence)
    else:
        print("\nNenhuma observação com alta influência identificada (Cook's distance).")
    
    # Análise dos resíduos: Histograma e QQ-Plot
    residuos = modelo.resid
    plt.figure(figsize=(6,4))
    sns.histplot(residuos, kde=True, color='blue')
    plt.title(f"Histograma dos Resíduos - {outcome_label}")
    plt.xlabel("Resíduos")
    plt.ylabel("Frequência")
    plt.savefig(f"hist_residuos_{outcome_label}.png")  # Salva o gráfico em um arquivo
    plt.close()
    
    sm.qqplot(residuos, line='45', fit=True)
    plt.title(f"QQ-Plot dos Resíduos - {outcome_label}")
    plt.savefig(f"qqplot_residuos_{outcome_label}.png")
    plt.close()
    
    # Teste de normalidade: D’Agostino & Pearson
    dagostino_stat, dagostino_pvalor = st.normaltest(residuos)
    print(f"\nTeste de D'Agostino & Pearson para {outcome_label}:")
    print(f"Estatística: {dagostino_stat:.4f}, p-valor: {dagostino_pvalor:.6f}")
    if dagostino_pvalor < 0.05:
        print("Conclusão: Resíduos NÃO seguem distribuição normal.")
    else:
        print("Conclusão: Não rejeitamos hipótese de normalidade.")
    
    # Verifica o efeito da variável PBN
    coef_pbn = modelo.params.get('PBN', float('nan'))
    pvalor_pbn = modelo.pvalues.get('PBN', float('nan'))
    print(f"\nEfeito da variável PBN em {outcome_label}:")
    print(f"Coeficiente: {coef_pbn:.4f}, p-valor: {pvalor_pbn:.6f}")
    if coef_pbn < 0 and pvalor_pbn < 0.05:
        print("Interpretação: Maior implantação de PBN está associada a uma redução significativa em", outcome_label)
    elif coef_pbn > 0 and pvalor_pbn < 0.05:
        print("Interpretação: Maior implantação de PBN está associada a um aumento significativo em", outcome_label)
    else:
        print("Interpretação: O efeito da variável PBN não é estatisticamente significativo.")
    
    return modelo

# 7. Ajuste dos modelos para os diferentes desfechos

# 7.1. Modelo para Tempo de Voo Real (min)
y_tempo = pd.to_numeric(df['Tempo_Voo_Real_min'], errors='coerce').fillna(df['Tempo_Voo_Real_min'].median())
modelo_tempo = ajustar_modelo(y_tempo, X_base, "Tempo de Voo Real (min)")

# 7.2. Modelo para Consumo de Combustível (kg)
y_combustivel = pd.to_numeric(df['Consumo_Combustível_kg'], errors='coerce').fillna(df['Consumo_Combustível_kg'].median())
modelo_combustivel = ajustar_modelo(y_combustivel, X_base, "Consumo de Combustível (kg)")

# 7.3. Modelo para Emissão de CO2 do Voo (kg)
y_co2 = pd.to_numeric(df['Consumo_CO2_do_Voo_kg'], errors='coerce').fillna(df['Consumo_CO2_do_Voo_kg'].median())
modelo_co2 = ajustar_modelo(y_co2, X_base, "Emissão de CO2 do Voo (kg)")
