def enviar_lista_influx(client, dados, measurement="sensores_raw", dispositivo="esp32_01"):
    for dado in dados:
        registro = {
            "measurement": measurement,
            "tags": {
                "dispositivo": dispositivo
            },
            "fields": {
                "temperatura": dado["temperatura"],
                "anomalia": False
            },
            "time": dado["tempo"]
        }

        client.write(record=registro)