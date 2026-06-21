import os
import random

import pygame

import src.funcoes as fn
from src.menu import ALTURA_TELA, LARGURA_TELA, executar_menu

from src.config import (
    VERDE_BASE,
    VERDE_CLARO,
    VERDE_ESCURO,
    VERDE_GRAMA,
    TERRA,
    TERRA_CLARA,
    TERRA_ESCURA,
    FOLHA_ESCURO,
    FOLHA_MEDIO,
    FOLHA_CLARO,
    FOLHA_LUZ,
    TRONCO,
    TRONCO_ESCURO,
    TRONCO_CLARO,
    PEDRA,
    PEDRA_LUZ,
    FLOR_BRANCA,
    FLOR_AMARELA,
    FLOR_ROSA,
    FLOR_AZUL,
    METEORO_IMPACTO_MS,
    DINO_TAMANHO,
    DINO_ANIMACAO_MS,
    CAMINHO_SPRITES_DINO1,
)

def carregar_frames_animacao(prefixo, quantidade):
    """
    Carrega e redimensiona os frames de uma animação a partir dos arquivos de imagem.

    Args:
        prefixo (str): Prefixo utilizado no nome dos arquivos da animação.
        quantidade (int): Quantidade de frames da animação.

    Returns:
        list[pygame.Surface]: Lista contendo os frames carregados.
    """
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(CAMINHO_SPRITES_DINO1, f"{prefixo} ({i}).png")).convert_alpha(),
            DINO_TAMANHO,
        )
        for i in range(1, quantidade + 1)
    ]


def carregar_animacoes_dino1():
    """
    Carrega todas as animações do dinossauro principal.

    Returns:
        dict: Dicionário contendo os frames das animações organizados por nome.
    """
    return {k.lower(): carregar_frames_animacao(k, q) for k, q in [("Idle", 10), ("Walk", 10), ("Run", 8), ("Dead", 8)]}


def escolher_animacao_dino1(vivo, movendo, lento):
    """
    Determina qual animação do dinossauro deve ser exibida.

    Args:
        vivo (bool): Indica se o jogador está vivo.
        movendo (bool): Indica se o jogador está se movendo.
        lento (bool): Indica se o jogador está em uma área de lentidão.

    Returns:
        str: Nome da animação correspondente ao estado atual.
    """
    return "dead" if not vivo else "idle" if not movendo else "walk" if lento else "run"


def obter_frame_animacao(frames, agora, repetir=True, iniciado_em=0):
    """
    Obtém o frame atual de uma animação com base no tempo.

    Args:
        frames (list): Lista de frames da animação.
        agora (int): Tempo atual em milissegundos.
        repetir (bool): Define se a animação deve repetir ao final.
        iniciado_em (int): Momento em que a animação começou.

    Returns:
        pygame.Surface: Frame correspondente ao instante atual.
    """
    indice = max(0, (agora - iniciado_em) // DINO_ANIMACAO_MS)
    return frames[indice % len(frames) if repetir else min(indice, len(frames) - 1)]


def criar_elementos_chao():
    """
    Cria os elementos decorativos utilizados no cenário.

    Returns:
        tuple: Listas contendo áreas de terra, flores, pedras e matinhos.
    """
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
    """
    Desenha o cenário base do jogo.

    Args:
        tela (pygame.Surface): Superfície onde o cenário será desenhado.
        terras (list): Áreas de terra do mapa.
        flores (list): Flores decorativas.
        pedras (list): Pedras decorativas.
        matinhos (list): Matinhos distribuídos pelo cenário.
    """
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
    """
    Desenha um arbusto no cenário.

    Args:
        tela (pygame.Surface): Superfície onde será desenhado.
        rect (pygame.Rect): Área de referência do arbusto.
    """
    x = rect.x
    y = rect.y
    for cor, r in [(FOLHA_ESCURO, (x + 4, y + 24, 62, 20)), (FOLHA_MEDIO, (x + 10, y + 12, 26, 28)), (FOLHA_CLARO, (x + 34, y + 8, 28, 28)), (FOLHA_LUZ, (x + 42, y + 14, 8, 8))]:
        pygame.draw.rect(tela, cor, r)


def desenhar_arvore(tela, rect, folhas=False):
    """
    Desenha uma árvore ou apenas sua copa.

    Args:
        tela (pygame.Surface): Superfície onde será desenhada.
        rect (pygame.Rect): Área de referência da árvore.
        folhas (bool): Se verdadeiro, desenha apenas as folhas.
    """
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
    """
    Cria árvores e arbustos em posições aleatórias do mapa,
    evitando as áreas seguras definidas.

    Args:
        areas_seguras (list): Lista de áreas onde objetos não podem surgir.

    Returns:
        tuple: Listas contendo árvores e arbustos gerados.
    """
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
    """
    Gera uma posição aleatória válida para a carne.

    Args:
        arvores (list): Lista de árvores presentes no mapa.

    Returns:
        tuple: Coordenadas centrais da nova posição da carne.
    """
    while True:
        rect = pygame.Rect(random.randint(40, LARGURA_TELA - 40), random.randint(40, ALTURA_TELA - 40), 50, 50)
        if not any(rect.colliderect(arvore["colisao"]) for arvore in arvores):
            return rect.center


def mover_com_colisao(dino_rect, movimento_x, movimento_y, arvores):
    """
    Move o jogador aplicando colisão com árvores e limites da tela.

    Args:
        dino_rect (pygame.Rect): Retângulo do jogador.
        movimento_x (int): Movimento horizontal.
        movimento_y (int): Movimento vertical.
        arvores (list): Lista de árvores com áreas de colisão.
    """
    for eixo, mov in [("x", movimento_x), ("y", movimento_y)]:
        setattr(dino_rect, eixo, getattr(dino_rect, eixo) + mov)
        pe_dino = fn.criar_pe_dino(dino_rect)
        for arvore in arvores:
            c = arvore["colisao"]
            if pe_dino.colliderect(c) and mov:
                if eixo == "x":
                    dino_rect.x += c.right - pe_dino.left if mov < 0 else -(pe_dino.right - c.left)
                else:
                    dino_rect.y += c.bottom - pe_dino.top if mov < 0 else -(pe_dino.bottom - c.top)
                pe_dino = fn.criar_pe_dino(dino_rect)
    dino_rect.clamp_ip(pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA))

def criar_meteoro(agora, tempo_decorrido_ms, modo="multiplayer"):
    """
    Cria um meteoro com posição, raio e tempos definidos.

    Args:
        agora (int): Tempo atual em milissegundos.
        tempo_decorrido_ms (int): Tempo de partida já transcorrido.
        modo (str): Modo de jogo atual.

    Returns:
        dict: Dados do meteoro criado.
    """
    _, _, tempo_alerta = fn.calcular_dificuldade_meteoros(tempo_decorrido_ms, modo)
    raio = fn.sortear_raio_meteoro(modo)
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


def desenhar_meteoros(tela, meteoros, agora):
    """
    Desenha os meteoros ativos e seus avisos de impacto.

    Args:
        tela (pygame.Surface): Superfície onde serão desenhados.
        meteoros (list): Lista de meteoros ativos.
        agora (int): Tempo atual em milissegundos.
    """
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
    """
    Exibe um marcador visual indicando que o jogador morreu.

    Args:
        tela (pygame.Surface): Superfície onde será desenhado.
        rect (pygame.Rect): Área ocupada pelo jogador.
    """
    pygame.draw.line(tela, (180, 30, 30), (rect.left, rect.top), (rect.right, rect.bottom), 5)
    pygame.draw.line(tela, (180, 30, 30), (rect.right, rect.top), (rect.left, rect.bottom), 5)


def exibir_resultado_partida(tela, modo, resultado):
    """
    Exibe a tela de fim de partida e aguarda uma ação do jogador.

    Args:
        tela (pygame.Surface): Superfície principal do jogo.
        modo (str): Modo de jogo utilizado.
        resultado (dict): Informações finais da partida.

    Returns:
        str: "menu" para retornar ao menu ou "sair" para encerrar o jogo.
    """
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
    """
    Executa o loop principal da partida.

    Controla movimentação, colisões, pontuação, meteoros,
    renderização e condições de derrota.

    Args:
        tela (pygame.Surface): Superfície principal do jogo.
        modo (str): Modo de jogo selecionado.

    Returns:
        str: Resultado da partida ou ação escolhida pelo jogador.
    """
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
    proximo_meteoro = fn.sortear_proximo_meteoro(tempo_inicio, 0, modo)

    while True:
        agora = pygame.time.get_ticks()
        tempo_decorrido = agora - tempo_inicio

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        if agora >= proximo_meteoro:
            meteoros.append(criar_meteoro(agora, tempo_decorrido, modo))
            proximo_meteoro = fn.sortear_proximo_meteoro(agora, tempo_decorrido, modo)

        teclas = pygame.key.get_pressed()
        dino_movendo = False
        dino_lento = False

        if vivo:
            velocidade = fn.velocidade_jogador(dino_rect, arbustos)
            dino_lento = velocidade == 2
            mx, my = fn.movimento_teclas(teclas, velocidade, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
            dino_movendo = mx != 0 or my != 0
            dino_direcao = "direita" if mx > 0 else "esquerda" if mx < 0 else dino_direcao
            mover_com_colisao(dino_rect, mx, my, arvores)

        if modo == "multiplayer" and vivo2:
            mx, my = fn.movimento_teclas(teclas, fn.velocidade_jogador(dino2_rect, arbustos), pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
            mover_com_colisao(dino2_rect, mx, my, arvores)

        for meteoro in meteoros:
            if agora >= meteoro["impacto_em"] and agora < meteoro["finaliza_em"]:
                if not meteoro["causou_dano"]:
                    if vivo and fn.jogador_na_area_do_meteoro(dino_rect, meteoro):
                        vivo = False
                        tempo_morte = agora
                    if modo == "multiplayer" and vivo2 and fn.jogador_na_area_do_meteoro(dino2_rect, meteoro):
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
            resultado = {"p1": fn.calcular_pontuacao_final(pontos, tempo_morte - tempo_inicio)}
            if modo == "multiplayer":
                resultado["p2"] = fn.calcular_pontuacao_final(pontos2, tempo_morte2 - tempo_inicio)
                resultado["vencedor"] = "P1 venceu" if resultado["p1"] > resultado["p2"] else "P2 venceu" if resultado["p2"] > resultado["p1"] else "Empate"
            return exibir_resultado_partida(tela, modo, resultado)


def executar_jogo():
    """
    Inicializa o Pygame, executa o menu principal
    e controla o fluxo geral do jogo.
    """
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