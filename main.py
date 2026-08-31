import time
from collections import deque
import traceback

from config.database import get_client
from services.select_db import buscar_dados_influx
from services.update_db import atualizar_anomalias_influx


from detection.detectar_anomalias import detectar_anomalias_zscore

# opcional (simulação)
from services.insert_db import enviar_lista_influx
from simulation.dados_teste import gerar_dados_teste

# ----------------------------
# CONFIG
# ----------------------------
MODO_SENSOR = True  # desativado para uso real
INTERVALO = 5
TAMANHO_JANELA = 30

historico = deque(maxlen=TAMANHO_JANELA)

client = get_client()

print("Worker iniciado...\n")

def processar_dados(dados):
    for novo_dado in dados:
        historico.append(novo_dado)

        if len(historico) < 3:
            continue

        # base sem o último
        base = list(historico)[:-1]

        base_filtrada = [d for d in base if not d.get("anomalia", False)]

        if len(base_filtrada) < 3:
            base_filtrada = base

        #detectar_anomalias_zscore(base_filtrada)
        detectar_anomalias_zscore(historico)

        dado_processado = historico[-1] 

        atualizar_anomalias_influx(client, [dado_processado])

        if dado_processado.get("anomalia", True):
            historico.pop()  # Remove o último elemento inserido

        print("Processado:", dado_processado)
        #print(historico[len(historico)-1])


#Teste com dados 
def executar_worker():
    while True:
        try:
            print("Novo ciclo...\n")

            if MODO_SENSOR:
                dados_teste = gerar_dados_teste()
                enviar_lista_influx(client, dados_teste)
                print(" Dado simulado enviado")

            dados = buscar_dados_influx(client)

            if dados:
                processar_dados(dados)
            else:
                print("Nenhum dado novo")

            time.sleep(INTERVALO)

        except KeyboardInterrupt:
            print("\n Encerrado pelo usuário")
            break

        except Exception:
            traceback.print_exc()
            time.sleep(5)


if __name__ == "__main__":
    executar_worker()