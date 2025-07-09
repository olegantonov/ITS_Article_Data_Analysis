"""Download dos arquivos VRA da ANAC.

Este script utiliza o caminho configurado em ``config.py`` para salvar os
arquivos CSV anuais. Caso esteja em um ambiente Windows sem ``wget`` no PATH,
defina a variável de ambiente ``WGET_PATH`` com o caminho completo para o
executável.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from config import RAW_DIR

# Garante que o diretório RAW exista
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Anos de interesse
years = range(2010, 2025)
base_url = "https://siros.anac.gov.br/siros/registros/diversos/vra/"
headers = {"User-Agent": "Mozilla/5.0"}

print(f"[LOG] Iniciando download dos arquivos VRA (2010–2024)...")

for year in years:
    year_url = f"{base_url}{year}/"
    print(f"\n🔎 [ANO {year}] Acessando: {year_url}")

    try:
        response = requests.get(year_url, headers=headers, timeout=60)
        response.raise_for_status()
    except Exception as e:
        print(f"  [ERRO] Falha ao acessar {year_url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    arquivos_csv = [a["href"] for a in links if a.get("href", "").endswith(".csv")]

    if not arquivos_csv:
        print(f"  [AVISO] Nenhum arquivo CSV encontrado para {year}.")
        continue

    # Cria subpasta por ano
    year_dir = RAW_DIR / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)

    for arquivo in arquivos_csv:
        arquivo_url = urljoin(year_url, arquivo)
        arquivo_nome = os.path.basename(arquivo)
        destino = year_dir / arquivo_nome

        if destino.exists():
            print(f"  [SKIP] Já existe: {arquivo_nome}")
            continue

        try:
            r = requests.get(arquivo_url, stream=True, timeout=60)
            r.raise_for_status()

            total_size = int(r.headers.get('content-length', 0))
            with open(destino, "wb") as f, tqdm(
                desc=f"  [↓] {arquivo_nome}",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                leave=False
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

            print(f"  [OK] Salvo em: {destino.relative_to(RAW_DIR)}")

        except Exception as e:
            print(f"  [ERRO] Falha no download de {arquivo_nome}: {e}")

print("\n✅ [FIM] Todos os downloads foram processados.")

