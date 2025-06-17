
## 📊 Análise de Dados de Voos da ANAC (2010–2024)

**Este repositório é parte integrante do artigo:**

> **THE IMPACTS OF INTELLIGENT TRANSPORTATION SYSTEMS ON AVIATION OPERATIONAL EFFICIENCY: AN ANALYSIS OF PBN IMPLEMENTATION ON BRAZIL'S MAIN AIR ROUTES**  
> **Autores:** Daniel Guilherme Marques da Silva, Pastor Willy Gonzales Taco  
> **Universidade de Brasília – Programa de Pós-Graduação em Transportes**

## 📄 Resumo (Abstract)

This study investigates the impacts of Intelligent Transport Systems (ITS) with an emphasis on Performance-Based Navigation (PBN) on the operational efficiency of Brazilian aviation. The analysis is based on the number of takeoffs observed on the 14 busiest air routes in the country, which accounted for more than 1% of the total regular passenger air transport volume between 2010 and 2024. The research correlates the adoption of ITS with operational gains, such as reductions in flight time, fuel savings, and lower CO₂ emissions into the atmosphere.

---

## 📁 Estrutura de Diretórios

Todos os arquivos são organizados automaticamente da seguinte forma:

- `raw/` – arquivos CSV originais por ano (2010–2024)
- `analysis/` – resultados processados e gráficos gerados

> Por padrão, os dados são salvos no diretório `data/`. Para personalizar o caminho, defina a variável de ambiente `ANAC_DATA_DIR`.

---

## ⚙️ Requisitos

- Python **3.10+**
- Instalação das bibliotecas:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

---

## 📥 Download dos Dados

Execute o script abaixo (exemplo para Google Colab):

```python
from google.colab import drive
import os

drive.mount('/content/drive')
output_dir = '/content/drive/MyDrive/ANAC_DATA'
os.makedirs(output_dir, exist_ok=True)

!wget -c -r -np -nH --cut-dirs=4 -R "index.html*" -P $output_dir \
https://siros.anac.gov.br/siros/registros/diversos/vra/
```

---

## ▶️ Execução dos Scripts

Execute os arquivos na ordem abaixo:

### 1. Download dos dados brutos:
```bash
python 0_DOWNLOAD_DADOS.PY
```

### 2. Consolidação dos CSVs:
```bash
python 1_CONSOLIDACAO_DADOS.PY
```

### 3. Análises iniciais:
```bash
python 2_ANALISE_DADOS_CONSOLIDADOS.PY
python 3_FILTRO_AERODROMOS_VARIAVEIS_AERONAVES.PY
python 3.1_ANALISE_GRAFICA_VOOS_POR_ANO_FILTRO.PY
```

### 4. Inserção de variáveis e filtros adicionais:
```bash
python 4_ANALISE_E_INSERCAO_DADOS_E_VARIAVEIS.PY
python 4.1_FILTRO_TEMPOS_DIFERENTES.PY
python 4.3_ANALISE_VOOS.PY
```

### 5. Modelagem estatística (regressão):
```bash
python 5_ANALISE_REGRESSAO_LINEAR_MULTIPLA.PY
```

### 🔍 Script auxiliar:
```bash
python 00_DEPURACAO.PY
```
> Use este script para verificações manuais ou análises pontuais.

---

## 📌 Observações

- O script de download organiza os dados em pastas anuais automaticamente.
- Todos os scripts devem ser executados sequencialmente para manter a integridade dos dados processados.
- Adapte os caminhos caso execute em ambiente local, fora do Google Colab ou Google Drive.

---

## 📬 Contato

Este projeto foi desenvolvido no contexto do Programa de Pós-Graduação em Transportes da Universidade de Brasília (UnB).  
Dúvidas ou sugestões? Entre em contato com os autores por meio dos canais acadêmicos disponíveis.
```
