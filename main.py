
import sys
import math
import random
from datetime import datetime

import pygame

# pyttsx3 e usado para falar (item 19). O import fica protegido para o
# jogo nao quebrar caso a biblioteca ainda nao esteja instalada.
try:
    import pyttsx3
except Exception:
    pyttsx3 = None

# Funcoes auxiliares exigidas pela atividade (item 7), vindas de Recursos/.
from recursos.trabalho import salvar_log, obter_melhor_jogador, formatar_melhor


# ----------------------------------------------------------------------
# TEMA DO JOGO  (troque aqui para criar uma tematica propria)
# ----------------------------------------------------------------------
TITULO_JOGO = "Princesa em Fuga"
NOME_PERSONAGEM = "princesa"
NOME_INIMIGO = "obstaculos"
NOME_RESGATADO = "principe"   # quem a princesa quer resgatar

# ----------------------------------------------------------------------
# CONFIGURACOES GERAIS
# ----------------------------------------------------------------------
LARGURA = 1000          # item 8: tela 1000 x 700
ALTURA = 700
FPS = 60
ARQUIVO_LOG = "log.dat"  # item 17: arquivo de log chamado log.dat

CHAO_Y = ALTURA - 110   # altura (linha) do chao onde a princesa corre

# Cores no formato (R, G, B)
BRANCO = (245, 245, 250)
PRETO = (0, 0, 0)
CEU = (150, 205, 245)
CHAO = (110, 175, 120)
CHAO_ESCURO = (80, 140, 95)
ROSA = (235, 110, 170)
VERDE = (60, 160, 90)
VERMELHO = (220, 70, 70)
AMARELO = (255, 205, 60)
CINZA = (90, 95, 110)
CINZA_CLARO = (70, 75, 90)

# ----------------------------------------------------------------------
# INICIALIZACAO DO PYGAME
# ----------------------------------------------------------------------
pygame.init()
pygame.font.init()
# Inicializa o som. Se a maquina nao tiver audio, o jogo continua sem travar.
try:
    pygame.mixer.init()
except Exception:
    pass

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Princess Esc')
relogio = pygame.time.Clock()

FONTE_GRANDE = pygame.font.SysFont("arial", 56, bold=True)
FONTE_MEDIA = pygame.font.SysFont("arial", 30, bold=True)
FONTE_NORMAL = pygame.font.SysFont("arial", 24)
FONTE_PEQUENA = pygame.font.SysFont("arial", 18)

# ----------------------------------------------------------------------
# CARREGAMENTO DOS ARQUIVOS DA PASTA bases/
# ----------------------------------------------------------------------
# Os arquivos abaixo ja existem como exemplos simples. Para personalizar
# o tema, basta substituir cada arquivo mantendo o MESMO nome:
#   bases/imagens/fundo.png       -> fundo (ceu)
#   bases/imagens/personagem.png  -> a princesa
#   bases/imagens/inimigo.png     -> os obstaculos
#   bases/imagens/decorativo.png  -> nuvem decorativa
#   bases/icones/icone.png        -> icone da janela
#   bases/sons/inicio.wav         -> som de abertura
#   bases/sons/fim.wav            -> som de fim de jogo
#
# Se algum arquivo for apagado ou der erro, o jogo continua funcionando
# com os desenhos basicos de reserva.

def carregar_imagem(caminho, tamanho=None):
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        if tamanho is not None:
            imagem = pygame.transform.smoothscale(imagem, tamanho)
        return imagem
    except Exception:
        return None

def carregar_som(caminho):
    try:
        return pygame.mixer.Sound(caminho)
    except Exception:
        return None

# Tamanhos da princesa e dos obstaculos (em pixels).
LARG_PRINCESA, ALT_PRINCESA = 52, 74
LARG_OBST, ALT_OBST = 48, 64

IMAGEM_FUNDO = carregar_imagem("bases/imagens/fundo.png", (LARGURA, ALTURA))
IMAGEM_PERSONAGEM = carregar_imagem("bases/imagens/personagem.png", (LARG_PRINCESA, ALT_PRINCESA))
IMAGEM_INIMIGO = carregar_imagem("bases/imagens/inimigo.png", (LARG_OBST, ALT_OBST))
IMAGEM_DECORATIVO = carregar_imagem("bases/imagens/decorativo.png", (110, 60))
SOM_INICIO = carregar_som("bases/sons/inicio.wav")
SOM_FIM = carregar_som("bases/sons/fim.wav")

try:
    icone_janela = pygame.image.load("bases/icones/icone.png").convert_alpha()
    pygame.display.set_icon(icone_janela)
except Exception:
    pass

# ----------------------------------------------------------------------
# FUNCOES DE APOIO
# ----------------------------------------------------------------------
def falar(texto):
    """
    Fala um texto em voz alta usando pyttsx3 (item 19).
    Se a biblioteca nao estiver instalada, simplesmente nao faz nada.
    """
    if pyttsx3 is None:
        return
    try:
        motor = pyttsx3.init()
        motor.say(texto)
        motor.runAndWait()
    except Exception:
        pass

def desenhar_texto(texto, fonte, cor, x, y, centro=False):
    """Desenha um texto na tela. Se centro=True, (x, y) e o centro do texto."""
    render = fonte.render(texto, True, cor)
    rect = render.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    tela.blit(render, rect)
    return rect

def desenhar_fundo():
    """
    Desenha o fundo (ceu) e a faixa de chao por onde a princesa corre.
    Usa a imagem real de bases/imagens/fundo.png; se faltar, usa cores.
    """
    if IMAGEM_FUNDO is not None:
        tela.blit(IMAGEM_FUNDO, (0, 0))
    else:
        tela.fill(CEU)
        desenhar_texto("AQUI VAI IMAGEM DE FUNDO", FONTE_PEQUENA, CINZA_CLARO,
                       LARGURA // 2, 60, centro=True)
    # Faixa de chao (desenhada por cima do fundo para alinhar com o jogo)
    pygame.draw.rect(tela, CHAO, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
    pygame.draw.line(tela, CHAO_ESCURO, (0, CHAO_Y), (LARGURA, CHAO_Y), 4)

def desenhar_sol_pulsante(passo):
    """
    Item 16: circulo amarelo (sol) em um canto, que pulsa de tamanho.
    O seno faz o raio aumentar e diminuir suavemente com o tempo.
    """
    raio = 42 + int(math.sin(passo * 0.05) * 12)
    pygame.draw.circle(tela, AMARELO, (905, 90), raio)
    pygame.draw.circle(tela, (255, 240, 170), (905, 90), max(6, raio // 2))

def novo_obstaculo(x_inicial):
    """
    Cria um obstaculo no chao, comecando na posicao x informada.
    A altura varia um pouco para dar variedade.
    """
    altura = random.choice([54, 64, 74])
    return {"x": x_inicial, "w": LARG_OBST, "h": altura}

def nova_nuvem():
    """
    Item 14: objeto decorativo (uma nuvem) que se move sozinho, de forma
    randomica, e que NAO interage com a jogadora.
    """
    return {
        "x": random.randint(200, LARGURA - 150),
        "y": random.randint(60, 200),
        "vx": random.choice([-2, -1, 1, 2]),
        "vy": random.choice([-1, 1]),
    }

# ----------------------------------------------------------------------
# TELA 1: DIGITAR O NOME
# ----------------------------------------------------------------------
def tela_nome():
    """Jogadora digita o nome e aperta ENTER. ESC fecha o jogo (item 20)."""
    nome = ""
    ja_falou = False

    while True:
        relogio.tick(FPS)
        desenhar_fundo()

        desenhar_texto(TITULO_JOGO, FONTE_GRANDE, ROSA, LARGURA // 2, 130, centro=True)
        desenhar_texto("Digite seu nome e pressione ENTER",
                       FONTE_NORMAL, CINZA_CLARO, LARGURA // 2, 220, centro=True)

        caixa = pygame.Rect(300, 280, 400, 56)
        pygame.draw.rect(tela, BRANCO, caixa, border_radius=8)
        pygame.draw.rect(tela, ROSA, caixa, 3, border_radius=8)
        desenhar_texto(nome if nome else "...", FONTE_NORMAL, PRETO,
                       caixa.x + 16, caixa.y + 15)

        desenhar_texto("ESC fecha o jogo a qualquer momento.",
                       FONTE_PEQUENA, CINZA_CLARO, LARGURA // 2, 380, centro=True)

        if not ja_falou:
            if SOM_INICIO is not None:
                SOM_INICIO.play()
            falar(f"Bem vinda ao jogo {TITULO_JOGO}")
            ja_falou = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:        # X no canto da janela
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # item 20
                    encerrar()
                elif evento.key == pygame.K_RETURN:
                    if nome.strip():
                        return nome.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 18 and evento.unicode.isprintable():
                        nome += evento.unicode

        pygame.display.flip()
