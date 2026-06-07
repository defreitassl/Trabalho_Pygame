import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('BIG BANG')
clock = pygame.time.Clock()

dino = pygame.image.load(
    "assets/imagens/dino sprites/Run (2).png" #carrega o dinossauro
).convert_alpha()
dino = pygame.transform.scale(dino, (100, 80)) #ajusta o tamanho do dinossauro
dino_rect = dino.get_rect(center = (400, 200)) #ajustará posições usando um retângulo invisivel

velocidade = 5

carne = pygame.image.load(
    "assets/imagens/MeatUI2.png"
).convert_alpha()
carne = pygame.transform.scale(carne, (50, 50))
carne_rect = carne.get_rect(center = (600, 200))

carne_coletada = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w]:
       dino_rect.y -= velocidade
    if teclas[pygame.K_s]:
       dino_rect.y += velocidade
    if teclas[pygame.K_d]:
       dino_rect.x += velocidade
    if teclas[pygame.K_a]:
       dino_rect.x -= velocidade

    screen.fill((30,30,30))
    screen.blit(dino, dino_rect)
    
    screen.blit(carne, carne_rect)

    if not carne_coletada and dino_rect.colliderect(carne_rect):
        carne_coletada = True
        print("CATOU A CARNE!")

    pygame.display.update()
    clock.tick(60)