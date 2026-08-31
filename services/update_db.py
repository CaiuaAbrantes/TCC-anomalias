def atualizar_anomalias_influx(client, dados, measurement="sensores_processados"):
    for d in dados:
        registro = {
            "measurement": measurement,
            "tags": {
                "dispositivo": "esp32_01"
            },
            "fields": {
                "temperatura": d["temperatura"],
                "anomalia": d["anomalia"]
            },
            "time": d["tempo"]
        }

        client.write(record=registro)