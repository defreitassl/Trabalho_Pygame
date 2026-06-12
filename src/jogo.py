import pygame

import src.funcoes as fn
from src.menu import ALTURA_TELA, LARGURA_TELA, executar_menu


def executar_loop_jogo(tela):
    """Executa a tela jogavel integrada ao menu."""
    clock = pygame.time.Clock()

    dino = pygame.image.load(
        "assets/imagens/dino sprites/Run (2).png"
    ).convert_alpha()
    dino = pygame.transform.scale(dino, (100, 80))
    dino_rect = dino.get_rect(center=(400, 200))

    carne = pygame.image.load("assets/imagens/MeatUI2.png").convert_alpha()
    carne = pygame.transform.scale(carne, (50, 50))
    carne_rect = carne.get_rect(center=(600, 200))

    fonte = pygame.font.Font(
        "assets/fontes/fonte_pixel.ttf",
        36
    )

    velocidade = 5
    pontos = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        teclas = pygame.key.get_pressed()
        fn.mover_jogador1(teclas, dino_rect, velocidade)

        tela.fill((30, 30, 30))
        texto_pontos = fonte.render(
            f"Pontos: {pontos}",
            True,
            (255,255,255)
        )

        tela.blit(dino, dino_rect)
        tela.blit(carne, carne_rect)
        tela.blit(texto_pontos, (20,20))
        
        if fn.verificar_colisao(dino_rect, carne_rect):
        
            pontos = fn.calcular_pontos(
                pontos, 10
            )

            carne_rect.center = fn.gerar_posicao_aleatoria() # Gera posição aleatória para a carne

            print(f"Pontos: {pontos}")

        pygame.display.update()
        clock.tick(60)


def executar_jogo():
    """Abre a janela do jogo, chama o menu inicial e inicia a partida."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("BIG BANG")

    executando = True

    while executando:
        opcao = executar_menu(tela)
        print(f"Opcao escolhida: {opcao}")

        if opcao == "sair":
            executando = False
        else:
            resultado = executar_loop_jogo(tela)
            if resultado == "sair":
                executando = False

    pygame.quit()
