# ITS Article Data Analysis

## Project Overview
This project analyzes data from the Brazilian National Civil Aviation Agency (ANAC) to study the impact of Intelligent Transport Systems (ITS) and Performance-Based Navigation (PBN) on aviation efficiency. The scripts consolidate flight data from 2010‑2024, generate descriptive statistics and graphics, and build regression models evaluating fuel consumption, CO₂ emissions and flight times on the country’s busiest routes.

## Downloading ANAC Data
The raw data come from the ANAC VRA records. They can be obtained using `wget` with recursive download. Below is an example using Google Colab to save the files to Google Drive:

```python
from google.colab import drive
import os

drive.mount('/content/drive')
output_dir = '/content/drive/MyDrive/ANAC_DATA'
os.makedirs(output_dir, exist_ok=True)
!wget -c -r -np -nH --cut-dirs=4 -R "index.html*" -P $output_dir \
       https://siros.anac.gov.br/siros/registros/diversos/vra/
```

The download creates annual folders with CSV files for each year between 2010 and 2024.

## Requirements
- Python 3.10+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels

Install the packages using pip:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

## Running the Scripts
Execute each stage of the analysis using Python. Example:

```bash
python 0_DOWNLOAD_DADOS.PY               # download VRA files
python 1_CONSOLIDAÇÃO_DADOS.PY           # merge yearly CSVs
python 2_ANÁLISE_DADOS_CONSOLIDADOS.PY   # inspect consolidated file
python 3_FILTRO_AERÓDROMOS_VARIAVEIS_AERONAVES.PY
python 3.1_ANÁLISE_GRÁFICA_VOOS_POR_ANO_FILTRO.PY
python 4_ANÁLISE_E_INSERÇÃO_DADOS_E_VARIÁVEIS.PY
python 4.1_FILTRO_TEMPOS_DIFERENTES.PY
python 4.3_ANÁLISE_VOOS.PY
python 5_ANÁLISE_REGRESSÃO_LINEAR_MULTIPLA.PY
```

The file `00_DEPURAÇÃO.PY` can be used for exploratory checks when troubleshooting the consolidated dataset.
