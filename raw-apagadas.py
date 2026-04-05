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
equipe_dia = dados.get('equipe', [])
data_contagem = dados.get('data', 'data desconhecida')

if not isinstance(equipe_dia, list):
    equipe_dia = []

if equipe_dia:
    print(cores.amarelo(f"Equipe do dia: {', '.join(equipe_dia)}"))
    resposta = input("Manter essa equipe/fotógrafo? [S/N]: ").strip().upper()
    resposta = resposta[0] if resposta else 'S'
    if resposta == 'N':
        equipe_dia, fotografo = _selecionar_equipe_e_fotografo()
else:
    equipe_dia, fotografo = _selecionar_equipe_e_fotografo()

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
dados['fotografo'] = fotografo
dados['equipe'] = equipe_dia

LOG_DIR.mkdir(parents=True, exist_ok=True)
with open(ARQUIVO_LOG, 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

nome_txt = fotografo.replace("/", "-").replace("\\", "-")
arquivo_txt = LOG_DIR / f"{nome_txt}.txt"
primeira_escrita = not arquivo_txt.exists()

with open(arquivo_txt, 'a', encoding='utf-8') as f:
    if primeira_escrita:
        # Caso contar-raw.py não tenha sido executado antes, garante o cabeçalho
        f.write(f"Fotógrafo: {fotografo}\n")
        if equipe_dia:
            f.write(f"Equipe do dia: {', '.join(equipe_dia)}\n")
        f.write(f"Data da escala: {datetime.now().strftime('%d/%m/%Y')}\n")
        f.write("=" * 40 + "\n")
    else:
        f.write("\n")
    f.write("--- Resultado da seleção ---\n")
    f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    if equipe_dia:
        f.write(f"Equipe do dia: {', '.join(equipe_dia)}\n")
    f.write(f"Pasta analisada: {PASTA_FOTOS}\n")
    f.write(f"Total recebido: {total_recebidas}\n")
    f.write(f"Total restante: {total_restantes}\n")
    f.write(f"Fotos apagadas: {fotos_apagadas}\n")
    f.write(f"Percentual de aprovação: {percentual_aprovacao:.2f}%\n")

print(cores.amarelo(f"\nResultado adicionado em '{arquivo_txt.name}' sem sobrescrever."))



