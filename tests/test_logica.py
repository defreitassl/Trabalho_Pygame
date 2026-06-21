import pygame

import src.menu as menu
import src.sons as sons
from src.funcoes import (
    calcular_pontuacao_final,
    calcular_dificuldade_meteoros,
    calcular_raio_meteoro,
    jogador_na_area_do_meteoro,
    movimento_teclas,
    sortear_raio_meteoro,
    sortear_proximo_meteoro,
    velocidade_jogador,
)

from src.jogo import (
    criar_meteoro,
    escolher_animacao_personagem,
    mover_com_colisao,
    obter_frame_animacao,
)


def test_calcular_pontuacao_final_soma_carne_e_tempo():
    assert calcular_pontuacao_final(30, 5000) == 40


def test_pontuacao_conta_apenas_segundos_completos():
    assert calcular_pontuacao_final(10, 999) == 10


def test_movimento_com_teclas_opostas_se_anula():
    teclas = [False] * 512
    teclas[pygame.K_w] = True
    teclas[pygame.K_s] = True

    assert movimento_teclas(teclas, 5, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a) == (0, 0)


def test_arbusto_reduz_velocidade_do_jogador():
    jogador = pygame.Rect(100, 100, 100, 80)
    arbustos = [{"lentidao": pygame.Rect(130, 158, 50, 28)}]

    assert velocidade_jogador(jogador, []) == 5
    assert velocidade_jogador(jogador, arbustos) == 2


def test_arvore_bloqueia_movimento_do_jogador():
    jogador = pygame.Rect(100, 100, 100, 80)
    arvores = [{"colisao": pygame.Rect(172, 158, 10, 18)}]

    mover_com_colisao(jogador, 5, 0, arvores)

    assert jogador.x == 100


def test_jogador_nao_sai_da_tela():
    jogador = pygame.Rect(0, 0, 100, 80)

    mover_com_colisao(jogador, -5, -5, [])

    assert jogador.topleft == (0, 0)


def test_configuracoes_padrao_quando_arquivo_nao_existe(tmp_path, monkeypatch):
    caminho = tmp_path / "configuracoes.json"
    monkeypatch.setattr(menu, "CAMINHO_CONFIGURACOES", str(caminho))

    assert menu.carregar_configuracoes() == {"volume": 50, "sons_ligados": True}


def test_salvar_e_carregar_configuracoes(tmp_path, monkeypatch):
    caminho = tmp_path / "configuracoes.json"
    monkeypatch.setattr(menu, "CAMINHO_CONFIGURACOES", str(caminho))
    configuracoes = {"volume": 70, "sons_ligados": False}

    menu.salvar_configuracoes(configuracoes)

    assert menu.carregar_configuracoes() == configuracoes


def test_efeitos_nao_carregam_quando_sons_estao_desligados():
    configuracoes = {"volume": 50, "sons_ligados": False}

    assert sons.carregar_efeitos(configuracoes) == {}


def test_tocar_efeito_carregado():
    class EfeitoFalso:
        def __init__(self):
            self.tocou = False

        def play(self):
            self.tocou = True

    efeito = EfeitoFalso()
    sons.tocar_efeito({"coleta": efeito}, "coleta")

    assert efeito.tocou is True


def test_volume_e_aplicado_aos_efeitos(monkeypatch):
    class EfeitoFalso:
        def set_volume(self, volume):
            self.volume = volume

    monkeypatch.setattr(sons.pygame.mixer, "get_init", lambda: True)
    monkeypatch.setattr(sons.pygame.mixer, "Sound", lambda caminho: EfeitoFalso())

    efeitos = sons.carregar_efeitos({"volume": 40, "sons_ligados": True})

    assert all(efeito.volume == 0.4 for efeito in efeitos.values())


def test_musica_do_menu_inicia_em_loop(monkeypatch):
    chamadas = {}
    monkeypatch.setattr(sons.pygame.mixer, "get_init", lambda: True)
    monkeypatch.setattr(sons.pygame.mixer.music, "get_busy", lambda: False)
    monkeypatch.setattr(sons.pygame.mixer.music, "load", lambda caminho: chamadas.update(caminho=caminho))
    monkeypatch.setattr(sons.pygame.mixer.music, "set_volume", lambda volume: chamadas.update(volume=volume))
    monkeypatch.setattr(sons.pygame.mixer.music, "play", lambda repeticoes: chamadas.update(repeticoes=repeticoes))

    sons.iniciar_musica_menu({"volume": 40, "sons_ligados": True})

    assert chamadas == {"caminho": sons.CAMINHO_MUSICA_MENU, "volume": 0.4, "repeticoes": -1}


def test_musica_do_menu_nao_inicia_com_sons_desligados(monkeypatch):
    caminhos = []
    monkeypatch.setattr(sons.pygame.mixer.music, "load", caminhos.append)

    sons.iniciar_musica_menu({"volume": 40, "sons_ligados": False})

    assert caminhos == []


def test_musica_fica_baixa_durante_o_jogo(monkeypatch):
    volumes = []
    monkeypatch.setattr(sons.pygame.mixer, "get_init", lambda: True)
    monkeypatch.setattr(sons.pygame.mixer.music, "set_volume", volumes.append)

    sons.ajustar_volume_musica({"volume": 30}, durante_jogo=True)

    assert volumes == [0.1]


def test_escolher_animacao_por_estado():
    assert escolher_animacao_personagem(True, False, False) == "idle"
    assert escolher_animacao_personagem(True, True, False) == "run"
    assert escolher_animacao_personagem(True, True, True) == "walk"
    assert escolher_animacao_personagem(False, True, False) == "dead"


def test_obter_frame_animacao_repete_frames():
    frames = ["a", "b", "c"]

    assert obter_frame_animacao(frames, 0) == "a"
    assert obter_frame_animacao(frames, 90) == "b"
    assert obter_frame_animacao(frames, 270) == "a"


def test_obter_frame_animacao_para_no_ultimo_frame():
    frames = ["a", "b", "c"]

    assert obter_frame_animacao(frames, 1000, repetir=False) == "c"


def test_jogador_na_area_do_meteoro():
    dino_rect = pygame.Rect(100, 100, 100, 80)

    meteoro = {
        "centro": (150, 165),
        "raio": 156,
    }

    assert jogador_na_area_do_meteoro(dino_rect, meteoro) is True


def test_jogador_fora_da_area_do_meteoro():
    dino_rect = pygame.Rect(100, 100, 100, 80)

    meteoro = {
        "centro": (400, 400),
        "raio": 156,
    }

    assert jogador_na_area_do_meteoro(dino_rect, meteoro) is False


def test_dificuldade_meteoros_aumenta_com_tempo():
    inicio = calcular_dificuldade_meteoros(0)
    avancado = calcular_dificuldade_meteoros(3000)

    assert avancado[0] < inicio[0]
    assert avancado[1] < inicio[1]
    assert avancado[2] < inicio[2]


def test_dificuldade_meteoros_sobe_a_cada_tres_segundos():
    antes = calcular_dificuldade_meteoros(2999)
    depois = calcular_dificuldade_meteoros(3000)

    assert depois[0] < antes[0]
    assert depois[1] < antes[1]
    assert depois[2] < antes[2]


def test_dificuldade_meteoros_respeita_limites_minimos():
    intervalo_min, intervalo_max, tempo_alerta = (
        calcular_dificuldade_meteoros(600000)
    )

    assert intervalo_min == 350
    assert intervalo_max == 950
    assert tempo_alerta == 850


def test_raio_meteoro_maior_no_singleplayer():
    assert calcular_raio_meteoro("multiplayer") == 234
    assert calcular_raio_meteoro("singleplayer") == 250


def test_criar_meteoro_usa_raio_do_modo():
    for modo in ["singleplayer", "multiplayer"]:
        raio_maximo = calcular_raio_meteoro(modo)
        raio_minimo = int(raio_maximo * 0.3)

        for _ in range(20):
            meteoro = criar_meteoro(1000, 0, modo)

            assert raio_minimo <= meteoro["raio"] <= raio_maximo


def test_meteoro_respeita_tempo_de_alerta_e_impacto():
    meteoro = criar_meteoro(1000, 0, "multiplayer")

    assert meteoro["impacto_em"] == 2900
    assert meteoro["finaliza_em"] == 3350


def test_proximo_meteoro_respeita_intervalo_sorteado(monkeypatch):
    monkeypatch.setattr("src.funcoes.random.randint", lambda minimo, maximo: minimo)

    assert sortear_proximo_meteoro(1000, 0, "multiplayer") == 1750


def test_sortear_raio_meteoro_varia_tamanho():
    raios = {sortear_raio_meteoro("singleplayer") for _ in range(100)}

    assert min(raios) < calcular_raio_meteoro("singleplayer")


def test_spawn_meteoros_mais_rapido():
    intervalo_min, intervalo_max, _ = (
        calcular_dificuldade_meteoros(0, "multiplayer")
    )

    assert intervalo_min == 750
    assert intervalo_max == 2166


def test_primeiro_nivel_tem_reducao_suave_no_multiplayer():
    intervalo_min, intervalo_max, tempo_alerta = calcular_dificuldade_meteoros(
        3000, "multiplayer"
    )

    assert intervalo_min == 735
    assert intervalo_max == 2136
    assert tempo_alerta == 1876


def test_singleplayer_tem_meteoros_mais_rapidos():
    multi = calcular_dificuldade_meteoros(0, "multiplayer")
    single = calcular_dificuldade_meteoros(0, "singleplayer")

    assert single[0] < multi[0]
    assert single[1] < multi[1]
    assert single[2] < multi[2]
