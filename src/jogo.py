import os
import random

import pygame

import src.funcoes as fn
from src.menu import ALTURA_TELA, LARGURA_TELA, executar_menu


VERDE_BASE, VERDE_CLARO, VERDE_ESCURO, VERDE_GRAMA = (105, 184, 62), (130, 210, 78), (77, 150, 55), (54, 123, 48)
TERRA, TERRA_CLARA, TERRA_ESCURA = (204, 139, 78), (226, 163, 94), (151, 94, 55)
FOLHA_ESCURO, FOLHA_MEDIO, FOLHA_CLARO, FOLHA_LUZ = (29, 91, 45), (45, 132, 58), (91, 181, 69), (145, 218, 75)
TRONCO, TRONCO_ESCURO, TRONCO_CLARO = (126, 75, 36), (79, 48, 27), (171, 104, 48)
PEDRA, PEDRA_LUZ = (118, 118, 118), (166, 166, 166)
FLOR_BRANCA, FLOR_AMARELA, FLOR_ROSA, FLOR_AZUL = (245, 245, 230), (238, 202, 54), (226, 93, 146), (74, 151, 219)

METEORO_RAIO_DANO, METEORO_ALERTA_MS, METEORO_IMPACTO_MS = 156, 1900, 450
METEORO_INTERVALO_MIN_MS, METEORO_INTERVALO_MAX_MS, METEORO_NIVEL_DIFICULDADE_MS = 900, 2600, 15000
METEORO_ALERTA_MIN_MS, METEORO_INTERVALO_MINIMO_MS, METEORO_INTERVALO_MAXIMO_MINIMO_MS = 850, 350, 950
METEORO_ESCALA_MINIMA, METEORO_MULTIPLICADOR_SPAWN = 0.3, 1.2
PONTOS_POR_SEGUNDO = 2
DINO_TAMANHO = (100, 80)
DINO_ANIMACAO_MS = 90
CAMINHO_SPRITES_DINO1 = os.path.join("assets", "imagens", "dino sprites")


def criar_pe_dino(dino_rect):
    return pygame.Rect(dino_rect.x + 30, dino_rect.y + 58, 42, 18)


def distancia_entre_pontos(ponto_1, ponto_2):
    return ((ponto_1[0] - ponto_2[0]) ** 2 + (ponto_1[1] - ponto_2[1]) ** 2) ** 0.5


def carregar_frames_animacao(prefixo, quantidade):
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(CAMINHO_SPRITES_DINO1, f"{prefixo} ({i}).png")).convert_alpha(),
            DINO_TAMANHO,
        )
        for i in range(1, quantidade + 1)
    ]


def carregar_animacoes_dino1():
    return {k.lower(): carregar_frames_animacao(k, q) for k, q in [("Idle", 10), ("Walk", 10), ("Run", 8), ("Dead", 8)]}


def escolher_animacao_dino1(vivo, movendo, lento):
    return "dead" if not vivo else "idle" if not movendo else "walk" if lento else "run"


def obter_frame_animacao(frames, agora, repetir=True, iniciado_em=0):
    indice = max(0, (agora - iniciado_em) // DINO_ANIMACAO_MS)
    return frames[indice % len(frames) if repetir else min(indice, len(frames) - 1)]


def criar_elementos_chao():
    terras = [
        [(390, 160), (425, 138), (500, 145), (570, 160), (615, 190), (590, 230), (510, 245), (430, 235), (380, 205)],
        [(760, 335), (805, 315), (890, 320), (950, 345), (930, 390), (850, 405), (780, 385)],
        [(190, 580), (250, 555), (350, 565), (430, 595), (400, 645), (295, 655), (205, 625)],
    ]
    flores = [
        (110, 260, FLOR_BRANCA), (270, 420, FLOR_ROSA),
        (530, 330, FLOR_AZUL), (720, 165, FLOR_BRANCA),
        (965, 250, FLOR_AMARELA), (600, 620, FLOR_BRANCA),
        (860, 590, FLOR_AZUL),
    ]
    pedras = [(60, 95), (340, 90), (690, 470), (990, 520), (160, 650)]
    matinhos = [
        (x, y, 1 if (x * 3 + y * 7) % 11 in [0, 2, 6] else 2)
        for y in range(20, ALTURA_TELA, 42)
        for x in range(20, LARGURA_TELA, 54)
        if (x * 3 + y * 7) % 11 in [0, 2, 6, 1, 7]
    ]
    return terras, flores, pedras, matinhos


def desenhar_chao(tela, terras, flores, pedras, matinhos):
    tela.fill(VERDE_BASE)
    for mancha in [(40, 40, 220, 130), (350, 20, 260, 120), (780, 70, 230, 150), (70, 500, 240, 120), (450, 520, 260, 130), (800, 430, 220, 150)]:
        pygame.draw.rect(tela, VERDE_CLARO, mancha)

    for pontos in terras:
        pygame.draw.polygon(tela, TERRA, pontos)
        for x, y in pontos:
            pygame.draw.rect(tela, VERDE_GRAMA, (x - 6, y - 4, 12, 6))

        min_x, max_x = min(p[0] for p in pontos), max(p[0] for p in pontos)
        min_y, max_y = min(p[1] for p in pontos), max(p[1] for p in pontos)
        for qtd, cor, w, h, ax, ay in [(12, TERRA_ESCURA, 9, 3, 31, 17), (4, TERRA_CLARA, 14, 5, 47, 23)]:
            for i in range(qtd):
                pygame.draw.rect(tela, cor, (min_x + (i * ax) % max(1, max_x - min_x), min_y + (i * ay) % max(1, max_y - min_y), w, h))

    for x, y, tipo in matinhos:
        itens = [(VERDE_GRAMA, (x, y + 10, 18, 4)), (VERDE_GRAMA, (x + 6, y + 4, 4, 12))] if tipo == 1 else [(VERDE_ESCURO, (x + 8, y, 7, 7)), (VERDE_CLARO, (x + 18, y + 10, 7, 7))]
        for cor, rect in itens:
            pygame.draw.rect(tela, cor, rect)

    for x, y, cor in flores:
        for rect in [(x, y - 5, 6, 6), (x, y + 5, 6, 6), (x - 5, y, 6, 6), (x + 5, y, 6, 6)]:
            pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, FLOR_AMARELA, (x + 1, y + 1, 4, 4))

    for x, y in pedras:
        for cor, rect in [(PEDRA, (x, y + 8, 28, 14)), (PEDRA_LUZ, (x + 8, y, 16, 10)), ((76, 76, 76), (x + 2, y + 18, 24, 5))]:
            pygame.draw.rect(tela, cor, rect)


def desenhar_arbusto(tela, rect):
    x = rect.x
    y = rect.y
    for cor, r in [(FOLHA_ESCURO, (x + 4, y + 24, 62, 20)), (FOLHA_MEDIO, (x + 10, y + 12, 26, 28)), (FOLHA_CLARO, (x + 34, y + 8, 28, 28)), (FOLHA_LUZ, (x + 42, y + 14, 8, 8))]:
        pygame.draw.rect(tela, cor, r)


def desenhar_arvore(tela, rect, folhas=False):
    x = rect.x
    y = rect.y

    partes = [
        (FOLHA_ESCURO, (x + 14, y + 40, 82, 46)), (FOLHA_MEDIO, (x + 4, y + 52, 42, 35)), (FOLHA_MEDIO, (x + 56, y + 50, 44, 36)),
        (FOLHA_MEDIO, (x + 24, y + 18, 58, 48)), (FOLHA_CLARO, (x + 36, y + 8, 42, 36)), (FOLHA_CLARO, (x + 48, y + 34, 38, 32)), (FOLHA_LUZ, (x + 48, y + 18, 10, 10)),
    ] if folhas else [
        ((52, 120, 46), (x + 30, y + 104, 50, 14)), (TRONCO_ESCURO, (x + 39, y + 60, 30, 58)), (TRONCO, (x + 43, y + 56, 25, 58)), (TRONCO_CLARO, (x + 52, y + 64, 5, 36)),
    ]
    for cor, r in partes:
        pygame.draw.rect(tela, cor, r)


def criar_objetos_randomizados(areas_seguras):
    def objetos(qtd, w, h, margem_x, margem_y, nome, ajuste):
        itens = []
        for _ in range(qtd):
            visual = pygame.Rect(0, 0, w, h)
            for _ in range(80):
                visual.topleft = (random.randint(margem_x, LARGURA_TELA - w - margem_x), random.randint(margem_y, ALTURA_TELA - h - margem_y))
                if not any(visual.colliderect(area) for area in areas_seguras):
                    break
            itens.append({"visual": visual, nome: pygame.Rect(visual.x + ajuste[0], visual.y + ajuste[1], ajuste[2], ajuste[3])})
        return itens

    return objetos(5, 110, 120, 40, 40, "colisao", (34, 80, 42, 40)), objetos(7, 70, 45, 30, 30, "lentidao", (10, 12, 50, 28))


def gerar_posicao_carne(arvores):
    while True:
        rect = pygame.Rect(random.randint(40, LARGURA_TELA - 40), random.randint(40, ALTURA_TELA - 40), 50, 50)
        if not any(rect.colliderect(arvore["colisao"]) for arvore in arvores):
            return rect.center


def mover_com_colisao(dino_rect, movimento_x, movimento_y, arvores):
    for eixo, mov in [("x", movimento_x), ("y", movimento_y)]:
        setattr(dino_rect, eixo, getattr(dino_rect, eixo) + mov)
        pe_dino = criar_pe_dino(dino_rect)
        for arvore in arvores:
            c = arvore["colisao"]
            if pe_dino.colliderect(c) and mov:
                if eixo == "x":
                    dino_rect.x += c.right - pe_dino.left if mov < 0 else -(pe_dino.right - c.left)
                else:
                    dino_rect.y += c.bottom - pe_dino.top if mov < 0 else -(pe_dino.bottom - c.top)
                pe_dino = criar_pe_dino(dino_rect)
    dino_rect.clamp_ip(pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA))


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


def criar_meteoro(agora, tempo_decorrido_ms, modo="multiplayer"):
    _, _, tempo_alerta = calcular_dificuldade_meteoros(tempo_decorrido_ms, modo)
    raio = sortear_raio_meteoro(modo)
    return {
        "centro": (
            random.randint(raio, LARGURA_TELA - raio),
            random.randint(raio, ALTURA_TELA - raio),
        ),
        "raio": raio,
        "impacto_em": agora + tempo_alerta,
        "finaliza_em": agora + tempo_alerta + METEORO_IMPACTO_MS,
        "causou_dano": False,
    }


def jogador_na_area_do_meteoro(dino_rect, meteoro):
    return distancia_entre_pontos(criar_pe_dino(dino_rect).center, meteoro["centro"]) <= meteoro["raio"]


def calcular_pontuacao_final(pontos_carne, tempo_sobrevivido_ms):
    return pontos_carne + (tempo_sobrevivido_ms // 1000) * PONTOS_POR_SEGUNDO


def velocidade_jogador(rect, arbustos):
    return 2 if any(criar_pe_dino(rect).colliderect(a["lentidao"]) for a in arbustos) else 5


def movimento_teclas(teclas, velocidade, cima, baixo, direita, esquerda):
    return ((teclas[direita] - teclas[esquerda]) * velocidade, (teclas[baixo] - teclas[cima]) * velocidade)


def desenhar_meteoros(tela, meteoros, agora):
    for meteoro in meteoros:
        centro = meteoro["centro"]
        raio = meteoro["raio"]

        if agora < meteoro["impacto_em"]:
            sombra = pygame.Surface((raio * 2 + 8, raio * 2 + 8), pygame.SRCALPHA)
            for args in [((35, 15, 15, 105), (raio + 4, raio + 4), raio), ((210, 45, 35, 180), (raio + 4, raio + 4), raio, 4), ((255, 210, 70, 180), (raio + 4, raio + 4), 8)]:
                pygame.draw.circle(sombra, *args)
            tela.blit(sombra, (centro[0] - raio - 4, centro[1] - raio - 4))
        elif agora < meteoro["finaliza_em"]:
            for args in [((95, 55, 38), centro, raio), ((210, 78, 38), centro, raio - 10, 5), ((245, 180, 64), centro, raio // 2), ((80, 80, 82), (centro[0] - 12, centro[1] - 8), 18), ((118, 118, 120), (centro[0] + 14, centro[1] + 6), 15)]:
                pygame.draw.circle(tela, *args)


def desenhar_jogador_morto(tela, rect):
    pygame.draw.line(tela, (180, 30, 30), (rect.left, rect.top), (rect.right, rect.bottom), 5)
    pygame.draw.line(tela, (180, 30, 30), (rect.right, rect.top), (rect.left, rect.bottom), 5)


def exibir_resultado_partida(tela, modo, resultado):
    fonte_titulo = pygame.font.Font("assets/fontes/fonte_pixel.ttf", 52)
    fonte_texto = pygame.font.Font("assets/fontes/fonte_pixel.ttf", 34)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE,
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
                f"Pontuação Final: {resultado['p1']}",
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
    clock = pygame.time.Clock()
    fonte = pygame.font.Font("assets/fontes/fonte_pixel.ttf", 36)

    animacoes_dino1 = carregar_animacoes_dino1()
    dino_rect = pygame.Rect(0, 0, *DINO_TAMANHO)
    dino_rect.center = (400, 200)
    dino_direcao = "direita"
    dino_movendo = False
    dino_lento = False

    if modo == "multiplayer":
        dino2 = pygame.image.load("assets/imagens/dino2 sprites/espinossauro.png").convert_alpha()
        dino2 = pygame.transform.flip(dino2, True, False)
        dino2 = pygame.transform.scale(dino2, DINO_TAMANHO)
        dino2_rect = dino2.get_rect(center=(680, 200))

    carne = pygame.image.load("assets/imagens/MeatUI2.png").convert_alpha()
    carne = pygame.transform.scale(carne, (50, 50))
    carne_rect = carne.get_rect(center=(600, 200))

    areas_seguras = [
        pygame.Rect(300, 120, 250, 220),
        pygame.Rect(520, 120, 180, 180),
    ]
    if modo == "multiplayer":
        areas_seguras.append(pygame.Rect(580, 120, 250, 220))

    arvores, arbustos = criar_objetos_randomizados(areas_seguras)
    terras, flores, pedras, matinhos = criar_elementos_chao()

    pontos = 0
    pontos2 = 0
    vivo = True
    vivo2 = modo == "multiplayer"
    tempo_inicio = pygame.time.get_ticks()
    tempo_morte = None
    tempo_morte2 = None
    meteoros = []
    proximo_meteoro = sortear_proximo_meteoro(tempo_inicio, 0, modo)

    while True:
        agora = pygame.time.get_ticks()
        tempo_decorrido = agora - tempo_inicio

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        if agora >= proximo_meteoro:
            meteoros.append(criar_meteoro(agora, tempo_decorrido, modo))
            proximo_meteoro = sortear_proximo_meteoro(agora, tempo_decorrido, modo)

        teclas = pygame.key.get_pressed()
        dino_movendo = False
        dino_lento = False

        if vivo:
            velocidade = velocidade_jogador(dino_rect, arbustos)
            dino_lento = velocidade == 2
            mx, my = movimento_teclas(teclas, velocidade, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
            dino_movendo = mx != 0 or my != 0
            dino_direcao = "direita" if mx > 0 else "esquerda" if mx < 0 else dino_direcao
            mover_com_colisao(dino_rect, mx, my, arvores)

        if modo == "multiplayer" and vivo2:
            mx, my = movimento_teclas(teclas, velocidade_jogador(dino2_rect, arbustos), pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
            mover_com_colisao(dino2_rect, mx, my, arvores)

        for meteoro in meteoros:
            if agora >= meteoro["impacto_em"] and agora < meteoro["finaliza_em"]:
                if not meteoro["causou_dano"]:
                    if vivo and jogador_na_area_do_meteoro(dino_rect, meteoro):
                        vivo = False
                        tempo_morte = agora
                    if modo == "multiplayer" and vivo2 and jogador_na_area_do_meteoro(dino2_rect, meteoro):
                        vivo2 = False
                        tempo_morte2 = agora
                    meteoro["causou_dano"] = True

        meteoros = [m for m in meteoros if agora < m["finaliza_em"]]

        desenhar_chao(tela, terras, flores, pedras, matinhos)
        desenhar_meteoros(tela, meteoros, agora)
        tela.blit(carne, carne_rect)

        for arbusto in arbustos:
            desenhar_arbusto(tela, arbusto["visual"])
        for arvore in arvores:
            desenhar_arvore(tela, arvore["visual"])

        frame_dino = obter_frame_animacao(animacoes_dino1[escolher_animacao_dino1(vivo, dino_movendo, dino_lento)], agora, repetir=vivo, iniciado_em=tempo_morte or agora)
        if dino_direcao == "esquerda":
            frame_dino = pygame.transform.flip(frame_dino, True, False)
        tela.blit(frame_dino, frame_dino.get_rect(center=dino_rect.center))

        if modo == "multiplayer":
            if vivo2:
                tela.blit(dino2, dino2_rect)
            else:
                desenhar_jogador_morto(tela, dino2_rect)

        for arvore in arvores:
            desenhar_arvore(tela, arvore["visual"], True)

        tela.blit(fonte.render(f"P1: {pontos}" if modo == "multiplayer" else f"Pontos: {pontos}", True, (255, 255, 255)), (20, 20))
        minutos, segundos = divmod(tempo_decorrido // 1000, 60)
        texto_tempo = fonte.render(f"{minutos:02d}:{segundos:02d}", True, (255, 255, 255))
        tela.blit(texto_tempo, texto_tempo.get_rect(center=(LARGURA_TELA // 2, 35)))

        if modo == "multiplayer":
            tela.blit(fonte.render(f"P2: {pontos2}", True, (255, 255, 255)), (LARGURA_TELA - 150, 20))

        if vivo and fn.verificar_colisao(dino_rect, carne_rect):
            pontos += 10
            carne_rect.center = gerar_posicao_carne(arvores)
            print(f"Pontos P1: {pontos}" if modo == "multiplayer" else f"Pontos: {pontos}")

        if modo == "multiplayer" and vivo2 and fn.verificar_colisao(dino2_rect, carne_rect):
            pontos2 += 10
            carne_rect.center = gerar_posicao_carne(arvores)
            print(f"Pontos P2: {pontos2}")

        pygame.display.update()
        clock.tick(60)

        if (modo == "multiplayer" and not vivo and not vivo2) or (modo != "multiplayer" and not vivo):
            tempo_morte, tempo_morte2 = tempo_morte or agora, tempo_morte2 or agora
            resultado = {"p1": calcular_pontuacao_final(pontos, tempo_morte - tempo_inicio)}
            if modo == "multiplayer":
                resultado["p2"] = calcular_pontuacao_final(pontos2, tempo_morte2 - tempo_inicio)
                resultado["vencedor"] = "P1 venceu" if resultado["p1"] > resultado["p2"] else "P2 venceu" if resultado["p2"] > resultado["p1"] else "Empate"
            return exibir_resultado_partida(tela, modo, resultado)


def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("BIG BANG")

    while True:
        opcao = executar_menu(tela)
        print(f"Opcao escolhida: {opcao}")

        if opcao == "sair":
            break

        resultado = executar_loop_jogo(tela, modo=opcao)
        if resultado == "sair":
            break

    pygame.quit()
