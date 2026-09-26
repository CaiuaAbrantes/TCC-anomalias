# 🧠 Worker - Processamento de Anomalias (IoT)

## 📌 Visão Geral

Este módulo é responsável pelo **processamento de dados de sensores IoT**, especificamente:

* Leitura de dados armazenados no InfluxDB
* Detecção de anomalias utilizando Z-score baseado em MAD (Median Absolute Deviation)
* Atualização dos dados processados no banco

⚠️ **Este módulo NÃO é uma API**
Ele funciona como um **serviço independente (worker)** que consome e processa dados.

---

## 🧩 Arquitetura do Sistema

O sistema completo é dividido em duas partes:

### 🔵 Backend (FastAPI) — responsabilidade do seu amigo

* Receber dados do ESP32 (HTTP)
* Validar dados
* Inserir no InfluxDB (`sensores_raw`)
* Disponibilizar dados via endpoints

### 🟡 Worker (este módulo)

* Buscar dados no InfluxDB
* Processar dados (detecção de anomalias)
* Atualizar dados processados (`sensores_processados`)

---

## 🔄 Fluxo de Dados

ESP32 → FastAPI → InfluxDB (sensores_raw)
↓
Worker → processa → InfluxDB (sensores_processados)
↓
FastAPI → fornece dados para frontend

---

## 📁 Estrutura do Projeto

```
worker/
├── main.py
├── services/
│   ├── select_db.py
│   ├── update_db.py
│   ├── insert_db.py
│   └── controle_tempo.py
├── detection/
│   └── detectar_anomalias.py
├── simulation/
│   └── dados_teste.py
├── config/
│   └── database.py
├── utils/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Como o Worker Funciona

O worker roda em loop contínuo:

1. (Opcional) Simula dados de sensor
2. Busca novos dados no InfluxDB
3. Mantém uma janela deslizante (histórico)
4. Aplica detecção de anomalias
5. Atualiza os dados processados no banco
6. Aguarda e repete

---

## 📊 Formato dos Dados

### 📥 Dados esperados no InfluxDB (`sensores_raw`)

```
{
  "tempo": "2026-04-06T14:53:59Z",
  "temperatura": 25.7,
  "anomalia": false
}
```

### 📤 Dados processados (`sensores_processados`)

```
{
  "tempo": "2026-04-06T14:53:59Z",
  "temperatura": 25.7,
  "anomalia": true/false
}
```

---

## ⚠️ Requisitos IMPORTANTES para o Backend (FastAPI)

Para garantir compatibilidade com o worker:

### ✔ Formato obrigatório

* `tempo`: string ISO 8601 com `Z`
* `temperatura`: float
* `anomalia`: boolean (inicialmente false)

---

### ✔ Regras críticas

* O backend deve salvar dados em:

  ```
  sensores_raw
  ```

* O campo `anomalia` deve ser:

  ```
  false (sempre na inserção)
  ```

* O backend NÃO deve modificar `anomalia` depois

---

## ⏱️ Frequência de Dados

* O sistema espera novos dados aproximadamente a cada **5 segundos**
* O worker é configurado para processar nesse intervalo

---

## 🧠 Lógica de Detecção de Anomalias

O algoritmo utilizado é:

* Z-score baseado em MAD (Median Absolute Deviation)
* Mais robusto contra outliers do que média/desvio padrão

### Processo:

1. Calcula a mediana das temperaturas
2. Calcula o MAD
3. Calcula score para cada ponto
4. Define como anomalia se ultrapassar limite

---

## 📌 Controle de Tempo

O worker utiliza um arquivo:

```
ultimo_tempo.txt
```

Para:

* evitar reprocessamento de dados antigos
* garantir continuidade entre execuções

---

## 🚀 Execução

### Instalar dependências:

```
pip install -r requirements.txt
```

### Rodar o worker:

```
python main.py
```

---

## 🧪 Modo de Teste

No `main.py`:

```
MODO_SENSOR = True
```

* Gera dados simulados
* Útil para testes sem ESP32/API

Para produção:

```
MODO_SENSOR = False
```

---

## 📌 Observações Importantes

* O worker pode processar múltiplos dados por ciclo (batch)
* O backend envia dados em tempo real (stream)
* Isso é comportamento esperado

---

## 🧠 Responsabilidades

### 🔵 Backend (FastAPI)

* Receber dados
* Validar
* Inserir no banco
* Disponibilizar via API

### 🟡 Worker

* Processar dados
* Detectar anomalias
* Atualizar banco

---

## 📬 Integração

O worker assume que:

* o backend está populando `sensores_raw`
* os dados seguem o formato especificado
* o tempo está ordenado corretamente

---

## ✅ Status

✔ Pipeline funcionando
✔ Detecção de anomalias implementada
✔ Integração com InfluxDB
✔ Pronto para integração com FastAPI

---

---

### 🚨 Problemas Conhecidos e Limitações
* **Análise Monovariada:** O algoritmo atualmente analisa a variável de temperatura individualmente, sem correlacionar simultaneamente outras variáveis como a umidade no mesmo cálculo estatístico.
* **Dependência da Conexão:** A execução contínua do worker depende de uma conexão ativa e estável com a instância do banco de dados (InfluxDB).

### 📑 Atendimento dos Requisitos de Entrega

| Requisito Solicitado | Status | Descrição do Atendimento |
| :--- | :---: | :--- |
| **Código-fonte completo** | ✅ | Módulos de banco, detecção, simulação e tempo integrados no repositório. |
| **Produto executável / acessível** | ✅ | Execução autônoma via `python main.py` ou em modo de simulação. |
| **README.md com instruções** | ✅ | Documentado com arquitetura, fluxo, execução e dependências. |
| **Descrição dos recursos** | ✅ | Módulos `detection`, `services`, `simulation` e `config` detalhados. |
| **Evidências de funcionamento** | ✅ | Testes locais com `MODO_SENSOR = True` validados. |
| **Problemas e limitações** | ✅ | Documentados no item "Problemas Conhecidos e Limitações". |
| **Demonstração para o cliente** | ✅ | Fluxo pronto para execução e verificação dos logs de detecção. |
