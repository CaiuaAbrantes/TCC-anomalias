from services.controle_tempo import ler_ultimo_tempo
from datetime import timedelta

def buscar_dados_influx(client):
    ultimo_tempo = ler_ultimo_tempo(client)

    if ultimo_tempo:
        ultimo_tempo_ajustado = ultimo_tempo.isoformat() + "Z"

        query = f"""
        SELECT *
        FROM sensores_raw
        WHERE time > '{ultimo_tempo_ajustado}'
        ORDER BY time ASC
        """
    else:
        query = """
        SELECT *
        FROM sensores_raw
        ORDER BY time ASC
        LIMIT 50
        """

    tabela = client.query(query)
    df = tabela.to_pandas()

    dados = []

    for _, linha in df.iterrows():
        dados.append({
            "tempo": linha["time"],
            "temperatura": linha["temperatura"],
            "anomalia": linha["anomalia"]
        })

    return dados