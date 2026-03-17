import sys
import json
from pathlib import Path
from datetime import datetime
from time import sleep
from interface import cores

EXTENSOES_RAW = {'.cr2', '.cr3', '.arw', '.jpeg', '.jpg'}
LOG_DIR = Path(__file__).parent / "logs"
ARQUIVO_LOG = LOG_DIR / "contagem_cartao.json"


def obter_pasta() -> Path:
    """Aceita numero da pasta Fotos ou caminho completo."""
    entrada = input("Numero da pasta Fotos ou caminho completo:\n> ").strip()

    if entrada.isdigit():
        return Path(rf"C:\Users\Guilherme\Desktop\Fotografia\Fotos {int(entrada)}")

    return Path(entrada)


# --- Lê contagem salva pelo contar-raw.py ---
if not ARQUIVO_LOG.exists():
    print(cores.vermelho(
        "ERRO: Arquivo 'contagem_cartao.json' nao encontrado.\n"
        "Execute contar-raw.py antes de usar este script."
    ))
    sys.exit(1)

with open(ARQUIVO_LOG, 'r', encoding='utf-8') as f:
    dados = json.load(f)

total_recebidas = int(dados.get('total_cartao', 0))
fotografo = dados.get('fotografo', 'sem identificação')
data_contagem = dados.get('data', 'data desconhecida')

print(cores.amarelo(f"Fotografo   : {fotografo}"))
print(cores.amarelo(f"Contagem em : {data_contagem}"))
print(cores.verde(f"Total recebido: {total_recebidas}"))
print()

# --- Solicita pasta e valida ---
try:
    PASTA_FOTOS = obter_pasta()
except KeyboardInterrupt:
    print(cores.vermelho("\nOperacao cancelada pelo usuario."))
    sys.exit(1)

if not PASTA_FOTOS.exists() or not PASTA_FOTOS.is_dir():
    print(cores.vermelho(f"ERRO: Pasta nao encontrada: {PASTA_FOTOS}"))
    sys.exit(1)

print(cores.amarelo(f"Verificando arquivos em: {PASTA_FOTOS}"))
sleep(0.5)

# --- Varre arquivos restantes ---
arquivos_restantes = [f for f in PASTA_FOTOS.rglob('*') if f.suffix.lower() in EXTENSOES_RAW]
total_restantes = len(arquivos_restantes)
fotos_apagadas = total_recebidas - total_restantes

if total_recebidas > 0:
    percentual_aprovacao = (total_restantes / total_recebidas) * 100
else:
    percentual_aprovacao = 0.0

print()
print(cores.verde(f"Total recebido : {total_recebidas}"))
print(cores.verde(f"Total restante : {total_restantes}"))
print(cores.azul(f"Fotos apagadas : {fotos_apagadas}"))
print(cores.amarelo(f"Percentual de aprovacao: {percentual_aprovacao:.2f}%"))

if fotos_apagadas < 0:
    print(cores.vermelho(
        "ATENCAO: a pasta informada possui mais arquivos que a contagem inicial."
    ))

# --- Salva no TXT do fotógrafo em append ---
nome_txt = fotografo.replace("/", "-").replace("\\", "-")
arquivo_txt = LOG_DIR / f"{nome_txt}.txt"

LOG_DIR.mkdir(parents=True, exist_ok=True)
with open(arquivo_txt, 'a', encoding='utf-8') as f:
    f.write("\n")
    f.write("--- Resultado da selecao ---\n")
    f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    f.write(f"Pasta analisada: {PASTA_FOTOS}\n")
    f.write(f"Total recebido: {total_recebidas}\n")
    f.write(f"Total restante: {total_restantes}\n")
    f.write(f"Fotos apagadas: {fotos_apagadas}\n")
    f.write(f"Percentual de aprovacao: {percentual_aprovacao:.2f}%\n")

print(cores.amarelo(f"\nResultado adicionado em '{arquivo_txt.name}' sem sobrescrever."))