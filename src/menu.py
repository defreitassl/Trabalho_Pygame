import json
import os
import random

import pygame


LARGURA_TELA = 1080
ALTURA_TELA = 720
CAMINHO_CONFIGURACOES = os.path.join("data", "configuracoes.json")
CAMINHO_LOGO = os.path.join("assets", "imagens", "logo_bigbang.png")
CAMINHO_BACKGROUND = os.path.join("assets", "imagens", "background_menu.png")
CAMINHO_FONTE_PIXEL = os.path.join("assets", "fontes", "fonte_pixel.ttf")
CAMINHO_BOTOES = {
    "jogar": os.path.join("assets", "imagens", "buttons", "play_button.png"),
    "configuracoes": os.path.join("assets", "imagens", "buttons", "config_button.png"),
    "sair": os.path.join("assets", "imagens", "buttons", "exit_button.png"),
    "singleplayer": os.path.join("assets", "imagens", "buttons", "singleplayer_button.png"),
    "multiplayer": os.path.join("assets", "imagens", "buttons", "multiplayer_button.png"),
    "voltar": os.path.join("assets", "imagens", "buttons", "back_button.png"),
    "voltar_modo": os.path.join("assets", "imagens", "buttons", "back_button.png"),
    "voltar_configuracoes": os.path.join("assets", "imagens", "buttons", "back_button.png"),
    "diminuir_volume": os.path.join("assets", "imagens", "buttons", "minus_button.png"),
    "aumentar_volume": os.path.join("assets", "imagens", "buttons", "plus_button.png"),
    "alternar_sons_ligado": os.path.join("assets", "imagens", "buttons", "turn_on_button.png"),
    "alternar_sons_desligado": os.path.join("assets", "imagens", "buttons", "turn_off_button.png"),
}
CONFIGURACOES_PADRAO = {
    "volume": 50,
    "sons_ligados": True,
}

COR_FUNDO = (8, 10, 26)
COR_TEXTO = (245, 245, 255)
COR_TEXTO_SECUNDARIO = (190, 195, 220)
COR_BOTAO = (38, 48, 92)
COR_BOTAO_HOVER = (70, 90, 160)
COR_BORDA = (130, 155, 240)


def desenhar_texto(tela, texto, fonte, cor, x, y, centralizado=True):
    """Desenha um texto na tela."""
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect()

    if centralizado:
        retangulo_texto.center = (x, y)
    else:
        retangulo_texto.topleft = (x, y)

    tela.blit(superficie_texto, retangulo_texto)
    return retangulo_texto


def criar_fonte_pixel(tamanho):
    """Cria uma fonte grossa com fallback pronto para uma fonte pixelada futura."""
    if os.path.exists(CAMINHO_FONTE_PIXEL):
        fonte = pygame.font.Font(CAMINHO_FONTE_PIXEL, tamanho)
    else:
        caminho_fonte = pygame.font.match_font("dejavusansmono", bold=True)
        fonte = pygame.font.Font(caminho_fonte, tamanho) if caminho_fonte else pygame.font.SysFont(
            "monospace",
            tamanho,
            bold=True,
        )

    fonte.set_bold(True)
    return fonte


def criar_fontes_menu():
    """Centraliza as fontes usadas no menu."""
    return {
        "titulo": criar_fonte_pixel(64),
        "titulo_medio": criar_fonte_pixel(42),
        "texto": criar_fonte_pixel(28),
        "botao": criar_fonte_pixel(24),
        "texto_pequeno": criar_fonte_pixel(18),
    }


def desenhar_botao(tela, texto, retangulo, fonte, mouse_pos, imagem=None):
    """Desenha um botao e muda a cor quando o mouse passa por cima."""
    mouse_em_cima = retangulo.collidepoint(mouse_pos)

    if imagem:
        tela.blit(imagem, retangulo)
        if mouse_em_cima:
            destaque = pygame.Surface(retangulo.size, pygame.SRCALPHA)
            destaque.fill((255, 255, 255, 30))
            tela.blit(destaque, retangulo)
        return

    cor = COR_BOTAO_HOVER if mouse_em_cima else COR_BOTAO

    pygame.draw.rect(tela, cor, retangulo, border_radius=12)
    pygame.draw.rect(tela, COR_BORDA, retangulo, 2, border_radius=12)
    desenhar_texto(tela, texto, fonte, COR_TEXTO, retangulo.centerx, retangulo.centery)


def verificar_clique_botao(evento, retangulo):
    """Retorna True quando o usuario clica dentro do botao."""
    return (
        evento.type == pygame.MOUSEBUTTONDOWN
        and evento.button == 1
        and retangulo.collidepoint(evento.pos)
    )


def carregar_configuracoes():
    """Carrega as configuracoes salvas ou cria valores padrao."""
    try:
        with open(CAMINHO_CONFIGURACOES, "r", encoding="utf-8") as arquivo:
            configuracoes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        configuracoes = CONFIGURACOES_PADRAO.copy()

    configuracoes["volume"] = max(0, min(100, int(configuracoes.get("volume", 50))))
    configuracoes["sons_ligados"] = bool(configuracoes.get("sons_ligados", True))
    return configuracoes


def salvar_configuracoes(configuracoes):
    """Salva as configuracoes em um arquivo JSON simples."""
    os.makedirs(os.path.dirname(CAMINHO_CONFIGURACOES), exist_ok=True)

    with open(CAMINHO_CONFIGURACOES, "w", encoding="utf-8") as arquivo:
        json.dump(configuracoes, arquivo, indent=4, ensure_ascii=False)


def aplicar_volume(configuracoes):
    """Aplica o volume caso o mixer de audio ja esteja pronto."""
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(configuracoes["volume"] / 100)


def carregar_logo():
    """Carrega a logo visual do jogo, mantendo proporcao."""
    if not os.path.exists(CAMINHO_LOGO):
        return None

    try:
        logo = pygame.image.load(CAMINHO_LOGO).convert_alpha()
        largura_original, altura_original = logo.get_size()
        largura_maxima = int(LARGURA_TELA * 0.55)
        altura_maxima = int(ALTURA_TELA * 0.28)
        escala = min(
            largura_maxima / largura_original,
            altura_maxima / altura_original,
        )
        tamanho_logo = (
            int(largura_original * escala),
            int(altura_original * escala),
        )
        return pygame.transform.smoothscale(logo, tamanho_logo)
    except pygame.error:
        return None


def carregar_background_menu():
    """Carrega o background do menu preenchendo a tela sem distorcer."""
    if not os.path.exists(CAMINHO_BACKGROUND):
        return None

    try:
        background = pygame.image.load(CAMINHO_BACKGROUND).convert()
        largura_original, altura_original = background.get_size()
        escala = max(
            LARGURA_TELA / largura_original,
            ALTURA_TELA / altura_original,
        )
        tamanho_background = (
            int(largura_original * escala),
            int(altura_original * escala),
        )
        return pygame.transform.smoothscale(background, tamanho_background)
    except pygame.error:
        return None


def carregar_imagens_botoes(botoes):
    """Carrega as imagens personalizadas dos botoes no tamanho dos retangulos."""
    imagens = {}

    for nome, caminho in CAMINHO_BOTOES.items():
        nome_botao = nome
        if nome.startswith("alternar_sons_"):
            nome_botao = "alternar_sons"

        if nome_botao not in botoes or not os.path.exists(caminho):
            continue

        try:
            imagem = pygame.image.load(caminho).convert_alpha()
            imagens[nome] = pygame.transform.smoothscale(imagem, botoes[nome_botao].size)
        except pygame.error:
            continue

    return imagens


def centro_tela():
    """Retorna o ponto central da tela do menu."""
    return LARGURA_TELA // 2, ALTURA_TELA // 2


def criar_botao_centralizado(y, largura=None, altura=None):
    """Cria um botao centralizado horizontalmente."""
    altura = altura or max(84, min(108, int(ALTURA_TELA * 0.15)))
    largura = largura or int(altura * 3)
    x = (LARGURA_TELA - largura) // 2
    return pygame.Rect(x, y, largura, altura)


def criar_layout_menu():
    """Calcula posicoes proporcionais ao tamanho atual da tela."""
    altura_botao = max(84, min(108, int(ALTURA_TELA * 0.15)))
    espaco_botoes = int(altura_botao * 1.2)
    primeiro_botao_y = int(ALTURA_TELA * 0.39)

    return {
        "titulo_y": int(ALTURA_TELA * 0.17),
        "subtitulo_y": int(ALTURA_TELA * 0.34),
        "primeiro_botao_y": primeiro_botao_y,
        "segundo_botao_y": primeiro_botao_y + espaco_botoes,
        "terceiro_botao_y": primeiro_botao_y + espaco_botoes * 2,
        "volume_texto_y": int(ALTURA_TELA * 0.42),
        "volume_botoes_y": int(ALTURA_TELA * 0.46),
        "sons_texto_y": int(ALTURA_TELA * 0.60),
        "alternar_sons_y": int(ALTURA_TELA * 0.65),
        "voltar_configuracoes_y": int(ALTURA_TELA * 0.78),
        "botao_altura": altura_botao,
    }


def criar_estrelas(quantidade=80):
    """Cria posicoes fixas para as estrelas do fundo."""
    random.seed(7)
    estrelas = []

    for _ in range(quantidade):
        x = random.randint(0, LARGURA_TELA)
        y = random.randint(0, ALTURA_TELA)
        raio = random.choice([1, 1, 1, 2])
        brilho = random.randint(120, 255)
        estrelas.append((x, y, raio, brilho))

    return estrelas


def desenhar_fundo_espacial(tela, estrelas):
    """Desenha um fundo escuro com estrelas simples."""
    tela.fill(COR_FUNDO)

    for x, y, raio, brilho in estrelas:
        pygame.draw.circle(tela, (brilho, brilho, brilho), (x, y), raio)


def desenhar_background_menu(tela, background, estrelas):
    """Desenha o background visual do menu ou o fallback de estrelas."""
    if not background:
        desenhar_fundo_espacial(tela, estrelas)
        return

    x = (LARGURA_TELA - background.get_width()) // 2
    y = (ALTURA_TELA - background.get_height()) // 2
    tela.blit(background, (x, y))


def desenhar_tela_configuracoes(
    tela,
    fontes,
    configuracoes,
    botoes,
    estrelas,
    background,
    imagens_botoes=None,
):
    """Desenha a tela de configuracoes."""
    mouse_pos = pygame.mouse.get_pos()
    centro_x, _ = centro_tela()
    layout = criar_layout_menu()

    desenhar_background_menu(tela, background, estrelas)
    desenhar_texto(
        tela,
        "CONFIGURAÇÕES",
        fontes["titulo_medio"],
        COR_TEXTO,
        centro_x,
        layout["titulo_y"],
    )
    desenhar_texto(
        tela,
        f"Volume geral: {configuracoes['volume']}%",
        fontes["texto"],
        COR_TEXTO,
        centro_x,
        layout["volume_texto_y"],
    )
    desenhar_texto(
        tela,
        f"Sons do jogo: {'Ligados' if configuracoes['sons_ligados'] else 'Desligados'}",
        fontes["texto"],
        COR_TEXTO,
        centro_x,
        layout["sons_texto_y"],
    )

    imagem_alternar_sons = (
        imagens_botoes.get("alternar_sons_ligado")
        if configuracoes["sons_ligados"]
        else imagens_botoes.get("alternar_sons_desligado")
    ) if imagens_botoes else None

    desenhar_botao(
        tela,
        "-",
        botoes["diminuir_volume"],
        fontes["botao"],
        mouse_pos,
        imagens_botoes.get("diminuir_volume") if imagens_botoes else None,
    )
    desenhar_botao(
        tela,
        "+",
        botoes["aumentar_volume"],
        fontes["botao"],
        mouse_pos,
        imagens_botoes.get("aumentar_volume") if imagens_botoes else None,
    )
    desenhar_botao(
        tela,
        "Ligar/Desligar",
        botoes["alternar_sons"],
        fontes["botao"],
        mouse_pos,
        imagem_alternar_sons,
    )
    desenhar_botao(
        tela,
        "Voltar",
        botoes["voltar"],
        fontes["botao"],
        mouse_pos,
        imagens_botoes.get("voltar") if imagens_botoes else None,
    )


def mostrar_configuracoes(tela):
    """Executa a tela de configuracoes e volta para o menu quando solicitado."""
    relogio = pygame.time.Clock()
    estrelas = criar_estrelas()
    background = carregar_background_menu()
    configuracoes = carregar_configuracoes()
    aplicar_volume(configuracoes)

    fontes = criar_fontes_menu()
    centro_x, _ = centro_tela()
    layout = criar_layout_menu()
    botoes = {
        "diminuir_volume": pygame.Rect(centro_x - 150, layout["volume_botoes_y"], 96, 72),
        "aumentar_volume": pygame.Rect(centro_x + 54, layout["volume_botoes_y"], 96, 72),
        "alternar_sons": criar_botao_centralizado(layout["alternar_sons_y"], 270, 90),
        "voltar": criar_botao_centralizado(layout["voltar_configuracoes_y"], 270, 90),
    }
    imagens_botoes = carregar_imagens_botoes(botoes)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_configuracoes(configuracoes)
                return "sair"

            if verificar_clique_botao(evento, botoes["diminuir_volume"]):
                configuracoes["volume"] = max(0, configuracoes["volume"] - 10)
                aplicar_volume(configuracoes)
                salvar_configuracoes(configuracoes)

            if verificar_clique_botao(evento, botoes["aumentar_volume"]):
                configuracoes["volume"] = min(100, configuracoes["volume"] + 10)
                aplicar_volume(configuracoes)
                salvar_configuracoes(configuracoes)

            if verificar_clique_botao(evento, botoes["alternar_sons"]):
                configuracoes["sons_ligados"] = not configuracoes["sons_ligados"]
                salvar_configuracoes(configuracoes)

            if verificar_clique_botao(evento, botoes["voltar"]):
                salvar_configuracoes(configuracoes)
                return "voltar"

        desenhar_tela_configuracoes(
            tela,
            fontes,
            configuracoes,
            botoes,
            estrelas,
            background,
            imagens_botoes,
        )
        pygame.display.flip()
        relogio.tick(60)


def executar_menu(tela):
    """Mostra o menu inicial e retorna a opcao escolhida pelo jogador."""
    relogio = pygame.time.Clock()
    estrelas = criar_estrelas()
    background = carregar_background_menu()
    logo = carregar_logo()
    configuracoes = carregar_configuracoes()
    aplicar_volume(configuracoes)
    secao_atual = "principal"
    layout = criar_layout_menu()

    fontes = criar_fontes_menu()
    botoes = {
        "jogar": criar_botao_centralizado(layout["primeiro_botao_y"]),
        "configuracoes": criar_botao_centralizado(layout["segundo_botao_y"]),
        "sair": criar_botao_centralizado(layout["terceiro_botao_y"]),
        "singleplayer": criar_botao_centralizado(layout["primeiro_botao_y"]),
        "multiplayer": criar_botao_centralizado(layout["segundo_botao_y"]),
        "voltar_modo": criar_botao_centralizado(layout["terceiro_botao_y"]),
        "diminuir_volume": pygame.Rect(
            (LARGURA_TELA // 2) - 150,
            layout["volume_botoes_y"],
            96,
            72,
        ),
        "aumentar_volume": pygame.Rect(
            (LARGURA_TELA // 2) + 54,
            layout["volume_botoes_y"],
            96,
            72,
        ),
        "alternar_sons": criar_botao_centralizado(layout["alternar_sons_y"], 270, 90),
        "voltar_configuracoes": criar_botao_centralizado(
            layout["voltar_configuracoes_y"], 270, 90
        ),
    }
    imagens_botoes = carregar_imagens_botoes(botoes)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_configuracoes(configuracoes)
                return "sair"

            if secao_atual == "principal":
                if verificar_clique_botao(evento, botoes["jogar"]):
                    secao_atual = "modo_jogo"

                if verificar_clique_botao(evento, botoes["configuracoes"]):
                    secao_atual = "configuracoes"

                if verificar_clique_botao(evento, botoes["sair"]):
                    salvar_configuracoes(configuracoes)
                    return "sair"

            elif secao_atual == "modo_jogo":
                if verificar_clique_botao(evento, botoes["singleplayer"]):
                    salvar_configuracoes(configuracoes)
                    return "singleplayer"

                if verificar_clique_botao(evento, botoes["multiplayer"]):
                    salvar_configuracoes(configuracoes)
                    return "multiplayer"

                if verificar_clique_botao(evento, botoes["voltar_modo"]):
                    secao_atual = "principal"

            elif secao_atual == "configuracoes":
                if verificar_clique_botao(evento, botoes["diminuir_volume"]):
                    configuracoes["volume"] = max(0, configuracoes["volume"] - 10)
                    aplicar_volume(configuracoes)
                    salvar_configuracoes(configuracoes)

                if verificar_clique_botao(evento, botoes["aumentar_volume"]):
                    configuracoes["volume"] = min(100, configuracoes["volume"] + 10)
                    aplicar_volume(configuracoes)
                    salvar_configuracoes(configuracoes)

                if verificar_clique_botao(evento, botoes["alternar_sons"]):
                    configuracoes["sons_ligados"] = not configuracoes["sons_ligados"]
                    salvar_configuracoes(configuracoes)

                if verificar_clique_botao(evento, botoes["voltar_configuracoes"]):
                    salvar_configuracoes(configuracoes)
                    secao_atual = "principal"

        desenhar_background_menu(tela, background, estrelas)

        if logo:
            retangulo_logo = logo.get_rect(center=(LARGURA_TELA // 2, layout["titulo_y"]))
            tela.blit(logo, retangulo_logo)
        else:
            desenhar_texto(
                tela,
                "BIG BANG",
                fontes["titulo"],
                COR_TEXTO,
                LARGURA_TELA // 2,
                layout["titulo_y"],
            )

        if secao_atual == "principal":
            desenhar_botao(
                tela,
                "Jogar",
                botoes["jogar"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("jogar"),
            )
            desenhar_botao(
                tela,
                "Configurações",
                botoes["configuracoes"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("configuracoes"),
            )
            desenhar_botao(
                tela,
                "Sair",
                botoes["sair"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("sair"),
            )

        elif secao_atual == "modo_jogo":
            desenhar_botao(
                tela,
                "SinglePlayer",
                botoes["singleplayer"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("singleplayer"),
            )
            desenhar_botao(
                tela,
                "MultiPlayer",
                botoes["multiplayer"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("multiplayer"),
            )
            desenhar_botao(
                tela,
                "Voltar",
                botoes["voltar_modo"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("voltar_modo"),
            )

        elif secao_atual == "configuracoes":
            desenhar_texto(
                tela,
                f"Volume geral: {configuracoes['volume']}%",
                fontes["texto"],
                COR_TEXTO,
                LARGURA_TELA // 2,
                layout["volume_texto_y"],
            )
            desenhar_texto(
                tela,
                f"Sons do jogo: {'Ligados' if configuracoes['sons_ligados'] else 'Desligados'}",
                fontes["texto"],
                COR_TEXTO,
                LARGURA_TELA // 2,
                layout["sons_texto_y"],
            )
            imagem_alternar_sons = (
                imagens_botoes.get("alternar_sons_ligado")
                if configuracoes["sons_ligados"]
                else imagens_botoes.get("alternar_sons_desligado")
            )
            desenhar_botao(
                tela,
                "-",
                botoes["diminuir_volume"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("diminuir_volume"),
            )
            desenhar_botao(
                tela,
                "+",
                botoes["aumentar_volume"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("aumentar_volume"),
            )
            desenhar_botao(
                tela,
                "Ligar/Desligar",
                botoes["alternar_sons"],
                fontes["botao"],
                mouse_pos,
                imagem_alternar_sons,
            )
            desenhar_botao(
                tela,
                "Voltar",
                botoes["voltar_configuracoes"],
                fontes["botao"],
                mouse_pos,
                imagens_botoes.get("voltar_configuracoes"),
            )

        pygame.display.flip()
        relogio.tick(60)


def mostrar_menu(tela):
    """Nome alternativo para facilitar a integracao com outros arquivos."""
    return executar_menu(tela)
