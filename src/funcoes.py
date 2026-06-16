import pygame
import random
from src.menu import ALTURA_TELA, LARGURA_TELA


def gerar_posicao_aleatoria():
    return random.randint(25, LARGURA_TELA - 25), random.randint(25, ALTURA_TELA - 25)


def calcular_pontos(pontos_atual, pontos_ganhos):
    return pontos_atual + pontos_ganhos


def mover(teclas, rect, velocidade, cima, baixo, direita, esquerda):
    rect.x += (teclas[direita] - teclas[esquerda]) * velocidade
    rect.y += (teclas[baixo] - teclas[cima]) * velocidade
    rect.clamp_ip(pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA))


def mover_jogador1(teclas, dino_rect, velocidade):
    mover(teclas, dino_rect, velocidade, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)


def mover_jogador2(teclas, dino_rect, velocidade):
    mover(teclas, dino_rect, velocidade, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)


def tomar_dano(vida_atual, dano): return vida_atual - dano
def jogador_perdeu(vidas): return vidas <= 0
def limitar_valor(valor, minimo, maximo): return max(minimo, min(valor, maximo))
def verificar_colisao(retangulo_1, retangulo_2): return retangulo_1.colliderect(retangulo_2)
