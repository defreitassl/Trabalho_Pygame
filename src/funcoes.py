import pygame
import random

from src.config import (
    METEORO_RAIO_DANO,
    METEORO_ALERTA_MS,
    METEORO_INTERVALO_MIN_MS,
    METEORO_INTERVALO_MAX_MS,
    METEORO_NIVEL_DIFICULDADE_MS,
    METEORO_ALERTA_MIN_MS,
    METEORO_INTERVALO_MINIMO_MS,
    METEORO_INTERVALO_MAXIMO_MINIMO_MS,
    METEORO_ESCALA_MINIMA,
    METEORO_MULTIPLICADOR_SPAWN,
    PONTOS_POR_SEGUNDO,
)

def calcular_pontos(pontos_atual, pontos_ganhos):
    """
    Soma os pontos ganhos à pontuação atual do jogador.

    Args:
        pontos_atual (int): Pontuação atual
        pontos_ganhos (int): Quantidade de pontos a adicionar
    
    Returns:
        int: Nova pontuação do jogador.
    """
    return pontos_atual + pontos_ganhos
        
def criar_pe_dino(dino_rect):
    """
    Cria o retângulo que representa os pés do dinossauro.

    Esse retângulo é utilizado para detectar colisões com
    obstáculos, arbustos e áreas de dano.

    Args:
        dino_rect (pygame.Rect): Retângulo principal do dinossauro.

    Returns:
        pygame.Rect: Retângulo correspondente aos pés do dinossauro.
    """
    return pygame.Rect(dino_rect.x + 30, dino_rect.y + 58, 42, 18)

def distancia_entre_pontos(ponto_1, ponto_2):
    """
    Calcula a distância euclidiana entre dois pontos.

    Args:
        ponto_1 (tuple): Coordenadas (x, y) do primeiro ponto.
        ponto_2 (tuple): Coordenadas (x, y) do segundo ponto.

    Returns:
        float: Distância entre os dois pontos.
    """
    return ((ponto_1[0] - ponto_2[0]) ** 2 + (ponto_1[1] - ponto_2[1]) ** 2) ** 0.5

def calcular_dificuldade_meteoros(tempo_decorrido_ms, modo="multiplayer"):
    """
    Calcula os parâmetros de dificuldade dos meteoros.

    Conforme o tempo de jogo aumenta, os meteoros surgem
    com maior frequência e possuem menos tempo de alerta.

    Args:
        tempo_decorrido_ms (int): Tempo de jogo em milissegundos.
        modo (str): Modo de jogo ("singleplayer" ou "multiplayer").

    Returns:
        tuple: Intervalo mínimo, intervalo máximo e tempo de alerta.
    """
    nivel = tempo_decorrido_ms // METEORO_NIVEL_DIFICULDADE_MS
    intervalo_min = max(METEORO_INTERVALO_MINIMO_MS, METEORO_INTERVALO_MIN_MS - nivel * 90)
    intervalo_max = max(METEORO_INTERVALO_MAXIMO_MINIMO_MS, METEORO_INTERVALO_MAX_MS - nivel * 180)
    tempo_alerta = max(METEORO_ALERTA_MIN_MS, METEORO_ALERTA_MS - nivel * 120)

    if modo == "singleplayer":
        intervalo_min, intervalo_max = max(METEORO_INTERVALO_MINIMO_MS, int(intervalo_min * 0.65)), max(METEORO_INTERVALO_MAXIMO_MINIMO_MS, int(intervalo_max * 0.65))
        tempo_alerta = max(METEORO_ALERTA_MIN_MS, int(tempo_alerta * 0.75))

    return (
        max(METEORO_INTERVALO_MINIMO_MS, int(intervalo_min / METEORO_MULTIPLICADOR_SPAWN)),
        max(METEORO_INTERVALO_MAXIMO_MINIMO_MS, int(intervalo_max / METEORO_MULTIPLICADOR_SPAWN)),
        tempo_alerta,
    )


def sortear_proximo_meteoro(agora, tempo_decorrido_ms, modo="multiplayer"):
    """
    Define o instante em que o próximo meteoro será criado.

    Args:
        agora (int): Tempo atual em milissegundos.
        tempo_decorrido_ms (int): Tempo de jogo em milissegundos.
        modo (str): Modo de jogo.

    Returns:
        int: Instante em que o próximo meteoro aparecerá.
    """
    intervalo_min, intervalo_max, _ = calcular_dificuldade_meteoros(tempo_decorrido_ms, modo)
    return agora + random.randint(intervalo_min, intervalo_max)


def calcular_raio_meteoro(modo):
    """
    Calcula o raio máximo de dano dos meteoros.

    Args:
        modo (str): Modo de jogo.

    Returns:
        int: Raio máximo do meteoro.
    """
    return round(METEORO_RAIO_DANO * 1.6) if modo == "singleplayer" else int(METEORO_RAIO_DANO * 1.5)

def sortear_raio_meteoro(modo):
    """
    Sorteia um raio aleatório para um meteoro.

    Args:
        modo (str): Modo de jogo.

    Returns:
        int: Raio sorteado para o meteoro.
    """
    raio_maximo = calcular_raio_meteoro(modo)
    return random.randint(max(1, int(raio_maximo * METEORO_ESCALA_MINIMA)), raio_maximo)


def jogador_na_area_do_meteoro(dino_rect, meteoro):
    """
    Verifica se o jogador está dentro da área de dano de um meteoro.

    Args:
        dino_rect (pygame.Rect): Retângulo do jogador.
        meteoro (dict): Dados do meteoro.

    Returns:
        bool: True se o jogador estiver na área de dano,
              False caso contrário.
    """
    return distancia_entre_pontos(criar_pe_dino(dino_rect).center, meteoro["centro"]) <= meteoro["raio"]


def calcular_pontuacao_final(pontos_carne, tempo_sobrevivido_ms):
    """
    Calcula a pontuação final da partida.

    A pontuação é composta pelos pontos obtidos ao coletar
    carnes e pelo tempo sobrevivido.

    Args:
        pontos_carne (int): Pontos obtidos ao coletar carnes.
        tempo_sobrevivido_ms (int): Tempo sobrevivido em milissegundos.

    Returns:
        int: Pontuação final do jogador.
    """
    return pontos_carne + (tempo_sobrevivido_ms // 1000) * PONTOS_POR_SEGUNDO


def velocidade_jogador(rect, arbustos):
    """
    Determina a velocidade de movimento do jogador.

    O jogador se move mais lentamente quando está sobre
    um arbusto.

    Args:
        rect (pygame.Rect): Retângulo do jogador.
        arbustos (list): Lista de arbustos do mapa.

    Returns:
        int: Velocidade do jogador.
    """
    return 2 if any(criar_pe_dino(rect).colliderect(a["lentidao"]) for a in arbustos) else 5


def movimento_teclas(teclas, velocidade, cima, baixo, direita, esquerda):
    """
    Calcula o deslocamento do jogador com base nas teclas pressionadas.

    Args:
        teclas: Estado atual das teclas pressionadas.
        velocidade (int): Velocidade de movimento.
        cima: Tecla para mover para cima.
        baixo: Tecla para mover para baixo.
        direita: Tecla para mover para a direita.
        esquerda: Tecla para mover para a esquerda.

    Returns:
        tuple: Deslocamento horizontal e vertical (x, y).
    """
    return ((teclas[direita] - teclas[esquerda]) * velocidade, (teclas[baixo] - teclas[cima]) * velocidade)

def verificar_colisao(retangulo_1, retangulo_2): 
    """
    Verifica se dois retângulos estão colidindo.

    Args:
        retangulo_1 (pygame.Rect): Primeiro retângulo.
        retangulo_2 (pygame.Rect): Segundo retângulo.

    Returns:
        bool: True se houver colisão, False caso contrário.
    """
    return retangulo_1.colliderect(retangulo_2)
