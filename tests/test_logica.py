import pygame

from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor
from src.jogo import calcular_pontuacao_final, jogador_na_area_do_meteoro


def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


def test_calcular_pontuacao_final_soma_carne_e_tempo():
    """Deve somar pontos de carne com bonus por segundos vivos."""
    assert calcular_pontuacao_final(30, 5000) == 40


def test_jogador_na_area_do_meteoro():
    """Deve detectar jogador dentro do raio de dano do meteoro."""
    dino_rect = pygame.Rect(100, 100, 100, 80)
    meteoro = {
        "centro": (150, 165),
        "raio": 58,
    }

    assert jogador_na_area_do_meteoro(dino_rect, meteoro) is True


def test_jogador_fora_da_area_do_meteoro():
    """Deve ignorar jogador fora do raio de dano do meteoro."""
    dino_rect = pygame.Rect(100, 100, 100, 80)
    meteoro = {
        "centro": (400, 400),
        "raio": 58,
    }

    assert jogador_na_area_do_meteoro(dino_rect, meteoro) is False
