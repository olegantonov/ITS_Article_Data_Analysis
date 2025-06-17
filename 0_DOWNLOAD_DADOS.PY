"""Download dos arquivos VRA da ANAC.

Este script utiliza o caminho configurado em ``config.py`` para salvar os
arquivos CSV anuais. Caso esteja em um ambiente Windows sem ``wget`` no PATH,
defina a variável de ambiente ``WGET_PATH`` com o caminho completo para o
executável.
"""

import os
import subprocess
from config import RAW_DIR

# Diretório de destino para os dados (``data/raw`` por padrão)
download_dir = RAW_DIR

# Caminho do executável ``wget``. Por padrão espera que ``wget`` esteja no PATH
wget_path = os.getenv("WGET_PATH", "wget")

# Garante que o diretório exista
download_dir.mkdir(parents=True, exist_ok=True)

# Lista dos anos para os quais serão baixados os arquivos (de 2010 a 2024)
years = range(2010, 2024)

# URL base para os arquivos
base_url = "https://siros.anac.gov.br/siros/registros/diversos/vra/"

# Loop pelos anos para baixar os arquivos CSV de cada ano
for year in years:
    url = f"{base_url}{year}/"
    print(f"[LOG] Iniciando download para o ano {year} a partir da URL: {url}")

    cmd = [
        wget_path,
        "-c",
        "-r",
        "-np",
        "-nH",
        "--cut-dirs=4",
        "-R",
        "index.html*",
        "-P",
        str(download_dir),
        url,
    ]

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"[LOG] Download para o ano {year} concluído.")
    else:
        print(
            f"[LOG] Erro no download para o ano {year}. Código: {result.returncode}"
        )
print("[LOG] Todos os downloads foram concluídos.")
