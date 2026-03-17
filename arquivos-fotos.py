import os
from interface import cores

BASE_PATH = r"C:\Users\Guilherme\Desktop\Fotografia"


def criar_pasta_fotos():
    """
    Cria uma única pasta dentro de C:\\Users\\Guilherme\\Desktop\\Fotografia\\.
    O caminho final será: C:\\Users\\Guilherme\\Desktop\\Fotografia\\<nome informado>.
    Avisa caso a pasta já exista.
    """
    nome = input("Digite o nome da pasta (ex: Fotos 1, Fotos 2...): ").strip()
    if not nome:
        print(cores.vermelho("Nome inválido. Operação cancelada."))
        return

    caminho = os.path.join(BASE_PATH, nome)

    if os.path.exists(caminho):
        print(cores.amarelo(f"A pasta '{caminho}' já existe."))
    else:
        os.makedirs(caminho)
        print(cores.verde(f"Pasta criada com sucesso: {caminho}"))


def criar_multiplas_pastas_fotos():
    """
    Cria múltiplas pastas dentro de C:\\Users\\Guilherme\\Desktop\\Fotografia\\ com numeração sequencial.
    O usuário informa o prefixo (ex: 'Fotos'), a quantidade e o número inicial.
    Exemplo de resultado: Fotografia\\Fotos 1, Fotografia\\Fotos 2, Fotografia\\Fotos 3...
    Avisa caso alguma pasta já exista.
    """
    prefixo = input("Digite o prefixo das pastas (ex: Fotos): ").strip()
    if not prefixo:
        print(cores.vermelho("Prefixo inválido. Operação cancelada."))
        return

    try:
        quantidade = int(input("Quantas pastas deseja criar? "))
    except ValueError:
        print(cores.vermelho("Quantidade inválida. Operação cancelada."))
        return

    inicio = int(input("A partir de qual número? (padrão: 1) ") or 1)

    for i in range(inicio, inicio + quantidade):
        nome = f"{prefixo} {i}"
        caminho = os.path.join(BASE_PATH, nome)
        if os.path.exists(caminho):
            print(cores.amarelo(f"Já existe: {caminho}"))
        else:
            os.makedirs(caminho)
            print(cores.verde(f"Criada: {caminho}"))

