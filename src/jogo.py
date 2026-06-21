import random
import os

import pygame

import src.config as cfg
import src.funcoes as fn
import src.sons as sons
from src.menu import ALTURA_TELA, LARGURA_TELA, carregar_configuracoes, executar_menu


def carregar_frames_animacao(pasta_base, prefixo, quantidade):
    """
    Carrega uma sequencia de frames a partir de arquivos PNG.

    Args:
        pasta_base (str): Pasta onde os frames estao armazenados.
        prefixo (str): Prefixo do estado, ex.: Idle ou Run.
        quantidade (int): Quantidade de frames.

    Returns:
        list[pygame.Surface]: Frames redimensionados.
    """
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(pasta_base, f"{prefixo} ({indice}).png")).convert_alpha(),
            cfg.DINO_TAMANHO,
        )
        for indice in range(1, quantidade + 1)
    ]


def carregar_animacoes(pasta):
    """
    Carrega as animacoes de um dinossauro.

    Returns:
        dict: Frames organizados por nome de animacao.
    """
    return {
        "idle": carregar_frames_animacao(pasta, "Idle", 2),
        "walk": carregar_frames_animacao(pasta, "Run", 2),
        "run": carregar_frames_animacao(pasta, "Run", 2),
        "dead": carregar_frames_animacao(pasta, "Dead", 1),
    }


def escolher_animacao_personagem(vivo, movendo, lento):
    """
    Determina qual animação do dinossauro deve ser exibida.

    Args:
        vivo (bool): Indica se o jogador está vivo.
        movendo (bool): Indica se o jogador está se movendo.
        lento (bool): Indica se o jogador está em uma área de lentidão.

    Returns:
        str: Nome da animação correspondente ao estado atual.
    """
    if not vivo:
        return "dead"
    if not movendo:
        return "idle"
    if lento:
        return "walk"
    return "run"


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
    indice = max(0, (agora - iniciado_em) // cfg.DINO_ANIMACAO_MS)
    return frames[indice % len(frames) if repetir else min(indice, len(frames) - 1)]


def criar_estado_jogador(posicao, controles, pasta_sprites):
    """
    Cria o estado de animacao e jogo de um personagem.

    Args:
        posicao (tuple): Posicao inicial do jogador.
        controles (tuple): Teclas de movimento.
        pasta_sprites (str): Pasta com os sprites do personagem.

    Returns:
        dict: Estado consolidado do jogador.
    """
    rect = pygame.Rect(0, 0, *cfg.DINO_TAMANHO)
    rect.center = posicao
    return {
        "rect": rect,
        "controles": controles,
        "animacoes": carregar_animacoes(pasta_sprites),
        "pontos": 0,
        "vivo": True,
        "tempo_morte": None,
        "direcao": "direita",
        "movendo": False,
        "lento": False,
    }


def obter_sprite_jogador(jogador, agora):
    """
    Resolve o sprite atual de um jogador a partir do seu estado.

    Args:
        jogador (dict): Estado do personagem.
        agora (int): Tempo atual em milissegundos.

    Returns:
        tuple[pygame.Surface, pygame.Rect]: Sprite final e retangulo de desenho.
    """
    nome_animacao = escolher_animacao_personagem(jogador["vivo"], jogador["movendo"], jogador["lento"])
    sprite = obter_frame_animacao(
        jogador["animacoes"][nome_animacao],
        agora,
        repetir=jogador["vivo"],
        iniciado_em=jogador["tempo_morte"] or agora,
    )

    if jogador["direcao"] == "esquerda":
        sprite = pygame.transform.flip(sprite, True, False)
    return sprite, sprite.get_rect(center=jogador["rect"].center)


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
        (110, 260, cfg.FLOR_BRANCA), (270, 420, cfg.FLOR_ROSA),
        (530, 330, cfg.FLOR_AZUL), (720, 165, cfg.FLOR_BRANCA),
        (965, 250, cfg.FLOR_AMARELA), (600, 620, cfg.FLOR_BRANCA),
        (860, 590, cfg.FLOR_AZUL),
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
    tela.fill(cfg.VERDE_BASE)
    for mancha in [(40, 40, 220, 130), (350, 20, 260, 120), (780, 70, 230, 150), (70, 500, 240, 120), (450, 520, 260, 130), (800, 430, 220, 150)]:
        pygame.draw.rect(tela, cfg.VERDE_CLARO, mancha)

    for pontos in terras:
        pygame.draw.polygon(tela, cfg.TERRA, pontos)
        for x, y in pontos:
            pygame.draw.rect(tela, cfg.VERDE_GRAMA, (x - 6, y - 4, 12, 6))

        min_x, max_x = min(p[0] for p in pontos), max(p[0] for p in pontos)
        min_y, max_y = min(p[1] for p in pontos), max(p[1] for p in pontos)
        for qtd, cor, w, h, ax, ay in [(12, cfg.TERRA_ESCURA, 9, 3, 31, 17), (4, cfg.TERRA_CLARA, 14, 5, 47, 23)]:
            for i in range(qtd):
                pygame.draw.rect(tela, cor, (min_x + (i * ax) % max(1, max_x - min_x), min_y + (i * ay) % max(1, max_y - min_y), w, h))

    for x, y, tipo in matinhos:
        itens = [(cfg.VERDE_GRAMA, (x, y + 10, 18, 4)), (cfg.VERDE_GRAMA, (x + 6, y + 4, 4, 12))] if tipo == 1 else [(cfg.VERDE_ESCURO, (x + 8, y, 7, 7)), (cfg.VERDE_CLARO, (x + 18, y + 10, 7, 7))]
        for cor, rect in itens:
            pygame.draw.rect(tela, cor, rect)

    for x, y, cor in flores:
        for rect in [(x, y - 5, 6, 6), (x, y + 5, 6, 6), (x - 5, y, 6, 6), (x + 5, y, 6, 6)]:
            pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, cfg.FLOR_AMARELA, (x + 1, y + 1, 4, 4))

    for x, y in pedras:
        for cor, rect in [(cfg.PEDRA, (x, y + 8, 28, 14)), (cfg.PEDRA_LUZ, (x + 8, y, 16, 10)), ((76, 76, 76), (x + 2, y + 18, 24, 5))]:
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
    for cor, r in [(cfg.FOLHA_ESCURO, (x + 4, y + 24, 62, 20)), (cfg.FOLHA_MEDIO, (x + 10, y + 12, 26, 28)), (cfg.FOLHA_CLARO, (x + 34, y + 8, 28, 28)), (cfg.FOLHA_LUZ, (x + 42, y + 14, 8, 8))]:
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
        (cfg.FOLHA_ESCURO, (x + 14, y + 40, 82, 46)), (cfg.FOLHA_MEDIO, (x + 4, y + 52, 42, 35)), (cfg.FOLHA_MEDIO, (x + 56, y + 50, 44, 36)),
        (cfg.FOLHA_MEDIO, (x + 24, y + 18, 58, 48)), (cfg.FOLHA_CLARO, (x + 36, y + 8, 42, 36)), (cfg.FOLHA_CLARO, (x + 48, y + 34, 38, 32)), (cfg.FOLHA_LUZ, (x + 48, y + 18, 10, 10)),
    ] if folhas else [
        ((52, 120, 46), (x + 30, y + 104, 50, 14)), (cfg.TRONCO_ESCURO, (x + 39, y + 60, 30, 58)), (cfg.TRONCO, (x + 43, y + 56, 25, 58)), (cfg.TRONCO_CLARO, (x + 52, y + 64, 5, 36)),
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
    dino_rect.x += movimento_x
    if any(fn.criar_pe_dino(dino_rect).colliderect(arvore["colisao"]) for arvore in arvores):
        dino_rect.x -= movimento_x

    dino_rect.y += movimento_y
    if any(fn.criar_pe_dino(dino_rect).colliderect(arvore["colisao"]) for arvore in arvores):
        dino_rect.y -= movimento_y

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
        "finaliza_em": agora + tempo_alerta + cfg.METEORO_IMPACTO_MS,
        "causou_dano": False,
        "som_tocado": False,
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
    configuracoes = carregar_configuracoes()
    efeitos = sons.carregar_efeitos(configuracoes)
    sons.ajustar_volume_musica(configuracoes, durante_jogo=True)

    jogador1 = criar_estado_jogador(
        (400, 200),
        (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a),
        cfg.CAMINHO_SPRITES_DINO1,
    )
    jogadores = [jogador1]

    if modo == "multiplayer":
        jogador2 = criar_estado_jogador(
            (680, 200),
            (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT),
            cfg.CAMINHO_SPRITES_DINO2,
        )
        jogadores.append(jogador2)

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

    tempo_inicio = pygame.time.get_ticks()
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
        for jogador in jogadores:
            jogador["movendo"] = False
            jogador["lento"] = False
            if not jogador["vivo"]:
                continue

            velocidade = fn.velocidade_jogador(jogador["rect"], arbustos)
            jogador["lento"] = velocidade == 2
            cima, baixo, direita, esquerda = jogador["controles"]
            mx, my = fn.movimento_teclas(teclas, velocidade, cima, baixo, direita, esquerda)
            jogador["movendo"] = bool(mx or my)
            if mx > 0:
                jogador["direcao"] = "direita"
            elif mx < 0:
                jogador["direcao"] = "esquerda"
            mover_com_colisao(jogador["rect"], mx, my, arvores)

        for meteoro in meteoros:
            if agora >= meteoro["impacto_em"] and not meteoro["som_tocado"]:
                sons.tocar_efeito(efeitos, "impacto")
                meteoro["som_tocado"] = True

            if meteoro["impacto_em"] <= agora < meteoro["finaliza_em"] and not meteoro["causou_dano"]:
                jogador_atingido = False
                for jogador in jogadores:
                    if jogador["vivo"] and fn.jogador_na_area_do_meteoro(jogador["rect"], meteoro):
                        jogador["vivo"] = False
                        jogador["tempo_morte"] = agora
                        jogador_atingido = True
                if jogador_atingido:
                    sons.tocar_efeito(efeitos, "morte")
                meteoro["causou_dano"] = True

        meteoros = [m for m in meteoros if agora < m["finaliza_em"]]

        desenhar_chao(tela, terras, flores, pedras, matinhos)
        desenhar_meteoros(tela, meteoros, agora)
        tela.blit(carne, carne_rect)

        for arbusto in arbustos:
            desenhar_arbusto(tela, arbusto["visual"])
        for arvore in arvores:
            desenhar_arvore(tela, arvore["visual"])

        for jogador in jogadores:
            sprite, rect = obter_sprite_jogador(jogador, agora)
            tela.blit(sprite, rect)

        for arvore in arvores:
            desenhar_arvore(tela, arvore["visual"], True)

        tela.blit(fonte.render(f"P1: {jogador1['pontos']}" if modo == "multiplayer" else f"Pontos: {jogador1['pontos']}", True, (255, 255, 255)), (20, 20))
        minutos, segundos = divmod(tempo_decorrido // 1000, 60)
        texto_tempo = fonte.render(f"{minutos:02d}:{segundos:02d}", True, (255, 255, 255))
        tela.blit(texto_tempo, texto_tempo.get_rect(center=(LARGURA_TELA // 2, 35)))

        if modo == "multiplayer":
            tela.blit(fonte.render(f"P2: {jogador2['pontos']}", True, (255, 255, 255)), (LARGURA_TELA - 150, 20))

        for numero, jogador in enumerate(jogadores, 1):
            if jogador["vivo"] and jogador["rect"].colliderect(carne_rect):
                jogador["pontos"] += 10
                sons.tocar_efeito(efeitos, "coleta")
                carne_rect.center = gerar_posicao_carne(arvores)
                print(f"Pontos P{numero}: {jogador['pontos']}" if modo == "multiplayer" else f"Pontos: {jogador['pontos']}")

        pygame.display.update()
        clock.tick(60)

        if not any(jogador["vivo"] for jogador in jogadores):
            resultado = {"p1": fn.calcular_pontuacao_final(jogador1["pontos"], jogador1["tempo_morte"] - tempo_inicio)}
            if modo == "multiplayer":
                resultado["p2"] = fn.calcular_pontuacao_final(jogador2["pontos"], jogador2["tempo_morte"] - tempo_inicio)
                if resultado["p1"] > resultado["p2"]:
                    resultado["vencedor"] = "P1 venceu"
                elif resultado["p2"] > resultado["p1"]:
                    resultado["vencedor"] = "P2 venceu"
                else:
                    resultado["vencedor"] = "Empate"
            return exibir_resultado_partida(tela, modo, resultado)


def executar_jogo():
    """
    Inicializa o Pygame, executa o menu principal
    e controla o fluxo geral do jogo.
    """
    pygame.mixer.pre_init(44100, -16, 2, 512)
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
