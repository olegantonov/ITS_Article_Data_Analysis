# 📊 Análise de Dados de Voos da ANAC (2010–2024)

**Este repositório é parte integrante do artigo:**

> **THE IMPACTS OF INTELLIGENT TRANSPORTATION SYSTEMS ON AVIATION OPERATIONAL EFFICIENCY: AN ANALYSIS OF PBN IMPLEMENTATION ON BRAZIL'S MAIN AIR ROUTES**  
> **Autores:** Daniel Guilherme Marques da Silva, Pastor Willy Gonzales Taco  
> **Universidade de Brasília – Programa de Pós-Graduação em Transportes**

---

## 📄 Resumo (Abstract)

This study investigates the impacts of Intelligent Transport Systems (ITS) with an emphasis on Performance-Based Navigation (PBN) on the operational efficiency of Brazilian aviation. The analysis is based on the number of takeoffs observed on the 14 busiest air routes in the country, which accounted for more than 1% of the total regular passenger air transport volume between 2010 and 2024. The research correlates the adoption of ITS with operational gains, such as reductions in flight time, fuel savings, and lower CO₂ emissions into the atmosphere.

---

## 📁 Estrutura de Diretórios

Todos os arquivos são organizados automaticamente da seguinte forma:

- `raw/` – arquivos CSV originais por ano (2010–2024)
- `analysis/` – resultados processados e gráficos gerados

> Por padrão, os dados são salvos no diretório `./data/`. Para customizar, defina a variável de ambiente `ANAC_DATA_DIR` ou configure via arquivo `.env`.

---

## ⚙️ Requisitos

- Python **3.10+**
- Instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração via `.env`

Crie um arquivo `.env` com a seguinte estrutura (exemplo disponível como `.env.example`):

```env
ANAC_DATA_DIR=/caminho/absoluto/para/data
```

---

## ▶️ Execução Automatizada com `main.py`

Execute todo o pipeline de forma sequencial ou a partir de qualquer etapa:

### 🔁 Executar todas as etapas:
```bash
python main.py
```

### 🔄 Executar a partir de um passo específico:
```bash
python main.py --from-step 3_FILTRO_AERÓDROMOS_VARIAVEIS_AERONAVES.PY
```

Etapas disponíveis:
- 0_DOWNLOAD_DADOS.PY
- 1_CONSOLIDAÇÃO_DADOS.PY
- 2_ANÁLISE_DADOS_CONSOLIDADOS.PY
- 3_FILTRO_AERÓDROMOS_VARIAVEIS_AERONAVES.PY
- 3.1_ANÁLISE_GRÁFICA_VOOS_POR_ANO_FILTRO.PY
- 4_ANÁLISE_E_INSERÇÃO_DADOS_E_VARIÁVEIS.PY
- 4.1_FILTRO_TEMPOS_DIFERENTES.PY
- 4.3_ANÁLISE_VOOS.PY
- 5_ANÁLISE_REGRESSÃO_LINEAR_MULTIPLA.PY
- 00_DEPURAÇÃO.PY

---

## 🛠️ Execução Manual (alternativa)

Você também pode executar os scripts separadamente, na ordem abaixo:

```bash
python 0_DOWNLOAD_DADOS.PY
python 1_CONSOLIDACAO_DADOS.PY
python 2_ANALISE_DADOS_CONSOLIDADOS.PY
python 3_FILTRO_AERODROMOS_VARIAVEIS_AERONAVES.PY
python 3.1_ANALISE_GRAFICA_VOOS_POR_ANO_FILTRO.PY
python 4_ANALISE_E_INSERCAO_DADOS_E_VARIAVEIS.PY
python 4.1_FILTRO_TEMPOS_DIFERENTES.PY
python 4.3_ANALISE_VOOS.PY
python 5_ANALISE_REGRESSAO_LINEAR_MULTIPLA.PY
python 00_DEPURACAO.PY
```

---

## 📌 Observações

- O script de download organiza automaticamente os dados por ano.
- Scripts podem ser executados com segurança em chunks — ótimo para grandes volumes.
- Logs informativos são emitidos durante cada etapa.
- Compatível com execução local ou ambiente em nuvem (ex: Colab, Kaggle).

---

## 📬 Contato

Este projeto foi desenvolvido no contexto do Programa de Pós-Graduação em Transportes da Universidade de Brasília (UnB).  
Dúvidas ou sugestões? Entre em contato com os autores por meio dos canais acadêmicos disponíveis.

---
