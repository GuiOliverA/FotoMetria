# Script para buscar arquivos RAW (Canon e Sony) no cartão de memória
import sys
import json
from pathlib import Path
from datetime import datetime
from time import sleep
from interface import cores

EXTENSOES_RAW = {'.cr2', '.cr3', '.arw', '.jpeg', '.jpg'}
LOG_DIR       = Path(__file__).parent / "logs"
ARQUIVO_LOG   = LOG_DIR / "contagem_cartao.json"


# FASE DE TESTES: pasta fixa para desenvolvimento
# Em escala real, substituir as linhas 27 e 28 pelo input abaixo:
# -
#         caminho = input("Cole o caminho da pasta do cartão:\n> ")
#         PASTA_CARTAO = Path(caminho)
# -
# TESTES:
#         caminho = int(input("Qual a numeração da pasta Fotos?\n> "))
#         PASTA_CARTAO = Path(rf"C:\Users\Guilherme\Desktop\Fotografia\Fotos {caminho}")

# --- Solicita a pasta ---
try:
    while True:
        caminho = int(input("Qual a numeração da pasta Fotos?\n> "))
        PASTA_CARTAO = Path(rf"C:\Users\Guilherme\Desktop\Fotografia\Fotos {caminho}")
        
        if PASTA_CARTAO.exists():
            print(cores.verde(f"Pasta encontrada: {PASTA_CARTAO}"))
            sleep(2)
            break
        else:
            print(cores.vermelho(f"Pasta 'Fotos {caminho}' não encontrada..."))

except ValueError:
    print(cores.vermelho("Entrada inválida. Por favor, digite um número inteiro (1,2,3...)."))
    sys.exit(1)
except KeyboardInterrupt:
    print(cores.vermelho("\nOperação cancelada pelo usuário."))
    sys.exit(1)
else:
    print(cores.amarelo(f"Verificando arquivos na pasta: {PASTA_CARTAO}"))
    sleep(1)


# --- Varre arquivos ---
arquivos = [f for f in PASTA_CARTAO.rglob('*') if f.suffix.lower() in EXTENSOES_RAW]


if not arquivos:
    print(cores.vermelho("Nenhum arquivo de foto (RAW ou JPEG) encontrado no cartão."))
    sys.exit(0)

for f in arquivos:
    print(f.suffix) 
    sleep(0.01)

contagem = len(arquivos)
print(cores.verde(f"\nTotal de arquivos no cartão: {contagem}"))


# --- Pede identificação do fotógrafo ---    
fotografo = input("Identificação: (Nome do fotógrafo): ").strip().title() or "sem identificação"

# --- Salva no log JSON ---
dados = {
    "fotografo": fotografo,
    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "total_cartao": contagem
}

LOG_DIR.mkdir(parents=True, exist_ok=True)
with open(ARQUIVO_LOG, 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# --- Salva TXT com o nome do fotógrafo ---
nome_txt = fotografo.replace("/", "-").replace("\\", "-")  # evita caracteres inválidos no nome do arquivo

arquivo_txt = LOG_DIR / f"{nome_txt}.txt"

# Se o arquivo já existir, adiciona um número para evitar sobrescrever com .json
contador = 1
while arquivo_txt.exists():
    arquivo_txt = LOG_DIR / f"{nome_txt}({contador}).txt"
    contador += 1
#

with open(arquivo_txt, 'w', encoding='utf-8') as f:
    f.write(f"Fotógrafo: {fotografo}\n")
    f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    f.write(f"Total no cartão: {contagem}\n")

print(cores.amarelo(f'\nContagem salva em "{ARQUIVO_LOG.name}" e "{arquivo_txt.name}" — não precisa anotar nada!'))




