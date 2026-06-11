# Princesa em Fuga

Jogo desenvolvido para a atividade avaliativa da disciplina de **Pensamento Computacional** (Atitus Educação), feito em Python com a biblioteca Pygame.

## Desenvolvedora

- Nome completo: Laura Ecco Tonet — RA: 1139470


## História do jogo

A princesa descobriu que o príncipe foi capturado e precisa atravessar um caminho cheio de obstáculos para alcançá-lo. Ela corre pelo cenário, pula sobre os obstáculos que aparecem pela frente e tenta resistir o maior tempo possível. Quanto mais longe ela vai sem ser atingida, maior é a pontuação.

## Como jogar

- Digite seu nome e pressione **ENTER**.
- Na tela de boas-vindas, clique em **INICIAR**.
- A princesa corre sozinha. Pressione a **seta para cima** para pular os obstáculos (movimento somente no eixo Y).
- **Espaço** pausa e despausa a partida.
- **ESC** fecha o jogo a qualquer momento.

## Tecnologias utilizadas

- Python
- Pygame
- pyttsx3 (voz)
- cx_Freeze (geração do executável)

## Estrutura de pastas

```text
jogo/
├── main.py
├── setup.py
├── README.md
├── log.dat
├── requirements.txt
├── bases/
│   ├── imagens/
│   ├── sons/
│   ├── icones/
│   └── fontes/
└── Recursos/
    ├── __init__.py
    └── trabalho.py
```

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

## Como gerar o executável

```bash
pip install cx_Freeze
python setup.py build
```

O executável é criado dentro da pasta `build/`.

## Personalização

As imagens e os sons ficam na pasta `bases/`. Para trocar, mantenha os mesmos nomes de arquivo: `fundo.png`, `personagem.png`, `inimigo.png`, `decorativo.png` (em `bases/imagens/`), `icone.png` (em `bases/icones/`) e `inicio.wav`, `fim.wav` (em `bases/sons/`). O título, os nomes do personagem e do resgatado podem ser mudados no início do `main.py`, no bloco "TEMA DO JOGO".
