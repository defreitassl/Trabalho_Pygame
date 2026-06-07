import pygame


def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


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


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    return max(minimo, min(valor, maximo))


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)
