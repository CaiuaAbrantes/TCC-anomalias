import numpy as np

def detectar_anomalias_zscore(dados, limite=3):
    temperaturas = np.array([d["temperatura"] for d in dados])

    mediana = np.median(temperaturas)
    desvios = np.abs(temperaturas - mediana)
    mad = np.median(desvios)

    for d in dados:
        if mad == 0:
            score = 0
        else:
            score = 0.6745 * (d["temperatura"] - mediana) / mad

        d["anomalia"] = bool(abs(score) > limite)