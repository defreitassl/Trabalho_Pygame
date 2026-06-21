# Testes

Esta pasta contem testes automatizados do projeto.

## Arquivos

- `test_logica.py`: valida regras de `src/funcoes.py` e `src/jogo.py`.

## Cobertura atual

- Pontuacao por coleta e tempo sobrevivido.
- Movimento, limites do mapa, arvores e arbustos.
- Estados e frames das animacoes.
- Area de dano, tamanho, intervalo e dificuldade dos meteoros.
- Leitura e gravacao das configuracoes do menu.
- Ativacao e volume dos efeitos sonoros.
- Reproducao em loop da musica do menu.

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Crie testes para toda regra de pontuacao, vidas e condicoes de fim de jogo.
- Prefira funcoes pequenas e testaveis no modulo `src/funcoes.py`.
