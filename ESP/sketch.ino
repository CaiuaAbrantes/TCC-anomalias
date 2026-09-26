#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h> // ADICIONADO: Necessário para a segurança HTTPS da AWS
#include <DHT.h>

// ===== SENSOR =====
#define DHTPIN 21
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

// ===== WIFI =====
const char* ssid = "Academicos";
const char* password = "";

// ===== AWS =====
// CORRIGIDO: Agora aponta para a URL completa com a rota exata exigida pelo FastAPI
const char* aws_url = "https://e6iwuc2lavoisqhknoaaml43ne0ebbdi.lambda-url.sa-east-1.on.aws/default/validador-sensores-tcc";

void setup() {
  Serial.begin(9600);
  dht.begin();

  Serial.println();
  Serial.println("Iniciando ESP32...");

  WiFi.begin(ssid, password);

  Serial.print("Conectando em ");
  Serial.println(ssid);

  int tentativas = 0;

  while (WiFi.status() != WL_CONNECTED && tentativas < 30) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Wi-Fi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Falha ao conectar no Wi-Fi!");
    Serial.println("Verifique nome da rede e senha.");
  }
}

void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi desconectado.");
    delay(5000);
    return;
  }

  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Erro ao ler DHT22");
    delay(3000);
    return;
  }

  String json = "{";
  json += "\"device_id\":\"esp32_01\",";
  json += "\"temperatura\":" + String(temperatura, 2) + ",";
  json += "\"umidade\":" + String(umidade, 2);
  json += "}";

  Serial.println("Enviando:");
  Serial.println(json);

  // ADICIONADO: Criação do cliente seguro para burlar a trava de SSL da AWS
  WiFiClientSecure client;
  client.setInsecure(); // Diz ao ESP32 para confiar na URL da AWS sem precisar instalar arquivos de certificado (.pem)

  HTTPClient http;

  // CORRIGIDO: Passando o cliente seguro junto com a URL de destino
  http.begin(client, aws_url);
  http.addHeader("Content-Type", "application/json");

  int resposta = http.POST(json);

  Serial.print("HTTP Code: ");
  Serial.println(resposta); // Se der 200, deu certo! Se der menor que 0, é erro de rede/Wi-Fi.

  if (resposta > 0) {
    Serial.println("Dados enviados!");
  } else {
    Serial.println("Falha no envio.");
  }

  http.end();

  delay(2000);
}
