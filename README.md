# BIG BANG

Projeto final da disciplina de Introdução à Algoritmos e Programação, desenvolvido em Python utilizando a biblioteca Pygame.

## Integrantes

- [Evelyn Costa](https://github.com/Evycostzocn) 
- [Douglas Freitas](https://github.com/defreitassl) 
- [João Pedro Alvarenga](https://github.com/joaopedro003) 
- [Eduardo Pêgo](https://github.com/Eduardo-Pegoz)

## Sobre o jogo

BIG BANG é um jogo de sobrevivência em que os jogadores controlam dinossauros em um ambiente pré-histórico. O objetivo é coletar pedaços de carne para aumentar a pontuação enquanto desviam de meteoros que caem aleatoriamente pelo mapa.

Ao longo da partida, a dificuldade aumenta a cada 3 segundos, fazendo com que os meteoros apareçam com maior frequência e oferecendo menos tempo de reação aos jogadores.

O jogo possui dois modos:

* **Singleplayer:** um jogador enfrenta uma quantidade maior de meteoros e áreas de dano ampliadas.
* **Multiplayer:** dois jogadores competem simultaneamente pela maior pontuação.

## Objetivo

Sobreviver o máximo de tempo possível e acumular a maior pontuação.

A pontuação final é calculada com base em:

* Carnes coletadas durante a partida.
* Tempo de sobrevivência.

## Regras

* Cada carne coletada concede 10 pontos ao jogador.
* Cada segundo sobrevivido acrescenta 2 pontos ao resultado final.
* Meteoros surgem aleatoriamente durante a partida.
* Permanecer dentro da área de impacto de um meteoro elimina o jogador.
* A dificuldade aumenta conforme o tempo passa.
* No modo multiplayer, a partida termina quando ambos os jogadores forem eliminados.
* Vence o jogador que obtiver a maior pontuação final.

## Controles

### Jogador 1

* W → mover para cima
* A → mover para esquerda
* S → mover para baixo
* D → mover para direita

### Jogador 2 (Multiplayer)

* ↑ → mover para cima
* ← → mover para esquerda
* ↓ → mover para baixo
* → → mover para direita

## Estrutura do projeto

```text
BIG_BANG/
│
├── assets/      # Imagens, fontes e demais recursos
├── docs/        # Documentação do projeto
├── src/         # Código-fonte principal
├── tests/       # Testes automatizados
├── main.py      # Ponto de entrada da aplicação
└── README.md
```

## Tecnologias utilizadas

* Python 3
* Pygame
* Pytest
* Git e GitHub

## Como executar o projeto

### Clonar o repositório

```bash
git clone https://github.com/defreitassl/Trabalho_Pygame.git
cd Trabalho_Pygame
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar o jogo

```bash
python main.py
```

## Executando os testes

```bash
pytest
```

Atualmente o projeto possui testes automatizados utilizando Pytest para validar regras de negócio e funções auxiliares do jogo.

## Organização do código

O projeto foi estruturado em módulos para facilitar manutenção e evolução:

* `config.py`: constantes e configurações globais.
* `funcoes.py`: regras de negócio e cálculos do jogo.
* `jogo.py`: loop principal, renderização e mecânicas.
* `menu.py`: interface de navegação entre telas.

## Status do projeto

✔ Sistema de pontuação

✔ Modo Singleplayer

✔ Modo Multiplayer

✔ Sistema de meteoros com dificuldade progressiva

✔ Colisões com obstáculos

✔ Personagens com animações de movimento e morte

✔ Menu de configurações de volume e sons

✔ Testes automatizados com Pytest

✔ Documentação com Docstrings
