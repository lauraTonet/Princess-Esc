
from datetime import datetime


def salvar_log(caminho_log, nome, pontuacao):
   
    agora = datetime.now()
    data = agora.strftime("HH/MM/SS")
    hora = agora.strftime("HH:MM:SS")  # formato HH:MM:SS exigido pela atividade

    linha = f"{nome};{pontuacao};{data};{hora}\n"

    # "a" significa "append": acrescenta no fim sem apagar o que já existe.
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def obter_melhor_jogador(caminho_log):
    
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
    
    if melhor is None:
        return "Recorde: ainda nao ha partidas registradas."

    return (
        f"Recorde: {melhor['nome']} com {melhor['pontuacao']} pontos "
        f"em {melhor['data']} as {melhor['hora']}"
    )