# Proposta do Projeto - BIG BANG

## 1. Nome do jogo

> BIG BANG

---

## 2. Integrantes do grupo

- [Evelyn Costa](https://github.com/Evycostzocn) 
- [Douglas Freitas](https://github.com/defreitassl) 
- [João Pedro Alvarenga](https://github.com/joaopedro003) 
- [Eduardo Pêgo](https://github.com/Eduardo-Pegoz)

---

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de sobrevivência e coleta de itens com desvio de obstáculos.

---

## 4. Descrição geral do jogo

BIG BANG é um jogo em que os jogadores controlam dinossauros em um cenário pré-histórico. Durante a partida, pedaços de carne aparecem pelo mapa e podem ser coletados para aumentar a pontuação.

Ao mesmo tempo, meteoros caem em locais aleatórios do cenário. Os jogadores precisam evitar as áreas de impacto para sobreviver.

O jogo possui modos Singleplayer e Multiplayer, permitindo que um ou dois jogadores disputem a maior pontuação.

---

## 5. Objetivo do jogador

Sobreviver pelo maior tempo possível e coletar o máximo de carnes para obter a maior pontuação final.

---

## 6. Regras principais

* O jogador pode se movimentar livremente pelo mapa.
* Cada carne coletada adiciona pontos à pontuação.
* Meteoros aparecem em posições aleatórias durante a partida.
* Permanecer dentro da área de impacto de um meteoro elimina o jogador.
* A dificuldade aumenta progressivamente ao longo da partida.

---

## 7. Condição de vitória

### Singleplayer

O objetivo é alcançar a maior pontuação possível antes de ser eliminado.

### Multiplayer

Vence o jogador que obtiver a maior pontuação final após a eliminação dos dois participantes.

---

## 8. Condição de derrota ou encerramento

### Singleplayer

A partida termina quando o jogador é atingido por um meteoro.

### Multiplayer

A partida termina quando ambos os jogadores forem eliminados.

---

## 9. Elementos presentes no jogo

### Jogador

Dinossauros controlados pelo teclado que podem se movimentar pelo cenário para coletar carnes e evitar perigos.

### Obstáculos e desafios

* Meteoros com área de impacto.
* Árvores que bloqueiam a movimentação.
* Arbustos que reduzem a velocidade dos jogadores.

### Objetos de interação

* Carnes coletáveis espalhadas pelo mapa.

### Sistema de pontuação

A pontuação final é composta por:

* Pontos obtidos ao coletar carnes.
* Bônus baseado no tempo de sobrevivência.

---

## 10. Controles

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

---

## 11. Organização do código

* `main.py`: ponto de entrada do jogo.
* `src/jogo.py`: loop principal e mecânicas do jogo.
* `src/menu.py`: menu principal.
* `src/funcoes.py`: funções auxiliares e regras de negócio.
* `src/config.py`: constantes e configurações globais.
* `tests/test_logica.py`: testes automatizados com Pytest.

---

## 12. Recursos externos utilizados

* Biblioteca Pygame.
* Sprites de dinossauros.
* Fonte pixel personalizada.
* Recursos gráficos utilizados para compor o cenário.

---

## 13. Principais dificuldades encontradas

* Implementação da colisão entre jogadores e obstáculos.
* Sistema de meteoros com dificuldade progressiva.
* Organização do projeto em múltiplos módulos.
* Configuração do Pytest para testes automatizados.
* Controle de animações dos personagens.
* Integração e gerenciamento do projeto utilizando Git e GitHub.

---

## 14. Escopo mínimo definido

A versão mínima do jogo deveria conter:

* Movimentação dos jogadores.
* Sistema de pontuação.
* Coleta de carnes.
* Obstáculos.
* Sistema de derrota.
* Tela de fim de jogo.

Todos os itens previstos foram implementados.

---

## 15. Melhorias futuras

* Sistema de ranking.
* Power-ups temporários.
* Novos tipos de obstáculos.
* Diferentes mapas.
* Sistema de pausa.
* Música e efeitos sonoros.
* Novos personagens jogáveis.
