# Estrutura do projeto `foto-metria`

Este arquivo explica, de forma simples, o que cada pasta e arquivo principal faz no projeto.

## Pastas

### `interface/`
Guarda arquivos auxiliares da interface no terminal.

- `cores.py`: contém funções para colorir mensagens no terminal (`verde`, `amarelo`, `vermelho`, etc.), deixando a visualização mais clara.

### `logs/`
Pasta usada para salvar os registros gerados pelos scripts.

Exemplos de conteúdo:
- `contagem_cartao.json`: salva a última contagem feita no cartão.
- `fotografos.json`: lista de fotógrafos cadastrados no sistema.
- `equipe_dia.json`: salva a equipe escolhida para o dia.
- `NomeDoFotografo.txt`: histórico individual de contagens e resultados.

### `.venv/` *(quando existir)*
Essa pasta é um **ambiente virtual do Python**.

Ela serve para:
- isolar dependências do projeto;
- evitar conflito com outros projetos Python;
- manter versões específicas de bibliotecas.

No seu caso, **ela não é obrigatória para rodar o projeto**, porque os scripts também podem ser executados com o Python instalado diretamente no Windows.

Por isso, se você não quiser usar `.venv`, pode continuar usando normalmente:

```powershell
python .\contar-raw.py
python .\raw-apagadas.py
python .\fotografos.py
```

---

## Arquivos principais

### `fotografos.py`
Gerencia os fotógrafos cadastrados.

Funções principais:
- listar fotógrafos;
- adicionar fotógrafo;
- remover fotógrafo;
- definir a equipe do dia.

Ele salva os dados principalmente em arquivos JSON dentro de `logs/`.

### `contar-raw.py`
Conta os arquivos de foto na pasta informada pelo usuário.

Também:
- registra o fotógrafo escolhido;
- pode usar os dados da equipe/fotógrafos já salvos;
- grava a contagem em JSON e TXT.

### `raw-apagadas.py`
Lê a contagem salva anteriormente e compara com a pasta após a seleção das fotos.

Ele mostra:
- total recebido;
- total restante;
- fotos apagadas;
- percentual de aprovação.

### `arquivos-fotos.py`
Arquivo auxiliar ligado à criação/organização de pastas de trabalho das fotos.

### `foto-medida.py`
Arquivo do projeto relacionado à lógica principal de metrificação fotográfica.

### `README.md`
Resumo geral do projeto: objetivo, fluxo de uso e estrutura básica.

---

## Resumo rápido

Se pensar de forma prática:
- `fotografos.py` = cadastro e equipe do dia
- `contar-raw.py` = entrada de fotos
- `raw-apagadas.py` = saída/seleção de fotos
- `logs/` = histórico salvo
- `interface/` = visual do terminal
- `.venv/` = ambiente virtual do Python (opcional)
