# Analysis of ANAC Flight Data (2010–2024)

**This repository is part of the article:**

> **THE IMPACTS OF INTELLIGENT TRANSPORTATION SYSTEMS ON AVIATION OPERATIONAL EFFICIENCY: AN ANALYSIS OF PBN IMPLEMENTATION ON BRAZIL'S MAIN AIR ROUTES**  
> **Authors:** Daniel Guilherme Marques da Silva, Pastor Willy Gonzales Taco  
> **University of Brasília – Graduate Program in Transport Engineering**

---

## Abstract

This study investigates the impacts of Intelligent Transport Systems (ITS) with an emphasis on Performance-Based Navigation (PBN) on the operational efficiency of Brazilian aviation. The analysis is based on the number of takeoffs observed on the 14 busiest air routes in the country, which accounted for more than 1% of the total regular passenger air transport volume between 2010 and 2024. The research correlates the adoption of ITS with operational gains, such as reductions in flight time, fuel savings, and lower CO₂ emissions into the atmosphere.

---

## Directory Structure

All files are automatically organized as follows:

- `raw/` – original CSV files by year (2010–2024)  
- `analysis/` – processed results and generated charts

By default, data is saved in the `./data/` directory. To customize, set the `ANAC_DATA_DIR` environment variable or configure via a `.env` file.

---

## Requirements

- Python **3.10+**
- Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the root directory:

```env
ANAC_DATA_DIR=/absolute/path/to/data
```

An example file `.env.example` is provided.

---

## Automated Execution

To run the entire processing pipeline:

```bash
python main.py
```

To run from a specific step:

```bash
python main.py --from-step 3_FILTER_AIRPORTS_AND_AIRCRAFT_VARIABLES.PY
```

**Available steps:**

- 0_DOWNLOAD_DATA.PY  
- 1_DATA_CONSOLIDATION.PY  
- 2_ANALYSIS_OF_CONSOLIDATED_DATA.PY  
- 3_FILTER_AIRPORTS_AND_AIRCRAFT_VARIABLES.PY  
- 3.1_GRAPHICAL_ANALYSIS_FLIGHTS_PER_YEAR.PY  
- 4_ANALYSIS_AND_INSERTION_OF_VARIABLES.PY  
- 4.1_FILTER_FLIGHTS_WITH_TIME_ANOMALIES.PY  
- 4.3_FLIGHT_ANALYSIS.PY  
- 5_MULTIPLE_LINEAR_REGRESSION_ANALYSIS.PY  
- 00_DEBUGGING.PY

---

## Manual Execution (Alternative)

To execute each step manually:

```bash
python 0_DOWNLOAD_DATA.PY
python 1_DATA_CONSOLIDATION.PY
python 2_ANALYSIS_OF_CONSOLIDATED_DATA.PY
python 3_FILTER_AIRPORTS_AND_AIRCRAFT_VARIABLES.PY
python 3.1_GRAPHICAL_ANALYSIS_FLIGHTS_PER_YEAR.PY
python 4_ANALYSIS_AND_INSERTION_OF_VARIABLES.PY
python 4.1_FILTER_FLIGHTS_WITH_TIME_ANOMALIES.PY
python 4.3_FLIGHT_ANALYSIS.PY
python 5_MULTIPLE_LINEAR_REGRESSION_ANALYSIS.PY
python 00_DEBUGGING.PY
```

---

## Notes

- The download script organizes data into folders by year.
- Scripts support chunked execution for large datasets.
- Informative logs are generated throughout processing.
- Compatible with local or cloud environments (e.g., Google Colab, Kaggle).

---

## Contact

This project was developed as part of the Graduate Program in Transport Engineering at the University of Brasília (UnB).  
For academic inquiries, please contact the authors via institutional channels.
