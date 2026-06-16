import pygame

from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor
from src.jogo import (
    calcular_dificuldade_meteoros,
    calcular_pontuacao_final,
    calcular_raio_meteoro,
    criar_meteoro,
    escolher_animacao_dino1,
    jogador_na_area_do_meteoro,
    obter_frame_animacao,
    sortear_raio_meteoro,
)


def test_calcular_pontos():
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu():
    assert jogador_perdeu(0) is True
    assert jogador_perdeu(3) is False


def test_limitar_valor():
    assert limitar_valor(-5, 0, 100) == 0
    assert limitar_valor(150, 0, 100) == 100
    assert limitar_valor(50, 0, 100) == 50


def test_calcular_pontuacao_final_soma_carne_e_tempo():
    assert calcular_pontuacao_final(30, 5000) == 40


def test_escolher_animacao_dino1_por_estado():
    assert escolher_animacao_dino1(True, False, False) == "idle"
    assert escolher_animacao_dino1(True, True, False) == "run"
    assert escolher_animacao_dino1(True, True, True) == "walk"
    assert escolher_animacao_dino1(False, True, False) == "dead"


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
    avancado = calcular_dificuldade_meteoros(60000)

    assert avancado[0] < inicio[0]
    assert avancado[1] < inicio[1]
    assert avancado[2] < inicio[2]


def test_dificuldade_meteoros_respeita_limites_minimos():
    intervalo_min, intervalo_max, tempo_alerta = calcular_dificuldade_meteoros(
        600000,
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


def test_sortear_raio_meteoro_varia_tamanho():
    raios = {sortear_raio_meteoro("singleplayer") for _ in range(100)}

    assert min(raios) < calcular_raio_meteoro("singleplayer")


def test_spawn_meteoros_mais_rapido():
    intervalo_min, intervalo_max, _ = calcular_dificuldade_meteoros(0, "multiplayer")

    assert intervalo_min == 750
    assert intervalo_max == 2166


def test_singleplayer_tem_meteoros_mais_rapidos():
    multi = calcular_dificuldade_meteoros(0, "multiplayer")
    single = calcular_dificuldade_meteoros(0, "singleplayer")

    assert single[0] < multi[0]
    assert single[1] < multi[1]
    assert single[2] < multi[2]
