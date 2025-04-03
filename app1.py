import requests
from bs4 import BeautifulSoup

def buscar_informacoes_personagem(nome_personagem):
    """
    Busca informações de um personagem no site e retorna um dicionário com os dados.

    Args:
        nome_personagem (str): O nome do personagem a ser pesquisado.

    Returns:
        dict: Um dicionário contendo Nome, Vocação e Nível do personagem, ou None se não encontrado.
    """
    url = "https://miracle74.com/?subtopic=characters"  # URL Do miracle da pagina de chars
    dados = {"name": nome_personagem}

    try:
        resposta = requests.post(url, data=dados)
        resposta.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        soup = BeautifulSoup(resposta.content, "html.parser")
        conteudo_personagem = soup.find("div", class_="BoxContentContainer")

        if conteudo_personagem:
            tabela = conteudo_personagem.find("table", class_="TableContent")
            linhas = tabela.find_all("tr")

            informacoes = {}
            for linha in linhas:
                celulas = linha.find_all("td")
                if len(celulas) == 2:
                    chave = celulas[0].text.strip().replace(":", "")
                    valor = celulas[1].text.strip()
                    informacoes[chave] = valor

            return {
                "Name": informacoes.get("Name"),
                "Vocation": informacoes.get("Vocation"),
                "Level": informacoes.get("Level"),
            }
        else:
            return None  # Personagem não encontrado

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def buscar_multiplos_personagens(nomes_personagens):
    """
    Busca informações de múltiplos personagens e retorna um dicionário com os resultados.

    Args:
        nomes_personagens (list): Uma lista de nomes de personagens.

    Returns:
        dict: Um dicionário onde as chaves são os nomes dos personagens e os valores são os dicionários de informações.
    """
    resultados = {}
    for nome in nomes_personagens:
        resultado = buscar_informacoes_personagem(nome)
        resultados[nome] = resultado
    return resultados

# Exemplo de uso
nomes = ['Tio Bille', 'The Snaker', "Lkn'zerah", 'Frenado', 'Exiva Hucz', 'Babuszka Od Buszka', 'Maddus', 'Sexi', 'Lady Magic', 'Sufipu', 'Neymarinho', 'Mrtt', 'Grill', 'Banditos', 'Zidi', 'Baby Girl', 'Luizzqqmuda', 'Ritauk']  # Nomes dos personagens pra checar
resultados = buscar_multiplos_personagens(nomes)

for nome, informacoes in resultados.items():
    print(f"Informações de {nome}:")
    if informacoes:
        print(f"  Nome: {informacoes['Name']}")
        print(f"  Vocação: {informacoes['Vocation']}")
        print(f"  Level: {informacoes['Level']}")
    else:
        print("  Personagem não encontrado.")
    print("-" * 20)