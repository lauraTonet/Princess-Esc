"""
trabalho.py
-----------
Funções auxiliares do jogo, exigidas pela atividade (item 7).

Aqui ficam as funções que cuidam do log da partida (log.dat) e da
descoberta do jogador com maior pontuação (o ranking). Elas são
importadas no main.py com:

    from Recursos.trabalho import salvar_log, obter_melhor_jogador, formatar_melhor

Manter essas funções separadas deixa o main.py mais limpo e organizado.
"""

from datetime import datetime


def salvar_log(caminho_log, nome, pontuacao):
    """
    Salva uma linha no arquivo de log a cada partida encerrada.

    Atende ao item 15: registra Nome, Pontuação, Data e Hora (HH:MM:SS).
    O formato escolhido separa os campos por ponto e vírgula, o que
    facilita ler o arquivo depois.

    Exemplo de linha gravada:
        Maria;128;08/06/2026;14:32:07
    """
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")  # formato HH:MM:SS exigido pela atividade

    linha = f"{nome};{pontuacao};{data};{hora}\n"

    # "a" significa "append": acrescenta no fim sem apagar o que já existe.
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def obter_melhor_jogador(caminho_log):
    """
    Lê o log.dat e devolve o jogador com a maior pontuação já registrada.

    Atende aos itens 9 e 18 (mostrar o competidor com maior número de pontos
    na tela de boas-vindas e na tela de fim de jogo).

    Retorna um dicionário no formato:
        {"nome": str, "pontuacao": int, "data": str, "hora": str}
    ou None quando ainda não há nenhuma partida registrada.
    """
    melhor = None

    try:
        with open(caminho_log, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")

                # Ignora linhas que não tenham exatamente os 4 campos esperados.
                if len(partes) != 4:
                    continue

                nome, pontuacao_texto, data, hora = partes

                # A pontuação foi salva como texto; precisa virar número
                # para poder comparar. Se vier algo inválido, pula a linha.
                try:
                    pontuacao = int(pontuacao_texto)
                except ValueError:
                    continue

                if melhor is None or pontuacao > melhor["pontuacao"]:
                    melhor = {
                        "nome": nome,
                        "pontuacao": pontuacao,
                        "data": data,
                        "hora": hora,
                    }

    except FileNotFoundError:
        # Na primeira execução o log.dat ainda não existe. Tudo bem.
        return None

    return melhor


def formatar_melhor(melhor):
    """
    Transforma o dicionário do melhor jogador em um texto pronto para
    ser desenhado na tela. Centraliza a formatação num único lugar.
    """
    if melhor is None:
        return "Recorde: ainda nao ha partidas registradas."

    return (
        f"Recorde: {melhor['nome']} com {melhor['pontuacao']} pontos "
        f"em {melhor['data']} as {melhor['hora']}"
    )