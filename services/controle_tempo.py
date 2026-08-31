import os
ARQUIVO_TEMPO = os.path.join(os.path.dirname(__file__), "ultimo_tempo.txt")

def salvar_ultimo_tempo(tempo):
    with open(ARQUIVO_TEMPO, "w") as f:
        f.write(str(tempo))

'''
def ler_ultimo_tempo():
    try:
        with open(ARQUIVO_TEMPO, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

'''
def ler_ultimo_tempo(client):
    query = """
    SELECT time
    FROM sensores_processados
    ORDER BY time DESC
    LIMIT 1
    """

    try:
        resultado = client.query(query=query)

        if resultado.num_rows == 0:
            return None

        return resultado["time"][0].as_py()

    except Exception as e:
        print(f"Erro ao ler último tempo: {e}")
