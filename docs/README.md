# Documentação

Esta pasta reúne documentos de apoio, planejamento e registros técnicos do projeto **BIG BANG**.

## Objetivo

Centralizar informações complementares ao código-fonte, facilitando a manutenção, o entendimento do projeto e a avaliação da disciplina.

---

## Arquivos

### proposta.MD

Documento contendo a proposta inicial do projeto, incluindo:

* Tema do jogo
* Objetivos
* Regras planejadas
* Escopo inicial

---

## Evidências do projeto

### Testes automatizados

O projeto utiliza **Pytest** para validar funções importantes da lógica do jogo.

#### Resultado dos testes

O comando `python -m pytest` valida atualmente pontuação, movimentação,
colisões, animações e dificuldade dos meteoros. A imagem abaixo registra
uma execução anterior da suíte:

![Resultado dos testes](/docs/pytest.png)

---

## Decisões técnicas

Durante o desenvolvimento foram adotadas algumas decisões importantes:

* Organização do código em módulos.
* Separação das constantes em `config.py`.
* Utilização de docstrings para documentação das funções.
* Implementação de testes automatizados com Pytest.
* Controle de versão utilizando Git e GitHub.

---

## Melhorias futuras

Possíveis evoluções para versões futuras do projeto:

* Sistema de ranking.
* Efeitos sonoros e música.
* Novos tipos de obstáculos.
* Power-ups.
* Sistema de fases.
* Diferentes mapas.

---

### Versão 1.0

* Implementação do modo Singleplayer.
* Implementação do modo Multiplayer.
* Sistema de meteoros.
* Sistema de pontuação.
* Animações dos dois personagens.
* Menu de configurações.
* Testes automatizados.
* Documentação do projeto.
