from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def buscar_informacoes_personagem(nome_personagem):
    url = "https://miracle74.com/?subtopic=characters"
    dados = {"name": nome_personagem}

    try:
        resposta = requests.post(url, data=dados)
        resposta.raise_for_status()

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
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def buscar_multiplos_personagens(nomes_personagens):
    resultados = {}
    for nome in nomes_personagens:
        resultado = buscar_informacoes_personagem(nome)
        resultados[nome] = resultado
    return resultados

def extrair_personagens_banidos(log):
    return re.findall(r"(\w+(?: \w+)?)(?: \[)", log)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nomes_personagens = request.form["nomes"].split(",")
        resultados = buscar_multiplos_personagens(nomes_personagens)
        return render_template("resultados.html", resultados=resultados)
    return render_template("index.html")

@app.route("/banidos", methods=["GET","POST"])
def banidos():
    if request.method == "POST":
        log = request.form["log"]
        personagens_banidos = extrair_personagens_banidos(log)
        return render_template("banidos.html", personagens_banidos=personagens_banidos)
    return render_template("banidos.html")