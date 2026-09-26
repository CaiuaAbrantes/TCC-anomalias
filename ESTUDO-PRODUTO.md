# Diagnóstico do Produto: Worker de Detecção de Anomalias IoT

## 1. Tarefa do Grupo: Diagnóstico do Produto Real Entregue

### 1.1 Qual é o produto e qual problema ele resolve?
O produto é um worker em Python especializado no processamento assíncrono e detecção de anomalias em tempo real para dados de sensores IoT. Ele resolve o problema de identificar automaticamente comportamentos atípicos e picos em séries temporais (como medições de temperatura) sem depender de supervisão ou análise manual contínua por parte do operador.

### 1.2 Quem usa, quem mantém e quem recebe as versões?
* **Quem usa:** O cliente/operador final através de dashboards de monitoramento (como Grafana) alimentados pelos dados processados no InfluxDB.
* **Quem mantém:** A equipe de desenvolvimento responsável pelo algoritmo e infraestrutura do worker.
* **Quem recebe as versões:** O servidor de execução em nuvem/local onde o serviço do worker roda de forma contínua.

### 1.3 Como o produto é executado hoje?
Atualmente, o produto é executado manualmente rodando o script principal `python main.py` diretamente no ambiente de desenvolvimento ou no servidor, após instalar as dependências do `requirements.txt` e configurar os parâmetros de banco de dados em `config/database.py`.

### 1.4 Quais passos ainda dependem de ação manual?
* Clonar ou atualizar o código via `git pull`.
* Instalar ou atualizar bibliotecas do Python.
* Ajustar manualmente as credenciais de banco e ambiente no arquivo `.env` ou `config/database.py`.
* Reiniciar o processo no terminal caso ocorra alguma falha crítica.
* Gerenciar/limpar o arquivo de controle de estado (`ultimo_tempo.txt`).

### 1.5 O que pode dar errado em uma nova entrega?
* **Incompatibilidade de formato:** O backend (FastAPI) alterar a estrutura dos campos em `sensores_raw` e quebrar a leitura do worker.
* **Erros de conexão:** Falha de comunicação não tratada com a instância do InfluxDB derrubar o loop principal.
* **Divergência de dependências:** Atualização de versão de bibliotecas gerar incompatibilidades na execução.
* **Distorção do algoritmo:** Alteração incorreta nos limiares do Z-Score/MAD gerar falsos positivos em massa.

### 1.6 Que evidência mostra que o produto está pronto hoje?
A execução funcional demonstrável via logs no terminal rodando `main.py` (ou em modo simulação com `dados_teste.py`), com a gravação correta dos registros processados contendo a tag `anomalia` no InfluxDB e a visualização gráfica correspondente no Grafana.

### 1.7 Que informação precisaria ser documentada para outra pessoa manter o sistema?
* Estrutura das medições e tabelas no InfluxDB (`sensores_raw` e `sensores_processados`).
* Lógica e parâmetros do cálculo estatístico (Mediana, MAD e limiar do Z-Score).
* Papel do arquivo de controle temporal `ultimo_tempo.txt`.
* Passo a passo para reinicialização e tratamento de erros do serviço.

---

## 2. Leitura do Futuro do Produto

### 2.1 Containerização (Docker)
* **Problema resolvido:** Elimina a divergência de ambiente de execução ("funciona na minha máquina, mas não no servidor").
* **Benefício:** Permite subir toda a aplicação (worker, dependências e configurações) com um único comando, garantindo portabilidade e facilidade de deploy.
* **Custo/Dificuldade:** Necessidade de aprender a construir e otimizar `Dockerfiles` e gerenciar volumes/redes.
* **Informação a investigar:** Qual o consumo de memória e CPU do container rodando o worker em loop contínuo.

### 2.2 Ambiente de Homologação (Staging)
* **Problema resolvido:** Evita testar alterações de código e algoritmo diretamente no banco de produção do cliente.
* **Benefício:** Permite simular a ingestão de dados e validar novas versões do worker sem colocar em risco o monitoramento ativo.
* **Custo/Dificuldade:** Custo financeiro e operacional adicional para manter uma infraestrutura espelho paralela.
* **Informação a investigar:** Como espelhar ou gerar dados sintéticos de teste fieis aos dados reais de produção.

### 2.3 Versionamento Estruturado com Branches (Git Flow)
* **Problema resolvido:** Evita que alterações instáveis no código influenciem a versão principal pronta para entrega.
* **Benefício:** Organiza o fluxo de desenvolvimento da equipe, separando correções de bugs, novas funcionalidades e versões estáveis.
* **Custo/Dificuldade:** Exige disciplina da equipe em seguir o fluxo de Pull Requests e resolução de conflitos (merges).
* **Informação a investigar:** Qual modelo de branching (ex.: GitHub Flow vs. Git Flow) atende melhor ao ritmo de entregas da dupla.
