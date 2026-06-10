
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

