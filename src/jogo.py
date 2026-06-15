import random

import pygame

import src.funcoes as fn
from src.menu import ALTURA_TELA, LARGURA_TELA, executar_menu


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

METEORO_RAIO_DANO = 58
METEORO_ALERTA_MS = 2200
METEORO_IMPACTO_MS = 450
METEORO_INTERVALO_MIN_MS = 1600
METEORO_INTERVALO_MAX_MS = 4200
PONTOS_POR_SEGUNDO = 2


def criar_pe_dino(dino_rect):
    """Retorna a area dos pes usada para colisao com obstaculos."""
    return pygame.Rect(
        dino_rect.x + 30,
        dino_rect.y + 58,
        42,
        18,
    )


def distancia_entre_rects(rect1, rect2):
    """Calcula a distancia entre os centros de dois retangulos."""
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery

    return (dx ** 2 + dy ** 2) ** 0.5


def distancia_entre_pontos(ponto_1, ponto_2):
    """Calcula a distancia entre dois pontos."""
    dx = ponto_1[0] - ponto_2[0]
    dy = ponto_1[1] - ponto_2[1]

    return (dx ** 2 + dy ** 2) ** 0.5


def criar_elementos_chao():
    """Cria os elementos fixos decorativos do chao."""
    terras = [
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

    for y in range(20, ALTURA_TELA, 42):
        for x in range(20, LARGURA_TELA, 54):
            codigo = (x * 3 + y * 7) % 11

            if codigo in [0, 2, 6]:
                matinhos.append((x, y, 1))
            elif codigo in [1, 7]:
                matinhos.append((x, y, 2))

    return terras, flores, pedras, matinhos


def desenhar_chao(tela, terras, flores, pedras, matinhos):
    """Desenha o mapa do jogo."""
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
    """Desenha um arbusto que reduz a velocidade do jogador."""
    x = rect.x
    y = rect.y

    pygame.draw.rect(tela, FOLHA_ESCURO, (x + 4, y + 24, 62, 20))
    pygame.draw.rect(tela, FOLHA_MEDIO, (x + 10, y + 12, 26, 28))
    pygame.draw.rect(tela, FOLHA_CLARO, (x + 34, y + 8, 28, 28))
    pygame.draw.rect(tela, FOLHA_LUZ, (x + 42, y + 14, 8, 8))


def desenhar_tronco_arvore(tela, rect):
    """Desenha a parte do tronco da arvore."""
    x = rect.x
    y = rect.y

    pygame.draw.rect(tela, (52, 120, 46), (x + 30, y + 104, 50, 14))
    pygame.draw.rect(tela, TRONCO_ESCURO, (x + 39, y + 60, 30, 58))
    pygame.draw.rect(tela, TRONCO, (x + 43, y + 56, 25, 58))
    pygame.draw.rect(tela, TRONCO_CLARO, (x + 52, y + 64, 5, 36))
    pygame.draw.rect(tela, TRONCO_ESCURO, (x + 31, y + 105, 16, 7))
    pygame.draw.rect(tela, TRONCO_ESCURO, (x + 62, y + 105, 16, 7))


def desenhar_folhas_arvore(tela, rect):
    """Desenha a copa da arvore acima do jogador."""
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


def criar_objetos_randomizados(areas_seguras):
    """Cria arvores e arbustos fora das areas iniciais importantes."""
    arvores = []
    arbustos = []

    for _ in range(5):
        tentativas = 0

        while True:
            tentativas += 1

            rect_visual = pygame.Rect(
                random.randint(40, LARGURA_TELA - 150),
                random.randint(40, ALTURA_TELA - 160),
                110,
                120,
            )

            muito_perto = any(
                distancia_entre_rects(rect_visual, arvore["visual"]) < 180
                for arvore in arvores
            )

            if muito_perto and tentativas < 100:
                continue

            rect_colisao = pygame.Rect(
                rect_visual.x + 34,
                rect_visual.y + 80,
                42,
                40,
            )

            if not any(rect_visual.colliderect(area) for area in areas_seguras):
                break

            if tentativas >= 100:
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
                random.randint(30, LARGURA_TELA - 100),
                random.randint(30, ALTURA_TELA - 80),
                70,
                45,
            )

            rect_lentidao = pygame.Rect(
                rect_visual.x + 10,
                rect_visual.y + 12,
                50,
                28,
            )

            perto_de_arvore = any(
                distancia_entre_rects(rect_visual, arvore["visual"]) < 130
                for arvore in arvores
            )
            perto_de_arbusto = any(
                distancia_entre_rects(rect_visual, arbusto["visual"]) < 90
                for arbusto in arbustos
            )

            if (perto_de_arvore or perto_de_arbusto) and tentativas < 100:
                continue

            if not any(rect_visual.colliderect(area) for area in areas_seguras):
                break

            if tentativas >= 100:
                break

        arbustos.append({
            "visual": rect_visual,
            "lentidao": rect_lentidao,
        })

    return arvores, arbustos


def gerar_posicao_carne(arvores):
    """Gera uma posicao para a carne fora das arvores."""
    while True:
        rect = pygame.Rect(
            random.randint(40, LARGURA_TELA - 40),
            random.randint(40, ALTURA_TELA - 40),
            50,
            50,
        )

        if not any(rect.colliderect(arvore["colisao"]) for arvore in arvores):
            return rect.center


def calcular_velocidade(pe_dino, arbustos, velocidade_normal, velocidade_lenta):
    """Retorna velocidade reduzida se o jogador estiver sobre um arbusto."""
    for arbusto in arbustos:
        if pe_dino.colliderect(arbusto["lentidao"]):
            return velocidade_lenta

    return velocidade_normal


def obter_movimento_jogador1(teclas, velocidade):
    """Retorna o deslocamento do jogador 1."""
    movimento_x = 0
    movimento_y = 0

    if teclas[pygame.K_w]:
        movimento_y -= velocidade
    if teclas[pygame.K_s]:
        movimento_y += velocidade
    if teclas[pygame.K_d]:
        movimento_x += velocidade
    if teclas[pygame.K_a]:
        movimento_x -= velocidade

    return movimento_x, movimento_y


def obter_movimento_jogador2(teclas, velocidade):
    """Retorna o deslocamento do jogador 2."""
    movimento_x = 0
    movimento_y = 0

    if teclas[pygame.K_UP]:
        movimento_y -= velocidade
    if teclas[pygame.K_DOWN]:
        movimento_y += velocidade
    if teclas[pygame.K_RIGHT]:
        movimento_x += velocidade
    if teclas[pygame.K_LEFT]:
        movimento_x -= velocidade

    return movimento_x, movimento_y


def mover_com_colisao(dino_rect, movimento_x, movimento_y, arvores):
    """Move o jogador por eixo para resolver colisao com troncos."""
    dino_rect.x += movimento_x
    pe_dino = criar_pe_dino(dino_rect)

    for arvore in arvores:
        if pe_dino.colliderect(arvore["colisao"]):
            if movimento_x > 0:
                dino_rect.x -= pe_dino.right - arvore["colisao"].left
            elif movimento_x < 0:
                dino_rect.x += arvore["colisao"].right - pe_dino.left

            pe_dino = criar_pe_dino(dino_rect)

    dino_rect.y += movimento_y
    pe_dino = criar_pe_dino(dino_rect)

    for arvore in arvores:
        if pe_dino.colliderect(arvore["colisao"]):
            if movimento_y > 0:
                dino_rect.y -= pe_dino.bottom - arvore["colisao"].top
            elif movimento_y < 0:
                dino_rect.y += arvore["colisao"].bottom - pe_dino.top

            pe_dino = criar_pe_dino(dino_rect)

    if dino_rect.left < 0:
        dino_rect.left = 0
    if dino_rect.right > LARGURA_TELA:
        dino_rect.right = LARGURA_TELA
    if dino_rect.top < 0:
        dino_rect.top = 0
    if dino_rect.bottom > ALTURA_TELA:
        dino_rect.bottom = ALTURA_TELA


def sortear_proximo_meteoro(agora):
    """Retorna o instante em que o proximo meteoro deve surgir."""
    intervalo = random.randint(
        METEORO_INTERVALO_MIN_MS,
        METEORO_INTERVALO_MAX_MS,
    )

    return agora + intervalo


def criar_meteoro(agora):
    """Cria um meteoro com aviso antes do impacto."""
    return {
        "centro": (
            random.randint(METEORO_RAIO_DANO, LARGURA_TELA - METEORO_RAIO_DANO),
            random.randint(METEORO_RAIO_DANO, ALTURA_TELA - METEORO_RAIO_DANO),
        ),
        "raio": METEORO_RAIO_DANO,
        "criado_em": agora,
        "impacto_em": agora + METEORO_ALERTA_MS,
        "finaliza_em": agora + METEORO_ALERTA_MS + METEORO_IMPACTO_MS,
        "causou_dano": False,
    }


def meteoro_em_alerta(meteoro, agora):
    """Indica se o meteoro ainda esta no periodo de aviso."""
    return agora < meteoro["impacto_em"]


def meteoro_em_impacto(meteoro, agora):
    """Indica se o meteoro esta causando dano."""
    return meteoro["impacto_em"] <= agora < meteoro["finaliza_em"]


def meteoro_finalizado(meteoro, agora):
    """Indica se o meteoro ja terminou sua animacao."""
    return agora >= meteoro["finaliza_em"]


def jogador_na_area_do_meteoro(dino_rect, meteoro):
    """Verifica se os pes do jogador estao dentro da area de dano."""
    pe_dino = criar_pe_dino(dino_rect)
    distancia = distancia_entre_pontos(pe_dino.center, meteoro["centro"])

    return distancia <= meteoro["raio"]


def calcular_pontuacao_final(pontos_carne, tempo_sobrevivido_ms):
    """Calcula a pontuacao total com carne coletada e tempo vivo."""
    segundos_vivos = tempo_sobrevivido_ms // 1000

    return pontos_carne + segundos_vivos * PONTOS_POR_SEGUNDO


def desenhar_sombra_meteoro(tela, meteoro, agora):
    """Desenha o aviso do impacto no mapa."""
    centro = meteoro["centro"]
    raio = meteoro["raio"]
    restante = max(0, meteoro["impacto_em"] - agora)
    pulso = 1 + (restante // 180) % 2

    sombra = pygame.Surface((raio * 2 + 8, raio * 2 + 8), pygame.SRCALPHA)
    pygame.draw.circle(
        sombra,
        (35, 15, 15, 105),
        (raio + 4, raio + 4),
        raio,
    )
    pygame.draw.circle(
        sombra,
        (210, 45, 35, 180),
        (raio + 4, raio + 4),
        raio - pulso * 3,
        4,
    )
    pygame.draw.circle(
        sombra,
        (255, 210, 70, 180),
        (raio + 4, raio + 4),
        8,
    )

    tela.blit(sombra, (centro[0] - raio - 4, centro[1] - raio - 4))


def desenhar_impacto_meteoro(tela, meteoro):
    """Desenha um impacto simples sem depender de imagem externa."""
    centro = meteoro["centro"]
    raio = meteoro["raio"]

    pygame.draw.circle(tela, (95, 55, 38), centro, raio)
    pygame.draw.circle(tela, (210, 78, 38), centro, raio - 10, 5)
    pygame.draw.circle(tela, (245, 180, 64), centro, raio // 2)
    pygame.draw.circle(
        tela,
        (80, 80, 82),
        (centro[0] - 12, centro[1] - 8),
        18,
    )
    pygame.draw.circle(
        tela,
        (118, 118, 120),
        (centro[0] + 14, centro[1] + 6),
        15,
    )
    pygame.draw.circle(
        tela,
        (55, 55, 58),
        (centro[0] + 2, centro[1] - 2),
        24,
        4,
    )


def desenhar_meteoros(tela, meteoros, agora):
    """Desenha todos os meteoros ativos."""
    for meteoro in meteoros:
        if meteoro_em_alerta(meteoro, agora):
            desenhar_sombra_meteoro(tela, meteoro, agora)
        elif meteoro_em_impacto(meteoro, agora):
            desenhar_impacto_meteoro(tela, meteoro)


def desenhar_jogador_morto(tela, dino_rect):
    """Marca visualmente o local onde o jogador morreu."""
    pygame.draw.line(
        tela,
        (180, 30, 30),
        (dino_rect.left, dino_rect.top),
        (dino_rect.right, dino_rect.bottom),
        5,
    )
    pygame.draw.line(
        tela,
        (180, 30, 30),
        (dino_rect.right, dino_rect.top),
        (dino_rect.left, dino_rect.bottom),
        5,
    )


def exibir_resultado_partida(tela, modo, resultado):
    """Mostra o resultado final ate o jogador voltar ao menu."""
    fonte_titulo = pygame.font.Font("assets/fontes/fonte_pixel.ttf", 52)
    fonte_texto = pygame.font.Font("assets/fontes/fonte_pixel.ttf", 34)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_RETURN,
                pygame.K_SPACE,
                pygame.K_ESCAPE,
            ]:
                return "menu"

        tela.fill((25, 25, 28))

        titulo = fonte_titulo.render("Fim de jogo", True, (245, 235, 210))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 170)))

        if modo == "multiplayer":
            linhas = [
                f"P1: {resultado['p1']} pontos",
                f"P2: {resultado['p2']} pontos",
                resultado["vencedor"],
                "Pressione Enter para voltar ao menu",
            ]
        else:
            linhas = [
                f"Pontuacao final: {resultado['p1']}",
                "Pressione Enter para voltar ao menu",
            ]

        y = 280
        for linha in linhas:
            texto = fonte_texto.render(linha, True, (245, 245, 245))
            tela.blit(texto, texto.get_rect(center=(LARGURA_TELA // 2, y)))
            y += 58

        pygame.display.update()
        clock.tick(30)


def executar_loop_jogo(tela, modo="singleplayer"):
    """Executa a tela jogavel integrada ao menu."""
    clock = pygame.time.Clock()

    dino = pygame.image.load(
        "assets/imagens/dino sprites/Run (2).png"
    ).convert_alpha()
    dino = pygame.transform.scale(dino, (100, 80))
    dino_rect = dino.get_rect(center=(400, 200))

    if modo == "multiplayer":
        dino2 = pygame.image.load(
            "assets/imagens/dino2 sprites/espinossauro.png"
        ).convert_alpha()
        dino2 = pygame.transform.flip(dino2, True, False)
        dino2 = pygame.transform.scale(dino2, (100, 80))
        dino2_rect = dino2.get_rect(center=(680, 200))

    carne = pygame.image.load("assets/imagens/MeatUI2.png").convert_alpha()
    carne = pygame.transform.scale(carne, (50, 50))
    carne_rect = carne.get_rect(center=(600, 200))

    fonte = pygame.font.Font(
        "assets/fontes/fonte_pixel.ttf",
        36
    )

    areas_seguras = [
        pygame.Rect(300, 120, 250, 220),
        pygame.Rect(520, 120, 180, 180),
    ]

    if modo == "multiplayer":
        areas_seguras.append(pygame.Rect(580, 120, 250, 220))

    arvores, arbustos = criar_objetos_randomizados(areas_seguras)
    terras, flores, pedras, matinhos = criar_elementos_chao()

    velocidade_normal = 5
    velocidade_lenta = 2
    pontos = 0
    vivo = True
    tempo_inicio = pygame.time.get_ticks()
    tempo_morte = None
    meteoros = []
    proximo_meteoro = sortear_proximo_meteoro(tempo_inicio)

    if modo == "multiplayer":
        pontos2 = 0
        vivo2 = True
        tempo_morte2 = None

    while True:
        agora = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        if agora >= proximo_meteoro:
            meteoros.append(criar_meteoro(agora))
            proximo_meteoro = sortear_proximo_meteoro(agora)

        teclas = pygame.key.get_pressed()

        if vivo:
            velocidade = calcular_velocidade(
                criar_pe_dino(dino_rect),
                arbustos,
                velocidade_normal,
                velocidade_lenta,
            )
            movimento_x, movimento_y = obter_movimento_jogador1(
                teclas,
                velocidade,
            )
            mover_com_colisao(dino_rect, movimento_x, movimento_y, arvores)

        if modo == "multiplayer" and vivo2:
            velocidade2 = calcular_velocidade(
                criar_pe_dino(dino2_rect),
                arbustos,
                velocidade_normal,
                velocidade_lenta,
            )
            movimento_x2, movimento_y2 = obter_movimento_jogador2(
                teclas,
                velocidade2,
            )
            mover_com_colisao(dino2_rect, movimento_x2, movimento_y2, arvores)

        for meteoro in meteoros:
            if not meteoro_em_impacto(meteoro, agora) or meteoro["causou_dano"]:
                continue

            if vivo and jogador_na_area_do_meteoro(dino_rect, meteoro):
                vivo = False
                tempo_morte = agora

            if (
                modo == "multiplayer"
                and vivo2
                and jogador_na_area_do_meteoro(dino2_rect, meteoro)
            ):
                vivo2 = False
                tempo_morte2 = agora

            meteoro["causou_dano"] = True

        meteoros = [
            meteoro
            for meteoro in meteoros
            if not meteoro_finalizado(meteoro, agora)
        ]

        desenhar_chao(tela, terras, flores, pedras, matinhos)
        desenhar_meteoros(tela, meteoros, agora)

        tela.blit(carne, carne_rect)

        for arbusto in arbustos:
            desenhar_arbusto(tela, arbusto["visual"])

        for arvore in arvores:
            desenhar_tronco_arvore(tela, arvore["visual"])

        if vivo:
            tela.blit(dino, dino_rect)
        else:
            desenhar_jogador_morto(tela, dino_rect)

        if modo == "multiplayer":
            if vivo2:
                tela.blit(dino2, dino2_rect)
            else:
                desenhar_jogador_morto(tela, dino2_rect)

        for arvore in arvores:
            desenhar_folhas_arvore(tela, arvore["visual"])

        texto_pontos = fonte.render(
            f"P1: {pontos}" if modo == "multiplayer" else f"Pontos: {pontos}",
            True,
            (255, 255, 255)
        )
        tela.blit(texto_pontos, (20, 20))

        if modo == "multiplayer":
            texto_pontos2 = fonte.render(
                f"P2: {pontos2}",
                True,
                (255, 255, 255)
            )
            tela.blit(texto_pontos2, (LARGURA_TELA - 150, 20))

        if vivo and fn.verificar_colisao(dino_rect, carne_rect):
            pontos = fn.calcular_pontos(pontos, 10)
            carne_rect.center = gerar_posicao_carne(arvores)
            print(
                f"Pontos P1: {pontos}"
                if modo == "multiplayer"
                else f"Pontos: {pontos}"
            )

        if modo == "multiplayer" and vivo2 and fn.verificar_colisao(
            dino2_rect,
            carne_rect,
        ):
            pontos2 = fn.calcular_pontos(pontos2, 10)
            carne_rect.center = gerar_posicao_carne(arvores)
            print(f"Pontos P2: {pontos2}")

        pygame.display.update()
        clock.tick(60)

        partida_finalizada = not vivo

        if modo == "multiplayer":
            partida_finalizada = not vivo and not vivo2

        if partida_finalizada:
            if tempo_morte is None:
                tempo_morte = agora

            resultado = {
                "p1": calcular_pontuacao_final(
                    pontos,
                    tempo_morte - tempo_inicio,
                )
            }

            if modo == "multiplayer":
                if tempo_morte2 is None:
                    tempo_morte2 = agora

                resultado["p2"] = calcular_pontuacao_final(
                    pontos2,
                    tempo_morte2 - tempo_inicio,
                )

                if resultado["p1"] > resultado["p2"]:
                    resultado["vencedor"] = "P1 venceu"
                elif resultado["p2"] > resultado["p1"]:
                    resultado["vencedor"] = "P2 venceu"
                else:
                    resultado["vencedor"] = "Empate"

            return exibir_resultado_partida(tela, modo, resultado)


def executar_jogo():
    """Abre a janela do jogo, chama o menu inicial e inicia a partida."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("BIG BANG")

    executando = True

    while executando:
        opcao = executar_menu(tela)
        print(f"Opcao escolhida: {opcao}")

        if opcao == "sair":
            executando = False
        else:
            resultado = executar_loop_jogo(tela, modo=opcao)
            if resultado == "sair":
                executando = False

    pygame.quit()
