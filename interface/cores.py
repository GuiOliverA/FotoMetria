'''PADRÃO PARA NOME DAS DEF's:

cores.cor_nome_da_cor + adicionais(txt)

'''
def verde(txt):
    """
    Retorna texto verde
    """
    return f'\033[0;32m{txt}\033[m'
def amarelo(txt):
    """
    Retorna texto amarelo
    """
    return f'\033[0;33m{txt}\033[m'

def vermelho(txt):
    """ 
    Retorna texto vermelho
    """   
    return f'\033[0;31m{txt}\033[m'


def azul(txt):
    """
    Retorna texto azul
    """
    return f'\033[0;34m{txt}\033[m'

def negrito_amarelo(txt):
    """
    Retorna estilo negrito e texto amarelo
    """
    return f'\033[1;33m{txt}\033[m'


def negrito_vermelho_cinza(txt):
    """
    Retorna estilo negrito, texto vermelho e fundo cinza
    """
    return f'\033[1;31;47m{txt}\033[m'

def negrito(txt):
    """
    Retorna apenas estilo negrito
    """
    return f'\033[1m{txt}\033[m'


