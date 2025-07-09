import argparse
import subprocess
import sys
from pathlib import Path

# Scripts disponíveis e ordem de execução
steps = [
    "0_DOWNLOAD_DADOS.PY",
    "1_CONSOLIDAÇÃO_DADOS.PY",
    "2_ANÁLISE_DADOS_CONSOLIDADOS.PY",
    "3_FILTRO_AERÓDROMOS_VARIAVEIS_AERONAVES.PY",
    "3.1_ANÁLISE_GRÁFICA_VOOS_POR_ANO_FILTRO.PY",
    "4_ANÁLISE_E_INSERÇÃO_DADOS_E_VARIÁVEIS.PY",
    "4.1_FILTRO_TEMPOS_DIFERENTES.PY",
    "4.3_ANÁLISE_VOOS.PY",
    "5_ANÁLISE_REGRESSÃO_LINEAR_MULTIPLA.PY",
    "00_DEPURAÇÃO.PY"
]

def run_script(script_name):
    print(f"\n🟢 Executando: {script_name}")
    result = subprocess.run([sys.executable, script_name])
    if result.returncode != 0:
        print(f"🔴 Erro ao executar {script_name}. Código de retorno: {result.returncode}")
        sys.exit(result.returncode)
    print(f"✅ Finalizado: {script_name}")

def main():
    parser = argparse.ArgumentParser(description="Executa etapas da análise ANAC em sequência.")
    parser.add_argument(
        "--from-step",
        help="Nome do script a partir do qual começar (ex: 2_ANÁLISE_DADOS_CONSOLIDADOS.PY)",
        default=None
    )
    args = parser.parse_args()

    # Define o ponto de partida
    start_index = 0
    if args.from_step:
        try:
            start_index = steps.index(args.from_step)
        except ValueError:
            print(f"❌ Etapa '{args.from_step}' não encontrada. Use uma das etapas abaixo:")
            for s in steps:
                print(" -", s)
            sys.exit(1)

    # Executa os scripts a partir do ponto definido
    for step in steps[start_index:]:
        run_script(step)

if __name__ == "__main__":
    main()
