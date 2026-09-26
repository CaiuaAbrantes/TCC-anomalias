# ⚡ Módulo AWS Lambda - API de Coleta e Ingestão IoT

> **Desenvolvido por:** Tácio Santos Matias  
> **Tecnologias:** AWS Lambda, FastAPI, Mangum, Pydantic, InfluxDB v2  
> **Projeto:** TCC - Monitoramento e Processamento de Anomalias IoT  

---

## 🎯 Descrição do Módulo
Este módulo é responsável por atuar como a camada serverless de recepção, validação e ingestão de dados de sensores IoT (ESP32). A aplicação utiliza **FastAPI** adaptada para execução Serverless via **Mangum**, recebendo requisições HTTP do microcontrolador, validando os dados com **Pydantic** (`device_id`, `temperatura`, `umidade`) e enviando os registros formatados em *Line Protocol* diretamente para a API do **InfluxDB Cloud**.

---

## 🛠️ Tecnologias e Bibliotecas
- **Framework Web:** FastAPI + Mangum (Adapter ASGI para AWS Lambda)
- **Validação de Schemas:** Pydantic (`BaseModel`)
- **Comunicação HTTP:** `urllib.request` (biblioteca nativa para requisições leves na Lambda)
- **Banco de Dados Temporal:** InfluxDB Cloud (v2 Line Protocol API)

---

## 📌 Modelo de Dados Esperado (Payload)

A API espera receber requisições do ESP32 no seguinte formato JSON:

```json
{
  "device_id": "ESP32_01",
  "temperatura": 25.4,
  "umidade": 60.2
}
