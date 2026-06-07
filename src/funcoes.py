import pygame

def mover_jogador1(teclas, dino_rect, velocidade):

    # movimentar jogador
    if teclas[pygame.K_w]:
        dino_rect.y -= velocidade 

    if teclas[pygame.K_s]:
        dino_rect.y += velocidade

    if teclas[pygame.K_d]:
        dino_rect.x += velocidade

    if teclas[pygame.K_a]:
        dino_rect.x -= velocidade

    # limites da tela

    if dino_rect.left < 0:
        dino_rect.left = 0

    if dino_rect.right > 1080:
        dino_rect.right = 1080

    if dino_rect.top < 0:
        dino_rect.top = 0

    if dino_rect.bottom > 720:
        dino_rect.bottom = 720
