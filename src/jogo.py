import pygame
import random
from sys import exit

pygame.init()

LARGURA = 1080
ALTURA = 720

screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("BIG BANG")
clock = pygame.time.Clock()

VERDE_BASE = (105, 184, 62)
VERDE_CLARO = (130, 210, 78)
VERDE_ESCURO = (77, 150, 55)
VERDE_GRAMA = (54, 123, 48)

TERRA = (204, 139, 78)
TERRA_CLARA = (226, 163, 94)
TERRA_ESCURA = (151, 94, 55)

FOLHA_ESCURO = (29, 91, 45)
FOLHA_MEDIO = (45, 132, 58)
FOLHA_CLARO = (91, 181, 69)
FOLHA_LUZ = (145, 218, 75)

TRONCO = (126, 75, 36)
TRONCO_ESCURO = (79, 48, 27)
TRONCO_CLARO = (171, 104, 48)

PEDRA = (118, 118, 118)
PEDRA_LUZ = (166, 166, 166)

FLOR_BRANCA = (245, 245, 230)
FLOR_AMARELA = (238, 202, 54)
FLOR_ROSA = (226, 93, 146)
FLOR_AZUL = (74, 151, 219)


def criar_pe_dino(dino_rect):
    return pygame.Rect(
        dino_rect.x + 30,
        dino_rect.y + 58,
        42,
        18,
    )


def distancia_entre_rects(rect1, rect2):
    centro1 = rect1.center
    centro2 = rect2.center

    dx = centro1[0] - centro2[0]
    dy = centro1[1] - centro2[1]

    return (dx ** 2 + dy ** 2) ** 0.5


def criar_elementos_chao():
    terra = [
        [
            (390, 160), (425, 138), (500, 145), (570, 160),
            (615, 190), (590, 230), (510, 245), (430, 235),
            (380, 205)
        ],
        [
            (760, 335), (805, 315), (890, 320), (950, 345),
            (930, 390), (850, 405), (780, 385)
        ],
        [
            (190, 580), (250, 555), (350, 565), (430, 595),
            (400, 645), (295, 655), (205, 625)
        ],
    ]

    flores = [
        (110, 260, FLOR_BRANCA),
        (270, 420, FLOR_ROSA),
        (530, 330, FLOR_AZUL),
        (720, 165, FLOR_BRANCA),
        (965, 250, FLOR_AMARELA),
        (600, 620, FLOR_BRANCA),
        (860, 590, FLOR_AZUL),
    ]

    pedras = [
        (60, 95),
        (340, 90),
        (690, 470),
        (990, 520),
        (160, 650),
    ]

    matinhos = []

    for y in range(20, ALTURA, 42):
        for x in range(20, LARGURA, 54):
            codigo = (x * 3 + y * 7) % 11

            if codigo in [0, 2, 6]:
                matinhos.append((x, y, 1))
            elif codigo in [1, 7]:
                matinhos.append((x, y, 2))

    return terra, flores, pedras, matinhos


def desenhar_chao(tela, terras, flores, pedras, matinhos):
    tela.fill(VERDE_BASE)

    manchas = [
        pygame.Rect(40, 40, 220, 130),
        pygame.Rect(350, 20, 260, 120),
        pygame.Rect(780, 70, 230, 150),
        pygame.Rect(70, 500, 240, 120),
        pygame.Rect(450, 520, 260, 130),
        pygame.Rect(800, 430, 220, 150),
    ]

    for mancha in manchas:
        pygame.draw.rect(tela, VERDE_CLARO, mancha)

    for pontos in terras:
        pygame.draw.polygon(tela, TERRA, pontos)

        for x, y in pontos:
            pygame.draw.rect(tela, VERDE_GRAMA, (x - 6, y - 4, 12, 6))

        min_x = min(p[0] for p in pontos)
        max_x = max(p[0] for p in pontos)
        min_y = min(p[1] for p in pontos)
        max_y = max(p[1] for p in pontos)

        for i in range(12):
            px = min_x + (i * 31) % max(1, max_x - min_x)
            py = min_y + (i * 17) % max(1, max_y - min_y)
            pygame.draw.rect(tela, TERRA_ESCURA, (px, py, 9, 3))

        for i in range(4):
            px = min_x + (i * 47) % max(1, max_x - min_x)
            py = min_y + (i * 23) % max(1, max_y - min_y)
            pygame.draw.rect(tela, TERRA_CLARA, (px, py, 14, 5))

    for x, y, tipo in matinhos:
        if tipo == 1:
            pygame.draw.rect(tela, VERDE_GRAMA, (x, y + 10, 18, 4))
            pygame.draw.rect(tela, VERDE_GRAMA, (x + 6, y + 4, 4, 12))
        else:
            pygame.draw.rect(tela, VERDE_ESCURO, (x + 8, y, 7, 7))
            pygame.draw.rect(tela, VERDE_CLARO, (x + 18, y + 10, 7, 7))

    for x, y, cor in flores:
        pygame.draw.rect(tela, cor, (x, y - 5, 6, 6))
        pygame.draw.rect(tela, cor, (x, y + 5, 6, 6))
        pygame.draw.rect(tela, cor, (x - 5, y, 6, 6))
        pygame.draw.rect(tela, cor, (x + 5, y, 6, 6))
        pygame.draw.rect(tela, FLOR_AMARELA, (x + 1, y + 1, 4, 4))

    for x, y in pedras:
        pygame.draw.rect(tela, PEDRA, (x, y + 8, 28, 14))
        pygame.draw.rect(tela, PEDRA_LUZ, (x + 8, y, 16, 10))
        pygame.draw.rect(tela, (76, 76, 76), (x + 2, y + 18, 24, 5))


def desenhar_arbusto(tela, rect):
    x = rect.x
    y = rect.y

    pygame.draw.rect(tela, FOLHA_ESCURO, (x + 4, y + 24, 62, 20))
    pygame.draw.rect(tela, FOLHA_MEDIO, (x + 10, y + 12, 26, 28))
    pygame.draw.rect(tela, FOLHA_CLARO, (x + 34, y + 8, 28, 28))
    pygame.draw.rect(tela, FOLHA_LUZ, (x + 42, y + 14, 8, 8))


def desenhar_tronco_arvore(tela, rect):
    x = rect.x
    y = rect.y

    pygame.draw.rect(tela, (52, 120, 46), (x + 30, y + 104, 50, 14))

    pygame.draw.rect(tela, TRONCO_ESCURO, (x + 39, y + 60, 30, 58))
    pygame.draw.rect(tela, TRONCO, (x + 43, y + 56, 25, 58))
    pygame.draw.rect(tela, TRONCO_CLARO, (x + 52, y + 64, 5, 36))

    pygame.draw.rect(tela, TRONCO_ESCURO, (x + 31, y + 105, 16, 7))
    pygame.draw.rect(tela, TRONCO_ESCURO, (x + 62, y + 105, 16, 7))


def desenhar_folhas_arvore(tela, rect):
    x = rect.x
    y = rect.y

    pygame.draw.rect(tela, FOLHA_ESCURO, (x + 14, y + 40, 82, 46))
    pygame.draw.rect(tela, FOLHA_MEDIO, (x + 4, y + 52, 42, 35))
    pygame.draw.rect(tela, FOLHA_MEDIO, (x + 56, y + 50, 44, 36))
    pygame.draw.rect(tela, FOLHA_MEDIO, (x + 24, y + 18, 58, 48))
    pygame.draw.rect(tela, FOLHA_CLARO, (x + 36, y + 8, 42, 36))
    pygame.draw.rect(tela, FOLHA_CLARO, (x + 48, y + 34, 38, 32))
    pygame.draw.rect(tela, FOLHA_LUZ, (x + 48, y + 18, 10, 10))
    pygame.draw.rect(tela, FOLHA_LUZ, (x + 67, y + 39, 9, 9))


def criar_objetos_randomizados():
    arvores = []
    arbustos = []

    area_segura_dino = pygame.Rect(300, 120, 250, 220)
    area_segura_carne = pygame.Rect(520, 120, 180, 180)

    for _ in range(5):
        tentativas = 0

        while True:
            tentativas += 1

            rect_visual = pygame.Rect(
                random.randint(40, LARGURA - 150),
                random.randint(40, ALTURA - 160),
                110,
                120,
            )

            muito_perto = False

            for arvore_existente in arvores:
                if distancia_entre_rects(rect_visual, arvore_existente["visual"]) < 180:
                    muito_perto = True
                    break

            if muito_perto and tentativas < 100:
                continue

            rect_colisao = pygame.Rect(
                rect_visual.x + 34,
                rect_visual.y + 80,
                42,
                40,
            )

            if (
                not rect_visual.colliderect(area_segura_dino)
                and not rect_visual.colliderect(area_segura_carne)
            ):
                break

        arvores.append({
            "visual": rect_visual,
            "colisao": rect_colisao,
        })

    for _ in range(7):
        tentativas = 0

        while True:
            tentativas += 1

            rect_visual = pygame.Rect(
                random.randint(30, LARGURA - 100),
                random.randint(30, ALTURA - 80),
                70,
                45,
            )

            rect_lentidao = pygame.Rect(
                rect_visual.x + 10,
                rect_visual.y + 12,
                50,
                28,
            )

            muito_perto = False

            for arvore in arvores:
                if distancia_entre_rects(rect_visual, arvore["visual"]) < 130:
                    muito_perto = True
                    break

            for arbusto_existente in arbustos:
                if distancia_entre_rects(rect_visual, arbusto_existente["visual"]) < 90:
                    muito_perto = True
                    break

            if muito_perto and tentativas < 100:
                continue

            if (
                not rect_visual.colliderect(area_segura_dino)
                and not rect_visual.colliderect(area_segura_carne)
            ):
                break

        arbustos.append({
            "visual": rect_visual,
            "lentidao": rect_lentidao,
        })

    return arvores, arbustos


def executar_jogo():
    dino = pygame.image.load(
        "assets/imagens/dino sprites/Run (2).png"
    ).convert_alpha()

    dino = pygame.transform.scale(dino, (100, 80))
    dino_rect = dino.get_rect(center=(400, 200))

    carne = pygame.image.load(
        "assets/imagens/MeatUI2.png"
    ).convert_alpha()

    carne = pygame.transform.scale(carne, (50, 50))
    carne_rect = carne.get_rect(center=(600, 200))

    velocidade_normal = 5
    velocidade_lenta = 2

    arvores, arbustos = criar_objetos_randomizados()
    terras, flores, pedras, matinhos = criar_elementos_chao()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        teclas = pygame.key.get_pressed()

        pe_dino = criar_pe_dino(dino_rect)
        velocidade = velocidade_normal

        for arbusto in arbustos:
            if pe_dino.colliderect(arbusto["lentidao"]):
                velocidade = velocidade_lenta

        movimento_x = 0
        movimento_y = 0

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            movimento_y -= velocidade

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            movimento_y += velocidade

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            movimento_x += velocidade

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            movimento_x -= velocidade

        dino_rect.x += movimento_x
        pe_dino = criar_pe_dino(dino_rect)

        for arvore in arvores:
            if pe_dino.colliderect(arvore["colisao"]):
                if movimento_x > 0:
                    dino_rect.x -= pe_dino.right - arvore["colisao"].left
                elif movimento_x < 0:
                    dino_rect.x += arvore["colisao"].right - pe_dino.left

        dino_rect.y += movimento_y
        pe_dino = criar_pe_dino(dino_rect)

        for arvore in arvores:
            if pe_dino.colliderect(arvore["colisao"]):
                if movimento_y > 0:
                    dino_rect.y -= pe_dino.bottom - arvore["colisao"].top
                elif movimento_y < 0:
                    dino_rect.y += arvore["colisao"].bottom - pe_dino.top

        if dino_rect.left < 0:
            dino_rect.left = 0

        if dino_rect.right > LARGURA:
            dino_rect.right = LARGURA

        if dino_rect.top < 0:
            dino_rect.top = 0

        if dino_rect.bottom > ALTURA:
            dino_rect.bottom = ALTURA

        desenhar_chao(screen, terras, flores, pedras, matinhos)

        screen.blit(carne, carne_rect)

        for arbusto in arbustos:
            desenhar_arbusto(screen, arbusto["visual"])

        for arvore in arvores:
            desenhar_tronco_arvore(screen, arvore["visual"])

        screen.blit(dino, dino_rect)

        for arvore in arvores:
            desenhar_folhas_arvore(screen, arvore["visual"])

        if dino_rect.colliderect(carne_rect):
            carne_rect.center = (
                random.randint(40, LARGURA - 40),
                random.randint(40, ALTURA - 40),
            )
            print("CATOU A CARNE!")

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    executar_jogo()