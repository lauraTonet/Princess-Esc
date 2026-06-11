
import sys
import math
import random
from datetime import datetime

import pygame

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

# Funcoes auxiliares exigidas pela atividade (item 7), vindas de Recursos/.
from recursos.trabalho import salvar_log, obter_melhor_jogador, formatar_melhor


TITULO_JOGO = "Princesa em Fuga"
NOME_PERSONAGEM = "princesa"
NOME_INIMIGO = "obstaculos"
NOME_RESGATADO = "principe"   

LARGURA = 1000          
ALTURA = 700
FPS = 60
ARQUIVO_LOG = "log.dat"  

CHAO_Y = ALTURA - 110   


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

pygame.init()
pygame.font.init()

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


LARG_PRINCESA, ALT_PRINCESA = 52, 74
LARG_OBST, ALT_OBST = 48, 64

IMAGEM_FUNDO = carregar_imagem("bases/imagens/fundo.png", (LARGURA, ALTURA))
IMAGEM_PERSONAGEM = carregar_imagem("bases/imagens/personagem.png", (LARG_PRINCESA, ALT_PRINCESA))
IMAGEM_INIMIGO = carregar_imagem("bases/imagens/inimigo.png", (LARG_OBST, ALT_OBST))
IMAGEM_DECORATIVO = carregar_imagem("bases/imagens/decorativo.png", (110, 60))
SOM_INICIO = carregar_som("bases/sons/jogo.wav")
SOM_FIM = carregar_som("bases/sons/fim.wav")

try:
    icone_janela = pygame.image.load("bases/icones/icone.png").convert_alpha()
    pygame.display.set_icon(icone_janela)
except Exception:
    pass


def falar(texto):
    
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
    
    if IMAGEM_FUNDO is not None:
        tela.blit(IMAGEM_FUNDO, (0, 0))
    else:
        tela.fill(CEU)
        desenhar_texto("fundo.png", FONTE_PEQUENA, CINZA_CLARO,
                       LARGURA // 2, 60, centro=True)
    
    pygame.draw.rect(tela, CHAO, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
    pygame.draw.line(tela, CHAO_ESCURO, (0, CHAO_Y), (LARGURA, CHAO_Y), 4)

def desenhar_sol_pulsante(passo):
    
    raio = 42 + int(math.sin(passo * 0.05) * 12)
    pygame.draw.circle(tela, AMARELO, (905, 90), raio)
    pygame.draw.circle(tela, (255, 240, 170), (905, 90), max(6, raio // 2))

def novo_obstaculo(x_inicial):
    
    altura = random.choice([54, 64, 74])
    return {"x": x_inicial, "w": LARG_OBST, "h": altura}

def nova_nuvem():
   
    return {
        "x": random.randint(200, LARGURA - 150),
        "y": random.randint(60, 200),
        "vx": random.choice([-2, -1, 1, 2]),
        "vy": random.choice([-1, 1]),
    }


def tela_nome():
    
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
            if evento.type == pygame.QUIT:        
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: 
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


def tela_boas_vindas(nome):
    
    melhor = obter_melhor_jogador(ARQUIVO_LOG)
    botao = pygame.Rect(375, 540, 250, 70)
    ja_falou = False

    instrucoes = [
        "Como jogar:",
        f"A {NOME_PERSONAGEM} corre sozinha pelo cenario.",
        "Pressione a SETA PARA CIMA para pular os obstaculos.",
        "Voce so se move no eixo Y (pulando).",
        f"Sobreviva o maximo possivel e resgate o {NOME_RESGATADO}!",
        "Espaco pausa e despausa. ESC fecha o jogo.",
    ]

    while True:
        relogio.tick(FPS)
        desenhar_fundo()

        desenhar_texto(f"Ola, {nome}!", FONTE_GRANDE, ROSA, LARGURA // 2, 90, centro=True)

        y = 180
        for i, linha in enumerate(instrucoes):
            fonte = FONTE_NORMAL if i == 0 else FONTE_PEQUENA
            desenhar_texto(linha, fonte, CINZA_CLARO, 130, y)
            y += 38

        desenhar_texto(formatar_melhor(melhor), FONTE_NORMAL, VERMELHO,
                       LARGURA // 2, 455, centro=True)

        pygame.draw.rect(tela, ROSA, botao, border_radius=12)
        pygame.draw.rect(tela, BRANCO, botao, 3, border_radius=12)
        desenhar_texto("INICIAR", FONTE_MEDIA, BRANCO,
                       botao.centerx, botao.centery, centro=True)

        if not ja_falou:
            falar(f"Ola {nome}. Clique em iniciar para comecar.")
            ja_falou = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                encerrar()
            if evento.type == pygame.MOUSEBUTTONDOWN and botao.collidepoint(evento.pos):
                return

        pygame.display.flip()


def jogar(nome):
    
    princesa_x = 150
    princesa_y = CHAO_Y - ALT_PRINCESA   
    vel_y = 0
    gravidade = 1
    forca_pulo = -18
    no_chao = True

    velocidade_jogo = 7
    obstaculos = [novo_obstaculo(LARGURA + i * 380) for i in range(3)]
    nuvem = nova_nuvem()

    pausado = False
    passo = 0
    inicio = pygame.time.get_ticks()
    pontuacao = 0

    while True:
        relogio.tick(FPS)
        passo += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:        
                    encerrar()
                if evento.key == pygame.K_SPACE:         
                    pausado = not pausado
                if evento.key == pygame.K_UP and no_chao and not pausado:
                    vel_y = forca_pulo                   
                    no_chao = False

        
        if not pausado:
            vel_y += gravidade
            princesa_y += vel_y
            if princesa_y >= CHAO_Y - ALT_PRINCESA:
                princesa_y = CHAO_Y - ALT_PRINCESA
                vel_y = 0
                no_chao = True

            pontuacao = (pygame.time.get_ticks() - inicio) // 100

            princesa_rect = pygame.Rect(princesa_x, princesa_y,
                                        LARG_PRINCESA, ALT_PRINCESA)

            
            for obst in obstaculos:
                obst["x"] -= velocidade_jogo
                if obst["x"] + obst["w"] < 0:
                    
                    mais_a_direita = max(o["x"] for o in obstaculos)
                    obst.update(novo_obstaculo(mais_a_direita + random.randint(320, 520)))

                obst_rect = pygame.Rect(obst["x"], CHAO_Y - obst["h"],
                                        obst["w"], obst["h"])
                if princesa_rect.colliderect(obst_rect):
                    salvar_log(ARQUIVO_LOG, nome, pontuacao)   
                    return pontuacao

            
            nuvem["x"] += nuvem["vx"]
            nuvem["y"] += nuvem["vy"]
            if nuvem["x"] < 40 or nuvem["x"] > LARGURA - 120:
                nuvem["vx"] *= -1
            if nuvem["y"] < 50 or nuvem["y"] > 230:
                nuvem["vy"] *= -1

        
        desenhar_fundo()
        desenhar_sol_pulsante(passo)

        
        if IMAGEM_DECORATIVO is not None:
            tela.blit(IMAGEM_DECORATIVO, (nuvem["x"], nuvem["y"]))
        else:
            pygame.draw.circle(tela, BRANCO, (nuvem["x"], nuvem["y"]), 22)

        
        for obst in obstaculos:
            obst_rect = pygame.Rect(obst["x"], CHAO_Y - obst["h"],
                                    obst["w"], obst["h"])
            if IMAGEM_INIMIGO is not None:
                imagem = pygame.transform.smoothscale(IMAGEM_INIMIGO,
                                                      (obst["w"], obst["h"]))
                tela.blit(imagem, obst_rect)
            else:
                pygame.draw.rect(tela, VERDE, obst_rect, border_radius=6)
                pygame.draw.rect(tela, BRANCO, obst_rect, 2, border_radius=6)

        
        if IMAGEM_PERSONAGEM is not None:
            tela.blit(IMAGEM_PERSONAGEM, (princesa_x, princesa_y))
        else:
            pygame.draw.rect(tela, ROSA, (princesa_x, princesa_y,
                                          LARG_PRINCESA, ALT_PRINCESA), border_radius=8)
            desenhar_texto("AQUI VAI", FONTE_PEQUENA, BRANCO,
                           princesa_x + LARG_PRINCESA // 2, princesa_y + 28, centro=True)
            desenhar_texto("IMAGEM", FONTE_PEQUENA, BRANCO,
                           princesa_x + LARG_PRINCESA // 2, princesa_y + 46, centro=True)

        
        desenhar_texto(f"Jogadora: {nome}", FONTE_PEQUENA, CINZA_CLARO, 20, 18)
        desenhar_texto(f"Pontuacao: {pontuacao}", FONTE_PEQUENA, CINZA_CLARO, 20, 44)
        desenhar_texto("Press Space to Pause Game.", FONTE_PEQUENA,
                       CINZA_CLARO, LARGURA - 250, ALTURA - 30)

       
        if pausado:
            sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 150))
            tela.blit(sombra, (0, 0))
            desenhar_texto("PAUSE", FONTE_GRANDE, BRANCO,
                           LARGURA // 2, ALTURA // 2, centro=True)

        pygame.display.flip()

def jogar(nome):
     
    princesa_x = 150
    princesa_y = CHAO_Y - ALT_PRINCESA   
    vel_y = 0
    gravidade = 1
    forca_pulo = -18
    no_chao = True

    velocidade_jogo = 7
    obstaculos = [novo_obstaculo(LARGURA + i * 380) for i in range(3)]
    nuvem = nova_nuvem()

    pausado = False
    passo = 0
    inicio = pygame.time.get_ticks()
    pontuacao = 0

    while True:
        relogio.tick(FPS)
        passo += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:        
                    encerrar()
                if evento.key == pygame.K_SPACE:         
                    pausado = not pausado
                if evento.key == pygame.K_UP and no_chao and not pausado:
                    vel_y = forca_pulo                   
                    no_chao = False

        
        if not pausado:
            
            vel_y += gravidade
            princesa_y += vel_y
            if princesa_y >= CHAO_Y - ALT_PRINCESA:
                princesa_y = CHAO_Y - ALT_PRINCESA
                vel_y = 0
                no_chao = True

            pontuacao = (pygame.time.get_ticks() - inicio) // 100

            princesa_rect = pygame.Rect(princesa_x, princesa_y,
                                        LARG_PRINCESA, ALT_PRINCESA)

            
            for obst in obstaculos:
                obst["x"] -= velocidade_jogo
                if obst["x"] + obst["w"] < 0:
                    mais_a_direita = max(o["x"] for o in obstaculos)
                    obst.update(novo_obstaculo(mais_a_direita + random.randint(320, 520)))

                obst_rect = pygame.Rect(obst["x"], CHAO_Y - obst["h"],
                                        obst["w"], obst["h"])
                if princesa_rect.colliderect(obst_rect):
                    salvar_log(ARQUIVO_LOG, nome, pontuacao)   
                    return pontuacao

        
            nuvem["x"] += nuvem["vx"]
            nuvem["y"] += nuvem["vy"]
            if nuvem["x"] < 40 or nuvem["x"] > LARGURA - 120:
                nuvem["vx"] *= -1
            if nuvem["y"] < 50 or nuvem["y"] > 230:
                nuvem["vy"] *= -1

        
        desenhar_fundo()
        desenhar_sol_pulsante(passo)

        
        if IMAGEM_DECORATIVO is not None:
            tela.blit(IMAGEM_DECORATIVO, (nuvem["x"], nuvem["y"]))
        else:
            pygame.draw.circle(tela, BRANCO, (nuvem["x"], nuvem["y"]), 22)

        
        for obst in obstaculos:
            obst_rect = pygame.Rect(obst["x"], CHAO_Y - obst["h"],
                                    obst["w"], obst["h"])
            if IMAGEM_INIMIGO is not None:
                imagem = pygame.transform.smoothscale(IMAGEM_INIMIGO,
                                                      (obst["w"], obst["h"]))
                tela.blit(imagem, obst_rect)
            else:
                pygame.draw.rect(tela, VERDE, obst_rect, border_radius=6)
                pygame.draw.rect(tela, BRANCO, obst_rect, 2, border_radius=6)

        
        if IMAGEM_PERSONAGEM is not None:
            tela.blit(IMAGEM_PERSONAGEM, (princesa_x, princesa_y))
        else:
            pygame.draw.rect(tela, ROSA, (princesa_x, princesa_y,
                                          LARG_PRINCESA, ALT_PRINCESA), border_radius=8)
            desenhar_texto("AQUI VAI", FONTE_PEQUENA, BRANCO,
                           princesa_x + LARG_PRINCESA // 2, princesa_y + 28, centro=True)
            desenhar_texto("IMAGEM", FONTE_PEQUENA, BRANCO,
                           princesa_x + LARG_PRINCESA // 2, princesa_y + 46, centro=True)

        
        desenhar_texto(f"Jogadora: {nome}", FONTE_PEQUENA, CINZA_CLARO, 20, 18)
        desenhar_texto(f"Pontuacao: {pontuacao}", FONTE_PEQUENA, CINZA_CLARO, 20, 44)
        desenhar_texto("Press Space to Pause Game.", FONTE_PEQUENA,
                       CINZA_CLARO, LARGURA - 250, ALTURA - 30)

        
        if pausado:
            sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 150))
            tela.blit(sombra, (0, 0))
            desenhar_texto("PAUSE", FONTE_GRANDE, BRANCO,
                           LARGURA // 2, ALTURA // 2, centro=True)

        pygame.display.flip()


def jogar(nome):

    princesa_x = 150
    princesa_y = CHAO_Y - ALT_PRINCESA   
    vel_y = 0
    gravidade = 1
    forca_pulo = -18
    no_chao = True

    velocidade_jogo = 7
    obstaculos = [novo_obstaculo(LARGURA + i * 380) for i in range(3)]
    nuvem = nova_nuvem()

    pausado = False
    passo = 0
    inicio = pygame.time.get_ticks()
    pontuacao = 0

    while True:
        relogio.tick(FPS)
        passo += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:        
                    encerrar()
                if evento.key == pygame.K_SPACE:         
                    pausado = not pausado
                if evento.key == pygame.K_UP and no_chao and not pausado:
                    vel_y = forca_pulo                   
                    no_chao = False

        
        if not pausado:
            vel_y += gravidade
            princesa_y += vel_y
            if princesa_y >= CHAO_Y - ALT_PRINCESA:
                princesa_y = CHAO_Y - ALT_PRINCESA
                vel_y = 0
                no_chao = True

            pontuacao = (pygame.time.get_ticks() - inicio) // 100

            princesa_rect = pygame.Rect(princesa_x, princesa_y,
                                        LARG_PRINCESA, ALT_PRINCESA)

            
            for obst in obstaculos:
                obst["x"] -= velocidade_jogo
                if obst["x"] + obst["w"] < 0:
                    mais_a_direita = max(o["x"] for o in obstaculos)
                    obst.update(novo_obstaculo(mais_a_direita + random.randint(320, 520)))

                obst_rect = pygame.Rect(obst["x"], CHAO_Y - obst["h"],
                                        obst["w"], obst["h"])
                if princesa_rect.colliderect(obst_rect):
                    salvar_log(ARQUIVO_LOG, nome, pontuacao)  
                    return pontuacao

        
            nuvem["x"] += nuvem["vx"]
            nuvem["y"] += nuvem["vy"]
            if nuvem["x"] < 40 or nuvem["x"] > LARGURA - 120:
                nuvem["vx"] *= -1
            if nuvem["y"] < 50 or nuvem["y"] > 230:
                nuvem["vy"] *= -1

        
        desenhar_fundo()
        desenhar_sol_pulsante(passo)

        
        if IMAGEM_DECORATIVO is not None:
            tela.blit(IMAGEM_DECORATIVO, (nuvem["x"], nuvem["y"]))
        else:
            pygame.draw.circle(tela, BRANCO, (nuvem["x"], nuvem["y"]), 22)

        
        for obst in obstaculos:
            obst_rect = pygame.Rect(obst["x"], CHAO_Y - obst["h"],
                                    obst["w"], obst["h"])
            if IMAGEM_INIMIGO is not None:
                imagem = pygame.transform.smoothscale(IMAGEM_INIMIGO,
                                                      (obst["w"], obst["h"]))
                tela.blit(imagem, obst_rect)
            else:
                pygame.draw.rect(tela, VERDE, obst_rect, border_radius=6)
                pygame.draw.rect(tela, BRANCO, obst_rect, 2, border_radius=6)

        
        if IMAGEM_PERSONAGEM is not None:
            tela.blit(IMAGEM_PERSONAGEM, (princesa_x, princesa_y))
        else:
            pygame.draw.rect(tela, ROSA, (princesa_x, princesa_y,
                                          LARG_PRINCESA, ALT_PRINCESA), border_radius=8)
            desenhar_texto("AQUI VAI", FONTE_PEQUENA, BRANCO,
                           princesa_x + LARG_PRINCESA // 2, princesa_y + 28, centro=True)
            desenhar_texto("IMAGEM", FONTE_PEQUENA, BRANCO,
                           princesa_x + LARG_PRINCESA // 2, princesa_y + 46, centro=True)

    
        desenhar_texto(f"Jogadora: {nome}", FONTE_PEQUENA, CINZA_CLARO, 20, 18)
        desenhar_texto(f"Pontuacao: {pontuacao}", FONTE_PEQUENA, CINZA_CLARO, 20, 44)
        
        desenhar_texto("Press Space to Pause Game.", FONTE_PEQUENA,
                       CINZA_CLARO, LARGURA - 250, ALTURA - 30)

        
        if pausado:
            sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 150))
            tela.blit(sombra, (0, 0))
            desenhar_texto("PAUSE", FONTE_GRANDE, BRANCO,
                           LARGURA // 2, ALTURA // 2, centro=True)

        pygame.display.flip()

       
def tela_fim(nome, pontuacao):
    melhor = obter_melhor_jogador(ARQUIVO_LOG)
    botao_jogar = pygame.Rect(290, 520, 180, 60)
    botao_sair = pygame.Rect(530, 520, 180, 60)
    ja_falou = False

    while True:
        relogio.tick(FPS)
        desenhar_fundo()

        desenhar_texto("FIM DE JOGO", FONTE_GRANDE, VERMELHO,
                       LARGURA // 2, 120, centro=True)
        desenhar_texto(f"{nome}, voce fez {pontuacao} pontos.", FONTE_MEDIA,
                       CINZA_CLARO, LARGURA // 2, 230, centro=True)
        desenhar_texto(formatar_melhor(melhor), FONTE_NORMAL, ROSA,
                       LARGURA // 2, 320, centro=True)

        pygame.draw.rect(tela, VERDE, botao_jogar, border_radius=10)
        desenhar_texto("JOGAR", FONTE_MEDIA, BRANCO,
                       botao_jogar.centerx, botao_jogar.centery, centro=True)
        pygame.draw.rect(tela, VERMELHO, botao_sair, border_radius=10)
        desenhar_texto("SAIR", FONTE_MEDIA, BRANCO,
                       botao_sair.centerx, botao_sair.centery, centro=True)

        if not ja_falou:
            if SOM_FIM is not None:
                SOM_FIM.play()
            falar(f"Fim de jogo. Voce fez {pontuacao} pontos.")
            ja_falou = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                encerrar()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return "jogar"
                if botao_sair.collidepoint(evento.pos):
                    encerrar()

        pygame.display.flip()


def encerrar():
    
    pygame.quit()
    sys.exit()

def main():
    
    while True:
        nome = tela_nome()
        tela_boas_vindas(nome)
        pontuacao = jogar(nome)
        decisao = tela_fim(nome, pontuacao)
        if decisao != "jogar":
            break
    encerrar()

if __name__ == "__main__":
    main()



