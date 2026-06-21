import pygame
import random
from src.menu import ALTURA_TELA, LARGURA_TELA

METEORO_RAIO_DANO, METEORO_ALERTA_MS, METEORO_IMPACTO_MS = 156, 1900, 450
METEORO_INTERVALO_MIN_MS, METEORO_INTERVALO_MAX_MS, METEORO_NIVEL_DIFICULDADE_MS = 900, 2600, 15000
METEORO_ALERTA_MIN_MS, METEORO_INTERVALO_MINIMO_MS, METEORO_INTERVALO_MAXIMO_MINIMO_MS = 850, 350, 950
METEORO_ESCALA_MINIMA, METEORO_MULTIPLICADOR_SPAWN = 0.3, 1.2
PONTOS_POR_SEGUNDO = 2

def gerar_posicao_aleatoria():
    return random.randint(25, LARGURA_TELA - 25), random.randint(25, ALTURA_TELA - 25)


def calcular_pontos(pontos_atual, pontos_ganhos):
    return pontos_atual + pontos_ganhos


def mover(teclas, rect, velocidade, cima, baixo, direita, esquerda):
    rect.x += (teclas[direita] - teclas[esquerda]) * velocidade
    rect.y += (teclas[baixo] - teclas[cima]) * velocidade
    rect.clamp_ip(pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA))


def mover_jogador1(teclas, dino_rect, velocidade):
    """Movimenta o jogador 1 com WASD e limita sua posicao na tela."""
    if teclas[pygame.K_w]:
        dino_rect.y -= velocidade

    if teclas[pygame.K_s]:
        dino_rect.y += velocidade

    if teclas[pygame.K_d]:
        dino_rect.x += velocidade

    if teclas[pygame.K_a]:
        dino_rect.x -= velocidade

    if dino_rect.left < 0:
        dino_rect.left = 0

    if dino_rect.right > 1080:
        dino_rect.right = 1080

    if dino_rect.top < 0:
        dino_rect.top = 0

    if dino_rect.bottom > 720:
        dino_rect.bottom = 720
        
def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano

def criar_pe_dino(dino_rect):
    return pygame.Rect(dino_rect.x + 30, dino_rect.y + 58, 42, 18)

def distancia_entre_pontos(ponto_1, ponto_2):
    return ((ponto_1[0] - ponto_2[0]) ** 2 + (ponto_1[1] - ponto_2[1]) ** 2) ** 0.5

def calcular_dificuldade_meteoros(tempo_decorrido_ms, modo="multiplayer"):
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
    intervalo_min, intervalo_max, _ = calcular_dificuldade_meteoros(tempo_decorrido_ms, modo)
    return agora + random.randint(intervalo_min, intervalo_max)


def calcular_raio_meteoro(modo):
    return round(METEORO_RAIO_DANO * 1.6) if modo == "singleplayer" else int(METEORO_RAIO_DANO * 1.5)

def sortear_raio_meteoro(modo):
    raio_maximo = calcular_raio_meteoro(modo)
    return random.randint(max(1, int(raio_maximo * METEORO_ESCALA_MINIMA)), raio_maximo)


def jogador_na_area_do_meteoro(dino_rect, meteoro):
    return distancia_entre_pontos(criar_pe_dino(dino_rect).center, meteoro["centro"]) <= meteoro["raio"]


def calcular_pontuacao_final(pontos_carne, tempo_sobrevivido_ms):
    return pontos_carne + (tempo_sobrevivido_ms // 1000) * PONTOS_POR_SEGUNDO


def velocidade_jogador(rect, arbustos):
    return 2 if any(criar_pe_dino(rect).colliderect(a["lentidao"]) for a in arbustos) else 5


def movimento_teclas(teclas, velocidade, cima, baixo, direita, esquerda):
    return ((teclas[direita] - teclas[esquerda]) * velocidade, (teclas[baixo] - teclas[cima]) * velocidade)

def jogador_perdeu(vidas): return vidas <= 0
def limitar_valor(valor, minimo, maximo): return max(minimo, min(valor, maximo))
def verificar_colisao(retangulo_1, retangulo_2): return retangulo_1.colliderect(retangulo_2)
