# foto-metria

## 1. Sobre o projeto
Sistema de metrificação fotográfica para controle de escalas. Registra quantas fotos foram recebidas por fotógrafo, quantas foram selecionadas e quantas foram descartadas, gerando um percentual de aprovação.

## 2. Estrutura do projeto
- `fotometria.py`: menu principal.
- `contar-raw.py`: contagem de entrada.
- `raw-apagadas.py`: contagem de saída e subtração.
- `arquivos-fotos.py`: criação de pastas.
- `interface/`: cores do terminal.
- `logs/`: TXTs e JSON gerados.

## 3. Fluxo de uso
1. Criar pasta.
2. Mover fotos do cartão.
3. Rodar `contar-raw.py`.
4. Selecionar fotos.
5. Rodar `raw-apagadas.py`.

## 4. Requisitos
- Python 3.x
- Windows
- Extensões suportadas: `.cr2`, `.cr3`, `.arw`, `.jpeg`, `.jpg`

## 5. Status do projeto
Em fase de testes — aguardando validação em escala real. Bugs conhecidos e melhorias futuras serão registrados após os testes.
