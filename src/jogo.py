import pygame


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()

    tela = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("BIG BANG")
    relogio = pygame.time.Clock()
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        tela.fill((0, 0, 0))
        pygame.display.update()
        relogio.tick(60)

    pygame.quit()
