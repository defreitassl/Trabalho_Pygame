import json
import os
import random

import pygame

import src.sons as sons


LARGURA_TELA, ALTURA_TELA = 1080, 720
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
CONFIGURACOES_PADRAO = {"volume": 50, "sons_ligados": True}
COR_FUNDO, COR_TEXTO = (8, 10, 26), (245, 245, 255)
COR_BOTAO, COR_BOTAO_HOVER, COR_BORDA = (38, 48, 92), (70, 90, 160), (130, 155, 240)


def desenhar_texto(tela, texto, fonte, cor, x, y, centralizado=True):
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect()
    retangulo_texto.center = (x, y) if centralizado else retangulo_texto.center
    retangulo_texto.topleft = (x, y) if not centralizado else retangulo_texto.topleft
    tela.blit(superficie_texto, retangulo_texto)
    return retangulo_texto


def criar_fonte_pixel(tamanho):
    if os.path.exists(CAMINHO_FONTE_PIXEL):
        fonte = pygame.font.Font(CAMINHO_FONTE_PIXEL, tamanho)
    else:
        caminho_fonte = pygame.font.match_font("dejavusansmono", bold=True)
        fonte = pygame.font.Font(caminho_fonte, tamanho) if caminho_fonte else pygame.font.SysFont("monospace", tamanho, bold=True)
    fonte.set_bold(True)
    return fonte


def desenhar_botao(tela, texto, retangulo, fonte, mouse_pos, imagem=None):
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
    return evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and retangulo.collidepoint(evento.pos)


def carregar_configuracoes():
    try:
        with open(CAMINHO_CONFIGURACOES, "r", encoding="utf-8") as arquivo:
            configuracoes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        configuracoes = CONFIGURACOES_PADRAO.copy()

    configuracoes["volume"] = max(0, min(100, int(configuracoes.get("volume", 50))))
    configuracoes["sons_ligados"] = bool(configuracoes.get("sons_ligados", True))
    return configuracoes


def salvar_configuracoes(configuracoes):
    os.makedirs(os.path.dirname(CAMINHO_CONFIGURACOES), exist_ok=True)
    with open(CAMINHO_CONFIGURACOES, "w", encoding="utf-8") as arquivo:
        json.dump(configuracoes, arquivo, indent=4, ensure_ascii=False)


def aplicar_volume(configuracoes):
    sons.ajustar_volume_musica(configuracoes)


def carregar_logo():
    if not os.path.exists(CAMINHO_LOGO):
        return None

    try:
        logo = pygame.image.load(CAMINHO_LOGO).convert_alpha()
        largura_original, altura_original = logo.get_size()
        escala = min(int(LARGURA_TELA * 0.55) / largura_original, int(ALTURA_TELA * 0.28) / altura_original)
        return pygame.transform.smoothscale(logo, (int(largura_original * escala), int(altura_original * escala)))
    except pygame.error:
        return None


def carregar_background_menu():
    if not os.path.exists(CAMINHO_BACKGROUND):
        return None

    try:
        background = pygame.image.load(CAMINHO_BACKGROUND).convert()
        largura_original, altura_original = background.get_size()
        escala = max(LARGURA_TELA / largura_original, ALTURA_TELA / altura_original)
        return pygame.transform.smoothscale(background, (int(largura_original * escala), int(altura_original * escala)))
    except pygame.error:
        return None


def carregar_imagens_botoes(botoes):
    imagens = {}

    for nome, caminho in CAMINHO_BOTOES.items():
        nome_botao = "alternar_sons" if nome.startswith("alternar_sons_") else nome
        if nome_botao not in botoes or not os.path.exists(caminho):
            continue
        try:
            imagens[nome] = pygame.transform.smoothscale(pygame.image.load(caminho).convert_alpha(), botoes[nome_botao].size)
        except pygame.error:
            pass

    return imagens


def criar_botao_centralizado(y, largura=324, altura=108):
    return pygame.Rect((LARGURA_TELA - largura) // 2, y, largura, altura)


def desenhar_background_menu(tela, background, estrelas):
    if not background:
        tela.fill(COR_FUNDO)
        for x, y, raio, brilho in estrelas:
            pygame.draw.circle(tela, (brilho, brilho, brilho), (x, y), raio)
        return
    tela.blit(background, ((LARGURA_TELA - background.get_width()) // 2, (ALTURA_TELA - background.get_height()) // 2))


def executar_menu(tela):
    relogio = pygame.time.Clock()
    estrelas = [(random.randint(0, LARGURA_TELA), random.randint(0, ALTURA_TELA), random.choice([1, 1, 1, 2]), random.randint(120, 255)) for _ in range(80)]
    background = carregar_background_menu()
    logo = carregar_logo()
    configuracoes = carregar_configuracoes()
    aplicar_volume(configuracoes)
    sons.iniciar_musica_menu(configuracoes)
    secao_atual = "principal"
    layout = {
        "titulo_y": 122, "primeiro_botao_y": 280, "segundo_botao_y": 409,
        "terceiro_botao_y": 538, "volume_texto_y": 302, "volume_botoes_y": 331,
        "sons_texto_y": 432, "alternar_sons_y": 468, "voltar_configuracoes_y": 561,
    }
    fontes = {nome: criar_fonte_pixel(tamanho) for nome, tamanho in [("titulo", 64), ("texto", 28), ("botao", 24)]}
    botoes = {
        "jogar": criar_botao_centralizado(layout["primeiro_botao_y"]),
        "configuracoes": criar_botao_centralizado(layout["segundo_botao_y"]),
        "sair": criar_botao_centralizado(layout["terceiro_botao_y"]),
        "singleplayer": criar_botao_centralizado(layout["primeiro_botao_y"]),
        "multiplayer": criar_botao_centralizado(layout["segundo_botao_y"]),
        "voltar_modo": criar_botao_centralizado(layout["terceiro_botao_y"]),
        "diminuir_volume": pygame.Rect((LARGURA_TELA // 2) - 150, layout["volume_botoes_y"], 96, 72),
        "aumentar_volume": pygame.Rect((LARGURA_TELA // 2) + 54, layout["volume_botoes_y"], 96, 72),
        "alternar_sons": criar_botao_centralizado(layout["alternar_sons_y"], 270, 90),
        "voltar_configuracoes": criar_botao_centralizado(layout["voltar_configuracoes_y"], 270, 90),
    }
    imagens_botoes = carregar_imagens_botoes(botoes)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_configuracoes(configuracoes)
                sons.parar_musica_menu()
                return "sair"

            if secao_atual == "principal":
                if verificar_clique_botao(evento, botoes["jogar"]):
                    secao_atual = "modo_jogo"

                if verificar_clique_botao(evento, botoes["configuracoes"]):
                    secao_atual = "configuracoes"

                if verificar_clique_botao(evento, botoes["sair"]):
                    salvar_configuracoes(configuracoes)
                    sons.parar_musica_menu()
                    return "sair"

            elif secao_atual == "modo_jogo":
                if verificar_clique_botao(evento, botoes["singleplayer"]):
                    salvar_configuracoes(configuracoes)
                    sons.ajustar_volume_musica(configuracoes, durante_jogo=True)
                    return "singleplayer"

                if verificar_clique_botao(evento, botoes["multiplayer"]):
                    salvar_configuracoes(configuracoes)
                    sons.ajustar_volume_musica(configuracoes, durante_jogo=True)
                    return "multiplayer"

                if verificar_clique_botao(evento, botoes["voltar_modo"]):
                    secao_atual = "principal"

            elif secao_atual == "configuracoes":
                for nome, delta in [("diminuir_volume", -10), ("aumentar_volume", 10)]:
                    if verificar_clique_botao(evento, botoes[nome]):
                        configuracoes["volume"] = max(0, min(100, configuracoes["volume"] + delta))
                        aplicar_volume(configuracoes)
                        salvar_configuracoes(configuracoes)

                if verificar_clique_botao(evento, botoes["alternar_sons"]):
                    configuracoes["sons_ligados"] = not configuracoes["sons_ligados"]
                    if configuracoes["sons_ligados"]:
                        sons.iniciar_musica_menu(configuracoes)
                    else:
                        sons.parar_musica_menu()
                    salvar_configuracoes(configuracoes)

                if verificar_clique_botao(evento, botoes["voltar_configuracoes"]):
                    salvar_configuracoes(configuracoes)
                    secao_atual = "principal"

        desenhar_background_menu(tela, background, estrelas)

        if logo:
            retangulo_logo = logo.get_rect(center=(LARGURA_TELA // 2, layout["titulo_y"]))
            tela.blit(logo, retangulo_logo)
        else:
            desenhar_texto(tela, "BIG BANG", fontes["titulo"], COR_TEXTO, LARGURA_TELA // 2, layout["titulo_y"])

        if secao_atual == "principal":
            for texto, nome in [("Jogar", "jogar"), ("Configurações", "configuracoes"), ("Sair", "sair")]:
                desenhar_botao(tela, texto, botoes[nome], fontes["botao"], mouse_pos, imagens_botoes.get(nome))

        elif secao_atual == "modo_jogo":
            for texto, nome in [("SinglePlayer", "singleplayer"), ("MultiPlayer", "multiplayer"), ("Voltar", "voltar_modo")]:
                desenhar_botao(tela, texto, botoes[nome], fontes["botao"], mouse_pos, imagens_botoes.get(nome))

        elif secao_atual == "configuracoes":
            for texto, y in [(f"Volume geral: {configuracoes['volume']}%", layout["volume_texto_y"]), (f"Sons do jogo: {'Ligados' if configuracoes['sons_ligados'] else 'Desligados'}", layout["sons_texto_y"])]:
                desenhar_texto(tela, texto, fontes["texto"], COR_TEXTO, LARGURA_TELA // 2, y)
            imagem_alternar_sons = imagens_botoes.get("alternar_sons_ligado" if configuracoes["sons_ligados"] else "alternar_sons_desligado")
            for texto, nome, imagem in [("-", "diminuir_volume", "diminuir_volume"), ("+", "aumentar_volume", "aumentar_volume"), ("Ligar/Desligar", "alternar_sons", None), ("Voltar", "voltar_configuracoes", "voltar_configuracoes")]:
                desenhar_botao(tela, texto, botoes[nome], fontes["botao"], mouse_pos, imagem_alternar_sons if nome == "alternar_sons" else imagens_botoes.get(imagem))

        pygame.display.flip()
        relogio.tick(60)
