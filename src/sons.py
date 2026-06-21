import pygame


CAMINHOS_EFEITOS = {
    "coleta": "assets/sons/coleta.wav",
    "impacto": "assets/sons/impacto_meteoro.wav",
    "morte": "assets/sons/morte.wav",
}
CAMINHO_MUSICA_MENU = "assets/sons/musica_menu.ogg"


def carregar_efeitos(configuracoes):
    """Carrega os efeitos do jogo usando as configuracoes do menu."""
    if not configuracoes["sons_ligados"] or not pygame.mixer.get_init():
        return {}

    efeitos = {}
    for nome, caminho in CAMINHOS_EFEITOS.items():
        try:
            efeitos[nome] = pygame.mixer.Sound(caminho)
            efeitos[nome].set_volume(configuracoes["volume"] / 100)
        except (FileNotFoundError, pygame.error):
            pass
    return efeitos


def tocar_efeito(efeitos, nome):
    """Toca um efeito se ele foi carregado corretamente."""
    if nome in efeitos:
        efeitos[nome].play()


def iniciar_musica_menu(configuracoes):
    """Inicia a musica do menu e a mantem repetindo."""
    if not configuracoes["sons_ligados"] or not pygame.mixer.get_init():
        return
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(CAMINHO_MUSICA_MENU)
            pygame.mixer.music.play(-1)
        ajustar_volume_musica(configuracoes)
    except (FileNotFoundError, pygame.error):
        pass


def ajustar_volume_musica(configuracoes, durante_jogo=False):
    """Usa volume normal no menu e volume baixo durante a partida."""
    if pygame.mixer.get_init():
        divisor = 300 if durante_jogo else 100
        pygame.mixer.music.set_volume(configuracoes["volume"] / divisor)


def parar_musica_menu():
    """Interrompe a musica antes de iniciar uma partida."""
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
