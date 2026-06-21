import math
import random

import pygame

import src.config as cfg

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
    nivel = tempo_decorrido_ms // cfg.METEORO_NIVEL_DIFICULDADE_MS
    intervalo_min = max(cfg.METEORO_INTERVALO_MINIMO_MS, cfg.METEORO_INTERVALO_MIN_MS - nivel * cfg.METEORO_REDUCAO_INTERVALO_MIN_MS)
    intervalo_max = max(cfg.METEORO_INTERVALO_MAXIMO_MINIMO_MS, cfg.METEORO_INTERVALO_MAX_MS - nivel * cfg.METEORO_REDUCAO_INTERVALO_MAX_MS)
    tempo_alerta = max(cfg.METEORO_ALERTA_MIN_MS, cfg.METEORO_ALERTA_MS - nivel * cfg.METEORO_REDUCAO_ALERTA_MS)

    if modo == "singleplayer":
        intervalo_min, intervalo_max = max(cfg.METEORO_INTERVALO_MINIMO_MS, int(intervalo_min * 0.65)), max(cfg.METEORO_INTERVALO_MAXIMO_MINIMO_MS, int(intervalo_max * 0.65))
        tempo_alerta = max(cfg.METEORO_ALERTA_MIN_MS, int(tempo_alerta * 0.75))

    return (
        max(cfg.METEORO_INTERVALO_MINIMO_MS, int(intervalo_min / cfg.METEORO_MULTIPLICADOR_SPAWN)),
        max(cfg.METEORO_INTERVALO_MAXIMO_MINIMO_MS, int(intervalo_max / cfg.METEORO_MULTIPLICADOR_SPAWN)),
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
    return round(cfg.METEORO_RAIO_DANO * 1.6) if modo == "singleplayer" else int(cfg.METEORO_RAIO_DANO * 1.5)

def sortear_raio_meteoro(modo):
    """
    Sorteia um raio aleatório para um meteoro.

    Args:
        modo (str): Modo de jogo.

    Returns:
        int: Raio sorteado para o meteoro.
    """
    raio_maximo = calcular_raio_meteoro(modo)
    return random.randint(max(1, int(raio_maximo * cfg.METEORO_ESCALA_MINIMA)), raio_maximo)


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
    return math.dist(criar_pe_dino(dino_rect).center, meteoro["centro"]) <= meteoro["raio"]


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
    return pontos_carne + (tempo_sobrevivido_ms // 1000) * cfg.PONTOS_POR_SEGUNDO


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
    movimento_x = 0
    movimento_y = 0
    if teclas[direita]:
        movimento_x += velocidade
    if teclas[esquerda]:
        movimento_x -= velocidade
    if teclas[baixo]:
        movimento_y += velocidade
    if teclas[cima]:
        movimento_y -= velocidade
    return movimento_x, movimento_y
