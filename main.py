import time
from core.corner_bot import analisar_jogos

if __name__ == "__main__":
    while True:
        print("🔄 Iniciando varredura de escanteios...")
        analisar_jogos()
        print("⏳ Aguardando 1 hora para nova varredura...")
        time.sleep(3600)