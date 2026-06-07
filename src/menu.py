import json
import os
import random

import pygame


LARGURA_TELA = 1080
ALTURA_TELA = 720
CAMINHO_CONFIGURACOES = os.path.join("data", "configuracoes.json")
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


def desenhar_botao(tela, texto, retangulo, fonte, mouse_pos):
    """Desenha um botao e muda a cor quando o mouse passa por cima."""
    mouse_em_cima = retangulo.collidepoint(mouse_pos)
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
    """Tenta carregar uma logo futura, mas o menu funciona sem ela."""
    caminho_logo = os.path.join("assets", "logo.png")

    if not os.path.exists(caminho_logo):
        return None

    try:
        logo = pygame.image.load(caminho_logo).convert_alpha()
        return pygame.transform.smoothscale(logo, (260, 100))
    except pygame.error:
        return None


def centro_tela():
    """Retorna o ponto central da tela do menu."""
    return LARGURA_TELA // 2, ALTURA_TELA // 2


def criar_botao_centralizado(y, largura=None, altura=None):
    """Cria um botao centralizado horizontalmente."""
    largura = largura or min(360, int(LARGURA_TELA * 0.42))
    altura = altura or max(50, min(64, int(ALTURA_TELA * 0.09)))
    x = (LARGURA_TELA - largura) // 2
    return pygame.Rect(x, y, largura, altura)


def criar_layout_menu():
    """Calcula posicoes proporcionais ao tamanho atual da tela."""
    altura_botao = max(50, min(64, int(ALTURA_TELA * 0.09)))
    espaco_botoes = int(altura_botao * 1.35)
    primeiro_botao_y = int(ALTURA_TELA * 0.44)

    return {
        "titulo_y": int(ALTURA_TELA * 0.22),
        "subtitulo_y": int(ALTURA_TELA * 0.31),
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


def desenhar_tela_configuracoes(tela, fontes, configuracoes, botoes, estrelas):
    """Desenha a tela de configuracoes."""
    mouse_pos = pygame.mouse.get_pos()
    centro_x, _ = centro_tela()
    layout = criar_layout_menu()

    desenhar_fundo_espacial(tela, estrelas)
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

    desenhar_botao(tela, "-", botoes["diminuir_volume"], fontes["botao"], mouse_pos)
    desenhar_botao(tela, "+", botoes["aumentar_volume"], fontes["botao"], mouse_pos)
    desenhar_botao(tela, "Ligar/Desligar", botoes["alternar_sons"], fontes["botao"], mouse_pos)
    desenhar_botao(tela, "Voltar", botoes["voltar"], fontes["botao"], mouse_pos)


def mostrar_configuracoes(tela):
    """Executa a tela de configuracoes e volta para o menu quando solicitado."""
    relogio = pygame.time.Clock()
    estrelas = criar_estrelas()
    configuracoes = carregar_configuracoes()
    aplicar_volume(configuracoes)

    fontes = {
        "titulo_medio": pygame.font.SysFont("arial", 42, bold=True),
        "texto": pygame.font.SysFont("arial", 26),
        "botao": pygame.font.SysFont("arial", 24, bold=True),
    }
    centro_x, _ = centro_tela()
    layout = criar_layout_menu()
    botoes = {
        "diminuir_volume": pygame.Rect(centro_x - 130, layout["volume_botoes_y"], 80, 50),
        "aumentar_volume": pygame.Rect(centro_x + 50, layout["volume_botoes_y"], 80, 50),
        "alternar_sons": criar_botao_centralizado(layout["alternar_sons_y"], 280, 56),
        "voltar": criar_botao_centralizado(layout["voltar_configuracoes_y"], 260, 58),
    }

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

        desenhar_tela_configuracoes(tela, fontes, configuracoes, botoes, estrelas)
        pygame.display.flip()
        relogio.tick(60)


def executar_menu(tela):
    """Mostra o menu inicial e retorna a opcao escolhida pelo jogador."""
    relogio = pygame.time.Clock()
    estrelas = criar_estrelas()
    logo = carregar_logo()
    configuracoes = carregar_configuracoes()
    aplicar_volume(configuracoes)
    secao_atual = "principal"
    layout = criar_layout_menu()

    fontes = {
        "titulo": pygame.font.SysFont("arial", 64, bold=True),
        "titulo_medio": pygame.font.SysFont("arial", 42, bold=True),
        "texto": pygame.font.SysFont("arial", 26),
        "botao": pygame.font.SysFont("arial", 24, bold=True),
        "texto_pequeno": pygame.font.SysFont("arial", 18),
    }
    botoes = {
        "jogar": criar_botao_centralizado(layout["primeiro_botao_y"]),
        "configuracoes": criar_botao_centralizado(layout["segundo_botao_y"]),
        "sair": criar_botao_centralizado(layout["terceiro_botao_y"]),
        "singleplayer": criar_botao_centralizado(layout["primeiro_botao_y"]),
        "multiplayer": criar_botao_centralizado(layout["segundo_botao_y"]),
        "voltar_modo": criar_botao_centralizado(layout["terceiro_botao_y"]),
        "diminuir_volume": pygame.Rect(
            (LARGURA_TELA // 2) - 130,
            layout["volume_botoes_y"],
            80,
            50,
        ),
        "aumentar_volume": pygame.Rect(
            (LARGURA_TELA // 2) + 50,
            layout["volume_botoes_y"],
            80,
            50,
        ),
        "alternar_sons": criar_botao_centralizado(layout["alternar_sons_y"], 280, 56),
        "voltar_configuracoes": criar_botao_centralizado(
            layout["voltar_configuracoes_y"], 260, 58
        ),
    }

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

        desenhar_fundo_espacial(tela, estrelas)

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
            desenhar_texto(
                tela,
                "Menu inicial",
                fontes["texto_pequeno"],
                COR_TEXTO_SECUNDARIO,
                LARGURA_TELA // 2,
                layout["subtitulo_y"],
            )

            desenhar_botao(tela, "Jogar", botoes["jogar"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "Configurações", botoes["configuracoes"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "Sair", botoes["sair"], fontes["botao"], mouse_pos)

        elif secao_atual == "modo_jogo":
            desenhar_texto(
                tela,
                "Escolha o modo de jogo",
                fontes["texto_pequeno"],
                COR_TEXTO_SECUNDARIO,
                LARGURA_TELA // 2,
                layout["subtitulo_y"],
            )

            desenhar_botao(tela, "SinglePlayer", botoes["singleplayer"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "MultiPlayer", botoes["multiplayer"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "Voltar", botoes["voltar_modo"], fontes["botao"], mouse_pos)

        elif secao_atual == "configuracoes":
            desenhar_texto(
                tela,
                "Configurações",
                fontes["texto_pequeno"],
                COR_TEXTO_SECUNDARIO,
                LARGURA_TELA // 2,
                layout["subtitulo_y"],
            )
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
            desenhar_botao(tela, "-", botoes["diminuir_volume"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "+", botoes["aumentar_volume"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "Ligar/Desligar", botoes["alternar_sons"], fontes["botao"], mouse_pos)
            desenhar_botao(tela, "Voltar", botoes["voltar_configuracoes"], fontes["botao"], mouse_pos)

        pygame.display.flip()
        relogio.tick(60)


def mostrar_menu(tela):
    """Nome alternativo para facilitar a integracao com outros arquivos."""
    return executar_menu(tela)
