import json
from pathlib import Path
from interface import cores

LOG_DIR            = Path(__file__).parent / "logs"
ARQUIVO_FOTOGRAFOS = LOG_DIR / "fotografos.json"
ARQUIVO_EQUIPE     = LOG_DIR / "equipe_dia.json"


# ─── Helpers de persistência ───────────────────────────────────────────────

def _carregar() -> list:
    if not ARQUIVO_FOTOGRAFOS.exists():
        return []
    with open(ARQUIVO_FOTOGRAFOS, 'r', encoding='utf-8') as f:
        return json.load(f)


def _salvar(fotografos: list) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO_FOTOGRAFOS, 'w', encoding='utf-8') as f:
        json.dump(fotografos, f, ensure_ascii=False, indent=2)


# ─── Opções do menu ────────────────────────────────────────────────────────

def listar_fotografos() -> None:
    fotografos = _carregar()
    if not fotografos:
        print(cores.amarelo("Nenhum fotógrafo cadastrado."))
        return
    print(cores.verde("\nFotógrafos cadastrados:"))
    for i, nome in enumerate(fotografos, 1):
        print(f"  {i}. {nome}")


def adicionar_fotografo() -> None:
    fotografos = _carregar()
    nome = input("Nome do fotógrafo: ").strip().title()
    if not nome:
        print(cores.vermelho("Nome inválido."))
        return
    if nome in fotografos:
        print(cores.amarelo(f"'{nome}' já está cadastrado."))
        return
    fotografos.append(nome)
    _salvar(fotografos)
    print(cores.verde(f"'{nome}' adicionado com sucesso!"))


def remover_fotografo() -> None:
    fotografos = _carregar()
    if not fotografos:
        print(cores.amarelo("Nenhum fotógrafo cadastrado."))
        return
    listar_fotografos()
    try:
        idx = int(input("\nNúmero do fotógrafo a remover: ").strip()) - 1
        if not (0 <= idx < len(fotografos)):
            print(cores.vermelho("Número inválido."))
            return
        removido = fotografos.pop(idx)
        _salvar(fotografos)
        print(cores.verde(f"'{removido}' removido com sucesso!"))
    except ValueError:
        print(cores.vermelho("Entrada inválida."))


def definir_equipe_dia() -> None:
    fotografos = _carregar()
    if not fotografos:
        print(cores.amarelo("Nenhum fotógrafo cadastrado. Adicione fotógrafos primeiro."))
        return

    print(cores.verde("\nSelecione os fotógrafos da escala de hoje:"))
    for i, nome in enumerate(fotografos, 1):
        print(f"  {i}. {nome}")

    entrada = input("\nDigite os números separados por vírgula (ex: 1,3): ").strip()
    try:
        indices = [int(x.strip()) - 1 for x in entrada.split(",") if x.strip()]
        equipe = []
        for idx in indices:
            if 0 <= idx < len(fotografos):
                equipe.append(fotografos[idx])
            else:
                print(cores.amarelo(f"Número {idx + 1} inválido, ignorado."))

        if not equipe:
            print(cores.vermelho("Nenhum fotógrafo selecionado."))
            return

        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(ARQUIVO_EQUIPE, 'w', encoding='utf-8') as f:
            json.dump({"equipe": equipe}, f, ensure_ascii=False, indent=2)

        print(cores.verde(f"\nEquipe do dia definida: {', '.join(equipe)}"))
    except ValueError:
        print(cores.vermelho("Entrada inválida."))


# ─── Menu principal ────────────────────────────────────────────────────────

def menu() -> None:
    opcoes = {
        "1": ("Listar fotógrafos cadastrados", listar_fotografos),
        "2": ("Adicionar novo fotógrafo",      adicionar_fotografo),
        "3": ("Remover fotógrafo",             remover_fotografo),
        "4": ("Definir equipe do dia",         definir_equipe_dia),
        "5": ("Sair",                          None),
    }
    while True:
        print(cores.amarelo("\n====== GERENCIAR FOTÓGRAFOS ======"))
        for chave, (desc, _) in opcoes.items():
            print(f"  {chave}. {desc}")

        try:
            escolha = input("\nEscolha uma opção: ").strip()
        except KeyboardInterrupt:
            print(cores.amarelo("\n\nInterrupção detectada. Encerrando sem erro..."))
            break

        if escolha not in opcoes:
            print(cores.vermelho("Opção inválida."))
            continue

        desc, func = opcoes[escolha]
        if func is None:
            print(cores.amarelo("Saindo..."))
            break

        try:
            func()
        except KeyboardInterrupt:
            print(cores.amarelo("\nOperação cancelada pelo usuário."))


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(cores.amarelo("\nExecução interrompida pelo usuário."))
