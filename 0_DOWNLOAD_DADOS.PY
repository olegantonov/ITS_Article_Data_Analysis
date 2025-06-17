import os
import subprocess

# Diretório de destino para os dados (pasta do projeto)
download_dir = r"C:\Users\danie\OneDrive\Documentos\Mestrado-ITS-Article\docs"

# Caminho completo do wget no Windows
wget_path = r"C:\ProgramData\chocolatey\lib\Wget\tools\wget.exe"

# Cria o diretório, se não existir
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
    print(f"[LOG] Diretório criado: {download_dir}")
else:
    print(f"[LOG] Diretório existente: {download_dir}")

# Lista dos anos para os quais serão baixados os arquivos (de 2010 a 2024)
years = range(2010, 2024)

# URL base para os arquivos
base_url = "https://siros.anac.gov.br/siros/registros/diversos/vra/"

# Loop pelos anos para baixar os arquivos CSV de cada ano
for year in years:
    url = f"{base_url}{year}/"
    print(f"[LOG] Iniciando download para o ano {year} a partir da URL: {url}")
    
    # Comando wget ajustado com caminho absoluto
    cmd = [
        wget_path,
        "-c",
        "-r",
        "-np",
        "-nH",
        "--cut-dirs=4",
        "-R", "index.html*",
        "-P", download_dir,
        url
    ]
    
    # Executa o comando
    result = subprocess.run(cmd, shell=True)
    
    # Verifica se o download foi bem-sucedido
    if result.returncode == 0:
        print(f"[LOG] Download para o ano {year} concluído com sucesso.")
    else:
        print(f"[LOG] Erro no download para o ano {year}. Código de saída: {result.returncode}")

print("[LOG] Todos os downloads foram concluídos.")