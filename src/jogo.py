import pygame

import src.funcoes as fn
from src.menu import ALTURA_TELA, LARGURA_TELA, executar_menu


def executar_loop_jogo(tela, modo="singleplayer"):
    """Executa a tela jogavel integrada ao menu."""
    clock = pygame.time.Clock()

    dino = pygame.image.load(
        "assets/imagens/dino sprites/Run (2).png"
    ).convert_alpha()
    dino = pygame.transform.scale(dino, (100, 80))
    dino_rect = dino.get_rect(center=(400, 200))

    # PLAYER 2: Inicializa o jogador 2 se o modo for multiplayer
    if modo == "multiplayer":
        dino2 = pygame.image.load(
            "assets/imagens/dino2 sprites/espinossauro.png"
        ).convert_alpha()
        dino2 = pygame.transform.flip(dino2, True, False)
        dino2 = pygame.transform.scale(dino2, (100, 80))
        dino2_rect = dino2.get_rect(center=(680, 200))

    carne = pygame.image.load("assets/imagens/MeatUI2.png").convert_alpha()
    carne = pygame.transform.scale(carne, (50, 50))
    carne_rect = carne.get_rect(center=(600, 200))

    fonte = pygame.font.Font(
        "assets/fontes/fonte_pixel.ttf",
        36
    )

    velocidade = 5
    pontos = 0
    
    # PLAYER 2: Inicializa a pontuação do jogador 2
    if modo == "multiplayer":
        pontos2 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        teclas = pygame.key.get_pressed()
        fn.mover_jogador1(teclas, dino_rect, velocidade)
        
        # PLAYER 2: Movimenta o jogador 2
        if modo == "multiplayer":
            fn.mover_jogador2(teclas, dino2_rect, velocidade)

        tela.fill((30, 30, 30))
        texto_pontos = fonte.render(
            f"P1: {pontos}" if modo == "multiplayer" else f"Pontos: {pontos}",
            True,
            (255,255,255)
        )
        
        # PLAYER 2: Texto de pontuação
        if modo == "multiplayer":
            texto_pontos2 = fonte.render(
                f"P2: {pontos2}",
                True,
                (255,255,255)
            )

        tela.blit(dino, dino_rect)
        
        # PLAYER 2: Desenha na tela
        if modo == "multiplayer":
            tela.blit(dino2, dino2_rect)
            
        tela.blit(carne, carne_rect)
        tela.blit(texto_pontos, (20,20))
        
        # PLAYER 2: Desenha pontuação na tela
        if modo == "multiplayer":
            tela.blit(texto_pontos2, (LARGURA_TELA - 150, 20))
        
        if fn.verificar_colisao(dino_rect, carne_rect):
        
            pontos = fn.calcular_pontos(
                pontos, 10
            )

            carne_rect.center = fn.gerar_posicao_aleatoria() # Gera posição aleatória para a carne

            print(f"Pontos P1: {pontos}" if modo == "multiplayer" else f"Pontos: {pontos}")
            
        # PLAYER 2: Verifica colisão com a carne
        if modo == "multiplayer" and fn.verificar_colisao(dino2_rect, carne_rect):
            pontos2 = fn.calcular_pontos(
                pontos2, 10
            )

            carne_rect.center = fn.gerar_posicao_aleatoria() # Gera posição aleatória para a carne

            print(f"Pontos P2: {pontos2}")

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
            # Passa a opcao (singleplayer ou multiplayer) para o loop do jogo
            resultado = executar_loop_jogo(tela, modo=opcao)
            if resultado == "sair":
                executando = False

    pygame.quit()