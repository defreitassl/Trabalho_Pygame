import pygame
import src.funcoes as fn
import random
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1080, 720)) # ajustes da tela
pygame.display.set_caption("BIG BANG") # nome da tela

clock = pygame.time.Clock() #controle de tempo para que a tela fique ativada

# Dino
dino = pygame.image.load(
    "assets/imagens/dino sprites/Run (2).png"
).convert_alpha()

dino = pygame.transform.scale(dino, (100, 80))

dino_rect = dino.get_rect(center=(400, 200))

# Carne

carne = pygame.image.load(
    "assets/imagens/MeatUI2.png"
).convert_alpha()

carne = pygame.transform.scale(carne, (50, 50))

carne_rect = carne.get_rect(center=(600, 200))

velocidade = 5

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()

    fn.mover_jogador1(teclas,dino_rect,velocidade) # chamada da função que está no outro arquivo

    screen.fill((30, 30, 30))

    screen.blit(dino, dino_rect)


    
    screen.blit(carne, carne_rect)

    if dino_rect.colliderect(carne_rect):
        x = random.randint(0, 1000)
        y = random.randint(0, 700)
        carne_rect.center = (x, y)
        print("CATOU A CARNE!")

    pygame.display.update()

    clock.tick(60)
