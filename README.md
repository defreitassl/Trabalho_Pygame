# BIG BANG

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

## Integrantes do grupo

- [Evelyn Costa](https://github.com/Evycostzocn)
- [Douglas Freitas](https://github.com/defreitassl)
- [João Pedro Alvarenga](https://github.com/joaopedro003)
- [Eduardo Pêgo](https://github.com/Eduardo-Pegoz) 

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O jogo consiste em controlar um dinossauro que deve coletar pedaços de carne e desviar dos meteoros para sobreviver. O jogo possui uma relação direta entre a quantidade de carnes coletadas e o tempo de sobrevivência, fazendo com que some mais pontos. Caso ele colete uma carne podre ele perde pontos coletou pegando carnes boas.

## Objetivo do jogador

O jogador que coletar o máximo de carnes boas possíveis ganha a partida independente do tempo que ele sobreviver.

## Regras do jogo

Principais regras do jogo.

- O jogador se movimenta usando as setas do teclado e as teclas WASD.
- Cada pedqaço de carne coletada aumenta a pontuação.
- Colidir com um meteoro faz com que um jogador perca.
- A partida termina quando os dois jogadores morrem.

## Controles

Comando utilizados para jogar

- Seta para cima: mover para cima
- Seta para baixo: mover para baixo
- Seta para esquerda: mover para esquerda
- Seta para direita: mover para direita
- W: mover para cima
- S: mover para baixo
- A: mover para esquerda
- D: mover para direita


## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/defreitassl/Trabalho_Pygame.git
cd Trabalho_Pygame
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
