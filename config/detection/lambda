import sys
import os

# Garante que a AWS Lambda encontre as bibliotecas na pasta 'package'
caminho_pacotes = os.path.join(os.path.dirname(__file__), 'package')
sys.path.insert(0, caminho_pacotes)

import urllib.request
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from mangum import Mangum

# Configurações do InfluxDB do Caiuá
INFLUX_HOST = 'https://us-east-1-1.aws.cloud2.influxdata.com'
INFLUX_TOKEN = 'K30HpwBohjzcJKF476OOjU7RjvG2oc5yYN66YivwJM_3NozT5ZyELl-tPZQsfvZPCZUcY9gYwVeWAX7fmOp80Q=='
INFLUX_ORG = 'TCC'
INFLUX_BUCKET = 'TCC'
URL_ESCRITA = f"{INFLUX_HOST}/api/v2/write?org={INFLUX_ORG}&bucket={INFLUX_BUCKET}"

app = FastAPI(title="API de Coleta IoT - TCC")

# Definição do Modelo de Dados (Pydantic) baseado no JSON do ESP32
class PayloadESP32(BaseModel):
    device_id: str
    temperatura: float
    umidade: float

@app.api_route("/{any_path:path}", methods=["POST", "GET"])
async def receber_dados_sensor(dados: PayloadESP32):
    try:
        # Formata os dados validados pelo FastAPI no padrão Line Protocol
        line_protocol = f"sensores_raw,dispositivo={dados.device_id} temperatura={dados.temperatura},anomalia=false"
        
        # Envia HTTP POST para o InfluxDB
        req = urllib.request.Request(
            URL_ESCRITA,
            data=line_protocol.encode('utf-8'),
            headers={
                'Authorization': f'Token {INFLUX_TOKEN}',
                'Content-Type': 'text/plain; charset=utf-8'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            status_banco = response.getcode()
            
        return {
            "status": "Sucesso",
            "mensagem": "Dado processado pelo FastAPI e enviado ao InfluxDB",
            "influx_status": status_banco
        }
        
    except urllib.error.HTTPError as e:
        raise HTTPException(status_code=e.code, detail=f"Erro no InfluxDB: {e.read().decode('utf-8')}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# O Mangum encapsula o FastAPI para que a AWS Lambda consiga executá-lo

handler = Mangum(app)
