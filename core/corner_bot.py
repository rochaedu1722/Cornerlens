import requests
import os
from datetime import datetime
from core.telegram import enviar_telegram

API_KEY = os.getenv("API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
TOKEN = os.getenv("TELEGRAM_TOKEN")
HEADERS = {"x-apisports-key": API_KEY}

def buscar_jogos():
    url = "https://v3.football.api-sports.io/fixtures?next=20"
    resposta = requests.get(url, headers=HEADERS)
    if resposta.status_code != 200:
        print("Erro ao buscar jogos")
        return []
    return resposta.json().get("response", [])

def buscar_estatisticas(time_id, liga_id):
    url = f"https://v3.football.api-sports.io/teams/statistics?team={time_id}&league={liga_id}&season=2025"
    resposta = requests.get(url, headers=HEADERS)
    if resposta.status_code != 200:
        return None
    return resposta.json()

def analisar_jogos():
    jogos = buscar_jogos()
    for jogo in jogos:
        try:
            time_casa = jogo["teams"]["home"]["name"]
            time_fora = jogo["teams"]["away"]["name"]
            id_casa = jogo["teams"]["home"]["id"]
            id_fora = jogo["teams"]["away"]["id"]
            id_liga = jogo["league"]["id"]
            data = jogo["fixture"]["date"]
            liga = jogo["league"]["name"]

            stats_casa = buscar_estatisticas(id_casa, id_liga)
            stats_fora = buscar_estatisticas(id_fora, id_liga)

            if not stats_casa or not stats_fora:
                continue

            media_casa = stats_casa["response"]["fixtures"]["corners"]["for"]["total"] / max(stats_casa["response"]["fixtures"]["played"]["total"], 1)
            media_fora = stats_fora["response"]["fixtures"]["corners"]["for"]["total"] / max(stats_fora["response"]["fixtures"]["played"]["total"], 1)

            media_total = round(media_casa + media_fora, 2)
            prob_over_10_5 = min(round((media_total - 8.5) * 10, 1), 90.0)

            if media_total >= 10 and prob_over_10_5 >= 65:
                mensagem = f"📢 Alerta de Escanteios:
🏆 {liga}
🏟 {time_casa} x {time_fora}
📊 Média real: {media_total} escanteios
🎯 Prob. Over 10.5: {prob_over_10_5}%
🕓 {data}"
                enviar_telegram(mensagem)
        except Exception as e:
            print("Erro ao processar jogo:", e)