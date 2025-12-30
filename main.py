import requests
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime
import os
import tweepy

# ========== CONFIG ==========
URLS = {
    "Classificação Geral": "https://www.mat.ufmg.br/futebol/classificacao-geral_seriea/",
    "⬇🛑 Risco de Rebaixamento": "https://www.mat.ufmg.br/futebol/rebaixamento_seriea/",
    "🏆 Classificação Sula": "https://www.mat.ufmg.br/futebol/classificacao-para-sulamericana_seriea/",
    "🏆 Classificação Libertadores": "https://www.mat.ufmg.br/futebol/classificacao-para-libertadores_seriea/"
}

TIME_ALVO = "VITORIA"
# ============================

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.upper()

def extrair_classificacao_geral(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tabela = soup.find("table")
    linhas = tabela.find_all("tr")

    for linha in linhas:
        cols = [c.get_text(strip=True) for c in linha.find_all("td")]
        if len(cols) < 11:
            continue
        if normalizar(cols[1]) == TIME_ALVO:
            return {
                "Posicao": cols[0] + "º",
                "Pnts": cols[2],
                "Jogos": cols[3] + "/38",
                f"🎯 V: {cols[4]} | E: {cols[5]} | D: {cols[6]}\n"
                "SG": cols[9],
                "Rendimento": cols[10] + "%",
            }
    return None

def extrair_probabilidade(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tabela = soup.find("table")
    linhas = tabela.find_all("tr")

    for linha in linhas:
        cols = [c.get_text(strip=True) for c in linha.find_all("td")]
        if len(cols) < 3:
            continue
        if normalizar(cols[1]) == TIME_ALVO:
            return cols[2]
    return None

def gerar_tweet():
    partes = [f"EC VITÓRIA 🔴⚫\n📅 {datetime.now().strftime('%d/%m/%y')}"]

    # Classificação Geral
    dados = extrair_classificacao_geral(URLS["Classificação Geral"])
    if dados:
        partes.append("\n📊 Serie A")
        for k, v in dados.items():
            partes.append(f"{k}: {v}")

    # Probabilidades
    for nome, url in URLS.items():
        if nome == "Classificação Geral":
            continue
        prob = extrair_probabilidade(url)
        if prob:
            prob_float = float(prob.replace(",", "."))
            partes.append(f"{nome}\n(%): {prob_float:.2f}%")

    partes.append("\nFonte: UFMG")

    tweet = "\n".join(partes)

    # Limitar a 280 caracteres (ou criar thread se quiser mais depois)
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    return tweet

def postar_tweet(tweet):
    client = tweepy.Client(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
    )
    client.create_tweet(text=tweet)
    print("Tweet postado com sucesso.")

if __name__ == "__main__":
    tweet = gerar_tweet()
    postar_tweet(tweet)
