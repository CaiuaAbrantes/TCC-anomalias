from datetime import datetime, timezone
import random

def gerar_dados_teste():
    temp = round(random.uniform(25, 27), 1)

    if random.random() < 0.1:
        temp = random.choice([10.0, 40.0])

    return [{
        "tempo": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "temperatura": temp
    }]