import pygame

from src.menu import ALTURA_TELA, LARGURA_TELA, executar_menu


def executar_jogo():
    """Abre a janela do jogo e chama o menu inicial."""
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
            print("A logica do jogo ainda sera integrada aqui.")
            executando = False

    pygame.quit()
