import time
from core.corner_bot import analisar_jogos

if __name__ == "__main__":
    while True:
        print("🟡 [LOG] Iniciando varredura de escanteios...", flush=True)
        try:
            analisar_jogos()
            print("🟢 [LOG] Varredura concluída com sucesso.", flush=True)
        except Exception as e:
            print(f"🔴 [ERRO] Falha durante a varredura: {e}", flush=True)
        print("⏳ Aguardando 15 minutos para nova varredura...\n", flush=True)
        time.sleep(900)
