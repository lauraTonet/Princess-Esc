
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

