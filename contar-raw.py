# Script para buscar arquivos RAW (Canon e Sony) no cartão de memória
import sys
import json
from pathlib import Path
from datetime import datetime
from time import sleep
from interface import cores

EXTENSOES_RAW      = {'.cr2', '.cr3', '.arw', '.jpeg', '.jpg'}
LOG_DIR            = Path(__file__).parent / "logs"
ARQUIVO_LOG        = LOG_DIR / "contagem_cartao.json"
ARQUIVO_FOTOGRAFOS = LOG_DIR / "fotografos.json"
ARQUIVO_EQUIPE     = LOG_DIR / "equipe_dia.json"


def _carregar_json(caminho: Path, padrao):
    if not caminho.exists():
        return padrao
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return padrao


def _selecionar_equipe_e_fotografo() -> tuple[list, str]:
    dados_equipe = _carregar_json(ARQUIVO_EQUIPE, {})
    equipe_dia = dados_equipe.get("equipe", []) if isinstance(dados_equipe, dict) else []
    fotografos = _carregar_json(ARQUIVO_FOTOGRAFOS, [])

    equipe_dia = [str(nome).strip().title() for nome in equipe_dia if str(nome).strip()]
    fotografos = [str(nome).strip().title() for nome in fotografos if str(nome).strip()]

    print(cores.negrito_amarelo("\n=== SELEÇÃO DE FOTÓGRAFO ==="))

    if equipe_dia:
        print(cores.verde("Equipe do dia carregada com sucesso:"))
        for i, nome in enumerate(equipe_dia, 1):
            print(cores.azul(f"  {i}. {nome}"))

        print(cores.amarelo("\nOpção manual (sem número): digite M"))

        while True:
            entrada = input("\nEscolha o número do fotógrafo ou digite M: ").strip()
            if entrada.lower() == 'm':
                nome = input("Nome do fotógrafo: ").strip().title() or "Sem Identificação"
                return [nome], nome

            if entrada.isdigit():
                idx = int(entrada) - 1
                if 0 <= idx < len(equipe_dia):
                    return equipe_dia, equipe_dia[idx]

            print(cores.vermelho("Entrada inválida. Escolha um número da equipe ou digite M."))

    print(cores.vermelho("\nNenhuma equipe do dia foi encontrada."))
    print(cores.amarelo("Cadastre a equipe antes em 'fotografos.py' para agilizar a seleção."))
    if fotografos:
        print(cores.azul(f"Fotógrafos cadastrados no sistema: {', '.join(fotografos)}"))
    print(cores.amarelo("\nCadastro manual de fotógrafo:"))

    nome = input("Nome do fotógrafo: ").strip().title() or "Sem Identificação"
    return [nome], nome


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

print(cores.verde('Contando arquivos...'))
sleep(1)

contagem = len(arquivos)
print(cores.verde(f"\nTotal de arquivos no cartão: {contagem}"))


# --- Lê equipe/fotógrafo cadastrados no fotografos.py ---
equipe_dia, fotografo = _selecionar_equipe_e_fotografo()

# --- Salva no log JSON ---
dados = {
    "fotografo": fotografo,
    "equipe": equipe_dia,
    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "total_cartao": contagem
}

LOG_DIR.mkdir(parents=True, exist_ok=True)
with open(ARQUIVO_LOG, 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# --- Salva TXT com o nome do fotógrafo ---
nome_txt = fotografo.replace("/", "-").replace("\\", "-")  # evita caracteres inválidos no nome do arquivo

arquivo_txt = LOG_DIR / f"{nome_txt}.txt"
primeira_escrita = not arquivo_txt.exists()

# Sempre usa o mesmo arquivo; cria na primeira vez, faz append nas seguintes
with open(arquivo_txt, 'a', encoding='utf-8') as f:
    if primeira_escrita:
        # Cabeçalho gravado apenas uma vez, na criação do arquivo
        f.write(f"Fotógrafo: {fotografo}\n")
        if equipe_dia:
            f.write(f"Equipe do dia: {', '.join(equipe_dia)}\n")
        f.write(f"Data da escala: {datetime.now().strftime('%d/%m/%Y')}\n")
        f.write("=" * 40 + "\n")
    else:
        f.write("\n")
    f.write(f"--- Contagem do cartão ---\n")
    f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    if equipe_dia:
        f.write(f"Equipe do dia: {', '.join(equipe_dia)}\n")
    f.write(f"Total no cartão: {contagem}\n")

print(cores.amarelo(f'\nContagem salva em "{ARQUIVO_LOG.name}" e "{arquivo_txt.name}" — não precisa anotar nada!'))




